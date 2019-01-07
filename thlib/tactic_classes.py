# module Tactic Classes
# file tactic_classes.py
# Global TACTIC Functions Module

import os
import shutil
import urlparse
import collections
import json
from bs4 import BeautifulSoup
from thlib.side.Qt import QtWidgets as QtGui
from thlib.side.Qt import QtGui as Qt4Gui
from thlib.side.Qt import QtCore
import thlib.proxy as proxy
from thlib.environment import env_mode, env_server, env_inst, env_tactic, dl
import global_functions as gf
import tactic_query as tq
import side.client.tactic_client_lib as tactic_client_lib


if env_mode.get_mode() == 'maya':
    import maya_functions as mf
    reload(mf)

# class ServerThread(QtCore.QThread):
#     def __init__(self, parent=None):
#         super(ServerThread, self).__init__(parent=parent)
#
#         self.kwargs = None
#         self.result = None
#         self.connected = False
#         self.failed = False
#
#     def isConnected(self):
#         return self.connected
#
#     def setConnected(self, boolean):
#         self.connected = boolean
#
#     def isFailed(self):
#         return self.failed
#
#     def setFailed(self, boolean):
#         self.failed = boolean
#
#     def routine(self, **kwargs):
#         pass
#
#     def run(self):
#         try:
#             self.result = self.routine(**(self.kwargs or {}))
#             self.setFailed(False)
#         except Exception as expected:
#             self.setFailed(True)
#
#             traceback.print_exc(file=sys.stdout)
#             stacktrace = traceback.format_exc()
#
#             exception = {
#                 'exception': expected,
#                 'stacktrace': stacktrace,
#             }
#             self.result = exception
#
#
# def get_server_thread(kwargs_dict, runnable_func, connected_func, parent=None):
#     thread = ServerThread(parent)
#
#     if not thread.isRunning():
#         thread.kwargs = kwargs_dict
#         thread.routine = runnable_func
#
#         if not thread.isConnected():
#             thread.finished.connect(connected_func)
#             thread.setConnected(True)
#             # thread.start()
#
#     return thread
#
#
# def treat_result(thread, silent=False):
#     if silent:
#         return thread
#     if thread.isFailed():
#         print 'ERROR TREATING'
#         return error_handle(thread)
#     else:
#         return thread


def server_auth(host, project=None, login=None, password=None, site=None, get_ticket=False):
    server = tactic_client_lib.TacticServerStub.get(protocol='xmlrpc', setup=False)
    server.set_transport(proxy.UrllibTransport())
    if env_server.get_proxy()['enabled']:
        server.transport.enable_proxy()
    else:
        server.transport.disable_proxy()

    server.set_server(host)
    server.set_project(project)
    server.set_site(site)

    ticket = env_server.get_ticket()
    if not ticket or get_ticket:
        ticket = server.get_ticket(login, password, site)
        if type(ticket) == dict:
            if ticket.get('exception'):
                return server
        else:
            env_server.set_ticket(ticket)

    server.set_ticket(ticket)

    return server


def server_start(get_ticket=False, project=None):
    if not project:
        project = 'sthpw'
    server = server_auth(
        env_server.get_server(),
        project,
        env_server.get_user(),
        '',
        env_server.get_site()['site_name'],
        get_ticket=get_ticket,
    )
    return server


def generate_new_ticket(explicit_username=None, parent=None):
    login_pass_dlg = QtGui.QMessageBox(
        QtGui.QMessageBox.Question,
        'Updating ticket',
        'Enter Your Login and Password.',
        QtGui.QMessageBox.NoButton,
        parent,
    )

    login_pass_dlg.addButton("Ok", QtGui.QMessageBox.YesRole)
    login_pass_dlg.addButton("Cancel", QtGui.QMessageBox.NoRole)

    layout = QtGui.QGridLayout()

    widget = QtGui.QWidget()
    widget.setLayout(layout)

    msb_layot = login_pass_dlg.layout()

    # workaround for pyside2
    wdg_list = []

    for i in range(msb_layot.count()):
        wdg = msb_layot.itemAt(i).widget()
        if wdg:
            wdg_list.append(wdg)

    msb_layot.addWidget(wdg_list[0], 0, 0)
    msb_layot.addWidget(wdg_list[1], 0, 1)
    msb_layot.addWidget(wdg_list[2], 2, 1)
    msb_layot.addWidget(widget, 1, 1)

    # Labels
    login_label = QtGui.QLabel('Login: ')
    pass_label = QtGui.QLabel('Password: ')

    # Line Edits
    login_line_edit = QtGui.QLineEdit()
    if explicit_username:
        login_line_edit.setText(explicit_username)
    else:
        login_line_edit.setText(env_server.get_user())
    pass_line_edit = QtGui.QLineEdit()
    pass_line_edit.setEchoMode(QtGui.QLineEdit.Password)

    layout.addWidget(login_label, 0, 0)
    layout.addWidget(login_line_edit, 0, 1)
    layout.addWidget(pass_label, 1, 0)
    layout.addWidget(pass_line_edit, 1, 1)

    pass_line_edit.setFocus()

    login_pass_dlg.exec_()

    host = env_server.get_server()
    project = 'sthpw'
    login = login_line_edit.text()
    password = pass_line_edit.text()
    site = env_server.get_site()['site_name']

    kwargs = dict(
        host=host,
        project=project,
        login=login,
        password=password,
        site=site,
        get_ticket=True
    )

    reply = login_pass_dlg.buttonRole(login_pass_dlg.clickedButton())

    if reply == QtGui.QMessageBox.YesRole:
        return kwargs


def server_ping():
    if server_start():
        if server_start().fast_ping() == 'OK':
            return True
        else:
            return False
    else:
        return False


def server_fast_ping_predefined(server_url, proxy_dict=None):
    server = tactic_client_lib.TacticServerStub.get(protocol='xmlrpc', setup=False)

    transport = proxy.UrllibTransport()
    server.set_transport(transport)

    if proxy_dict.get('enabled'):
        server.transport.update_proxy(proxy_dict)
        server.transport.enable_proxy()
    else:
        server.transport.update_proxy(proxy_dict)
        server.transport.disable_proxy()
        # server.set_transport(None)

    server.set_server(server_url)

    if server.fast_ping() == 'OK':
        del server
        return 'ping_ok'
    else:
        del server
        return 'ping_fail'


def server_fast_ping():
    server = tactic_client_lib.TacticServerStub.get(protocol='xmlrpc', setup=False)
    if env_server.get_proxy()['enabled']:
        transport = proxy.UrllibTransport()
        server.set_transport(transport)
    else:
        if server.transport:
            server.transport.update_proxy()
        server.set_transport(None)
    server.set_server(env_server.get_server())

    if server.fast_ping() == 'OK':
        del server
        return 'ping_ok'
    else:
        del server
        return 'ping_fail'


def split_search_key(search_key):
    search_type, asset_code = server_start().split_search_key(search_key)
    if len(search_type.split('?project=')) > 1:
        pipeline_code, project_code = search_type.split('?project=')
    else:
        search_type, project_code = server_start().split_search_key(search_key)
        asset_code = None
        pipeline_code = None

    return {
        'search_type': search_type,
        'asset_code': asset_code,
        'pipeline_code': pipeline_code,
        'project_code': project_code
    }


