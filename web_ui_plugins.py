import os
import datetime
import gossip
from flask import request, abort, render_template_string
from flaskext.markdown import Markdown
from bson.json_util import dumps
from eva.config import save_config
import eva.util
from eva.plugin import plugin_enabled, \
                       get_plugin_directory, \
                       get_downloadable_plugins, \
                       refresh_downloadable_plugins, \
                       download_plugin
from eva import conf
from eva import log

dir_path = os.path.dirname(os.path.realpath(__file__))
plugins_markup = open(dir_path + '/templates/plugins.html').read()
configuration_markup = open(dir_path + '/templates/configuration.html').read()

@gossip.register('eva.web_ui.start', provides=['web_ui_plugins'])
def web_ui_start(app):
    Markdown(app, extensions=['codehilite', 'fenced_code'])
    app.add_url_rule('/plugins', 'plugins', plugins)
    app.add_url_rule('/plugins/save', 'plugins_save', plugins_save, methods=["POST"])
    app.add_url_rule('/plugins/configuration/<plugin_id>', 'plugin_edit', plugin_edit)
    app.add_url_rule('/plugins/configuration/<plugin_id>', 'plugin_save', plugin_save, methods=["POST"])
    app.add_url_rule('/plugins/download', 'plugins_download', plugins_download, methods=["POST"])
    app.add_url_rule('/plugins/download/<plugin_id>', 'plugin_download', plugin_download)

@gossip.register('eva.web_ui.menu_items', needs=['web_ui'], provides=['web_ui_plugins'])
def web_ui_menu_items(menu_items):
    menu_item = {'path': '/plugins', 'title': 'Plugins'}
    menu_items.append(menu_item)

def get_plugins_table_columns():
    plugins_cols = ['Enabled', 'Name', 'Description', 'Version', 'Dependencies', 'Settings']
    gossip.trigger('eva.web_ui_plugins.plugins_columns', plugins_cols=plugins_cols)
    return plugins_cols

def get_plugins_table_rows():
    rows = []
    for plugin_id in sorted(conf['plugins']):
        row_data = [get_enabled_markup(plugin_id),
                       conf['plugins'][plugin_id]['info']['name'],
                       conf['plugins'][plugin_id]['info']['description'],
                       conf['plugins'][plugin_id]['info']['version'],
                       ', '.join(conf['plugins'][plugin_id]['info']['dependencies']),
                       get_actions_markup(plugin_id)]
        gossip.trigger('eva.web_ui_plugins.plugins_row', plugin_id=plugin_id, row_data=row_data)
        rows.append(row_data)
    gossip.trigger('eva.web_ui_plugins.plugins_rows', rows=rows)
    return rows

def get_available_table_columns():
    cols = ['Downloaded', 'Name', 'Description', 'Code']
    gossip.trigger('eva.web_ui_plugins.available_columns', cols=cols)
    return cols

def get_available_table_rows():
    rows = []
    # Get list of downloadable plugins (don't pull repo if already cloned).
    downloadable_plugins = get_downloadable_plugins(False)
    for plugin_id in sorted(downloadable_plugins.keys()):
        plugin_data = downloadable_plugins[plugin_id]
        row_data = [get_downloaded_markup(plugin_id),
                    plugin_data['name'],
                    plugin_data['description'],
                    get_code_markup(plugin_data['url'])]
        gossip.trigger('eva.web_ui_plugins.available_row', plugin_id=plugin_id, row_data=row_data)
        rows.append(row_data)
    gossip.trigger('eva.web_ui_plugins.available_rows', rows=rows)
    return rows

def get_downloaded_markup(plugin_id):
    markup = '<div class="checkbox"><label>'
    if plugin_id in conf['plugins']:
        markup += '<input type="checkbox" checked name="downloaded[]" value="%s">' %plugin_id
    else:
        markup += '<input type="checkbox" name="downloaded[]" value="%s">' %plugin_id
    markup += '</label></div>'
    return markup

def get_code_markup(plugin_url):
    return '<a href="%s" class="btn btn-primary" target="_blank">View</a>' %plugin_url

def get_download_markup(plugin_id):
    return '<a href="/plugins/download/%s" class="btn btn-success">Download</a>' %plugin_id

def get_enabled_markup(plugin_id):
    markup = '<div class="checkbox"><label>'
    if plugin_enabled(plugin_id):
        markup += '<input type="checkbox" checked name="enabled[]" value="%s">' %plugin_id
    else:
        markup += '<input type="checkbox" name="enabled[]" value="%s">' %plugin_id
    markup += '</label></div>'
    return markup

def get_actions_markup(plugin_id):
    actions_markup = ['<a class="btn btn-primary" href="/plugins/configuration/%s">Config</a>' %plugin_id]
    gossip.trigger('eva.web_ui_plugins.pre_actions_markup',
                   plugin_id=plugin_id,
                   actions_markup=actions_markup)
    return ''.join(actions_markup)

