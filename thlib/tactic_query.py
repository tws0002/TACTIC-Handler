# Internal server-side sctipts

import global_functions as gf
import inspect


def prepare_serverside_script(func, kwargs, return_dict=True, has_return=True, shrink=True):
    func_lines = inspect.getsourcelines(func)
    if has_return:
        run_command = func_lines[0][0].replace('def ', 'return ')[:-2]
    else:
        run_command = func_lines[0][0].replace('def ', '')[:-2]

    # i don't want 're' here, so try to understand logic, with love to future me :-*
    # TODO multiline bug
    val_split = run_command.split(',')
    left_part = val_split[0].split('(')
    right_part = val_split[-1][:-1]
    full_list = [left_part[1]] + val_split[1:-1] + [right_part]

    all_vars = []
    for split in full_list:
        # split keys and values, and add to list keys which values need update
        fltr = split.split('=')[0].replace(' ', '')
        if fltr in kwargs.keys():
            all_vars.append(fltr)

    for i, k in enumerate(all_vars):
        for key, val in kwargs.items():
            if k == key:
                all_vars[i] = '{0}={1}'.format(key, repr(val))

    var_stitch = ', '.join(all_vars)
    ready_run_command = '{0}({1})'.format(run_command[:run_command.find('(')], var_stitch)

    traceback = inspect.getsourcelines(get_traceback)
    handle = inspect.getsourcelines(traceback_handle)

    code = ''.join(traceback[0]) + ''.join(handle[0]) + '@traceback_handle \n' + ''.join(func_lines[0]) + ready_run_command

    if shrink:
        code = gf.minify_code(source=code, pack=False)

    if return_dict:
        code_dict = {
            'code': code
        }
        return code_dict
    else:
        return code


def traceback_handle(func):
    def traceback_handle_wrap(*arg, **kwarg):
        try:
            result = func(*arg, **kwarg)
        except:
            result = get_traceback()
        return result

    return traceback_handle_wrap


def get_traceback():
    result = u''
    import traceback, sys
    exception_type, exception_value, exception_traceback = sys.exc_info()

    exception_type_string = exception_type is not None and exception_type.__name__ or u'UnknownError'
    exception_value_string = exception_value is not None and exception_value.message or u'Unknown error handled'

    format_traceback = traceback.format_exception(exception_type, exception_value, exception_traceback, limit=100)
    if format_traceback:
        if isinstance(format_traceback, (list, set, tuple)):
            format_traceback_list = list(format_traceback)
        else:
            format_traceback_list = [format_traceback]
        for format_traceback in format_traceback_list:
            if isinstance(format_traceback, (basestring, unicode)):
                result += format_traceback
            else:
                try:
                    result += format_traceback.__repr__()
                except:
                    try:
                        result += unicode(format_traceback)
                    except:
                        result += u'( Failed to decode Exception data )'
    if not result:
        result = u'Error: ' + exception_value_string + u'\n' + exception_type_string + u': ' + exception_value_string

    return result


def get_result(result):
    if result['info']['spt_ret_val'][0:9] == 'Traceback':
        raise Exception(result['info']['spt_ret_val'])
    else:
        return result['info']['spt_ret_val']