# Projects related classes
class Project(object):
    def __init__(self, project):

        self.info = project
        self.stypes = None
        self.workflow = None

    def get_info(self):
        return self.info

    def get_workflow(self):
        return self.workflow

    def get_code(self):
        return self.info.get('code')

    def get_type(self):
        return self.info.get('type')

    def is_template(self):
        return self.info.get('is_template')

    def get_stypes(self):
        if not self.stypes:
            self.query_stypes()

        return self.stypes

    def query_stypes(self):
        self.stypes = self.query_search_types()

        return self.stypes

    def query_search_types(self):
        kwargs = {
            'project_code': self.info.get('code'),
            'namespace': self.info.get('type')
        }

        code = tq.prepare_serverside_script(tq.query_search_types_extended, kwargs, return_dict=True)

        # import time
        # start = time.time()
        # for i in range(10):
        result = server_start(project=kwargs['project_code']).execute_python_script('', kwargs=code)

        # print time.time() - start

        stypes = json.loads(result['info']['spt_ret_val'])

        schema = stypes.get('schema')
        # TODO site-wide pipelines
        pipelines = stypes.get('pipelines')
        stypes = stypes.get('stypes')

        # from pprint import pprint

        # print(schema)
        # print(pipelines)
        # print(stypes)

        if schema:
            prj_schema = schema[0]['schema']
        else:
            prj_schema = None

        if not pipelines or not prj_schema:
            return []
        else:
            return self.get_all_search_types(stypes, pipelines, prj_schema)

    def get_all_search_types(self, stype_list, process_list, schema):

        pipeline = BeautifulSoup(schema, 'html.parser')
        all_connectionslist = []
        # dct = collections.defaultdict(list)
        dct = collections.OrderedDict()

        for pipe in pipeline.find_all(name='connect'):
            all_connectionslist.append(pipe.attrs)

        for pipe in pipeline.find_all(name='search_type'):
            dct.setdefault(pipe.attrs['name'], []).append({'search_type': pipe.attrs})
            # dct[pipe.attrs['name']].append({'search_type': pipe.attrs})

            conn = {
                'children': [],
                'parents': [],
            }
            for connect in all_connectionslist:
                if pipe.attrs['name'] == connect['from']:
                    conn['parents'].append(connect)
                if pipe.attrs['name'] == connect['to']:
                    conn['children'].append(connect)

            # dct[pipe.attrs['name']].append(conn)
            dct.setdefault(pipe.attrs['name'], []).append(conn)

        # getting workflow here
        self.workflow = Workflow(process_list)

        # getting stypes processes here
        stypes_objects = collections.OrderedDict()
        for stype in stype_list:
            stype_process = collections.OrderedDict()
            stype_schema = dct.get(stype['code'])

            for process in process_list:
                if dct.get(stype['code']):
                    if process['search_type'] == dct.get(stype['code'])[0]['search_type']['name']:
                        stype_process[process['code']] = process

            stype_obj = SType(stype, stype_schema, stype_process, project=self)
            stypes_objects[stype['code']] = stype_obj

        return stypes_objects


# sTypes related classes
class SType(object):
    """

    .schema.info
    .schema.parents
    .schema.children

    .pipeline.info
    .pipeline.process
    .pipeline.process['Blocking'].get('parents')
    .pipeline.process['Blocking'].get('children')

    """
    def __init__(self, stype, schema=None, pipelines=None, project=None):

        self.info = stype
        self.project = project
        self.schema = None
        self.pipeline = self.__init_pipelines(pipelines)

        if schema:
            self.schema = Schema(schema)

    @staticmethod
    def __init_pipelines(pipelines):

        ready_pipeline = collections.OrderedDict()
        if pipelines:
            for key, pipeline in pipelines.iteritems():
                ready_pipeline[key] = Pipeline(pipeline)

        if ready_pipeline:
            return ready_pipeline

    def get_pretty_name(self):
        title = self.info.get('title')
        if title:
            return title.title()
        else:
            title = self.info.get('code').split('/')[-1]
            if title:
                return title.replace('_', ' ').title()
            else:
                return self.info['table_name'].title()

    def get_stype_color(self, fmt='rgb', alpha=None, tuple=False):
        color = self.info['color']
        if color:
            if fmt == 'rgb':
                return gf.hex_to_rgb(color, alpha=alpha, tuple=tuple)
            else:
                return color

    def get_code(self):
        return self.info['code']

    def get_project(self):
        return self.project

    def get_info(self):
        return self.info

    def get_schema(self):
        return self.schema

    def get_pipeline(self):
        return self.pipeline

    def get_workflow(self):
        return self.project.get_workflow()

    def get_columns_info(self):
        return self.info['column_info']

    def get_definition(self, definition='table', processed=True):
        if processed:

            definition_bs = BeautifulSoup(self.info['definition'].get(definition), 'html.parser')

            all_elements = []
            for element in definition_bs.find_all(name='element'):
                all_elements.append(element.attrs)

            return all_elements

        else:
            return self.info['definition'].get(definition)


class Schema(object):
    def __init__(self, schema_dict):

        self.__schema_dict = schema_dict
        self.info = self.get_info()

        self.parents = self.get_parents()
        self.children = self.get_children()

    def get_info(self):
        return self.__schema_dict[0]['search_type']

    def get_parents(self):
        return self.__schema_dict[1].get('parents')

    def get_children(self):
        return self.__schema_dict[1].get('children')


class Workflow(object):
    def __init__(self, pipeline):

        self.__pipeline_list = pipeline

    def get_child_pipeline_by_process_code(self, parent_pipeline, process):
        parent_process = None
        if parent_pipeline.processes:
            for proc in parent_pipeline.processes:
                if proc['process'] == process:
                    parent_process = proc
        if parent_process:
            # TODO SOMETHING WRONG WITH THIS, may be it query too much pipelines
            return self.get_pipeline_by_parent(parent_process)

    def get_pipeline_by_parent(self, parent_process):
        for pipe in self.__pipeline_list:
            if pipe['parent_process'] == parent_process['code']:
                return Pipeline(pipe)

    def get_by_stype(self):
        pass

    def get_pipeline(self):

        from pprint import pprint

        for pipe in self.__pipeline_list:
            pprint(pipe)

        return self.__pipeline_list


class Pipeline(object):
    def __init__(self, process):

        self.__process_dict = process

        self.process = collections.OrderedDict()

        self.get_pipeline()
        self.processes = self.get_processes()
        self.info = self.get_info()

    def get_processes(self):
        return self.__process_dict['stypes_processes']

    def get_info(self):
        return self.__process_dict

    def get_process(self, process):
        # what if we have duplicated processes?
        for proc in self.processes:
            if proc['process'] == process:
                return proc

    def get_all_processes_names(self):
        process_names_list = []

        for process in self.process:
            process_names_list.append(process)

        return process_names_list

    def get_pipeline(self):

        all_connectionslist = []
        pipeline = BeautifulSoup(self.__process_dict['pipeline'], 'html.parser')

        for pipe in pipeline.find_all(name='connect'):
            all_connectionslist.append(pipe.attrs)

        for pipe in pipeline.find_all(name='process'):
            self.process[pipe.attrs.get('name')] = pipe.attrs

            for connect in all_connectionslist:
                if pipe.attrs['name'] == connect['from']:
                    self.process[pipe.attrs.get('name')]['parents'] = connect
                if pipe.attrs['name'] == connect['to']:
                    self.process[pipe.attrs.get('name')]['children'] = connect


