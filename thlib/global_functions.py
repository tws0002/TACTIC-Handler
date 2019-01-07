# file global_functions.py
# Global Functions Module

import sys
import os
from stat import ST_SIZE
import subprocess
import copy
import ast
import json
import zlib
import binascii
import collections
import re
import traceback
import side.qtawesome as qta
import side.natsort as natsort
from bs4 import BeautifulSoup
from thlib.side.Qt import QtWidgets as QtGui
from thlib.side.Qt import QtGui as Qt4Gui
from thlib.side.Qt import QtCore
from thlib.side.watchdog.observers import Observer
from thlib.side.watchdog.events import FileSystemEventHandler, EVENT_TYPE_MOVED, EVENT_TYPE_CREATED, EVENT_TYPE_DELETED, EVENT_TYPE_MODIFIED

from environment import env_mode, env_tactic, env_inst, dl


class EventHandler(FileSystemEventHandler, QtCore.QObject):
    created = QtCore.Signal(object, object)
    deleted = QtCore.Signal(object, object)
    moved = QtCore.Signal(object, object)
    modified = QtCore.Signal(object, object)
    any = QtCore.Signal(object, object)

    def __init__(self):
        super(EventHandler, self).__init__()

    def dispatch(self, event, watch):
        self.on_any_event(event, watch)
        _method_map = {
            EVENT_TYPE_MODIFIED: self.on_modified,
            EVENT_TYPE_MOVED: self.on_moved,
            EVENT_TYPE_CREATED: self.on_created,
            EVENT_TYPE_DELETED: self.on_deleted,
        }
        event_type = event.event_type
        _method_map[event_type](event, watch)

    def on_any_event(self, event, watch):
        self.any.emit(event, watch)

    def on_created(self, event, watch):
        self.created.emit(event, watch)

    def on_deleted(self, event, watch):
        self.deleted.emit(event, watch)

    def on_moved(self, event, watch):
        self.moved.emit(event, watch)

    def on_modified(self, event, watch):
        self.modified.emit(event, watch)


class FSObserver(Observer):

    def __init__(self):
        super(FSObserver, self).__init__()

        self.event_handler = EventHandler()
        self.started = False

        self.observers_dict = {}

    def set_created_signal(self, func):
        self.event_handler.created.connect(func)

    def append_watch(self, watch_name, paths=None, repos=None, recursive=None):

        if watch_name not in self.observers_dict.keys():

            for i, path in enumerate(paths):
                watch = self.schedule(self.event_handler, path=path, recursive=recursive)
                watch.watch_name = watch_name
                watch.repo = repos[i]
                self.observers_dict.setdefault(watch_name, []).append(watch)
                dl.info(u'Enabled Watching path: {0}'.format(path),
                        group_id='watch_folders_ui')

    def remove_watch(self, watch_name):

        if watch_name in self.observers_dict.keys():
            for observer in self.observers_dict.pop(watch_name):
                self.unschedule(observer)
                dl.info(u'Disabling Watch: {0}'.format(observer.path),
                        group_id='watch_folders_ui')

    def stop(self):
        self.started = False
        super(FSObserver, self).stop()

    def is_started(self):
        return self.started

    def start(self):
        self.started = True
        super(FSObserver, self).start()

    def dispatch_events(self, event_queue, timeout):
        # OVERRIDEN, to see which watch handles event
        event, watch = event_queue.get(block=True, timeout=timeout)

        with self._lock:
            # To allow unschedule/stop and safe removal of event handlers
            # within event handlers itself, check if the handler is still
            # registered after every dispatch.
            for handler in list(self._handlers.get(watch, [])):
                if handler in self._handlers.get(watch, []):
                    handler.dispatch(event, watch)
        event_queue.task_done()


class ThreadSignals(QtCore.QObject):
    finished = QtCore.Signal()
    error = QtCore.Signal(tuple)
    result = QtCore.Signal(object)
    progress = QtCore.Signal(object, object)
    stop = QtCore.Signal(object)


class ThreadWorker(QtCore.QRunnable):
    """
    Adapted from: https://martinfitzpatrick.name/article/multithreading-pyqt-applications-with-qthreadpool/
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param agent: This is function which will be started by QRunnable.
    :type agent: function

    """

    def __init__(self, agent, thread_pool, parent=None):
        super(ThreadWorker, self).__init__(parent=parent)
        # Settings
        self.setAutoDelete(False)

        # Vars
        self.agent = agent

        # we can access thread_worker from running agent func
        self.agent.thread_worker = self

        self.thread_pool = thread_pool
        self.signals_enabled = True

        self.failed = False
        self.error_tuple = None

        # Signals
        self.signals = ThreadSignals()

    def add_custom_kwargs(self, **kwargs):
        for kwarg, value in kwargs.items():
            setattr(self, kwarg, value)

    def disable_signals(self):
        self.signals_enabled = False

    def is_signals_enabled(self):
        return self.signals_enabled

    def start(self, priority=0):
        self.thread_pool.start(self, priority)

    def try_start(self):
        return self.thread_pool.tryStart(self)

    def get_thread_pool(self):
        return self.thread_pool

    def is_failed(self):
        return self.failed

    def set_failed(self, boolean):
        self.failed = boolean

    def get_error_tuple(self):
        return self.error_tuple

    def finished_func(self, func=None):
        if func:
            vars(func)['thread_worker'] = self
            self.signals.finished.connect(func)

    def error_func(self, func=None):
        if func:
            vars(func)['thread_worker'] = self
            self.signals.error.connect(func)

    def result_func(self, func=None):
        if func:
            vars(func)['thread_worker'] = self
            self.signals.result.connect(func)

    def progress_func(self, func=None):
        if func:
            vars(func)['thread_worker'] = self
            self.signals.progress.connect(func)

    def stop_func(self, func=None):
        if func:
            vars(func)['thread_worker'] = self
            self.signals.stop.connect(func)

    def emit_finished(self):
        if self.signals_enabled:
            self.signals.finished.emit()

    def emit_error(self, error):
        if self.signals_enabled:
            self.signals.error.emit(error)
        self.error_tuple = error

    def emit_result(self, result):
        if self.signals_enabled:
            self.signals.result.emit(result)

    def emit_progress(self, progress, obj=None):
        if self.signals_enabled:
            self.signals.progress.emit(progress, obj)

    def emit_stop(self, stop):
        self.signals.stop.emit(stop)

    @QtCore.Slot()
    def run(self):
        try:
            result = self.agent()
        except Exception as expected:
            if self.signals_enabled:
                traceback.print_exc(file=sys.stdout)
            stacktrace = traceback.format_exc()

            exception = {
                'exception': expected,
                'stacktrace': stacktrace,
            }

            dl.exception(stacktrace, group_id='{0}/{1}'.format(
                'threaded_exceptions',
                self.agent.func_name, ))

            self.set_failed(True)
            self.emit_error((exception, self))
        else:
            self.setAutoDelete(True)
            self.emit_result(result)
            self.set_failed(False)
        finally:
            self.emit_finished()


def get_thread_worker(agent_func, thread_pool=None, result_func=None, error_func=None,
                      finished_func=None, progress_func=None, stop_func=None, parent=None):
    """
    This will create worker with thread pool for you, or you can add worker to your existing thread

    :param agent_func: This will be run, cannot be lambda.
    :param thread_pool: If no passed, will creates global instance, which can be accessed from worker.
    :param result_func: This func will be executed when thread finished without error, and should have return
    :param error_func: Executed when thread will fail
    :param finished_func: Executed even when thread fail, should not have any return
    :param progress_func: Emitting progress
    :param parent: Parent of the worker
    :return: Worker object
    """
    if not thread_pool:
        thread_pool = QtCore.QThreadPool().globalInstance()

    worker = ThreadWorker(agent_func, thread_pool, parent=parent)
    worker.result_func(result_func)
    worker.error_func(error_func)
    worker.finished_func(finished_func)
    worker.progress_func(progress_func)
    worker.stop_func(stop_func)

    return worker


def catch_error(func):
    def __tryexcept__(*args, **kwargs):

        try:
            func(*args, **kwargs)
        except Exception as expected:
            traceback.print_exc(file=sys.stdout)
            stacktrace = traceback.format_exc()

            exception = {
                'exception': expected,
                'stacktrace': stacktrace,
            }

            dl.exception(stacktrace, group_id='{0}/{1}'.format(
                'exceptions',
                func.func_name,))

            error_handle((exception, None))

    return __tryexcept__