def query_EditWdg(args=None, search_type=''):
    import json
    from pyasm.widget.widget_config import WidgetConfigView

    def pop_classes(in_dict):
        out_dict = {}
        for key, val in in_dict.iteritems():
            if not (hasattr(val, '__dict__') or key.startswith('_')):
                out_dict[key] = val
        return out_dict

    class_name = 'tactic.ui.panel.EditWdg'

    args_array = []

    from pyasm.common import Common

    # from pyasm.common import Container
    widget = Common.create_from_class_path(class_name, args_array, args)
    widget.explicit_display()
    result_dict = {
        'EditWdg': {
            'element_descriptions': widget.element_descriptions,
            'element_names': widget.element_names,
            'element_titles': widget.element_titles,
            'input_prefix': widget.input_prefix,
            'kwargs': widget.kwargs,
            'mode': widget.mode,
            'security_denied': widget.security_denied,
            'title': widget.title,
        },
        'InputWidgets': [],
        'sobject': '',
    }
    input_widgets = widget.get_widgets()
    wdg_config = WidgetConfigView.get_by_element_names(search_type, widget.element_names, base_view=args['view'])

    temprorary_ignore = ['pyasm.prod.web.prod_input_wdg.ProjectSelectWdg']
    # , 'pyasm.widget.input_wdg.SelectWdg' bug with this widget

    for i_widget in input_widgets:
        widget_dict = pop_classes(i_widget.__dict__)
        # for wv, wi in widget_dict.items():
        #     if type(wi) not in [dict, None, str, int, bool, list, set, tuple]:
        #         widget_dict[wv] = str(wi)
        widget_dict['action_options'] = wdg_config.get_action_options(widget_dict.get('name'))
        widget_dict['class_name'] = i_widget.get_class_name()
        item_values = i_widget.get_values()
        if item_values:
            widget_dict['values'] = item_values
        if widget_dict['class_name'] not in temprorary_ignore:
            result_dict['InputWidgets'].append(widget_dict)

    return json.dumps(result_dict, separators=(',', ':'))
    # return str(widget.get_widgets())
    # return (dir(widget))

    # Container.put("request_top_wdg", widget)
    # html = widget.get_buffer_display()
    # m = Container.get_instance()
    # m.get_data()
    # print m.get('SearchType:virtual_stypes')

    # widget_html = server.get_widget(class_name, args, [])
    # return widget_html


def delete_sobject(search_key, include_dependencies=False, list_dependencies=None):
    '''Invokes the delete method.  Note: this function may fail due
    to dependencies.  Tactic will not cascade delete.  This function
    should be used with extreme caution because, if successful, it will
    permenently remove the existence of an sobject

    @params
    ticket - authentication ticket
    search_key - the key identifying
                  the search_type table.
    include_dependencies - true/false
    list_dependencies - dependency dict {
        'related_types': ["sthpw/note", "sthpw/file"],
        'files_list': {
                        'search_key': [],
                        'file_path': [],
                        'delete_snapshot': True,
    } etc...

    @return
    sobject - a dictionary that represents values of the sobject in the
        form name/value pairs
    '''
    api = server.server
    sobjects = api._get_sobjects(search_key)
    if not sobjects:
        raise Exception("SObject [%s] does not exist" % search_key)
    sobject = sobjects[0]

    # delete this sobject
    if include_dependencies:
        from tactic.ui.tools import DeleteCmd
        cmd = DeleteCmd(sobject=sobject, auto_discover=True)
        cmd.execute()
    elif list_dependencies:
        from tactic.ui.tools import DeleteCmd
        cmd = DeleteCmd(sobject=sobject, values=list_dependencies)
        cmd.execute()
    else:
        sobject.delete()

    return api._get_sobject_dict(sobject)


def get_notes_and_stypes_counts(process, search_key, stypes_list):
    # getting notes by search_type process and count of stypes from stypes_list
    from pyasm.search import Search

    search_type, search_code = server.split_search_key(search_key)

    cnt = {
        'notes': {},
        'stypes': {},
    }
    if process:
        for p in process:
            search = Search('sthpw/note')
            search.add_op_filters([('process', p), ('search_type', search_type), ('search_code', search_code)])
            cnt['notes'][p] = search.get_count()

    for stype in stypes_list:
        try:
            search = Search(stype)
            search.add_parent_filter(search_key)
            count = search.get_count(True)
            if count == -1:
                count = 0
            cnt['stypes'][stype] = count
        except:
            cnt['stypes'][stype] = 0

    return cnt