# SObject class
class SObject(object):
    """
    Main class for all types of sobjects
    creates structured tree of objects
    to see all output:

    sobjects = get_sobjects(sobjects_list, snapshots_list)

    # test particular output example, outputs versioned and versionless snapshots
    for c, v in sobjects['PROPS00001'].process['Modeling'].contexts.iteritems():
        pprint(c)
        pprint(v.versionless)
        pprint(v.versions)

    # Test full output example, outputs all versioned and versionless snapshots
    for read in sobjects.iterkeys():
        print('____________________________________________:'+read+'____________________________________________')
        for key, value in sobjects[read].process.iteritems():
            for key2, val2 in value.contexts.iteritems():
                print('Process: {0},\n\nContext: {1}, \n\nSnapshot versionless: {2},\n\nSnapshot versions: {
                3}'.format(key, key2, value.contexts[key2].versionless, value.contexts[key2].versions))

    # Usage variants:
    # .get_snapshots()
    # .process['sculpt'].snapshots['maya']()  # gets all versionless snapshots per context typed 'maya'
    # .process['sculpt'].snapshots['context'].versions() # gets all dependent to context versions

    # .get_tasks()
    # .tasks['sculpt'].contexts['sculpt'].task['context'].get_notes() # gets notes per task context
    # .tasks['sculpt'].contexts['sculpt'].task['context'].notes # return all notes per task context

    # .get_notes()
    # .notes['sculpt'].notes()
    """

    def __init__(self, in_sobj=None, in_process=None, project=None):
        """
        :param in_sobj: input list with info on particular sobject
        :param in_process: list of current sobject possible process, need to query tasks per process
        :return:
        """

        # INPUT VARS
        self.info = in_sobj
        self.all_process = in_process
        self.project = project

        # OUTPUT VARS
        self.process = {}
        self.tasks = {}
        self.notes = {}
        self.snapshots = {}

        # Info Vars
        self.tasks_count = {'__total__': 0}
        self.notes_count = {'publish': 0}

    # Snapshots by search code
    def query_snapshots(self, s_code=None, s_id=None, process=None, order_bys=None, user=None):
        """
        Query for Snapshots
        :param s_code: Code of asset related to snapshot
        :param process: Process code
        :param order_bys: Order By
        :param user: Optional users names
        :return:
        """

        if process:
            if s_code:
                filters = [('search_code', s_code), ('process', process), ('project_code', self.project.info['code'])]
            elif s_id:
                filters = [('search_id', s_id), ('process', process), ('project_code', self.project.info['code'])]
        else:
            if s_code:
                filters = [('search_code', s_code), ('project_code', self.project.info['code'])]
            elif s_id:
                filters = [('search_id', s_id), ('project_code', self.project.info['code'])]

        return server_start(project=self.project.info['code']).query_snapshots(filters=filters, order_bys=order_bys, include_files=True)

    # Tasks by search code
    def query_tasks(self, s_code, process=None, user=None):
        """
        Query for Task
        :param s_code: Code of asset related to task
        :param process: Process code
        :param user: Optional users names
        :return:
        """
        server = server_start(project=self.project.info['code'])

        search_type = 'sthpw/task'
        if process:
            filters = [('search_code', s_code), ('process', process), ('project_code', self.project.info['code'])]
        else:
            filters = [('search_code', s_code), ('project_code', self.project.info['code'])]

        return server.query(search_type, filters)

    # Notes by search code
    def query_notes(self, s_code, process=None):
        """
        Query for Notes
        :param s_code: Code of asset related to note
        :param process: Process code
        :return:
        """
        server = server_start(project=self.project.info['code'])

        search_type = 'sthpw/note'
        if process:
            filters = [('search_code', s_code), ('process', process), ('project_code', self.project.info['code'])]
        else:
            filters = [('search_code', s_code), ('project_code', self.project.info['code'])]

        return server.query(search_type, filters)

    # Query snapshots to update current
    def update_snapshots(self, order_bys=None):
        # import time
        # start = time.time()
        if self.info.get('code'):
            snapshot_dict = self.query_snapshots(s_code=self.info['code'], order_bys=order_bys)
        else:
            snapshot_dict = self.query_snapshots(s_id=self.info['id'], order_bys=order_bys)
        self.init_snapshots(snapshot_dict)

        # end = time.time()
        # dl.info('Updating Snapshots time: {0}'.format(1215), group_id='server_query')

    # Initial Snapshots by process without query
    def init_snapshots(self, snapshot_dict):
        process_set = set(snapshot['process'] for snapshot in snapshot_dict)

        for process in process_set:
            self.process[process] = Process(snapshot_dict, process)

    # Snapshots by SObject
    def get_snapshots(self, order_bys=None):
        snapshots_list = self.query_snapshots(self.info['code'], order_bys=order_bys)
        process_set = set(snapshot['process'] for snapshot in snapshots_list)

        for process in process_set:
            self.snapshots[process] = Process(snapshots_list, process)

    # Tasks by SObject
    def get_tasks(self):
        tasks_list = self.query_tasks(self.info['code'])
        process_set = set(task['process'] for task in tasks_list)

        for process in process_set:
            self.tasks[process] = Process(tasks_list, process, True)

    def set_tasks_count(self, process, count):
        self.tasks_count[process] = count

    def get_tasks_count(self, process=None):
        if process:
            return self.tasks_count.get(process)
        else:
            return self.tasks_count

    # Notes by SObject
    def get_notes(self):
        notes_list = self.query_notes(self.info['code'])
        process_set = set(note['process'] for note in notes_list)

        for process in process_set:
            self.notes[process] = Process(notes_list, process, True)

    def set_notes_count(self, process, count):
        self.notes_count[process] = count

    def get_notes_count(self, process=None):
        if process:
            return self.notes_count.get(process)
        else:
            return self.notes_count

    def get_search_key(self):
        return self.info.get('__search_key__')

    def delete_sobject(self, include_dependencies=False, list_dependencies=None):

        snapshot_del_confirm = sobject_delete_confirm(self.get_search_key())
        if snapshot_del_confirm:
            include_dependencies = True
            list_dependencies = {
                'related_types': ['sthpw/file']
            }

            kwargs = {
                'search_key': self.get_search_key(),
                'include_dependencies': include_dependencies,
            }
            code = tq.prepare_serverside_script(tq.delete_sobject, kwargs, return_dict=True)
            result = server_start().execute_python_script('', kwargs=code)

            return result['info']['spt_ret_val']

    def get_pipeline_code(self):
        return self.info.get('pipeline_code')

    def get_title(self):
        title = self.info.get('name')
        if not title:
            title = self.info.get('title')
        if not title:
            title = self.info.get('code')

        return title

    def get_info(self):
        return self.info

    def get_project(self):
        return self.project

    def get_process(self, process):
        return self.process.get(process)

    def get_all_processes(self):
        # returning dict with all processes if it's have snapshots
        return self.process


class Process(object):
    def __init__(self, in_dict, process, single=False):
        # Contexts
        self.contexts = {}
        contexts = set()
        if single:
            items = collections.defaultdict(list)
            for item in in_dict:
                items[item['context']].append(item)
                if item['process'] == process:
                    contexts.add(item['context'])
            for context in contexts:
                self.contexts[context] = Contexts(single=items[context])
        else:
            versions = collections.defaultdict(list)
            versionless = collections.defaultdict(list)

            for snapshot in in_dict:
                if snapshot['process'] == process and (snapshot['version'] == -1 or snapshot['version'] == 0):
                    versionless[snapshot['context']].append(snapshot)
                elif snapshot['process'] == process and (snapshot['version'] != -1 or snapshot['version'] != 0):
                    versions[snapshot['context']].append(snapshot)
                if snapshot['process'] == process:
                    contexts.add(snapshot['context'])

            for context in contexts:
                self.contexts[context] = Contexts(versionless[context], versions[context])

    def get_contexts(self):
        return self.contexts


class Contexts(object):
    def __init__(self, versionless=None, versions=None, single=None):

        self.versions = None
        self.versionless = None

        if single:
            self.items = collections.OrderedDict()
            for item in single:
                self.items[item['code']] = SObject(item)
        else:
            self.versions = collections.OrderedDict()
            self.versionless = collections.OrderedDict()
            for sn in versions:
                self.versions[sn['code']] = Snapshot(sn)
            for sn in versionless:
                self.versionless[sn['code']] = Snapshot(sn)

    def get_versions(self):
        return self.versions

    def get_versionless(self):
        return self.versionless