def error_handle(args):
    stacktrace_dict, worker = args
    expected = stacktrace_dict['exception']

    error_type = catch_error_type(expected)

    exception_text = u'{0}<p>{1}</p><p><b>Catched Error: {2}</b></p>'.format(
        unicode(str(expected.__doc__), 'utf-8', errors='ignore'),
        unicode(str(expected.message), 'utf-8', errors='ignore'),
        str(error_type))

    if error_type in ['unknown_error', 'attribute_error']:
        title = u'{0}'.format(unicode(str(expected.__doc__), 'utf-8', errors='ignore'))
        message = u'{0}<p>{1}</p>'.format(
            u"<p>This is not usual type of Exception! See stacktrace for information</p>",
            exception_text)
        buttons = [('Ok', QtGui.QMessageBox.NoRole)]
        if worker:
            buttons.append(('Retry', QtGui.QMessageBox.ApplyRole))

        reply = show_message_predefined(
            title=title,
            message=message,
            stacktrace=stacktrace_dict['stacktrace'],
            buttons=buttons,
            parent=env_inst.ui_main,
            message_type='question',
        )
        if reply == QtGui.QMessageBox.ApplyRole:
            worker.try_start()

        return reply

    if error_type in ['connection_refused', 'connection_timeout']:
        title = '{0}, {1}'.format("Cannot connect to TACTIC Server!", error_type)
        message = u'{0}<p>{1}</p>'.format(
            u"<p>There is no Network connection to TACTIC Server, or Connection Timed Out</p>"
            u"<p>May be you set wrong server address?</p>",
            exception_text)
        buttons = [('Ok', QtGui.QMessageBox.NoRole)]

        if worker:
            buttons.append(('Retry', QtGui.QMessageBox.ApplyRole))

        if not env_inst.ui_conf:
            buttons.append(('Open Config', QtGui.QMessageBox.ActionRole))

        reply = show_message_predefined(
            title=title,
            message=message,
            stacktrace=stacktrace_dict['stacktrace'],
            buttons=buttons,
            parent=env_inst.ui_main,
            message_type='critical',
        )
        if reply == QtGui.QMessageBox.ApplyRole:
            worker.try_start()
        if reply == QtGui.QMessageBox.ActionRole:
            env_inst.ui_main.open_config_dialog()

        return reply

    if error_type == 'ticket_error':
        title = '{0}, {1}'.format("Ticket Error!", error_type)
        message = u'{0}<p>{1}</p>'.format(
            u"<p>Wrong ticket, or session may have expired!</p> <p>Generate new ticket?</p>",
            exception_text)
        buttons = [('Yes', QtGui.QMessageBox.YesRole),
                   ('No', QtGui.QMessageBox.NoRole)]

        if not env_inst.ui_conf:
            buttons.append(('Open Config', QtGui.QMessageBox.ActionRole))

        reply = show_message_predefined(
            title=title,
            message=message,
            stacktrace=stacktrace_dict['stacktrace'],
            buttons=buttons,
            parent=None,
            message_type='question',
        )
        if reply == QtGui.QMessageBox.YesRole:
            env_inst.ui_main.open_config_dialog()
            env_inst.ui_conf.hide()
            env_inst.ui_conf.create_server_page()
            env_inst.ui_conf.serverPageWidget.generate_ticket()
        if reply == QtGui.QMessageBox.ActionRole:
            env_inst.ui_main.open_config_dialog()

        return reply

    if error_type == 'no_project_error':
        title = '{0}, {1}'.format("This Project does not exists!", error_type)
        message = u'{0}<p>{1}</p>'.format(
            u"<p>Project from previous session currently not Exists!</p>",
            exception_text)
        buttons = [('Ok', QtGui.QMessageBox.NoRole)]

        if not env_inst.ui_conf:
            buttons.append(('Open Config', QtGui.QMessageBox.ActionRole))

        reply = show_message_predefined(
            title=title,
            message=message,
            stacktrace=stacktrace_dict['stacktrace'],
            buttons=buttons,
            parent=None,
            message_type='critical',
        )
        if reply == QtGui.QMessageBox.NoRole:
            env_inst.ui_main.restart_ui_main()
        if reply == QtGui.QMessageBox.ActionRole:
            env_inst.ui_main.open_config_dialog()

        return reply

    if error_type == 'login_pass_error':
        title = '{0}, {1}'.format("Wrong user Login or Password for TACTIC Server!", error_type)
        message = u'{0}<p>{1}</p>'.format(
            u"<p>You need to open config, and type correct Login and Password!</p>",
            exception_text)
        buttons = [('Ok', QtGui.QMessageBox.NoRole), ('Retry', QtGui.QMessageBox.ApplyRole)]

        if not env_inst.ui_conf:
            buttons.append(('Open Config', QtGui.QMessageBox.ActionRole))

        reply = show_message_predefined(
            title=title,
            message=message,
            stacktrace=stacktrace_dict['stacktrace'],
            buttons=buttons,
            parent=None,
            message_type='critical',
        )
        if reply == QtGui.QMessageBox.ActionRole:
            env_inst.ui_main.open_config_dialog()

        return reply

    if error_type == 'sql_connection_error':
        title = '{0}, {1}'.format("SQL Server Error!", error_type)
        message = u'{0}<p>{1}</p>'.format(
            u"<p>TACTIC Server can't connect to SQL server, may be SQL Server Down! Or wrong server port/ip </p>",
            exception_text)
        buttons = [('Ok', QtGui.QMessageBox.NoRole)]

        if not env_inst.ui_conf:
            buttons.append(('Open Config', QtGui.QMessageBox.ActionRole))

        reply = show_message_predefined(
            title=title,
            message=message,
            stacktrace=stacktrace_dict['stacktrace'],
            buttons=buttons,
            parent=None,
            message_type='critical',
        )
        if reply == QtGui.QMessageBox.ActionRole:
            env_inst.ui_main.open_config_dialog()

        return reply

    if error_type == 'protocol_error':
        title = '{0}, {1}'.format("Error with the Protocol!", error_type)
        message = u'{0}<p>{1}</p>'.format(u"<p>Something wrong!</p>", exception_text)
        buttons = [('Ok', QtGui.QMessageBox.NoRole),
                   ('Retry', QtGui.QMessageBox.ApplyRole)]

        if not env_inst.ui_conf:
            buttons.append(('Open Config', QtGui.QMessageBox.ActionRole))

        reply = show_message_predefined(
            title=title,
            message=message,
            stacktrace=stacktrace_dict['stacktrace'],
            buttons=buttons,
            parent=None,
            message_type='critical',
        )
        if reply == QtGui.QMessageBox.ActionRole:
            env_inst.ui_main.open_config_dialog()

        return reply


def show_message_predefined(title, message, stacktrace=None, buttons=None, parent=None, message_type='question'):
    """
    Showing message with title, text and returns pressed button
    :param title: 'Message Title'
    :param message: 'Message Text'
    :param message_type: 'question', 'warning', etc...
    :param buttons: tuple of buttons: (('Yes', QtGui.QMessageBox.YesRole), ('No', QtGui.QMessageBox.NoRole)), etc...
    :return: button role
    """
    if not buttons:
        buttons = (('Yes', QtGui.QMessageBox.YesRole), ('No', QtGui.QMessageBox.NoRole))

    if message_type == 'warning':
        msb_type = QtGui.QMessageBox.Warning
    elif message_type == 'information':
        msb_type = QtGui.QMessageBox.Information
    elif message_type == 'critical':
        msb_type = QtGui.QMessageBox.Critical
    else:
        msb_type = QtGui.QMessageBox.Question

    message_box = QtGui.QMessageBox(
        msb_type,
        title,
        message,
        QtGui.QMessageBox.NoButton,
        parent,
    )

    if stacktrace:
        layout = QtGui.QVBoxLayout()

        from thlib.ui_classes import ui_misc_classes

        collapse_wdg = ui_misc_classes.Ui_collapsableWidget(state=True)
        collapse_wdg.setLayout(layout)
        collapse_wdg.setText('Hide Stacktrace')
        collapse_wdg.setCollapsedText('Show Stacktrace')

        msb_layot = message_box.layout()

        # workaround for pyside2
        wdg_list = []

        for i in range(msb_layot.count()):
            wdg = msb_layot.itemAt(i).widget()
            if wdg:
                wdg_list.append(wdg)

        msb_layot.addWidget(wdg_list[0], 0, 0)
        msb_layot.addWidget(wdg_list[1], 0, 1)
        msb_layot.addWidget(wdg_list[2], 2, 1)
        msb_layot.addWidget(collapse_wdg, 1, 1)

        text_edit = QtGui.QPlainTextEdit()
        text_edit.setMinimumWidth(600)
        text_edit.setPlainText(stacktrace)

        layout.addWidget(text_edit)

    for title, role in buttons:
        message_box.addButton(title, role)

    message_box.exec_()
    return message_box.buttonRole(message_box.clickedButton())


def catch_error_type(exception):
    # print('Some exception appeared!', str(type(exception)), unicode(str(exception), 'utf-8', errors='ignore'))

    error = 'unknown_error'

    # Catch project existance
    if str(exception).find('No project') != -1:
        error = 'no_project_error'

    # Catch ticket error
    if str(exception).find('Cannot login with key:') != -1:
        error = 'ticket_error'

    # Catch socket exception, connection error
    if str(exception).find(
            'A connection attempt failed because the connected party did not properly respond after a period of time') != -1:
        error = 'connection_timeout'

    # Catch Connection refused
    if str(exception).find('No connection could be made because the target machine actively refused it') != -1:
        error = 'connection_refused'

    if str(exception).find('Connection refused') != -1:
        error = 'connection_refused'

    if str(exception).find('getaddrinfo failed') != -1:
        error = 'connection_refused'

    if str(exception).find('Login/Password combination incorrect') != -1:
        error = 'login_pass_error'

    if str(exception).find('connect to MySQL server') != -1:
        error = 'sql_connection_error'

    if str(exception).find('ProtocolError') != -1:
        error = 'protocol_error'

    if str(exception).find('object has no attribute') != -1:
        error = 'attribute_error'

    return error


def hex_to_rgb(hex_v, alpha=None, tuple=False):
    """
    Converts hex color to rgb/a
    Usage: hex_to_rgb('#9f8acf', 128)
    :param hex_v: string like "#9f8acf"
    :param alpha: string or int alpha ex: 128
    :return: rgba(r,g,b,a) or rgb(r,g,b)
    """
    r = int('0x' + hex_v[1:3], 0)
    g = int('0x' + hex_v[3:5], 0)
    b = int('0x' + hex_v[5:7], 0)
    if alpha:
        a = int(alpha)
        if tuple:
            return r, g, b, a
        else:
            return 'rgba({},{},{},{})'.format(r, g, b, a)
    else:
        if tuple:
            return r, g, b
        else:
            return 'rgb({},{},{})'.format(r, g, b)


def get_prc(prc, number):
    return int(prc * number / 100)


def sizes(size, precision=2):
    if size != '':
        size = int(size)
    else:
        size = 0
    suffixes = [' b', ' Kb', ' Mb', ' Gb', ' Tb']
    suffix_index = 0

    while size > 1024 and suffix_index < 4:
        suffix_index += 1
        if not size:
            size = 0
        size /= 1024.0

    return '{1:.{0}f} {2}'.format(precision, size, suffixes[suffix_index])


def html_to_hex(text_html):
    text_html_cmp = zlib.compress(text_html.encode('utf-8'), 9)
    text_html_hex = 'zlib:' + binascii.b2a_hex(text_html_cmp)
    if len(text_html_hex) > len(text_html):
        text_html_hex = text_html

    return text_html_hex


def hex_to_html(text_hex):
    if text_hex:
        detect_zlib = text_hex.rfind('zlib:')
        if detect_zlib == 0:
            hex_to_text = zlib.decompress(binascii.a2b_hex(text_hex[5:]))
        else:
            hex_to_text = text_hex

        return hex_to_text