def get_pre_plugins_table_markup():
    pre_plugins_table_markup = []
    gossip.trigger('eva.web_ui_plugins.pre_plugins_table_markup', pre_plugins_table_markup=pre_plugins_table_markup)
    return ''.join(pre_plugins_table_markup)

def get_post_plugins_table_markup():
    post_plugins_table_markup = []
    gossip.trigger('eva.web_ui_plugins.post_plugins_table_markup', post_plugins_table_markup=post_plugins_table_markup)
    return ''.join(post_plugins_table_markup)

def get_pre_available_table_markup():
    pre_available_table_markup = []
    gossip.trigger('eva.web_ui_plugins.pre_available_table_markup', pre_available_table_markup=pre_available_table_markup)
    return ''.join(pre_available_table_markup)

def get_post_available_table_markup():
    post_available_table_markup = []
    gossip.trigger('eva.web_ui_plugins.post_available_table_markup', post_available_table_markup=post_available_table_markup)
    return ''.join(post_available_table_markup)

def plugins():
    menu_items = []
    gossip.trigger('eva.web_ui.menu_items', menu_items=menu_items)
    pre_plugins_table_markup = get_pre_plugins_table_markup()
    plugins_table_columns = get_plugins_table_columns()
    plugins_table_rows = get_plugins_table_rows()
    post_plugins_table_markup = get_post_plugins_table_markup()
    pre_available_table_markup = get_pre_available_table_markup()
    available_table_columns = get_available_table_columns()
    available_table_rows = get_available_table_rows()
    post_available_table_markup = get_post_available_table_markup()
    return render_template_string(plugins_markup,
                                  menu_items=menu_items,
                                  pre_plugins_table_markup=pre_plugins_table_markup,
                                  plugins_table_columns=plugins_table_columns,
                                  plugins_table_rows=plugins_table_rows,
                                  post_plugins_table_markup=post_plugins_table_markup,
                                  pre_available_table_markup=pre_available_table_markup,
                                  available_table_columns=available_table_columns,
                                  available_table_rows=available_table_rows,
                                  post_available_table_markup=post_available_table_markup)

def plugins_save():
    # Save new configs.
    enabled_plugins = request.form.getlist('enabled[]')
    conf['eva']['enabled_plugins'] = enabled_plugins
    save_config(section='eva')
    return conf['plugins']['web_ui']['module'].restart_page()

def plugin_edit(plugin_id):
    if plugin_id not in conf['plugins']: abort(404)
    plugin = conf['plugins'][plugin_id]
    plugin['id'] = plugin_id
    options = []
    for option in conf['plugins'][plugin_id]['config']:
        value = conf['plugins'][plugin_id]['config'][option]
        data = {'name': option, 'value': value, 'input_type': get_input_type(value)}
        options.append(data)
    # Get README.md file content.
    readme_markdown = ''
    for readme_path in [plugin['path'] + '/README.md', plugin['path'] + '/README']:
        if os.path.exists(readme_path):
            md_file = open(readme_path)
            readme_markdown = md_file.read()
            md_file.close()
            break
    menu_items = []
    gossip.trigger('eva.web_ui.menu_items', menu_items=menu_items)
    return render_template_string(configuration_markup,
                                  menu_items=menu_items,
                                  plugin=plugin,
                                  options=options,
                                  readme_markdown=readme_markdown)

def get_input_type(value):
    if isinstance(value, bool): return 'radio'
    else: return 'textfield'

def plugin_save(plugin_id):
    if plugin_id not in conf['plugins']: abort(404)
    plugin = conf['plugins'][plugin_id]
    # Update the conf singleton.
    for configuration in request.form:
        current_value = conf['plugins'][plugin_id]['config'][configuration]
        new_value = request.form[configuration]
        input_type = get_input_type(current_value)
        if input_type == 'radio': new_value = bool(int(new_value))
        conf['plugins'][plugin_id]['config'][configuration] = new_value
    # Persist the conf singleton to disk.
    save_config(plugin_id=plugin_id)
    return conf['plugins']['web_ui']['module'].restart_page()

def plugin_download(plugin_id):
    downloadable_plugins = get_downloadable_plugins(False)
    if plugin_id not in downloadable_plugins.keys(): abort(404)
    destination = get_plugin_directory() + '/' + plugin_id
    try:
        download_plugin(plugin_id, destination)
        return conf['plugins']['web_ui']['module'].restart_page()
    except:
        abort(404)

def plugins_download():
    downloaded = request.form.getlist('downloaded[]')
    for to_download in downloaded:
        if to_download in conf['plugins']: continue
        destination = get_plugin_directory() + '/' + to_download
        try: download_plugin(to_download, destination)
        except: pass
    refresh_downloadable_plugins()
    return conf['plugins']['web_ui']['module'].restart_page()