class Snapshot(SObject, object):
    def __init__(self, snapshot):
        super(self.__class__, self).__init__(snapshot)

        self.__files = snapshot['__files__']
        self.files = collections.OrderedDict()

        self.files_objects = None
        self.preview_files_objects = None

        for fl in self.__files:
            self.files.setdefault(fl['type'], []).append(fl)

        self.snapshot = snapshot
        # delete unused big entries
        del self.snapshot['__files__'], self.snapshot['snapshot']

    def get_files(self):
        return self.files

    def get_code(self):
        return self.snapshot.get('code')

    def get_search_key(self):
        return self.snapshot['__search_key__']

    def get_files_objects(self, group_by=None):
        if not group_by:
            # if self.files_objects:
            #     return self.files_objects

            files_objects = []
            for fl in self.__files:
                files_objects.append(File(fl, self))
        else:
            files_objects = collections.OrderedDict()
            for fl in self.__files:
                files_objects.setdefault(fl[group_by], []).append(File(fl, self))

        self.files_objects = files_objects

        return self.files_objects

    def get_previewable_files_objects(self):
        if self.preview_files_objects:
            return self.preview_files_objects

        files_objects = self.get_files_objects()
        preview_objects = []
        for fo in files_objects:
            if fo.get_type() not in ['icon', 'web']:
                if fo.is_previewable():
                    preview_objects.append(fo)

        self.preview_files_objects = preview_objects
        return preview_objects

    def get_snapshot(self):
        return self.snapshot

    def get_version(self):
        return self.snapshot.get('version')

    def is_latest(self):
        return self.snapshot.get('is_latest')

    def is_versionless(self):
        if self.get_version() == -1:
            return True
        else:
            return False


class File(object):
    def __init__(self, file_dict, snapshot=None):

        self.__file = file_dict
        self.__snapshot = snapshot
        self.previewable = False
        self.meta_file_object = False
        self.get_meta_file_object()

    def get_dict(self):
        return self.__file

    def get_search_key(self):
        return self.__file['__search_key__']

    def get_file_size(self, check_real_size=False):
        return self.__file['st_size']

    def get_snapshot(self):
        return self.__snapshot

    def get_metadata(self):
        return self.__file.get('metadata')

    def get_meta_file_object(self):
        file_object = None
        metadata = self.get_metadata()
        if metadata:
            if metadata.get('template'):
                match_template = gf.MatchTemplate()
                file_object = match_template.init_from_tactic_file_object(self)

        if file_object:
            self.meta_file_object = True
            return file_object.values()[0][0]

    def is_meta_file_obj(self):
        return self.meta_file_object

    def get_type(self):
        return self.__file['type']

    def get_base_type(self):
        return self.__file['base_type']

    def get_ext(self):
        ext = gf.extract_extension(self.__file['file_name'])
        return ext[0]

    def get_filename_with_ext(self):
        return self.__file['file_name']

    def get_filename(self):
        filename = self.__file['file_name']
        ext = gf.extract_extension(filename)
        if ext:
            return filename.replace('.' + ext[0], '')
        else:
            return filename

    def get_filename_no_type_prefix(self):
        # guess right only if type at the end
        filename = self.get_filename()
        prefix = self.__file['type']
        if prefix:
            if filename.endswith(prefix):
                no_prefix_name = filename.split('_')
                return '_'.join(no_prefix_name[:-1])
            else:
                return filename
        else:
            return filename

    def get_abs_path(self):
        snapshot = self.__snapshot.get_snapshot()
        repo_name = snapshot.get('repo')
        if not repo_name:
            repo_name = 'base'

        if repo_name:
            asset_dir = env_tactic.get_base_dir(repo_name)['value'][0]
        else:
            asset_dir = env_tactic.get_base_dir('client')['value'][0]

        abs_path = gf.form_path(
            '{0}/{1}'.format(asset_dir, self.__file['relative_dir']))
        return abs_path

    def get_full_abs_path(self):
        return gf.form_path('{0}/{1}'.format(self.get_abs_path(), self.__file['file_name']))

    def is_exists(self):
        return os.path.exists(self.get_full_abs_path())

    def is_previewable(self):
        if self.previewable:
            return True

        previewable = False
        ext = gf.extract_extension(self.__file['file_name'])
        if self.__file['type'] in ['icon', 'web', 'image', 'playblast']:
            return True
        elif ext[3] == 'preview':
            previewable = True

        self.previewable = previewable

        return previewable

    def get_web_preview(self):
        # return web file object related to this file
        if self.__file['type'] != 'web':
            files = self.__snapshot.get_files_objects()
            filename = self.get_filename_no_type_prefix()
            for fl in files:
                if fl.get_type() == 'web':
                    if filename in fl.get_filename():
                        return fl
        else:
            return self

    def get_icon_preview(self):
        # return icon file object related to this file
        if self.__file['type'] != 'icon':
            files = self.__snapshot.get_files_objects()
            filename = self.get_filename_no_type_prefix()
            for fl in files:
                if fl.get_type() == 'icon':
                    if filename in fl.get_filename():
                        return fl
        else:
            return self

    def open_file(self):
        gf.open_file_associated(self.get_full_abs_path())

    def open_folder(self):
        gf.open_folder(self.get_full_abs_path())

# End of SObject Class


def query_all_projects():
    server = server_start()
    search_type = 'sthpw/project'
    filters = []
    projects = server.query(search_type, filters)

    return projects


def get_all_projects():

    projects_list = query_all_projects()

    result = collections.OrderedDict()

    exclude_list = ['sthpw', 'unittest', 'admin']
    if len(projects_list) == 2:
        exclude_list = []

    for project in projects_list:
        if project.get('code') not in exclude_list:
            result[project.get('code')] = Project(project)

    env_inst.projects = result

    return result


def get_sobjects_new(search_type, filters=[], order_bys=[], limit=None, offset=None, process_list=[]):
    """
    Filters snapshot by search codes, and sobjects codes
    :param sobjects_list: full list of stypes
    :param get_snapshots: query for snapshots per sobject or not
    :param project_code: assign project class to particular sObject
    :return: dict of sObjects objects
    """
    kwargs = {
        'search_type': search_type,
        'filters': filters,
        'order_bys': order_bys,
        'limit': limit,
        'offset': offset,
    }

    code = tq.prepare_serverside_script(tq.query_sobjects, kwargs, return_dict=True)
    project_code = split_search_key(search_type)['project_code']
    result = server_start(project=project_code).execute_python_script('', kwargs=code)

    if result['info']['spt_ret_val']:
        if result['info']['spt_ret_val'].startswith('Traceback'):
            sobjects_list = {'sobjects_list': []}
            info = None
        else:
            sobjects_list = json.loads(result['info']['spt_ret_val'])
            info = {
                'total_sobjects_count': sobjects_list['total_sobjects_count'],
                'total_sobjects_query_count': sobjects_list['total_sobjects_query_count'],
                'limit': sobjects_list['limit'],
                'offset': sobjects_list['offset'],
            }

        sobjects = collections.OrderedDict()

        # process_codes = []
        process_codes = list(process_list)
        for builtin in ['icon', 'attachment', 'publish']:
            if builtin not in process_codes:
                process_codes.append(builtin)

        # Create list of Sobjects
        for sobject in sobjects_list['sobjects_list']:
            sobjects[sobject['__search_key__']] = SObject(sobject, process_codes, env_inst.projects[project_code])
            sobjects[sobject['__search_key__']].init_snapshots(sobject['__snapshots__'])
            sobjects[sobject['__search_key__']].set_notes_count('publish', sobject['__notes_count__'])
            sobjects[sobject['__search_key__']].set_tasks_count('__total__', sobject['__tasks_count__'])

        return sobjects, info