def query_search_types_extended(project_code, namespace):
    """
    This crazy stuff made to execute queries on server
    All needed info is getting almost half time faster
    :return:
    """
    # TODO remove query, and dig deeper to get more info about pipelines, processes, stypes
    # from pyasm.search import Search
    # from pyasm.biz import Pipeline
    #
    # search_type = 'cgshort/scenes'
    # search = Search("sthpw/pipeline")
    # search.add_filter("search_type", search_type)
    # pipelines = search.get_sobjects()
    #
    # return str(pipelines)
    import json
    from pyasm.biz import Project
    api = server.server
    get_sobject_dict = api.get_sobject_dict

    prj = Project.get_by_code(project_code)

    stypes = prj.get_search_types()

    from pyasm.widget import WidgetConfigView
    from pyasm.search import WidgetDbConfig
    from pyasm.biz import Project

    all_stypes = []
    for stype in stypes:
        stype_dict = get_sobject_dict(stype)
        stype_dict['column_info'] = stype.get_column_info(stype.get_code())
        all_stypes.append(stype_dict)

        # getting views for columns viewer
        views = ['table', 'definition', 'color', 'edit', 'edit_definition']
        definition = {}
        full_search_type = Project.get_full_search_type(stype)
        for view in views:

            db_config = WidgetDbConfig.get_by_search_type(full_search_type, view)
            if db_config:
                config = db_config.get_xml()
            else:
                config_view = WidgetConfigView.get_by_search_type(stype, view)
                config = config_view.get_config()

            definition[view] = config.to_string()

        stype_dict['definition'] = definition

    # getting pipeline process
    # stypes_codes = []
    # for stype in all_stypes:
    #     stypes_codes.append(stype['code'])
    # stypes_codes.append('sthpw/task')
    search_type = 'sthpw/pipeline'
    # filters = [('search_type', stypes_codes)] - THIS IS VALID CODE
    # filters = [('project_code', 'is', 'NULL'), ('project_code', 'like', project_code)]
    filters = [] # temporary
    stypes_pipelines = server.query(search_type, filters, return_sobjects=True)

    # getting processes info
    pipelines = []
    for stype in stypes_pipelines:
        stypes_dict = stype.get_sobject_dict()

        processes = []
        for process in stype.get_process_names():
            process_sobject = stype.get_process_sobject(process)
            if process_sobject:
                processes.append(api.get_sobject_dict(process_sobject))

        task_processes = []
        for process in stype.get_processes():
            process_obj = process.get_task_pipeline()
            if process_obj != 'task':
                task_processes.append(process_obj)

        stypes_dict['tasks_processes'] = task_processes
        stypes_dict['stypes_processes'] = processes
        pipelines.append(stypes_dict)

    # getting project schema
    schema = server.query('sthpw/schema', [('code', project_code)])

    result = {'schema': schema, 'pipelines': pipelines, 'stypes': all_stypes}

    return json.dumps(result, separators=(',', ':'))


def get_dirs_with_naming(search_key=None, process_list=None):
    import json
    from pyasm.biz import Snapshot
    from pyasm.biz import Project
    from pyasm.search import SearchType

    dir_naming = Project.get_dir_naming()

    dirs_dict = {
        'versions': [],
        'versionless': [],
    }

    if process_list:
        processes = process_list
    else:
        from pyasm.biz import Pipeline
        sobjects = server.server._get_sobjects(search_key)
        sobject = sobjects[0]
        pipelines = Pipeline.get_by_search_type(sobject.get_base_search_type())
        processes = pipelines[0].get_process_names()

    search_type, search_code = server.split_search_key(search_key)
    search_type = search_type.split('?')[0]

    for process in processes:
        # querying sobjects every time because we need to refresh naming
        sobject = server.query(search_type, filters=[('code', search_code)], return_sobjects=True, single=True)
        dir_naming.set_sobject(sobject)
        file_object = SearchType.create('sthpw/file')
        dir_naming.set_file_object(file_object)
        snapshot = Snapshot.create(sobject, snapshot_type='file', context=process, commit=False)
        dir_naming.set_snapshot(snapshot)
        dirs_dict['versions'].append(dir_naming.get_dir('relative'))

        snapshot_versionless = Snapshot.create(sobject, snapshot_type='file', context=process, process=process,
                                               commit=False, version=-1)
        dir_naming.set_snapshot(snapshot_versionless)
        dirs_dict['versionless'].append(dir_naming.get_dir('relative'))

    return json.dumps(dirs_dict, separators=(',', ':'))