def to_json(obj, pretty=False, use_ast=False):

    if use_ast:
        return str(obj)
    else:
        indent = None
        separators = (',', ':')
        if pretty:
            indent = 4
            separators = (', ', ': ')
        return json.dumps(obj, indent=indent, separators=separators)


def from_json(obj, use_ast=False):
    if obj:
        if use_ast:
            return ast.literal_eval(str(obj))
        else:
            return json.loads(obj)


def gen_acronym(word, length=2):
    acronym = ''
    if not word:
        return 'E'
    word = word[0].upper() + word[1:]

    for k, v in enumerate(word):
        if v.isupper() and len(acronym) < length:
            acronym += v
            if v == acronym[:-1]:
                acronym = acronym[:-1]

    if len(acronym) < length:
        acronym += word[1:length]
    return acronym


def prettify_text(text, first_letter=False):
    if text:
        if first_letter:
            text = text.replace('_', ' ').split(' ')
            final_text = []
            for word in text:
                word = word[:1].upper() + word[1:]
                final_text.append(word)
            return u' '.join(final_text)
        else:
            return text.replace('_', ' ').title()


def minify_code(source, pack=False):
    import side.pyminifier as pyminifier
    cleanup_comments = pyminifier.minification.remove_comments_and_docstrings(source)
    cleanup_blanks = pyminifier.minification.remove_blank_lines(cleanup_comments)
    multi_line = pyminifier.minification.join_multiline_pairs(cleanup_blanks)
    dedent = pyminifier.minification.dedent(multi_line)
    reduce_op = pyminifier.minification.reduce_operators(dedent)
    if pack:
        return pyminifier.compression.gz_pack(reduce_op)
    else:
        return reduce_op


def get_ver_rev(ver=None, rev=None):
    if ver > 0 and rev > 0:
        result = '<span style="color:#008498;">Ver: {0:03d};</span><span style="color:#0a9800;"> Rev: {1:03d}</span>'.format(
            ver,
            rev)
    elif ver > 0 and rev == 0:
        result = '<span style="color:#008498;">Ver: {0:03d}</span>'.format(ver)
    elif ver == 0 and rev > 0:
        result = '<span style="color:#0a9800;"> Rev: {0:03d}</span>'.format(rev)
    else:
        result = ''

    return result


def group_dict_by(dicts_list, group_by):
    grouped = collections.defaultdict(list)
    for dic in dicts_list:
        grouped[dic.get(group_by)].append(dic)

    return grouped


def get_controls_dict(ignore_list=None):
    controls_dict = {
        'QLineEdit': {'obj_name': [], 'value': []},
        'QCheckBox': {'obj_name': [], 'value': []},
        'QComboBox': {'obj_name': [], 'value': []},
        'QTreeWidget': {'obj_name': [], 'value': []},
        'QToolButton': {'obj_name': [], 'value': []},
        'QRadioButton': {'obj_name': [], 'value': []},
        'QGroupBox': {'obj_name': [], 'value': []},
        'QSpinBox': {'obj_name': [], 'value': []},
    }
    if ignore_list:
        for item in ignore_list:
            if item == QtGui.QLineEdit:
                controls_dict.pop('QLineEdit')
            if item == QtGui.QCheckBox:
                controls_dict.pop('QCheckBox')
            if item == QtGui.QComboBox:
                controls_dict.pop('QComboBox')
            if item == QtGui.QTreeWidget:
                controls_dict.pop('QTreeWidget')
            if item == QtGui.QToolButton:
                controls_dict.pop('QToolButton')
            if item == QtGui.QRadioButton:
                controls_dict.pop('QRadioButton')
            if item == QtGui.QGroupBox:
                controls_dict.pop('QGroupBox')
            if item == QtGui.QGroupBox:
                controls_dict.pop('QSpinBox')

    return copy.deepcopy(controls_dict)


def get_value_from_config(config_dict, control):
    if config_dict:
        for all_values in config_dict.itervalues():
            for obj_name, value in zip(all_values['obj_name'], all_values['value']):
                if control == obj_name:
                    return value


def walk_through_layouts(args=None, ignore_list=None):
    all_widgets = []
    if not ignore_list:
        ignore_list = []
    for layout in args:
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if type(widget) not in ignore_list:
                all_widgets.append(layout.itemAt(i).widget())

    return all_widgets


def clear_property_dict(in_dict):
    # clearing all dict
    for i in in_dict.itervalues():
        for val in i.itervalues():
            val[:] = []


def campare_dicts(dict_one, dict_two):
    result = True

    for key, val in dict_one.iteritems():
        for key1, val1 in dict_two.iteritems():
            if key == key1:
                for i, j in enumerate(val['value']):
                    if j != val1['value'][i]:
                        result = False
                        break

    return result


def store_property_by_widget_type(widget, in_dict):
    if isinstance(widget, QtGui.QLineEdit):
        if not in_dict.get('QLineEdit'):
            in_dict['QLineEdit'] = {'value': [], 'obj_name': []}
        in_dict['QLineEdit']['value'].append(str(widget.text()))
        in_dict['QLineEdit']['obj_name'].append(widget.objectName())

    if isinstance(widget, QtGui.QCheckBox):
        if not in_dict.get('QCheckBox'):
            in_dict['QCheckBox'] = {'value': [], 'obj_name': []}
        in_dict['QCheckBox']['value'].append(int(bool(widget.checkState())))
        in_dict['QCheckBox']['obj_name'].append(widget.objectName())

    if isinstance(widget, QtGui.QComboBox):
        if not in_dict.get('QComboBox'):
            in_dict['QComboBox'] = {'value': [], 'obj_name': []}
        in_dict['QComboBox']['value'].append(int(widget.currentIndex()))
        in_dict['QComboBox']['obj_name'].append(widget.objectName())

    if isinstance(widget, QtGui.QTreeWidget):
        if not in_dict.get('QTreeWidget'):
            in_dict['QTreeWidget'] = {'value': [], 'obj_name': []}
        in_dict['QTreeWidget']['value'].append(int(widget.topLevelItemCount()))
        in_dict['QTreeWidget']['obj_name'].append(widget.objectName())

    if isinstance(widget, QtGui.QToolButton):
        if not in_dict.get('QToolButton'):
            in_dict['QToolButton'] = {'value': [], 'obj_name': []}
        in_dict['QToolButton']['value'].append(str(widget.styleSheet()))
        in_dict['QToolButton']['obj_name'].append(widget.objectName())

    if isinstance(widget, QtGui.QGroupBox):
        if not in_dict.get('QGroupBox'):
            in_dict['QGroupBox'] = {'value': [], 'obj_name': []}
        in_dict['QGroupBox']['value'].append(int(bool(widget.isChecked())))
        in_dict['QGroupBox']['obj_name'].append(widget.objectName())

    if isinstance(widget, QtGui.QRadioButton):
        if not in_dict.get('QRadioButton'):
            in_dict['QRadioButton'] = {'value': [], 'obj_name': []}
        in_dict['QRadioButton']['value'].append(int(bool(widget.isChecked())))
        in_dict['QRadioButton']['obj_name'].append(widget.objectName())

    if isinstance(widget, QtGui.QSpinBox):
        if not in_dict.get('QSpinBox'):
            in_dict['QSpinBox'] = {'value': [], 'obj_name': []}
        in_dict['QSpinBox']['value'].append(int(widget.value()))
        in_dict['QSpinBox']['obj_name'].append(widget.objectName())


def change_property_by_widget_type(widget, in_dict):
    if isinstance(widget, QtGui.QLineEdit) and in_dict.get('QLineEdit'):
        if widget.objectName() in in_dict['QLineEdit']['obj_name']:
            val = in_dict['QLineEdit']['value'][in_dict['QLineEdit']['obj_name'].index(widget.objectName())]
            widget.setText(val)

    elif isinstance(widget, QtGui.QCheckBox) and in_dict.get('QCheckBox'):
        if widget.objectName() in in_dict['QCheckBox']['obj_name']:
            val = in_dict['QCheckBox']['value'][in_dict['QCheckBox']['obj_name'].index(widget.objectName())]
            widget.setChecked(val)

    elif isinstance(widget, QtGui.QGroupBox) and in_dict.get('QGroupBox'):
        if widget.objectName() in in_dict['QGroupBox']['obj_name']:
            val = in_dict['QGroupBox']['value'][in_dict['QGroupBox']['obj_name'].index(widget.objectName())]
            widget.setChecked(val)

    elif isinstance(widget, QtGui.QRadioButton) and in_dict.get('QRadioButton'):
        if widget.objectName() in in_dict['QRadioButton']['obj_name']:
            val = in_dict['QRadioButton']['value'][in_dict['QRadioButton']['obj_name'].index(widget.objectName())]
            widget.setChecked(val)

    elif isinstance(widget, QtGui.QSpinBox) and in_dict.get('QSpinBox'):
        if widget.objectName() in in_dict['QSpinBox']['obj_name']:
            val = in_dict['QSpinBox']['value'][in_dict['QSpinBox']['obj_name'].index(widget.objectName())]
            widget.setValue(int(val))

    elif isinstance(widget, QtGui.QComboBox) and in_dict.get('QComboBox'):
        if widget.objectName() in in_dict['QComboBox']['obj_name']:
            val = in_dict['QComboBox']['value'][in_dict['QComboBox']['obj_name'].index(widget.objectName())]
            widget.setCurrentIndex(int(val))

    elif isinstance(widget, QtGui.QToolButton) and in_dict.get('QToolButton'):
        if widget.objectName() in in_dict['QToolButton']['obj_name']:
            val = in_dict['QToolButton']['value'][in_dict['QToolButton']['obj_name'].index(widget.objectName())]
            widget.setStyleSheet(val)


def dockwidget_area_to_str(main_window, dockwidget):
    if main_window.dockWidgetArea(dockwidget) == QtCore.Qt.TopDockWidgetArea:
        return 'top'
    if main_window.dockWidgetArea(dockwidget) == QtCore.Qt.BottomDockWidgetArea:
        return 'bottom'
    if main_window.dockWidgetArea(dockwidget) == QtCore.Qt.LeftDockWidgetArea:
        return 'left'
    if main_window.dockWidgetArea(dockwidget) == QtCore.Qt.RightDockWidgetArea:
        return 'right'