# DEPRECATED, IT IS NOT RESPECT SORTING
# def get_sobjects(process_list=None, sobjects_list=None, get_snapshots=True, project_code=None):
#     """
#     Filters snapshot by search codes, and sobjects codes
#     :param sobjects_list: full list of stypes
#     :param get_snapshots: query for snapshots per sobject or not
#     :param project_code: assign project class to particular sObject
#     :return: dict of sObjects objects
#     """
#     sobjects = collections.OrderedDict()
#     if get_snapshots:
#         process_codes = list(process_list)
#         for builtin in ['icon', 'attachment', 'publish']:
#             if builtin not in process_codes:
#                 process_codes.append(builtin)
#
#         s_code = [s['code'] for s in sobjects_list]
#
#         snapshots_list = query_snapshots(process_codes, s_code, project_code)
#
#         snapshots = collections.OrderedDict()
#
#         # filter snapshots by search_code
#         for snapshot in snapshots_list:
#             snapshots.setdefault(snapshot['search_code'], []).append(snapshot)
#
#         # append sObject info to the end of each search_code filtered list
#         for sobject in sobjects_list:
#             snapshots.setdefault(sobject['code'], []).append(sobject)
#
#         # creating dict of ready SObjects
#         for k, v in snapshots.items():
#             sobjects[k] = SObject(v[-1], process_codes, env_inst.projects[project_code])
#             sobjects[k].init_snapshots(v[:-1])
#     else:
#         # Create list of Sobjects
#         for sobject in sobjects_list:
#             sobjects[sobject['code']] = SObject(sobject)
#
#     return sobjects


# def query_snapshots(process_list=None, s_code=None, project_code=None):
#     """
#     Query for snapshots belongs to asset
#     :return: list of snapshots
#     """
#
#     filters_snapshots = [
#         ('process', process_list),
#         ('project_code', project_code),
#         ('search_code', s_code),
#     ]
#
#     return server_start().query_snapshots(filters=filters_snapshots, include_files=True)


def server_query(filters, stype, columns=None, project=None, limit=0, offset=0, order_bys='timestamp desc'):
    """
    Query for searching assets
    """
    if not columns:
        columns = []

    server = server_start(project=project)

    # filters = []
    # expr = ''
    # if query[1] == 0:
    #     filters = [('name', 'EQI', query[0])]
    # if query[1] == 1:
    #     filters = [('code', query[0])]
    # if query[1] == 2:
    #     filters = None
    #     parents_codes = ['scenes_code', 'sets_code']
    #     for parent in parents_codes:
    #         expr += '@SOBJECT(cgshort/shot["{0}", "{1}"]), '.format(parent, query[0])
    # if query[1] == 3:
    #     filters = [('description', 'EQI', query[0])]
    # if query[1] == 4:
    #     filters = [('keywords', 'EQI', query[0])]
    #
    # if query[0] == '*':
    #     filters = []

    built_process = server.build_search_type(stype, project)
    # print s_code
    # import time
    # start = time.time()
    # result =

    # end = time.time()
    # dl.info('Query Assets Names time: {0}'.format(5415), group_id='server_query/{0}')
    # print 'query time: ' + str(end - start)
    # print assets_list

    return server.query(built_process, filters, columns, order_bys, limit=limit, offset=offset)


# def assets_query_new(query, stype, columns=None, project=None, limit=0, offset=0, order_bys='timestamp desc'):
#     """
#     Query for searching assets
#     """
#     if not columns:
#         columns = []
#     # TODO This is old and will be deprecated
#     server = server_start()
#     filters = []
#     expr = ''
#     if query[1] == 0:
#         filters = [('name', 'EQI', query[0])]
#     if query[1] == 1:
#         filters = [('code', query[0])]
#     if query[1] == 2:
#         filters = None
#         parents_codes = ['scenes_code', 'sets_code']
#         for parent in parents_codes:
#             expr += '@SOBJECT(cgshort/shot["{0}", "{1}"]), '.format(parent, query[0])
#     if query[1] == 3:
#         filters = [('description', 'EQI', query[0])]
#     if query[1] == 4:
#         filters = [('keywords', 'EQI', query[0])]
#
#     if query[0] == '*':
#         filters = []
#
#     built_process = server.build_search_type(stype, project)
#     # print s_code
#     # import time
#     # start = time.time()
#     assets_list = server.query(built_process, filters, columns, order_bys, limit=limit, offset=offset)
#
#     # end = time.time()
#     # dl.info('Query Assets Names time: {0}'.format(5415), group_id='server_query/{0}')
#     # print 'query time: ' + str(end - start)
#     # print assets_list
#     return assets_list


def get_notes_count(sobject, process, children_stypes):
    kwargs = {
        'process': process,
        'search_key': sobject.get_search_key(),
        'stypes_list': children_stypes
    }
    code = tq.prepare_serverside_script(tq.get_notes_and_stypes_counts, kwargs, return_dict=True)
    project_code = split_search_key(kwargs['search_key'])
    result = server_start(project=project_code['project_code']).execute_python_script('', kwargs=code)

    return result['info']['spt_ret_val']


def users_query():
    """
    Query for Users
    :param asset_code: Code of asset related to task
    :param user: Optional users names
    :return:
    """
    server = server_start()
    search_type = 'sthpw/login'
    filters = []
    logins = server.query(search_type, filters)

    result = collections.OrderedDict()
    for login in logins:
        result[login['login']] = login

    return result


def delete_sobject_snapshot(sobject, delete_snapshot=True, search_keys=None, files_paths=None):
    dep_list = {
        'related_types': ['sthpw/file'],
        'files_list': {'search_key': search_keys,
                       'file_path': files_paths,
                       'delete_snapshot': delete_snapshot,
                       },
    }
    try:
        print server_start().delete_sobject(sobject, list_dependencies=dep_list), 'delete_sobject_snapshot'
        return True
    except Exception as err:
        print(err, 'delete_sobject_snapshot')
        return False


def delete_sobject_item(skey, delete_files=False):
    server_start().delete_sobject(skey, delete_files)


def sobject_delete_confirm(sobject):
    # ver_rev = gf.get_ver_rev(snapshot['version'], snapshot['revision'])

    msb = QtGui.QMessageBox(QtGui.QMessageBox.Question, 'Confirm deleting',
                            '<p><p>Do you really want to delete sobject:</p>{0}<p>Version: {1}</p>Also remove dependencies?</p>'.format(
                                sobject, 'VERREV'),
                            QtGui.QMessageBox.NoButton, env_inst.ui_main)

    msb.addButton("Delete", QtGui.QMessageBox.YesRole)
    msb.addButton("Cancel", QtGui.QMessageBox.NoRole)

    layout = QtGui.QVBoxLayout()

    widget = QtGui.QWidget()
    widget.setLayout(layout)

    msb_layot = msb.layout()

    # workaround for pyside2
    wdg_list = []

    for i in range(msb_layot.count()):
        wdg = msb_layot.itemAt(i).widget()
        if wdg:
            wdg_list.append(wdg)

    msb_layot.addWidget(wdg_list[0], 0, 0)
    msb_layot.addWidget(wdg_list[1], 0, 1)
    msb_layot.addWidget(wdg_list[2], 2, 1)
    msb_layot.addWidget(widget, 1, 1)

    from thlib.ui_classes.ui_dialogs_classes import deleteSobjectWidget

    delete_sobj_widget = deleteSobjectWidget(sobject=sobject)

    layout.addWidget(delete_sobj_widget)

    msb.exec_()
    reply = msb.buttonRole(msb.clickedButton())

    if reply == QtGui.QMessageBox.YesRole:
        return delete_sobj_widget.get_data_dict()
    else:
        return None