def query_sobjects(search_type, filters=[], order_bys=[], limit=None, offset=None):
    import json
    from pyasm.search import Search
    from pyasm.biz import Snapshot

    sobjects_list = server.query(search_type, filters=filters, order_bys=order_bys, limit=limit, offset=offset)

    total_sobjects_count = len(server.query(search_type))
    total_sobjects_query_count = len(server.query(search_type, filters=filters))

    result = {
        'total_sobjects_count': total_sobjects_count,
        'total_sobjects_query_count': total_sobjects_query_count,
        'sobjects_list': sobjects_list,
        'limit': limit,
        'offset': offset,
    }
    have_search_code = False
    if sobjects_list:
        if sobjects_list[0].get('code'):
            have_search_code = True

    for sobject in sobjects_list:

        search = Search('sthpw/note')
        if have_search_code:
            search.add_op_filters(
                [('process', 'publish'), ('search_type', search_type), ('search_code', sobject['code'])])
        else:
            search.add_op_filters(
                [('process', 'publish'), ('search_type', search_type), ('search_id', sobject['id'])])

        sobject['__notes_count__'] = search.get_count()

        search = Search('sthpw/task')
        if have_search_code:
            search.add_op_filters([('search_type', search_type), ('search_code', sobject['code'])])
        else:
            search.add_op_filters([('search_type', search_type), ('search_id', sobject['id'])])

        sobject['__tasks_count__'] = search.get_count()

        search = Search('sthpw/snapshot')
        if have_search_code:
            search.add_op_filters(
                [('process', ['icon', 'attachment', 'publish']), ('search_type', search_type), ('search_code', sobject['code'])])
        else:
            search.add_op_filters(
                [('process', ['icon', 'attachment', 'publish']), ('search_type', search_type), ('search_id', sobject['id'])])
        # search.add_order_by('timestamp asc')
        snapshots = search.get_sobjects()

        snapshot_files = Snapshot.get_files_dict_by_snapshots(snapshots)

        snapshots_list = []
        for snapshot in snapshots:
            snapshot_dict = server.server._get_sobject_dict(snapshot)
            files_list = []
            files = snapshot_files.get(snapshot_dict['code'])
            if files:
                for fl in files:
                    files_list.append(server.server._get_sobject_dict(fl))
            snapshot_dict['__files__'] = files_list
            snapshots_list.append(snapshot_dict)

        sobject['__snapshots__'] = snapshots_list

    return json.dumps(result, separators=(',', ':'))