def str_to_dockwidget_area(area):
    if area == 'top':
        return QtCore.Qt.TopDockWidgetArea
    elif area == 'bottom':
        return QtCore.Qt.BottomDockWidgetArea
    elif area == 'left':
        return QtCore.Qt.LeftDockWidgetArea
    elif area == 'right':
        return QtCore.Qt.RightDockWidgetArea


def toolbar_area_to_str(main_window, toolbar):
    if main_window.toolBarArea(toolbar) == QtCore.Qt.TopToolBarArea:
        return 'top'
    elif main_window.toolBarArea(toolbar) == QtCore.Qt.BottomToolBarArea:
        return 'bottom'
    elif main_window.toolBarArea(toolbar) == QtCore.Qt.LeftToolBarArea:
        return 'left'
    elif main_window.toolBarArea(toolbar) == QtCore.Qt.RightToolBarArea:
        return 'right'


def str_to_toolbar_area(area):
    if area == 'top':
        return QtCore.Qt.TopToolBarArea
    elif area == 'bottom':
        return QtCore.Qt.BottomToolBarArea
    elif area == 'left':
        return QtCore.Qt.LeftToolBarArea
    elif area == 'right':
        return QtCore.Qt.RightToolBarArea


def store_dict_values(widgets, out_dict, parent):
    clear_property_dict(out_dict)
    for widget in widgets:
        if isinstance(widget,
                      (QtGui.QLineEdit,
                       QtGui.QCheckBox,
                       QtGui.QComboBox,
                       QtGui.QTreeWidget,
                       QtGui.QToolButton,
                       QtGui.QRadioButton,
                       QtGui.QGroupBox,
                       QtGui.QSpinBox,)):
            store_property_by_widget_type(widget, out_dict)
            widget.installEventFilter(parent)


def apply_dict_values(widgets, in_dict):
    for widget in widgets:
        if isinstance(widget,
                      (QtGui.QLineEdit,
                       QtGui.QCheckBox,
                       QtGui.QComboBox,
                       QtGui.QTreeWidget,
                       QtGui.QToolButton,
                       QtGui.QRadioButton,
                       QtGui.QGroupBox,
                       QtGui.QSpinBox,)):
            change_property_by_widget_type(widget, in_dict)


def collect_defaults(defaults_dict=None, init_dict=None, layouts_list=None, get_values=False, apply_values=False,
                     store_defaults=False, undo_changes=False, parent=None, ignore_list=None):
    widgets = walk_through_layouts(layouts_list, ignore_list)

    if not init_dict:
        init_dict = get_controls_dict(ignore_list)

    if undo_changes:
        apply_dict_values(widgets, defaults_dict)

    if apply_values:
        apply_dict_values(widgets, init_dict)

    if get_values:
        store_dict_values(widgets, init_dict, parent)

    if store_defaults:
        store_dict_values(widgets, defaults_dict, parent)

    if not defaults_dict:
        defaults_dict = get_controls_dict(ignore_list)
        store_dict_values(widgets, defaults_dict, parent)

    return defaults_dict, init_dict


def create_tab_label(tab_name, stype):
    wdg = QtGui.QFrame()
    lay = QtGui.QVBoxLayout()
    lay.setSpacing(0)
    lay.setContentsMargins(4, 4, 4, 6)
    wdg.setLayout(lay)
    tab_label = QtGui.QLabel()
    lay.addWidget(tab_label)
    tab_label.setText(tab_name)
    tab_label.setAlignment(QtCore.Qt.AlignCenter)

    font = Qt4Gui.QFont()
    font.setPointSize(8)
    font.setWeight(65)
    font.setBold(True)
    tab_label.setFont(font)
    tab_label.setTextFormat(QtCore.Qt.PlainText)
    tab_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
    tab_label.setMargin(0)

    tab_color = stype.info['color']
    if tab_color:
        effect = QtGui.QGraphicsDropShadowEffect(tab_label)
        t_c = hex_to_rgb(tab_color, alpha=8, tuple=True)
        effect.setOffset(2, 2)
        effect.setColor(Qt4Gui.QColor(t_c[0], t_c[1], t_c[2], t_c[3]))
        effect.setBlurRadius(8)
        tab_label.setGraphicsEffect(effect)

        tab_color_rgb = hex_to_rgb(tab_color, alpha=128)
        tab_label.setStyleSheet('QLabel {border: 0px;}')
        wdg.setStyleSheet('QFrame {background-color: transparent;' +
                          'border-bottom: 2px solid {0};'.format(tab_color_rgb) + '}')
    return wdg


def get_icon(icon_name, icon_name_active=None, color=None, color_active=None, icons_set='fa', **kwargs):

    if not color:
        color = Qt4Gui.QColor(200, 200, 200)
    if not color_active:
        color_active = Qt4Gui.QColor(240, 240, 240)
    if not icon_name_active:
        icon_name_active = icon_name
    styling_icon = qta.icon(
        '{0}.{1}'.format(icons_set, icon_name),
        active='{0}.{1}'.format(icons_set, icon_name_active),
        color=color,
        color_active=color_active,
        **kwargs)

    return styling_icon


# New QTreeWidget funcs

def add_item_to_tree(tree_widget, tree_item, tree_item_widget=None, insert_pos=None):
    if type(tree_widget) == QtGui.QTreeWidget:
        if insert_pos is not None:
            tree_widget.insertTopLevelItem(insert_pos, tree_item)
        else:
            tree_widget.addTopLevelItem(tree_item)
        if tree_item_widget:
            tree_widget.setItemWidget(tree_item, 0, tree_item_widget)
            tree_widget.resizeColumnToContents(0)
    else:
        if insert_pos is not None:
            tree_widget.insertChild(insert_pos, tree_item)
        else:
            tree_widget.addChild(tree_item)
        if tree_item_widget:
            tree_widget.treeWidget().setItemWidget(tree_item, 0, tree_item_widget)
            tree_widget.treeWidget().resizeColumnToContents(0)


def add_preview_item(parent_item, file_object=None, screenshot=None):
    from thlib.ui_classes.ui_item_classes import Ui_previewItemWidget

    tree_item = QtGui.QTreeWidgetItem()

    tree_item_widget = Ui_previewItemWidget(file_object=file_object, screenshot=screenshot)

    add_item_to_tree(parent_item, tree_item, tree_item_widget)

    tree_item_widget.setParent(tree_item_widget.parent())

    return tree_item_widget


def add_commit_item(parent_item, item_widget):
    from thlib.ui_classes.ui_item_classes import Ui_commitItemWidget

    tree_item = QtGui.QTreeWidgetItem()

    tree_item_widget = Ui_commitItemWidget(item_widget=item_widget)

    add_item_to_tree(parent_item, tree_item, tree_item_widget)

    tree_item_widget.setParent(tree_item_widget.parent())

    return tree_item_widget


def add_sobject_item(parent_item, parent_widget, sobject, stype, item_info, insert_pos=None, ignore_dict=None):
    from thlib.ui_classes.ui_item_classes import Ui_itemWidget
    tree_item = QtGui.QTreeWidgetItem()
    item_info_dict = {
        'relates_to': item_info['relates_to'],
        'is_expanded': False,
        'sep_versions': item_info['sep_versions']
    }

    tree_item.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.ShowIndicator)
    tree_item_widget = Ui_itemWidget(sobject, stype, item_info_dict, ignore_dict)

    tree_item_widget.tree_item = tree_item
    tree_item_widget.search_widget = parent_widget

    add_item_to_tree(parent_item, tree_item, tree_item_widget, insert_pos=insert_pos)

    tree_item_widget.setParent(tree_item_widget.parent())

    return tree_item_widget


def add_process_item(tree_widget, parent_widget, sobject, stype, process, item_info, insert_pos=None, pipeline=None):

    from thlib.ui_classes.ui_item_classes import Ui_processItemWidget

    tree_item = QtGui.QTreeWidgetItem()
    item_info_dict = {
        'relates_to': item_info['relates_to'],
        'is_expanded': False,
        'sep_versions': item_info['sep_versions']
    }

    tree_item_widget = Ui_processItemWidget(sobject, stype, process, item_info_dict, pipeline)

    tree_item_widget.tree_item = tree_item
    tree_item_widget.search_widget = parent_widget

    add_item_to_tree(tree_widget, tree_item, tree_item_widget, insert_pos=insert_pos)

    tree_item_widget.setParent(tree_item_widget.parent())

    return tree_item_widget


def add_snapshot_item(tree_widget, parent_widget, sobject, stype, process, pipeline, snapshots, item_info, sep_versions=False,
                      insert_at_top=True):
    from thlib.ui_classes.ui_item_classes import Ui_snapshotItemWidget
    snapshots_items = []

    for key, context in snapshots.contexts.items():
        tree_item = QtGui.QTreeWidgetItem()
        item_info_dict = {
            'relates_to': item_info['relates_to'],
            'is_expanded': False,
            'sep_versions': item_info['sep_versions']
        }
        snapshot_item = Ui_snapshotItemWidget(
            sobject,
            stype,
            process,
            pipeline,
            key,
            context.versionless.values(),
            item_info_dict
        )
        snapshot_item.tree_item = tree_item
        snapshot_item.search_widget = parent_widget

        insert_pos = 0
        if insert_at_top:
            add_item_to_tree(tree_widget, tree_item, snapshot_item, insert_pos)
        else:
            add_item_to_tree(tree_widget, tree_item, snapshot_item)

        snapshot_item.setParent(snapshot_item.parent())

        if not sep_versions:
            for i, versions in enumerate(context.versions.values()):
                tree_item_versions = QtGui.QTreeWidgetItem()
                item_info_dict = {
                    'relates_to': item_info['relates_to'],
                    'is_expanded': False,
                    'sep_versions': item_info['sep_versions']
                }
                snapshot_item_versions = Ui_snapshotItemWidget(
                    sobject,
                    stype,
                    process,
                    pipeline,
                    key,
                    [versions],
                    item_info_dict,
                )
                snapshot_item_versions.tree_item = tree_item_versions
                snapshot_item_versions.search_widget = parent_widget

                add_item_to_tree(tree_item, tree_item_versions, snapshot_item_versions)

                snapshot_item_versions.setParent(snapshot_item_versions.parent())

    return snapshots_items