def snapshot_delete_confirm(snapshot, files):
    ver_rev = gf.get_ver_rev(snapshot['version'], snapshot['revision'])

    msb = QtGui.QMessageBox(QtGui.QMessageBox.Question, 'Confirm deleting',
                            '<p><p>Do you really want to delete snapshot, with context:</p>{0}<p>Version: {1}</p>Also remove selected Files?</p>'.format(
                                snapshot['context'], ver_rev),
                            QtGui.QMessageBox.NoButton, env_inst.ui_main)

    msb.addButton("Delete", QtGui.QMessageBox.YesRole)
    msb.addButton("Cancel", QtGui.QMessageBox.NoRole)

    layout = QtGui.QVBoxLayout()

    widget = QtGui.QWidget()
    widget.setLayout(layout)

    msb_layot = msb.layout()

    # workaround for pyside2
    wdg_list = []

    for i in range(msb_layot.count()):
        wdg = msb_layot.itemAt(i).widget()
        if wdg:
            wdg_list.append(wdg)

    msb_layot.addWidget(wdg_list[0], 0, 0)
    msb_layot.addWidget(wdg_list[1], 0, 1)
    msb_layot.addWidget(wdg_list[2], 2, 1)
    msb_layot.addWidget(widget, 1, 1)

    checkboxes = []
    files_list = []
    files_filtered_search_keys = []
    files_filtered_file_paths = []

    delete_snapshot_checkbox = QtGui.QCheckBox('Delete snapshot')
    delete_snapshot_checkbox.setChecked(True)
    layout.addWidget(delete_snapshot_checkbox)

    for i, fl in enumerate(files.itervalues()):
        checkboxes.append(QtGui.QCheckBox(fl[0]['file_name']))
        files_list.append(fl[0])
        checkboxes[i].setChecked(True)
        layout.addWidget(checkboxes[i])

    msb.exec_()
    reply = msb.buttonRole(msb.clickedButton())

    if reply == QtGui.QMessageBox.YesRole:

        if snapshot.get('repo'):
            asset_dir = env_server.rep_dirs[snapshot.get('repo')][0]
        else:
            asset_dir = env_server.rep_dirs['asset_base_dir'][0]

        for i, checkbox in enumerate(checkboxes):
            if checkbox.isChecked():
                files_filtered_search_keys.append(files_list[i]['__search_key__'])
                files_filtered_file_paths.append(
                    gf.form_path(
                        '{0}/{1}/{2}'.format(asset_dir, files_list[i]['relative_dir'], files_list[i]['file_name'])))

        return True, files_filtered_search_keys, files_filtered_file_paths, delete_snapshot_checkbox.isChecked()
    else:
        return False, None


def save_confirm(item_widget, paths, repo, context, update_versionless=True, description=''):

    message = '<p>You are about to save {0} file(s).</p><p>Continue?</p>'.format(len(paths))

    msb = QtGui.QMessageBox(
        QtGui.QMessageBox.Question,
        'Confirm saving',
        message,
        QtGui.QMessageBox.NoButton,
        env_inst.ui_main
        )

    layout = QtGui.QVBoxLayout()

    widget = QtGui.QWidget()
    widget.setLayout(layout)

    msb_layot = msb.layout()

    # workaround for pyside2
    wdg_list = []

    for i in range(msb_layot.count()):
        wdg = msb_layot.itemAt(i).widget()
        if wdg:
            wdg_list.append(wdg)

    msb_layot.addWidget(wdg_list[0], 0, 0)
    msb_layot.addWidget(wdg_list[1], 0, 1)
    msb_layot.addWidget(wdg_list[2], 2, 1)
    msb_layot.addWidget(widget, 1, 1)

    from thlib.ui_classes.ui_dialogs_classes import commitWidget

    save_confirm_widget = commitWidget(item_widget, paths, repo, context, update_versionless, description)

    layout.addWidget(save_confirm_widget)

    msb.addButton("Yes", QtGui.QMessageBox.YesRole)
    msb.addButton("No", QtGui.QMessageBox.NoRole)
    msb.exec_()
    reply = msb.buttonRole(msb.clickedButton())

    if reply == QtGui.QMessageBox.YesRole:
        return save_confirm_widget.get_data_dict()
    else:
        return None


def get_dirs_with_naming(search_key, process_list=None):
    kwargs = {
        'search_key': search_key,
        'process_list': process_list
    }
    code = tq.prepare_serverside_script(tq.get_dirs_with_naming, kwargs, return_dict=True)
    project_code = split_search_key(search_key)
    result = server_start(project=project_code['project_code']).execute_python_script('', kwargs=code)

    return json.loads(result['info']['spt_ret_val'])


def get_virtual_snapshot(search_key, context, files_dict, snapshot_type='file', is_revision=False, keep_file_name=False,
                         explicit_filename=None, version=None, checkin_type='file', ignore_keep_file_name=False):

    kwargs = {
        'search_key': search_key,
        'context': context,
        'snapshot_type': snapshot_type,
        'is_revision': is_revision,
        'files_dict': files_dict,
        'keep_file_name': keep_file_name,
        'explicit_filename': explicit_filename,
        'version': version,
        'checkin_type': checkin_type,
        'ignore_keep_file_name': ignore_keep_file_name,
    }

    code = tq.prepare_serverside_script(tq.get_virtual_snapshot_extended, kwargs, return_dict=True)
    project_code = split_search_key(search_key)
    server = server_start(project=project_code['project_code'])
    result = server.execute_python_script('', kwargs=code)
    virtual_snapshot = json.loads(result['info']['spt_ret_val'])

    return virtual_snapshot


def checkin_snapshot(search_key, context, snapshot_type=None, is_revision=False, description=None, version=None,
                     update_versionless=True, only_versionless=False, keep_file_name=False, repo_name=None, virtual_snapshot=None,
                     files_dict=None, mode=None, create_icon=False, files_objects=None):

    files_info = {
        'version_files': [],
        'version_files_paths': [],
        'versionless_files': [],
        'versionless_files_paths': [],
        'files_types': [],
        'file_sizes': [],
        'version_metadata': [],
        'versionless_metadata': []
    }

    repo = repo_name['value'][0]

    for (k1, v1), (k2, v2), file_object in zip(virtual_snapshot, files_dict, files_objects):
        for path_v, name_v, path_vs, name_vs, tp in zip(v1['versioned']['paths'],
                                                        v1['versioned']['names'],
                                                        v1['versionless']['paths'],
                                                        v1['versionless']['names'],
                                                        v2['t']):
            file_path_v = u'{0}/{1}'.format(repo, path_v)
            file_full_path_v = u'{0}/{1}'.format(file_path_v, ''.join(name_v))
            files_info['version_files'].append(file_full_path_v)
            files_info['version_files_paths'].append(path_v)
            file_path_vs = u'{0}/{1}'.format(repo, path_v)
            file_full_path_vs = u'{0}/{1}'.format(file_path_vs, ''.join(name_vs))
            files_info['versionless_files'].append(file_full_path_vs)
            files_info['versionless_files_paths'].append(path_vs)
            files_info['files_types'].append(tp)
            new_files_list = file_object.get_all_new_files_list(name_v, file_path_v)
            files_info['file_sizes'].append(file_object.get_sizes_list(together=True, files_list=new_files_list))
            files_info['version_metadata'].append(file_object.get_metadata())
            file_object.get_all_new_files_list(name_vs, file_path_vs)
            files_info['versionless_metadata'].append(file_object.get_metadata())

    kwargs = {
        'search_key': search_key,
        'context': context,
        'snapshot_type': snapshot_type,
        'is_revision': is_revision,
        'description': description,
        'version': version,
        'update_versionless': update_versionless,
        'only_versionless': only_versionless,
        'keep_file_name': keep_file_name,
        'files_info': files_info,
        'repo_name': repo_name['value'][3],
        'mode': mode,
        'create_icon': create_icon,
    }

    code = tq.prepare_serverside_script(tq.create_snapshot_extended, kwargs, return_dict=True)
    project_code = split_search_key(search_key)
    result = server_start(project=project_code['project_code']).execute_python_script('', kwargs=code)

    return result