def get_virtual_snapshot_extended(search_key, context, files_dict, snapshot_type="file", is_revision=False, level_key=None, keep_file_name=False, explicit_filename=None, version=None, update_versionless=True, ignore_keep_file_name=False, checkin_type='file'):
    '''creates a virtual snapshot and returns a path that this snapshot
    would generate through the naming conventions''

    @params
    snapshot creation:
    -----------------
    search_key - a unique identifier key representing an sobject
    context - the context of the checkin
    snapshot_type - [optional] descibes what kind of a snapshot this is.
        More information about a snapshot type can be found in the
        prod/snapshot_type sobject
    level_key - the unique identifier of the level that this
        is to be checked into

    path creation:
    --------------
    file_type: the type of file that will be checked in.  Some naming
        conventions make use of this information to separate directories
        for different file types
    file_name: the desired file name of the preallocation.  This information
        may be ignored by the naming convention or it may use this as a
        base for the final file name
    ext: force the extension of the file name returned

    @return
    path as determined by the naming conventions
    '''
    # getting virtual snapshots
    import json
    from pyasm.biz import Snapshot
    from pyasm.biz import Project
    # from pyasm.biz import File, FileGroup, FileRange
    from pyasm.search import SearchType
    api = server.server

    sobjects = api._get_sobjects(search_key)
    sobject = sobjects[0]

    # get the level object
    if level_key:
        levels = api._get_sobjects(level_key)
        level = levels[0]
        level_type = level.get_search_type()
        level_id = level.get_id()
    else:
        level_type = None
        level_id = None

    description = "No description"

    # this is only to avoid naming intersection
    if checkin_type == 'file':
        if len(files_dict) > 1 and not ignore_keep_file_name:
            keep_file_name = True

    # if checkin_type == 'multi_file':
    #     keep_file_name = False

    # if len(set(file_type)) != 1:
    #     keep_file_name = False

    if not version:
        ver = server.eval("@MAX(sthpw/snapshot['context', '{0}'].version)".format(context), search_keys=[search_key])
        if ver:
            if is_revision:
                version = int(ver)
            else:
                version = int(ver) + 1
        else:
            version = 1

    file_naming = Project.get_file_naming()
    file_naming.set_sobject(sobject)

    snapshot_versioned = Snapshot.create(sobject, snapshot_type=snapshot_type, context=context, description=description,
                                         is_revision=is_revision, level_type=level_type, level_id=level_id,
                                         commit=False, version=version)

    if is_revision:
        snapshot_versioned.set_value('version', version)

    if update_versionless:
        snapshot_versionless = Snapshot.create(sobject, snapshot_type=snapshot_type, context=context,
                                               description=description, is_revision=False, level_type=level_type,
                                               level_id=level_id, commit=False, version=-1)

    file_object = SearchType.create("sthpw/file")

    def prepare_filename(filenaming, f_l, ext, postfix, metadata):

        if keep_file_name:
            file_type = filenaming.get_file_type()
            if file_type in ['web', 'icon']:
                postfix = file_type
            if postfix:
                result_file_name = f_l + '_' + postfix + '.' + ext
            else:
                if ext:
                    result_file_name = f_l + '.' + ext
                else:
                    result_file_name = f_l
        else:
            name_ext = filenaming.get_file_name()

            # filenaming.get_file_name()
            if postfix:
                result_file_name = name_ext.replace(filenaming.get_ext(), '_{0}.{1}'.format(postfix, ext))
            else:
                result_file_name = name_ext

        first_part = result_file_name.replace(filenaming.get_ext(), '')
        # second_part = ''
        #
        # if metadata:
        #     if metadata.get('type') in ['udim', 'layer_udim', 'udim_sequence', 'layer_udim_sequence']:
        #         result_file_name = result_file_name.replace(filenaming.get_ext(), '_[UUVV].{0}'.format(ext))
        #
        #     if metadata.get('type') in ['uv', 'layer_uv', 'uv_sequence', 'layer_uv_sequence']:
        #         result_file_name = result_file_name.replace(filenaming.get_ext(), '_[u<>_v<>].{0}'.format(ext))
        #
        #     if metadata.get('type') in ['sequence', 'layer_sequence', 'layer_uv_sequence', 'layer_udim_sequence', 'uv_sequence', 'udim_sequence']:
        #         padding = int(metadata['padding'])
        #         result_file_name = result_file_name.replace(filenaming.get_ext(), '.[{0}].{1}'.format('#' * padding, ext))
        #
        #     second_part = result_file_name.replace(first_part, '').replace(filenaming.get_ext(), '')

        # from pyasm.biz import Naming
        # b = Naming.get(filenaming.sobject, filenaming.snapshot, file_path=filenaming.file_object.get_full_file_name())

        if metadata:
            return first_part, metadata.get('name_part'), filenaming.get_ext()
        else:
            return first_part, '', filenaming.get_ext()

    def prepare_folder(d, sub):
        if sub:
            return d + '/' + sub
        else:
            return d

    result_list = []
    # fl::file, t::type, e::extension, s::sub-folder, p::postfix, m::metadata
    for fl, val in files_dict:

        result_dict = {'versionless': {'paths': [], 'names': []}, 'versioned': {'paths': [], 'names': []}}

        if not fl:
            fl = sobject.get_code()
        elif not fl:
            fl = sobject.get_name()
        elif not fl:
            fl = "unknown"

        if explicit_filename:
            keep_file_name = True
            fl = explicit_filename

        for t, e, s, p in zip(val['t'], val['e'], val['s'], val['p']):
            file_object.set_value("file_name", fl)
            file_object.set_value("type", t)
            if val['m']:
                file_object.set_value("metadata", json.dumps(val['m'], separators=(',', ':')))

            file_naming.set_snapshot(snapshot_versioned)
            file_naming.set_ext(e)
            file_naming.set_file_object(file_object)
            result_dict['versioned']['paths'].append(prepare_folder(snapshot_versioned.get_dir('relative', file_type=t), s))
            result_dict['versioned']['names'].append(prepare_filename(file_naming, fl, e, p, val['m']))

            if update_versionless:
                file_naming.set_snapshot(snapshot_versionless)
                file_naming.set_ext(e)
                file_naming.set_file_object(file_object)
                result_dict['versionless']['paths'].append(prepare_folder(snapshot_versionless.get_dir('relative', file_type=t), s))
                result_dict['versionless']['names'].append(prepare_filename(file_naming, fl, e, p, val['m']))

        result_list.append((fl, result_dict))

    return json.dumps(result_list, separators=(',', ':'))