def add_versions_snapshot_item(tree_widget, parent_widget, sobject, stype, process, pipeline, context, snapshots, item_info):

    from thlib.ui_classes.ui_item_classes import Ui_snapshotItemWidget

    for i, (key, snapshot) in enumerate(snapshots.items()):
        tree_item = QtGui.QTreeWidgetItem()
        item_info_dict = {
            'relates_to': item_info['relates_to'],
            'is_expanded': False,
            'sep_versions': item_info['sep_versions']
        }
        snapshot_item = Ui_snapshotItemWidget(
            sobject,
            stype,
            process,
            pipeline,
            context,
            [snapshot],
            item_info_dict,
        )
        snapshot_item.tree_item = tree_item
        snapshot_item.search_widget = parent_widget

        add_item_to_tree(tree_widget, tree_item, snapshot_item)

        snapshot_item.setParent(snapshot_item.parent())


def add_child_item(tree_widget, parent_widget, sobject, stype, child, item_info):
    from thlib.ui_classes.ui_item_classes import Ui_childrenItemWidget
    tree_item = QtGui.QTreeWidgetItem()
    item_info_dict = {
        'relates_to': item_info['relates_to'],
        'is_expanded': False,
        'sep_versions': item_info['sep_versions']
    }
    tree_item_widget = Ui_childrenItemWidget(sobject, stype, child, item_info_dict)

    tree_item_widget.tree_item = tree_item
    tree_item_widget.search_widget = parent_widget

    add_item_to_tree(tree_widget, tree_item, tree_item_widget)

    tree_item_widget.setParent(tree_item_widget.parent())

    return tree_item_widget


def get_all_tree_item_widgets(wdg, items_list=None):

    if not items_list:
        items_list = []

    if type(wdg) == QtGui.QTreeWidget:
        items_count = wdg.topLevelItemCount()
        tree_item = wdg.topLevelItem
        tree_wdg = wdg
    else:
        items_count = wdg.childCount()
        tree_item = wdg.child
        tree_wdg = wdg.treeWidget()

    for i in range(items_count):
        item = tree_item(i)
        item_wdg = tree_wdg.itemWidget(item, 0)
        items_list.append(item_wdg)

        if item.childCount() > 0:
            get_all_tree_item_widgets(item, items_list)

    return items_list


def recursive_close_tree_item_widgets(wdg):
    if type(wdg) == QtGui.QTreeWidget:
        items_count = wdg.topLevelItemCount()
        tree_item = wdg.topLevelItem
        tree_wdg = wdg
    else:
        items_count = wdg.childCount()
        tree_item = wdg.child
        tree_wdg = wdg.treeWidget()

    for i in range(items_count):
        item = tree_item(i)
        item_wdg = tree_wdg.itemWidget(item, 0)
        if item_wdg:
            item_wdg.close()

        if item.childCount() > 0:
            recursive_close_tree_item_widgets(item)


def tree_recursive_expand(wdg, state):
    """ Expanding tree to the ground"""

    if type(wdg) == QtGui.QTreeWidget:
        items_count = wdg.topLevelItemCount()
        tree_item = wdg.topLevelItem
        tree_wdg = wdg
    else:
        items_count = wdg.childCount()
        tree_item = wdg.child
        tree_wdg = wdg.treeWidget()

    for i in range(items_count):
        item = tree_item(i)
        item.setExpanded(state)
        item_wdg = tree_wdg.itemWidget(item, 0)
        if state:
            item_wdg.expand_recursive()
        else:
            item_wdg.collapse_recursive()


def tree_state(wdg, state_dict):
    """ Recursive getting data from each tree item"""

    if type(wdg) == QtGui.QTreeWidget:
        lv = wdg.topLevelItemCount()
        for i in range(lv):
            item = wdg.topLevelItem(i)
            d = {
                'd': {'s': item.isSelected(), 'e': item.isExpanded()},
                's': {}
            }
            if item.childCount() > 0:
                tree_state(item, d)
            state_dict[i] = d
    else:
        lv = wdg.childCount()
        for i in range(lv):
            item = wdg.child(i)
            d = {
                'd': {'s': item.isSelected(), 'e': item.isExpanded()},
                's': {}
            }
            if item.childCount() > 0:
                tree_state(item, d)
            state_dict['s'][i] = d

    return state_dict


def tree_state_revert(wdg, state_dict):
    """ Recursive setting data to each tree item"""
    if type(wdg) == QtGui.QTreeWidget:
        lv = wdg.topLevelItemCount()
        tree_item = wdg.topLevelItem
        tree_wdg = wdg
    else:
        lv = wdg.childCount()
        tree_item = wdg.child
        tree_wdg = wdg.treeWidget()

    for i in range(lv):
        if state_dict.get(i):
            item = tree_item(i)
            item_widget = tree_wdg.itemWidget(item, 0)
            item_widget.set_expand_state(state_dict[i]['d']['e'])
            item_widget.set_selected_state(state_dict[i]['d']['s'])
            item_widget.set_children_states(state_dict[i]['s'])
            if item.childCount() > 0:
                tree_state_revert(item, state_dict[i]['s'])
            # Scrolling to item
            if item.isSelected():
                tree_wdg.scrollToItem(item)


# files etc routine

def split_files_and_dirs(filename):
    dirs_list = []
    files_list = []
    for single in filename:
        if os.path.isdir(single):
            dirs_list.append(single)
        else:
            files_list.append(single)

    return dirs_list, files_list


def file_format(ext):
    formats = {
        'ma': ['ma', 'mayaAscii', 'maya', 'file'],
        'mb': ['mb', 'mayaBinary', 'maya', 'file'],
        'hip': ['hip', 'Houdini', 'houdini', 'file'],
        '3b': ['3b', '3D-Coat', 'coat', 'file'],
        'max': ['max', '3DSMax scene', 'max', 'file'],
        'scn': ['scn', 'Softimage XSI', 'xsi', 'file'],
        'mud': ['mud', 'Mudbox', 'mudbox', 'file'],
        'abc': ['abc', 'Alembic', 'cache', 'file'],
        'obj': ['obj', 'OBJ', 'obj', 'file'],
        '3ds': ['3ds', '3DSMax model', 'obj', 'file'],
        'nk': ['nk', 'Nuke', 'nuke', 'file'],
        'fbx': ['fbx', 'FBX', 'obj', 'file'],
        'dae': ['dae', 'COLLADA', 'cache', 'file'],
        'rs': ['rs', 'Redshift Proxy', 'cache', 'file'],
        'vdb': ['vdb', 'Open VDB', 'cache', 'file'],
        'jpg': ['jpg', 'JPEG Image', 'image', 'preview'],
        'jpeg': ['jpeg', 'JPEG Image', 'image', 'preview'],
        'psd': ['psd', 'Photoshop PSD', 'image', 'file'],
        'tif': ['tif', 'TIFF Image', 'image', 'preview'],
        'tiff': ['tiff', 'TIFF Image', 'image', 'preview'],
        'png': ['png', 'PNG Image', 'image', 'preview'],
        'tga': ['tga', 'TARGA Image', 'image', 'file'],
        'exr': ['exr', 'EXR Image', 'image', 'file'],
        'hdr': ['hdr', 'HDR Image', 'image', 'file'],
        'dpx': ['dpx', 'DPX Image', 'image', 'file'],
        'mov': ['mov', 'MOV Animation', 'movie', 'file'],
        'avi': ['avi', 'AVI Animation', 'movie', 'file'],
    }
    low_case_ext = ext.lower()
    if low_case_ext in formats.keys():
        return formats[low_case_ext]
    else:
        return [low_case_ext, low_case_ext, 'main', 'file']


def extract_extension(filename):
    base_filename = unicode(os.path.basename(filename))
    ext = base_filename.split('.', -1)
    if not os.path.isdir(filename):
        if base_filename == ext[0]:
            return ['', 'No Ext', 'main', 'file']
        elif len(ext) > 1:
            return file_format(ext[-1])
    elif os.path.isdir(filename):
        return ['', 'Folder', 'folder', 'folder']


def extract_filename(filename, no_ext=False):
    name = unicode(os.path.basename(filename)).split('.')
    if len(name) > 1:
        if no_ext:
            return u'.'.join(name[:-1])
        else:
            return u'.'.join(name)
    else:
        return name[0]


def extract_dirname(filename):
    dir = unicode(os.path.realpath(filename)).split('.', 1)
    if dir[0] == filename:
        return os.path.dirname(filename)
    if len(dir) == 1 and not os.path.isdir(filename):
        return dir[0]
    else:
        return os.path.dirname(filename)