# def add_repo_info(search_key, context, snapshot, repo):
#     server = server_start()
#     # adding repository info
#     splitted_skey = server.split_search_key(search_key)
#     filters_snapshots = [
#         ('context', context),
#         ('search_code', splitted_skey[1]),
#         ('search_type', splitted_skey[0]),
#         ('version', -1),
#     ]
#     parent = server.query_snapshots(filters=filters_snapshots, include_files=False)[0]
#
#     data = {
#         snapshot.get('__search_key__'): {'repo': repo['name']},
#         parent.get('__search_key__'): {'repo': repo['name']},
#     }
#     server.update_multiple(data, False)


def update_description(search_key, description):
    data = {
        'description': description
    }
    transaction = server_start().update(search_key, data)

    return transaction


def add_note(search_key, process, context, note, note_html, login):
    search_type = 'sthpw/note'

    data = {
        'process': process,
        'context': context,
        'note': note,
        # 'note_html': gf.html_to_hex(note_html),
        'login': login,
    }
    project_code = split_search_key(search_key)
    transaction = server_start(project=project_code['project_code']).insert(search_type, data, parent_key=search_key, triggers=False)

    return transaction


def task_process_query(seach_key):
    # TODO Query task process per process
    # from pprint import pprint
    server = server_start()
    processes = {}
    default_processes = ['Assignment', 'Pending', 'In Progress', 'Waiting', 'Need Assistance', 'Revise', 'Reject',
                         'Complete', 'Approved']
    default_colors = ['#ecbf7f', '#8ad3e5', '#e9e386', '#a96ccf', '#a96ccf', '#e84a4d', '#e84a4d', '#a3d991', '#a3d991']

    processes['process'] = default_processes
    processes['color'] = default_colors

    # process_expr = "@SOBJECT(sthpw/pipeline['search_type', 'sthpw/task'].config/process)"
    # process_expr = "@SOBJECT(sthpw/pipeline['code', 'the_pirate/Concept'].config/process)"
    # process_expr = "@SOBJECT(sthpw/pipeline['code', 'cgshort/props'].config/process)"
    # process_expr = "@SOBJECT(sthpw/subscription['login','{0}'])".format('admin')
    # process_expr = "@SOBJECT(sthpw/message_log['message_code','cgshort/characters?project=the_pirate&code=CHARACTERS00001'])"
    # process_list = server_start().eval(process_expr)
    # print(dir(thread_server_start()))
    # thr = ServerThread()
    # print(ServerThread().isRunning())

    # def rt():
    #
    #     filters = [('search_code', ['PROPS00001', 'PROPS00002', 'PROPS00003', 'PROPS00004','PROPS00005','PROPS00006','PROPS00007','PROPS00008','PROPS00009','PROPS00010','PROPS00011','PROPS00012','PROPS00013','PROPS00014','PROPS00015','PROPS00016','PROPS00017','PROPS00018','PROPS00019','PROPS00021']), ('project_code', 'the_pirate')]
    #     return thr.server.query_snapshots(filters=filters, include_files=True)
    # return thr.server.get_all_children('cgshort/props?project=the_pirate&code=PROPS00001', 'sthpw/snapshot')
    # return asd
    # thr.routine = rt
    # print(thr.isRunning())
    # thr.start()
    # print(thr.isRunning())
    #
    # def print_result():
    #     print(thr.result)
    #
    # thr.finished.connect(print_result)
    # pprint(asd)


    code = [('message_code', 'cgshort/characters?project=the_pirate&code=CHARACTERS00001')]
    search_type = 'sthpw/message_log'

    message = server.query(search_type, code)

    # from pprint import pprint
    print('from task_process_query!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    # pprint(message)
    # print(message[0])
    # import json
    # data = json.loads(message[0]['message'])
    # pprint(data)
    # if (len(process_list) == 0):
    #     process_list = default_processes


    # print('from task_process_query!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    # pprint(process_list)

    return processes


def task_priority_query(seach_key):
    """
    Takes info from html widget, to get priority values
    :return: tuple lavel - value
    """
    # TODO Use this method, and make it templates
    # defin = server_start().get_config_definition('sthpw/task', 'edit_definition', 'priority')
    # print('from task_priority_query')
    # print(defin)

    class_name = 'tactic.ui.manager.EditElementDefinitionWdg'

    args = {
        'config_xml': '',
        'element_name': 'priority',
        'path': '/Edit/priority',
        'search_type': 'sthpw/task',
        'view': 'edit_definition',
    }

    widget_html = server_start().get_widget(class_name, args, [])

    import re

    values_expr = '<values>(.*?)</values>'
    values_pattern = re.compile(values_expr)
    values_result = re.findall(values_pattern, widget_html)
    values = values_result[0].split('|')

    labels_expr = '<labels>(.*?)</labels>'
    labels_pattern = re.compile(labels_expr)
    labels_result = re.findall(labels_pattern, widget_html)
    labels = labels_result[0].split('|')

    result = zip(labels, values)

    return result


def generate_web_and_icon(source_image_path, web_save_path=None, icon_save_path=None):

    image = Qt4Gui.QImage(0, 0, Qt4Gui.QImage.Format_ARGB32)

    if image.load(source_image_path):
        if web_save_path:
            web = image.scaledToWidth(640, QtCore.Qt.SmoothTransformation)
            web.save(web_save_path)
        if icon_save_path:
            icon = image.scaledToWidth(120, QtCore.Qt.SmoothTransformation)
            icon.save(icon_save_path)


def inplace_checkin(file_paths, virtual_snapshot, repo_name, update_versionless, only_versionless=False, generate_icons=True,
                    files_objects=None, padding=None, progress_callback=None):
    check_ok = False

    def copy_file(dest_path, source_path):
        if dest_path == source_path:
            print('Destination path is equal to source path, skipping...', dest_path)
        else:
            shutil.copyfile(source_path, dest_path)
        if not os.path.exists(dest_path):
            return False
        else:
            return True

    versions = ['versioned']
    if update_versionless:
        versions.extend(['versionless'])

    if only_versionless:
        versions = ['versionless']

    for i, (key, val) in enumerate(virtual_snapshot):
        if progress_callback:
            info_dict = {
                'status_text': key,
                'total_count': len(virtual_snapshot)
            }
            progress_callback(i, info_dict)
        for ver in versions:
            dest_path_vers = repo_name['value'][0] + '/' + val[ver]['paths'][0]
            dest_files_vers = files_objects[i].get_all_new_files_list(val[ver]['names'][0], dest_path_vers, new_frame_padding=padding)

            # create dest dirs
            if not os.path.exists(dest_path_vers):
                os.makedirs(dest_path_vers)

            # copy files to dest dir
            for j, fl in enumerate(file_paths[i]):
                check_ok = copy_file(gf.form_path(dest_files_vers[j]), gf.form_path(fl))
                if progress_callback:
                    info_dict = {
                        'status_text': gf.extract_filename(fl),
                        'total_count': len(file_paths[i])
                    }
                    progress_callback(j, info_dict)

            if generate_icons and len(val[ver]['paths']) > 1:
                dest_web_path_vers = gf.form_path(
                    repo_name['value'][0] + '/' +
                    val[ver]['paths'][1]
                )
                dest_web_file_vers = files_objects[i].get_all_new_files_list(val[ver]['names'][1], dest_web_path_vers)

                dest_icon_path_vers = gf.form_path(
                    repo_name['value'][0] + '/' +
                    val[ver]['paths'][2]
                )
                dest_icon_file_vers = files_objects[i].get_all_new_files_list(val[ver]['names'][2], dest_icon_path_vers)
                if not os.path.exists(dest_web_path_vers):
                    os.makedirs(dest_web_path_vers)
                if not os.path.exists(dest_icon_path_vers):
                    os.makedirs(dest_icon_path_vers)

                # convert original to web and icon format
                # TODO at this moment it converting twice when doing versionless
                for k, fl in enumerate(file_paths[i]):
                    generate_web_and_icon(fl, dest_web_file_vers[k], dest_icon_file_vers[k])
                    # if ver == 'versioned':
                    #     generate_web_and_icon(fl, dest_web_file_vers[k], dest_icon_file_vers[k])
                    # else:
                    #     copy_file(dest_files_vers[j], fl)

    return check_ok


# Checkin functions
def checkin_file(search_key, context, snapshot_type='file', is_revision=False, description=None, version=None,
                 only_versionless=False, update_versionless=True, file_types=None, file_names=None, file_paths=None,
                 exts=None, subfolders=None, postfixes=None, metadata=None, padding=None, keep_file_name=False,
                 repo_name=None, mode=None, create_icon=True, ignore_keep_file_name=False, checkin_app='standalone',
                 selected_objects=False, ext_type='mayaAscii', setting_workspace=False, checkin_type='file',
                 files_dict=None, item_widget=None, files_objects=None, explicit_filename=None, commit_silently=False):

    if not files_dict:
        files_dict = []

        for i, fn in enumerate(file_names):
            file_dict = dict()
            file_dict['t'] = [file_types[i]]
            file_dict['s'] = [subfolders[i]]
            file_dict['e'] = [exts[i]]
            file_dict['p'] = [postfixes[i]]
            if metadata:
                file_dict['m'] = metadata[i]
            else:
                file_dict['m'] = None

            files_dict.append((fn, file_dict))

        # extending files which can have thumbnails
        for key, val in files_dict:
            if gf.file_format(val['e'][0])[3] == 'preview':
                val['t'].extend(['web', 'icon'])
                val['s'].extend(['__preview/web', '__preview/icon'])
                val['e'].extend(['jpg', 'png'])
                val['p'].extend(['', ''])

    args_dict = {
        'search_key': search_key,
        'context': context,
        'snapshot_type': snapshot_type,
        'is_revision': is_revision,
        'description': description,
        'version': version,
        'update_versionless': update_versionless,
        'only_versionless': only_versionless,
        'file_paths': file_paths,
        'padding': padding,
        'files_dict': files_dict,
        'keep_file_name': keep_file_name,
        'explicit_filename': explicit_filename,
        'repo_name': repo_name,
        'mode': mode,
        'create_icon': create_icon,
        'ignore_keep_file_name': ignore_keep_file_name,
        'checkin_app': checkin_app,
        'selected_objects': selected_objects,
        'ext_type': ext_type,
        'setting_workspace': setting_workspace,
        'checkin_type': checkin_type,
        'item_widget': item_widget,
        'files_objects': files_objects,
    }

    search_key_split = split_search_key(search_key)

    if commit_silently:
        checkin_wdg = env_inst.get_check_tree(search_key_split['project_code'], 'checkin_out', search_key_split['pipeline_code'])

        commit_queue = env_inst.get_commit_queue('global_commit_queue')
        if not commit_queue:
            from thlib.ui_classes.ui_dialogs_classes import Ui_commitQueueWidget
            commit_queue = Ui_commitQueueWidget(parent=checkin_wdg)
            env_inst.commit_queue['global_commit_queue'] = commit_queue

        commit_queue.setParent(checkin_wdg)
        commit_queue.add_item_to_queue(args_dict, commit_queue)
        commit_queue.setWindowModality(QtCore.Qt.ApplicationModal)
        commit_queue.splitter.moveSplitter(2000, 0)
        commit_queue.show()
    else:
        commit_queue = env_inst.get_commit_queue(search_key_split['project_code'])
        commit_queue.add_item_to_queue(args_dict)
        commit_queue.show()

    return commit_queue


def checkin_playblast(snapshot_code, file_name, custom_repo_path):
    """
    :return:
    """

    # code = [('code', 'cgshort/props?project=the_pirate&code=PROPS00001')]
    # search_type = 'sthpw/message'
    #
    # message = server_query(search_type, code)
    #
    # from pprint import pprint
    # pprint(message[0]['message'])
    #
    # import json
    # data = json.loads(message[0]['message'])
    #
    # pprint(data)

    # subs = 'cgshort/props?project=the_pirate&code=PROPS00004'

    # subscribe = server_start().subscribe(subs, 'sobject')
    # print(subscribe)

    # snapshot_code = 'SNAPSHOT00000213'
    # path = 'D:/mountain.jpg'

    playblast = server_start().add_file(
        snapshot_code,
        file_name,
        file_type='playblast',
        mode='preallocate',
        create_icon=True,
        # dir_naming='{project.code}/{search_type.table_name}/{sobject.name}/work/{snapshot.process}/versions/asd',
        # file_naming='{sobject.name}_{snapshot.context}_{file.type}_v{version}.{ext}',
        checkin_type='auto',
        custom_repo_path=custom_repo_path,
        do_update_versionless=True,
    )
    return playblast


def checkin_icon(snapshot_code, file_name):
    """
    :return:
    """

    icon = server_start().add_file(snapshot_code, file_name, file_type='main', mode='upload', create_icon=True,
                                   file_naming='{sobject.name}_{file.type}_v{version}.{ext}',
                                   checkin_type='auto')
    return icon


# Skey functions
def parce_skey(skey, get_skey_and_context=False):

    if get_skey_and_context:
        skey_list = skey[7:].split('&context=')
        return {'search_key': skey_list[0], 'context': skey_list[1]}

    skey_splitted = urlparse.urlparse(skey)
    skey_dict = dict(urlparse.parse_qsl(skey_splitted.query))
    skey_dict['namespace'] = skey_splitted.netloc
    skey_dict['pipeline_code'] = skey_splitted.path[1:]

    if skey_splitted.scheme == 'skey':
        if skey_dict['pipeline_code'] == 'snapshot':
            skey_dict['type'] = 'snapshot'
            snapshot = server_start().query('sthpw/snapshot', [('code', skey_dict.get('code'))])
            if snapshot:
                snapshot = snapshot[0]
                skey_dict['pipeline_code'] = snapshot['search_type'].split('/')[-1].split('?')[0]
                skey_dict['namespace'] = snapshot['search_type'].split('/')[0]
                skey_dict['project'] = snapshot['project_code']
                skey_dict['context'] = snapshot['context']
                skey_dict['code'] = snapshot['search_code']
                skey_dict['item_code'] = snapshot['code']
        else:
            skey_dict['type'] = 'sobject'
            if not skey_dict.get('context'):
                skey_dict['context'] = '_no_context_'
        return skey_dict
    else:
        return None


def generate_skey(pipeline_code=None, code=None):
    skey = 'skey://{0}/{1}?project={2}&code={3}'.format(
        env_server.get_namespace(),
        pipeline_code,
        env_server.get_project(),
        code
    )

    return skey