def create_snapshot_extended(search_key, context, snapshot_type=None, is_revision=False, is_latest=True, is_current=False, description=None, version=None, level_key=None, update_versionless=True, only_versionless=False, keep_file_name=True, repo_name=None, files_info=None, mode=None, create_icon=False):
    import os
    import json
    from pyasm.biz import Snapshot
    from pyasm.checkin import FileAppendCheckin
    from pyasm.search import Search

    api = server.server

    sobjects = api._get_sobjects(search_key)
    sobject = sobjects[0]

    # get the level object
    if level_key:
        levels = api._get_sobjects(level_key)
        level = levels[0]
        level_type = level.get_search_type()
        level_id = level.get_id()
    else:
        level_type = None
        level_id = None

    if not description:
        description = 'No description'
    if not snapshot_type:
        snapshot_type = 'file'

    if not version:
        ver = server.eval("@MAX(sthpw/snapshot['context', '{0}'].version)".format(context), search_keys=[search_key])
        if ver:
            if is_revision:
                version = int(ver)
            else:
                version = int(ver) + 1
        else:
            version = 1

    snapshot = Snapshot.create(sobject, snapshot_type=snapshot_type, context=context, description=description, is_revision=is_revision, is_latest=is_latest, is_current=is_current, level_type=level_type, level_id=level_id, commit=False, version=version)

    if repo_name:
        snapshot.set_value('repo', repo_name)
    if is_latest:
        snapshot.set_value('is_latest', 1)
    if is_current:
        snapshot.set_value('is_current', 1)

    if is_revision:
        snapshot_code = server.eval("@GET(sthpw/snapshot['version', {0}].code)".format(version),
                                    search_keys=[search_key], single=True)
        revision = server.eval("@MAX(sthpw/snapshot.revision)",
                               search_keys=['sthpw/snapshot?code={0}'.format(snapshot_code)])

        snapshot.set_value('version', version)
        snapshot.set_value('revision', revision + 1)

    if only_versionless:
        snapshot.set_value('version', -1)
        snapshot.set_value('is_current', 0)
        snapshot.set_value('is_latest', 1)
        update_versionless = True
        existing_versionless_snapshot = snapshot.get_by_sobjects([sobject], context, version=-1)
        if existing_versionless_snapshot:
            from tactic.ui.tools import DeleteCmd
            cmd = DeleteCmd(sobject=existing_versionless_snapshot[0], auto_discover=True)
            cmd.execute()

    snapshot.commit(triggers=True, log_transaction=True)

    dir_naming = None
    file_naming = None

    checkin = FileAppendCheckin(snapshot.get_code(), files_info['version_files'], files_info['files_types'],
                                keep_file_name=keep_file_name, mode=mode, source_paths=files_info['version_files'],
                                dir_naming=dir_naming, file_naming=file_naming, checkin_type='auto',
                                do_update_versionless=False)
    checkin.execute()

    files_list = checkin.get_file_objects()
    for i, fl in enumerate(files_list):
        fl.set_value(name='st_size', value=files_info['file_sizes'][i])
        fl.set_value(name='relative_dir', value=files_info['version_files_paths'][i])
        fl.set_value(name='metadata', value=json.dumps(files_info['version_metadata'][i], separators=(',', ':')))
        fl.commit()

    if update_versionless:
        snapshot.update_versionless('latest', sobject=sobject, checkin_type='auto')
        versionless_snapshot = snapshot.get_by_sobjects([sobject], context, version=-1)
        if repo_name:
            versionless_snapshot[0].set_value('repo', repo_name)
        versionless_snapshot[0].set_value('login', snapshot.get_attr_value('login'))
        versionless_snapshot[0].set_value('timestamp', snapshot.get_attr_value('timestamp'))
        versionless_snapshot[0].set_value('description', description)
        versionless_snapshot[0].commit(triggers=True, log_transaction=True)
        search = Search('sthpw/file')
        search.add_op_filters([('snapshot_code', versionless_snapshot[0].get_code())])
        file_objects = search.get_sobjects()

        for i, file_object in enumerate(file_objects):
            file_object.set_value(name='st_size', value=files_info['file_sizes'][i])
            file_object.set_value(name='project_code', value=snapshot.get_project_code())
            file_object.set_value(name='relative_dir', value=files_info['versionless_files_paths'][i])
            file_object.set_value(name='metadata', value=json.dumps(files_info['versionless_metadata'][i], separators=(',', ':')))
            file_object.set_value(name='source_path', value=files_info['versionless_files'][i])
            file_object.set_value(name='file_name', value=os.path.basename(files_info['versionless_files'][i]))
            file_object.commit()

    return str('OKEEDOKEE')