def open_file_associated(filepath):
    # print 'OPENING FILE'
    if filepath and os.path.exists(filepath):
        if env_mode.get_platform() == 'Linux':
            subprocess.Popen(('xdg-open', filepath), stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            # print proc.communicate()
            # print os.environ
        else:
            os.startfile(filepath)


def open_folder(filepath, highlight=True):
    if filepath and os.path.exists(filepath):
        if env_mode.get_platform() == 'Linux':
            if highlight:
                subprocess.call(('nautilus', '-s', filepath))
            else:
                subprocess.call(('xdg-open', filepath))
        elif env_mode.get_platform() == 'Windows':
            if highlight:
                subprocess.call(u'explorer /select, "{0}"'.format(filepath))
            else:
                os.startfile(filepath)
        else:
            os.startfile(filepath)


def form_path(path, tp=None):
    if env_mode.get_platform() == 'Linux' or tp == 'linux':
        formed_path = path.replace('\\', '/').replace('\\\\', '/').replace('//', '/')
    elif env_mode.get_platform() == 'Windows' or tp == 'win':
        formed_path = path.replace('/', '\\')
    else:
        formed_path = path.replace('\\', '/')
    return formed_path


def get_st_size(file_path):
    if type(file_path) == list:
        total_size = 0
        for fl in file_path:
            if os.path.exists(fl):
                total_size += os.stat(fl)[ST_SIZE]
        return total_size
    else:
        if os.path.exists(file_path):
            return os.stat(file_path)[ST_SIZE]


def get_file_asset_dir(item):
    repo_name = item.snapshot.get('repo')
    base_dir = env_tactic.get_base_dir('base')
    if repo_name:
        current_dir = env_tactic.get_base_dir(repo_name)
        if current_dir:
            asset_dir = current_dir.get('value')[0]
        else:
            asset_dir = base_dir.get('value')[0]
    else:
        asset_dir = base_dir.get('value')[0]
    return asset_dir


def get_abs_path(item, file_type=None):
    if file_type:
        modes = file_type
    else:
        modes = env_mode.modes
    modes.append('main')

    for mode in modes:
        if item.files.get(mode):
            main_file = item.files[mode][0]
            asset_dir = get_file_asset_dir(item)
            file_path = form_path(
                '{0}/{1}/{2}'.format(asset_dir, main_file['relative_dir'], main_file['file_name']))

            return file_path


def get_snapshot_asset_dir(snapshot_dict):
    repo_name = snapshot_dict.get('repo')
    base_dir = env_tactic.get_base_dir('base')
    if repo_name:
        current_dir = env_tactic.get_base_dir(repo_name)
        if current_dir:
            asset_dir = current_dir.get('value')[0]
        else:
            asset_dir = base_dir.get('value')[0]
    else:
        asset_dir = base_dir.get('value')[0]
    return asset_dir


def get_abs_file_path_name(snapshot_dict, file_dict):
    asset_dir = get_snapshot_asset_dir(snapshot_dict)
    file_path = form_path(
        '{0}/{1}/{2}'.format(asset_dir, file_dict['relative_dir'], file_dict['file_name']))

    return file_path


def simplify_html(html, pretty=False):
    soup = BeautifulSoup(html, "html.parser")
    if pretty:
        return unicode(soup.body.prettify())
    else:
        return unicode(soup.body)


def to_plain_text(html, strip=80):
    text_doc = Qt4Gui.QTextDocument()
    text_doc.setHtml(html)
    if strip:
        plain_text = text_doc.toPlainText()[:strip]
        if len(plain_text) > strip - 1:
            plain_text += ' ...'
    else:
        plain_text = text_doc.toPlainText()

    return plain_text


def qsize_to_tuple(qsize):
    return qsize.toTuple()


def tuple_to_qsize(qtuple, qtype='size'):
    if qtype == 'size':
        return QtCore.QSize(qtuple[0], qtuple[1])
    elif qtype == 'pos':
        return QtCore.QPoint(qtuple[0], qtuple[1])
    elif qtype == 'rect':
        return QtCore.QRect(qtuple[0], qtuple[1], qtuple[2], qtuple[3])


# CLASSES #

class FileObject(object):
    def __init__(self, file_=None, template_=None):

        self._file = file_
        self._template = template_
        self._type = None
        self._previewable = None
        self._file_type = None
        self._files_list = []
        self._file_path = None
        self._file_name = None
        self._sizes_list = []
        self._new_filename = None
        self._new_filepath = None
        self._new_frame_padding = None
        self._new_template = None
        self._abs_file_name = None
        self._pretty_file_name = None
        self._file_ext = None
        self._layer = None
        self._base_file_type_pretty_name = None
        self._base_file_type = None
        self._tactic_file_type = None
        self._sequence_length = None
        self._sequence_padding = None
        self._sequence_frames = []
        self._sequence_start = None
        self._sequence_end = None
        self._sequence_missing_frames = None
        self._app_info = None

        self._tiles_count = None
        self._tiles = []

        if self._file:
            self.init_files()

    def get_abs_file_name(self, file_dict=None, pretty=False, filename=False, no_ext=False):

        if not file_dict:
            file_dict = self.get_all_files_dicts(True)

        if not file_dict and self._abs_file_name:
            return self._abs_file_name

        separators = self._template['pattern_separators']
        order = self._template['order']

        if len(order) - len(separators) > 0:
            separators.insert(0, '')

        order_format = u''.join('%s{%s}' % (k, j) for j, k in zip(order, separators))

        if pretty:
            self._abs_file_name = order_format.format(**self.get_pretty_frames_and_udims(file_dict.copy()))
        else:
            self._abs_file_name = order_format.format(**file_dict)
        if filename:
            if no_ext:
                return self.__get_filename(file_dict.copy(), no_ext=True).get('filename')
            else:
                return order_format.format(**self.__get_filename(file_dict.copy()))

        return self._abs_file_name

    @staticmethod
    def __get_filename(file_dict, no_ext=False):
        if file_dict.get('filename'):
            file_dict['filename'] = file_dict.get('filename').split('/')[-1]
            if no_ext and file_dict.get('ext'):
                file_dict['filename'].replace('.{0}'.format(file_dict['ext']), '')
        return file_dict

    def get_pretty_frames_and_udims(self, file_dict):
        if file_dict.get('frame'):
            file_dict['frame'] = '[{}]'.format('#' * self.get_sequence_padding())
        if file_dict.get('udim'):
            file_dict['udim'] = '[UUVV]'
        if file_dict.get('uv'):
            file_dict['uv'] = '[u<>_v<>]'

        return file_dict

    def get_metadata(self):
        metadata_dict = {}
        if self.get_file_name(True):
            metadata_dict['filename'] = self.get_file_name(True)
        if self.get_file_ext():
            metadata_dict['ext'] = self.get_file_ext()
        if self.get_layer():
            metadata_dict['layer'] = self.get_layer()
        if self.get_sequence_frameranges():
            metadata_dict['frameranges'] = self.get_sequence_frameranges()
        if self.get_sequence_frame_range():
            metadata_dict['frame_range'] = self.get_sequence_frame_range()
        if self.get_sequence_padding():
            metadata_dict['padding'] = self.get_sequence_padding()
        if self.get_tiles():
            metadata_dict['udims'] = self.get_tiles()
        if self.get_type():
            metadata_dict['type'] = self.get_type()
        if not self._sizes_list:
            metadata_dict['st_sizes'] = self.get_sizes_list()
        if self._sizes_list:
            metadata_dict['st_size'] = self.get_sizes_list(together=True)
        if self.get_app_info():
            metadata_dict['app_info'] = self.get_app_info()
        if self._template:
            metadata_dict['template'] = self._template['pattern_string']
        if self._new_filename:
            metadata_dict['new_filename'] = self._new_filename[0]
            metadata_dict['new_file_part'] = self._new_filename[1]
            metadata_dict['new_file_ext'] = self._new_filename[2].replace('.', '')
        if self._new_template:
            metadata_dict['new_template'] = self._new_template
        if self._new_frame_padding:
            metadata_dict['new_padding'] = self._new_frame_padding

        return metadata_dict

    def get_app_info(self):
        return self._app_info

    def set_app_info(self, app_info_dict):
        if app_info_dict:
            self._app_info = app_info_dict
        else:
            self._app_info = None

    def get_type(self):
        return self._type

    def set_type(self, type_):
        if type_:
            self._type = type_['type']
        else:
            self._type = 'file'

    def get_sizes_list(self, together=False, files_list=None):
        if self._sizes_list:
            if together:
                return sum(self._sizes_list)
            else:
                return self._sizes_list

        sizes_list = []
        if not files_list:
            files_list = self.get_all_files_list()
        for fl in files_list:
            size = get_st_size(fl)
            if size:
                sizes_list.append(size)

        if sizes_list:
            if together:
                return sum(sizes_list)
            else:
                return sizes_list

    def set_sizes_list(self, _sizes_list):
        if _sizes_list:
            self._sizes_list = _sizes_list

    def get_file_type(self):
        return extract_extension(self.get_abs_file_name())

    def get_file_path(self):
        return extract_dirname(self.get_abs_file_name())

    def get_all_files_list(self, first=False, filenames=False, no_ext=False):

        if filenames:
            # Only for external calls
            file_names_list = []
            for fld in self.get_all_files_dicts():
                file_names_list.append(form_path(self.get_abs_file_name(fld, filename=True, no_ext=no_ext)))
            return sorted(file_names_list)

        if not self._files_list:
            for fld in self.get_all_files_dicts():
                self._files_list.append(form_path(self.get_abs_file_name(fld)))
            self._files_list = sorted(self._files_list)

        if first:
            return form_path(self._files_list[0])
        else:
            return sorted(self._files_list)

    def get_all_files_dicts(self, first=False):
        if first:
            return self._file[1][0]
        else:
            return self._file[1]

    def get_file_name(self, no_ext=False):
        if not self._file_name:
            self._file_name = self.get_abs_file_name(filename=True, no_ext=no_ext)
        return self._file_name

    def get_name_part(self, frame_padding=4, template='.$LAYER_$UDIM/UV.$FRAME'):
        pattern, separators = self.split_template(template)

        order_format = ''
        for file_dict in self.get_all_files_dicts():
            order_format = ''
            for item, sep in zip(reversed(pattern), reversed(separators)):
                if item == '$UDIM/UV':
                    if file_dict.get('udim'):
                        item = '[UUVV]'
                    elif file_dict.get('uv'):
                        item = 'u<>_v<>'
                if item == '$FRAME':
                    item = '[{}]'.format('#' * frame_padding)
                if item == '$LAYER':
                    item = file_dict['layer']

                order_format = sep + item + order_format

        return order_format

    def get_all_new_files_list(self, new_filename=None, new_filepath=None, new_frame_padding=None, no_ext=False, new_template='$FILENAME.$LAYER_$UDIM/UV.$FRAME.$EXT'):
        """
        This can only be used once, it creates metadata with new data, and returning list with new file names.

        :param new_filename:
        :param new_filepath:
        :param new_frame_padding:
        :param no_ext:
        :param new_template:
        :return:
        """
        if new_filename:
            self._new_filename = new_filename
        if new_filepath:
            self._new_filepath = new_filepath
        if new_frame_padding:
            self._new_frame_padding = new_frame_padding

        pattern, separators = self.split_template(new_template)

        order_format_list = []

        for file_dict in self.get_all_files_dicts():
            order_format = ''
            template = ''
            for item, sep in zip(reversed(pattern), reversed(separators)):
                temp = ''
                if item == '$FILENAME':
                    item = u'{0}/{1}'.format(self._new_filepath, self._new_filename[0])
                    temp = '$FILENAME'
                if item == '$UDIM/UV':
                    if file_dict.get('udim'):
                        item = file_dict['udim']
                        temp = '$UDIM'
                    elif file_dict.get('uv'):
                        item = file_dict['uv']
                        temp = '$UV'
                if item == '$FRAME':
                    item = file_dict['frame'].zfill(self._new_frame_padding)
                    temp = '$FRAME'
                if item == '$LAYER':
                    item = file_dict['layer']
                    temp = '$LAYER'
                if item == '$EXT' and not no_ext:
                    item = self._new_filename[2].replace('.', '')
                    temp = '$EXT'

                order_format = sep + item + order_format
                template = sep + temp + template

            order_format_list.append(order_format)

            self._new_template = template

        return order_format_list

    def split_template(self, template):
        match_template = MatchTemplate([template])

        template = match_template.split_patterns.values()[0][0]

        pattern = template[0]
        separators = template[1]
        if len(pattern) - len(separators) > 0:
            separators.insert(0, '')

        new_pattern = []
        new_separators = []
        for cp, cp_sep in zip(pattern, separators):
            for i, op in enumerate(self._template['pattern']):
                if op in ['$UDIM', '$UV']:
                    op = '$UDIM/UV'
                if cp == op:
                    new_pattern.append(cp)
                    new_separators.append(cp_sep)

        return new_pattern, new_separators

    def get_file_id(self):
        return self._file[0]

    def get_pretty_file_name(self):
        if self.get_type() not in ['layer_file', 'file', 'no_ext']:
            return extract_filename(self.get_abs_file_name(pretty=True))
        return extract_filename(self.get_abs_file_name())

    def get_file_ext(self):
        if not self._file_ext:
            self._file_ext = self.get_file_type()[0]
        return self._file_ext

    def get_layer(self):
        return self._layer

    def get_base_file_type_pretty_name(self):
        if not self._base_file_type_pretty_name:
            self._base_file_type_pretty_name = self.get_file_type()[1]
        return self._base_file_type_pretty_name

    def get_base_file_type(self):
        if not self._base_file_type:
            self._base_file_type = self.get_file_type()[2]
        return self._base_file_type

    def get_tactic_file_type(self):
        if not self._tactic_file_type:
            self._tactic_file_type = self.get_file_type()[3]
        return self._tactic_file_type

    def get_sequence_frameranges(self, padding=False):

        if self._sequence_frames:
            if self.get_type() in ['layer_uv_sequence', 'layer_udim_sequence', 'uv_sequence', 'udim_sequence']:

                self._sequence_length = collections.defaultdict(list)
                self._sequence_start = collections.defaultdict(list)
                self._sequence_end = collections.defaultdict(list)
                self._sequence_missing_frames = collections.defaultdict(list)
                sequence_ranges = collections.defaultdict(list)
                for uv, frames in self._sequence_frames:
                    frame_list = sorted(frames)
                    first_frame = min(frame_list)
                    last_frame = max(frame_list)
                    frames_buffer = []
                    missing_frames = []

                    for frame in range(first_frame, last_frame + 2):

                        frames_buffer.append(frame)
                        if frame not in frame_list:

                            if frames_buffer[0] == frame - 1:
                                if padding:
                                    sequence_ranges[uv].append(self.get_frame_with_padding(frames_buffer[0]))
                                else:
                                    sequence_ranges[uv].append(str(frames_buffer[0]))
                            elif frame - 1 in frame_list:
                                if padding:
                                    sequence_ranges[uv].append(
                                        '{0}-{1}'.format(self.get_frame_with_padding(frames_buffer[0]),
                                                         self.get_frame_with_padding(frame - 1)))
                                else:
                                    sequence_ranges[uv].append('{0}-{1}'.format(frames_buffer[0], frame - 1))
                            frames_buffer = []

                            if last_frame > frame:
                                missing_frames.append(frame)

                    self._sequence_length[uv].append(len(frame_list))
                    self._sequence_start[uv].append(first_frame)
                    self._sequence_end[uv].append(last_frame)
                    self._sequence_missing_frames[uv].append(missing_frames)

                return sequence_ranges.items()

            elif self.get_type() in ['sequence', 'layer_sequence']:

                frame_list = sorted(self._sequence_frames)
                first_frame = min(frame_list)
                last_frame = max(frame_list)
                frames_buffer = []
                sequence_ranges = []
                missing_frames = []

                for frame in range(first_frame, last_frame + 2):

                    frames_buffer.append(frame)
                    if frame not in frame_list:

                        if frames_buffer[0] == frame - 1:
                            if padding:
                                sequence_ranges.append(self.get_frame_with_padding(frames_buffer[0]))
                            else:
                                sequence_ranges.append(str(frames_buffer[0]))
                        elif frame - 1 in frame_list:
                            if padding:
                                sequence_ranges.append('{0}-{1}'.format(self.get_frame_with_padding(frames_buffer[0]),
                                                                        self.get_frame_with_padding(frame - 1)))
                            else:
                                sequence_ranges.append('{0}-{1}'.format(frames_buffer[0], frame - 1))
                        frames_buffer = []

                        if last_frame > frame:
                            missing_frames.append(self.get_frame_with_padding(frame))

                self._sequence_length = len(frame_list)
                self._sequence_start = first_frame
                self._sequence_end = last_frame
                self._sequence_missing_frames = missing_frames

                return sequence_ranges

    def get_sequence_frame_range(self):
        if self._sequence_frames:
            if self.get_type() in ['layer_uv_sequence', 'layer_udim_sequence', 'uv_sequence', 'udim_sequence']:
                sequence_ranges = []
                for start, end in zip(self.get_sequence_start().items(), self.get_sequence_end().items()):
                    sequence_ranges.append((start[0], '{0}-{1}'.format(start[1][0], end[1][-1])))
                return sequence_ranges
            elif self.get_type() in ['sequence', 'layer_sequence']:
                return '{0}-{1}'.format(self.get_sequence_start(), self.get_sequence_end())

    def get_frame_with_padding(self, frame):
        return '%0*d' % (self.get_sequence_padding(), int(frame))

    def get_sequence_frameranges_string(self, brackets=None):
        frames = self.get_sequence_frameranges()
        if frames:
            if self.get_type() in ['layer_uv_sequence', 'layer_udim_sequence', 'uv_sequence', 'udim_sequence']:
                framerange_strings = []
                for uv, frame in frames:
                    framerange_string = '{1} ({0})'.format(uv, ', '.join(frame))
                    if brackets:
                        framerange_string = '%s%s%s' % (brackets[0], framerange_string, brackets[1])
                    framerange_strings.append(framerange_string)

                return ', '.join(framerange_strings)

            elif self.get_type() in ['sequence', 'layer_sequence']:
                framerange_string = ', '.join(frames)
                if brackets:
                    return '%s%s%s' % (brackets[0], framerange_string, brackets[1])

                return framerange_string

    def init_files(self):
        if self._template:
            self.set_type(self._template)
        if self._sequence_frames:
            return self._sequence_frames
        else:
            all_files_dicts = self.get_all_files_dicts()
            if self.get_type() in ['layer_file', 'file', 'no_ext']:
                for fld in all_files_dicts:
                    self._layer = fld.get('layer')

            elif self.get_type() in ['layer_uv', 'layer_udim', 'uv', 'udim']:
                for fld in all_files_dicts:
                    udim = fld.get('udim')
                    if not udim:
                        udim = fld.get('uv')
                    self._tiles.append(udim)
                    self._layer = fld.get('layer')
                self._tiles_count = len(self._tiles)

            elif self.get_type() in ['sequence', 'layer_sequence']:
                for fld in all_files_dicts:
                    self._sequence_padding = len(fld['frame'])
                    self._sequence_frames.append(int(fld['frame']))
                    self._layer = fld.get('layer')

            elif self.get_type() in ['layer_uv_sequence', 'layer_udim_sequence', 'uv_sequence', 'udim_sequence']:
                frames_by_udims = collections.defaultdict(list)
                for fld in all_files_dicts:
                    self._sequence_padding = len(fld['frame'])
                    udim = fld.get('udim')
                    if not udim:
                        udim = fld.get('uv')
                    frames_by_udims[udim].append(int(fld['frame']))
                    self._layer = fld.get('layer')
                self._sequence_frames = frames_by_udims.items()
                self._tiles = frames_by_udims.keys()
                self._tiles_count = len(self._tiles)

            return self._sequence_frames

    def get_sequence_lenght(self):
        return self._sequence_length

    def get_sequence_padding(self):
        return self._sequence_padding

    def get_sequence_start(self):
        return self._sequence_start

    def get_sequence_end(self):
        return self._sequence_end

    def get_sequence_missing_frames(self):
        return self._sequence_missing_frames

    def get_tiles_count(self):
        return self._tiles_count

    def get_tiles(self):
        return self._tiles

    def is_exists(self, check_all_files=False):
        if check_all_files:
            exist = False
            for fl in self.get_all_files_list():
                exist = os.path.exists(fl)
            return exist
        else:
            return os.path.exists(self.get_all_files_list(True))

    def is_previewable(self):
        if self._previewable:
            return True

        ext = self.get_file_type()
        if ext[3] == 'preview':
            self._previewable = True

        return self._previewable

    def open_file(self):
        open_file_associated(form_path(self.get_all_files_list(True)))

    def open_folder(self):
        open_folder(form_path(self.get_all_files_list(first=True)), highlight=True)


class MatchTemplate(object):
    default_patterns = [
        '$FILENAME',
        '$FILENAME.$EXT'
    ]

    def __init__(self, patterns=None, padding=3, add_default_patterns=False):

        if patterns:
            self.patterns = set(patterns)
        else:
            self.patterns = None
        if add_default_patterns:
            if patterns:
                patterns.extend(self.default_patterns)
                self.patterns = set(patterns)
            else:
                self.patterns = set(self.default_patterns)
        self.padding = padding
        self.split_patterns = None

        if self.patterns:
            self.parse_patterns()

    def get_preview_string(self):

        return self.patterns.pop()\
            .replace('$FILENAME', 'Filename')\
            .replace('$EXT', 'tif')\
            .replace('$UDIM', '[UUVV]')\
            .replace('$UV', '[u<>_v<>]')\
            .replace('$FRAME', '[###]')\
            .replace('$LAYER', 'layer')

    def get_type_string(self):
        return self.split_patterns.keys()[0].replace('_', ' | ')

    def get_template(self, template):
        templates = {
            '$EXT': ['(?P<ext>[0-9A-z]+)', 'ext'],
            '$FILENAME': ['(?P<filename>.+)', 'filename'],
            '$UDIM': ['(?P<udim>(?P<u>[0-9]{2})(?P<v>[0-9]{2}))', 'udim'],
            '$UV': ['(?P<uv>u(?P<u>[0-9]{1,2})_v(?P<v>[0-9]{1,2}))', 'uv'],
            '$FRAME': ['(?P<frame>[0-9]{%s,})' % self.padding, 'frame'],  # must be at least 3 frames by default
            '$LAYER': ['(?P<layer>[A-z0-9]*[A-z]+[A-z0-9]*)', 'layer'],  # layer must not have digits only
        }

        return templates.get(template)

    @staticmethod
    def get_type(keys_list):
        if all(('$UV' in keys_list, '$FRAME' in keys_list, '$LAYER' in keys_list)):
            return 'layer_uv_sequence'
        if all(('$UDIM' in keys_list, '$FRAME' in keys_list, '$LAYER' in keys_list)):
            return 'layer_udim_sequence'
        if all(('$UV' in keys_list, '$FRAME' in keys_list)):
            return 'uv_sequence'
        if all(('$UDIM' in keys_list, '$FRAME' in keys_list)):
            return 'udim_sequence'
        if all(('$LAYER' in keys_list, '$FRAME' in keys_list)):
            return 'layer_sequence'
        if all(('$LAYER' in keys_list, '$UV' in keys_list)):
            return 'layer_uv'
        if all(('$LAYER' in keys_list, '$UDIM' in keys_list)):
            return 'layer_udim'
        if '$FRAME' in keys_list:
            return 'sequence'
        if '$UV' in keys_list:
            return 'uv'
        if '$UDIM' in keys_list:
            return 'udim'
        if '$LAYER' in keys_list:
            return 'layer_file'
        if '$EXT' in keys_list:
            return 'file'
        return 'no_ext'

    def parse_patterns(self, patterns=None):
        if patterns:
            self.patterns = patterns

        values_pattern = re.compile('[.|_]')
        split_patterns = collections.defaultdict(list)

        for ptn in self.patterns:
            key = re.split(values_pattern, ptn)
            split_patterns[self.get_type(key)].append((key, re.findall(values_pattern, ptn), ptn))

        self.split_patterns = split_patterns
        return self.split_patterns

    def get_re_patterns(self, patterns):
        re_temp = []
        re_seps = []
        order = []

        for i, key in enumerate(patterns[0]):
            if len(patterns[1]) > i and patterns[1][i]:
                re_seps.append('[{}]'.format(patterns[1][i]))
            else:
                re_seps.append('')
            template = self.get_template(key)
            if template:
                re_temp.append(template[0])
                order.append(template[1])
            else:
                re_temp.append(key)

        pattern = '^{0}$'.format(''.join(j + k for j, k in zip(re_temp, re_seps)))

        return pattern, order

    @staticmethod
    def get_unique_name(group_dict, order, separators):

        if len(order) - len(separators) > 0:
            separators.insert(0, '')

        order_format = ''
        for item, sep in zip(order, separators):
            if item == 'frame':
                item = '[$FRAME' + str(len(group_dict['frame'])) + '$]'
            if item == 'uv':
                item = '[$UV$]'
            if item == 'udim':
                item = '[$UDIM$]'
            if item == 'ext':
                item = group_dict['ext']
            if item == 'filename':
                item = group_dict['filename']
            if item == 'layer':
                item = group_dict['layer']

            order_format = order_format + sep + item

        return order_format

    def match_by_template(self, files_list, templates, template_names):
        match_dicts = []
        tpls_names = []

        for i, template in enumerate(templates):
            values_pattern = re.compile(template[0])
            def_dict = collections.defaultdict(list)
            not_matched = []
            for fl in files_list:
                # for windows os
                fl_norm = fl.replace('\\', '/')
                search_result = re.search(values_pattern, fl_norm)
                if search_result:
                    group_dict = search_result.groupdict()
                    unique_filename = self.get_unique_name(group_dict, template[1], template_names[i][1][1])
                    group_dict['orig_file'] = fl_norm
                    def_dict[unique_filename].append(group_dict)
                else:
                    not_matched.append(fl_norm)

            # if not found, match with next template
            files_list = not_matched
            if def_dict:
                match_dicts.append(def_dict)
                template_dict = {
                    'type': template_names[i][0],
                    're_string': template[0],
                    'order': template[1],
                    'pattern': template_names[i][1][0],
                    'pattern_separators': template_names[i][1][1],
                    'pattern_string': template_names[i][1][2],
                }
                tpls_names.append(template_dict)

        return zip(match_dicts, tpls_names)

    def get_files(self, files_list=None, default_types=False):
        templates = []
        template_names = []

        # this is needed, because we need to get uv sequences first, then others
        types = [
            'layer_uv_sequence',
            'layer_udim_sequence',
            'uv_sequence',
            'udim_sequence',
            'layer_sequence',
            'layer_uv',
            'layer_udim',
            'sequence',
            'uv',
            'udim',
            'layer_file',
            'file',
            'no_ext'
        ]

        def_types = [
            'file',
            'no_ext'
        ]

        if default_types:
            types = def_types

        for tp in types:
            if self.split_patterns.get(tp):
                for patterns in self.split_patterns.get(tp):
                    templates.append(self.get_re_patterns(patterns))
                    template_names.append((tp, patterns))

        return self.match_by_template(set(files_list), templates, template_names)

    def get_files_objects(self, files_list, allow_single_sequence=False, allow_single_udim=False, sort=True):
        if sort:
            found_files = self.get_files(natsort.realsorted(files_list))
        else:
            found_files = self.get_files(files_list)
        out_dict = collections.defaultdict(list)

        single_sequences_and_udims = []

        for files, tpl in found_files:
            for fl in files.items():
                if not allow_single_sequence or allow_single_udim:
                    if tpl['type'] in ['layer_uv_sequence', 'layer_udim_sequence', 'uv_sequence', 'udim_sequence', 'layer_sequence', 'sequence'] and len(fl[1]) == 1:
                        single_sequences_and_udims.append(fl[1][0]['orig_file'])
                    elif tpl['type'] in ['layer_uv', 'layer_udim', 'sequence', 'uv', 'udim'] and len(fl[1]) == 1:
                        single_sequences_and_udims.append(fl[1][0]['orig_file'])
                    else:
                        file_obj = FileObject(fl, tpl)
                        out_dict[tpl['type']].append(file_obj)

        # getting all single sequences or udims/uvs
        if single_sequences_and_udims:
            single_found_files = self.get_files(single_sequences_and_udims, default_types=True)
            for files, tpl in single_found_files:
                for fl in files.items():
                    file_obj = FileObject(fl, tpl)
                    out_dict[tpl['type']].append(file_obj)

        return out_dict

    def init_from_tactic_file_object(self, tactic_file_object):
        metadata = tactic_file_object.get_metadata()
        path = tactic_file_object.get_abs_path()
        template = self.parse_patterns([metadata.get('new_template')]).values()[0][0]
        pattern = template[0]
        separators = template[1]
        if len(pattern) - len(separators) > 0:
            separators.insert(0, '')

        files_list = []
        if metadata.get('type') in ['layer_uv_sequence', 'layer_udim_sequence', 'uv_sequence', 'udim_sequence']:
            udims_list = self.unpack_udims(metadata.get('frameranges'))
            for udim, frames in udims_list:
                for frame in frames:
                    name = self.unpack_name(
                        pattern,
                        separators,
                        metadata.get('new_filename'),
                        metadata.get('new_file_ext'),
                        udim,
                        '%0*d' % (metadata.get('new_padding'), int(frame)),
                        metadata.get('layer'),
                    )
                    files_list.append('%s/%s' % (path, name))
        elif metadata.get('type') in ['layer_uv', 'layer_udim', 'uv', 'udim']:
            udims_list = metadata.get('udims')
            for udim in udims_list:
                name = self.unpack_name(
                    pattern,
                    separators,
                    metadata.get('new_filename'),
                    metadata.get('new_file_ext'),
                    udim,
                    None,
                    metadata.get('layer'),
                )
                files_list.append('%s/%s' % (path, name))
        elif metadata.get('type') in ['sequence', 'layer_sequence']:
            frames_list = self.unpack_frames(metadata.get('frameranges'))
            for frame in frames_list:
                name = self.unpack_name(
                    pattern,
                    separators,
                    metadata.get('new_filename'),
                    metadata.get('new_file_ext'),
                    None,
                    '%0*d' % (metadata.get('new_padding'), int(frame)),
                    metadata.get('layer'),
                )
                files_list.append('%s/%s' % (path, name))
        elif metadata.get('type') in ['layer_file', 'file', 'no_ext']:
            name = self.unpack_name(
                pattern,
                separators,
                metadata.get('new_filename'),
                metadata.get('new_file_ext'),
                None,
                None,
                metadata.get('layer'),
            )
            files_list.append('%s/%s' % (path, name))

        self.__init__(
            [metadata.get('new_template')],
            padding=metadata.get('new_padding'),
            # add_default_patterns=True
        )
        files_objects_dict = self.get_files_objects(files_list)

        return files_objects_dict

    @staticmethod
    def unpack_name(pattern, separators, file_name=None, file_ext=None, udim=None, frame=None, layer=None):
        result_name = []

        for p, s in zip(pattern, separators):
            if p == '$FILENAME':
                result_name.append(s + file_name)
            if p in ['$UDIM', '$UV']:
                result_name.append(s + udim)
            if p == '$LAYER':
                result_name.append(s + layer)
            if p == '$FRAME':
                result_name.append(s + frame)
            if p == '$EXT':
                result_name.append(s + file_ext)

        return ''.join(result_name)

    def unpack_udims(self, udims):

        udims_list = []
        for udim, frames in udims:
            udims_list.append((udim, self.unpack_frames(frames)))

        return udims_list

    @staticmethod
    def unpack_frames(frameranges):
        # does not support negative values
        frames = []
        for frame in frameranges:
            split = frame.split('-')
            if len(split) > 1:
                frames.extend(range(int(split[0]), int(split[1])+1))
            else:
                frames.append(int(frame))
        return frames