"""

# get all snapshots dicts with files dicts ver 1

import collections
from pyasm.search import Search
from pyasm.prod.service import ApiXMLRPC
xml_api = ApiXMLRPC()
search = Search('sthpw/snapshot')
filters = [('process', [u'Concept', u'Sculpt', u'Rigging', u'Hairs', u'Texturing', u'Final', u'Modeling', u'Dynamics', u'Blocking', 'icon', 'attachment', 'publish']), ('project_code', u'the_pirate'), ('search_code', [u'CHARACTERS00003', u'CHARACTERS00002', u'CHARACTERS00001'])]
search.add_op_filters(filters)
snapshots_sobjects = search.get_sobjects()

snapshots_def = collections.defaultdict(list)
files_def = collections.defaultdict(list)

for snapshot in snapshots_sobjects:
   snapshot_dict = xml_api.get_sobject_dict(snapshot)
   snapshot_files = snapshot.get_files_by_snapshots([snapshot])
   files_list = []
   for file in snapshot_files:
      files_list.append(xml_api.get_sobject_dict(file))
   snapshots_def[snapshot_dict['code']].append(snapshot_dict)
   files_def[snapshot_dict['code']].append(files_list)

return 'OK'


# get all snapshots dicts with files dicts ver 2 (Faster)

import collections
from pyasm.search import Search
from pyasm.biz import Snapshot
from pyasm.prod.service import ApiXMLRPC

xml_api = ApiXMLRPC()
search = Search('sthpw/snapshot')
filters = [('process',
            [u'Concept', u'Sculpt', u'Rigging', u'Hairs', u'Texturing', u'Final', u'Modeling', u'Dynamics',
             u'Blocking', 'icon', 'attachment', 'publish']), ('project_code', u'the_pirate'),
           ('search_code', [u'CHARACTERS00003', u'CHARACTERS00002', u'CHARACTERS00001'])]
search.add_op_filters(filters)
snapshots_sobjects = search.get_sobjects()
snapshots_files = Snapshot.get_files_dict_by_snapshots(snapshots_sobjects)

snapshots_def = collections.defaultdict(list)

for snapshot in snapshots_sobjects:
    snapshot_dict = xml_api.get_sobject_dict(snapshot, use_id=True)
    snapshot_files = snapshots_files.get(snapshot_dict['code'])
    files_list = []
    if snapshot_files:
        for file in snapshot_files:
            files_list.append(xml_api.get_sobject_dict(file, use_id=True))
    snapshot_dict['files'] = files_list
    snapshots_def[snapshot_dict['code']].append(snapshot_dict)

return snapshots_def.values()

"""

# from pyasm.biz import Snapshot
# import time
# start = time.time()
# api = server.server
# search_key = 'cgshort/props?project=portfolio&code=PROPS00012'
#
# for i in range(100):
#     sobjects = api._get_sobjects(search_key)
#     sobject = sobjects[0]
#     Snapshot.create(sobject, snapshot_type='file', context='publish', description='', is_revision=False, level_type=None, level_id=None, commit=False, version=None)
#
# end = time.time()
# return(end - start)
# 13.653764963150024 CHERRYPY


# class_name = 'tactic.ui.manager.EditElementDefinitionWdg'
#
# args = {
# 	'config_xml': '',
# 	'element_name': 'priority',
# 	'path': '/Edit/priority',
# 	'search_type': 'sthpw/task',
# 	'view': 'edit_definition',
# }
# args_array = []
# from pyasm.common import Common
# from pyasm.common import Container
# widget = Common.create_from_class_path(class_name, args_array, args)
#
# Container.put("request_top_wdg", widget)
# html = widget.get_buffer_display()
# m = Container.get_instance()
# print m.get('WidgetConfigView:display_options_cache')
# return str(m.info)
#
# #widget_html = server.get_widget(class_name, args, [])
# #return widget_html

# class_name = 'tactic.ui.panel.EditWdg'
#
# args = {
# 	'input_prefix': 'edit',
# 	'search_key': 'cgshort/scenes?project=the_pirate&id=2',
# 	'view': 'edit',
# }
# args_array = []
# from pyasm.common import Common
# from pyasm.common import Container
# widget = Common.create_from_class_path(class_name, args_array, args)
#
# Container.put("request_top_wdg", widget)
# html = widget.get_buffer_display()
# m = Container.get_instance()
# #print m.get('WidgetConfigView:display_options_cache')
# return str(m.get_data())
#
# #widget_html = server.get_widget(class_name, args, [])
# #return widget_html


# class_name = 'tactic.ui.panel.EditWdg'
#
# args = {
# 	'input_prefix': 'edit',
# 	'search_key': 'cgshort/textures?project=the_pirate&id=1',
# 	'view': 'edit',
# }
# args_array = []
# from pyasm.common import Common
# from pyasm.common import Container
# widget = Common.create_from_class_path(class_name, args_array, args)
#
# Container.put("request_top_wdg", widget)
# #widget.get_buffer_display()
# widget.explicit_display()
# m = Container.get_instance()
# return m.get_data().keys()
# #return (m.get('WidgetConfigView:display_options_cache'))
# return str(m.get("Expression:@GET(cgshort/props.name)|['cgshort/props']|[]"))
# return str(m.get("Expression:@GET(cgshort/applications_list.name)|['cgshort/applications_list']|[]"))
# return str(m.get("Expression:@GET(cgshort/applications_list.code)|['cgshort/applications_list']|[]"))
# return str(m.get("Expression:@GET(cgshort/props.name)|['cgshort/props']|[]"))
# return str(m.get("Expression:@GET(cgshort/props.code)|['cgshort/props']|[]"))
#
# widget_html = server.get_widget(class_name, args, [])
# return widget_html


# class_name = 'tactic.ui.panel.EditWdg'
#
# args = {
# 	'input_prefix': 'edit',
# 	'search_key': 'cgshort/textures?project=the_pirate&id=1',
# 	'view': 'edit',
# }
# args_array = []
# from pyasm.common import Common
# from pyasm.common import Container
# widget = Common.create_from_class_path(class_name, args_array, args)
#
# Container.put("request_top_wdg", widget)
# #widget.get_buffer_display()
# widget.explicit_display()
# edit_widgets = widget.get_widgets()
# return (edit_widgets[5].values)
# m = Container.get_instance()
# return m.get_data().keys()
# return (m.get('WidgetConfigView:display_options_cache'))
# return str(m.get("Expression:@GET(cgshort/props.name)|['cgshort/props']|[]"))
# return str(m.get("Expression:@GET(cgshort/applications_list.name)|['cgshort/applications_list']|[]"))
# return str(m.get("Expression:@GET(cgshort/applications_list.code)|['cgshort/applications_list']|[]"))
# return str(m.get("Expression:@GET(cgshort/props.name)|['cgshort/props']|[]"))
# return str(m.get("Expression:@GET(cgshort/props.code)|['cgshort/props']|[]"))
#
# widget_html = server.get_widget(class_name, args, [])
# return widget_html