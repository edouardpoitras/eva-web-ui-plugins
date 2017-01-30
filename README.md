Web UI Plugins
==============

An Eva plugin to allow the configuration and management of Eva plugins though the [Eva Web UI](https://github.com/edouardpoitras/eva-web-ui).

## Installation

Web UI Plugins is installed by default on Eva's first boot. This is to facilitate the installation of other plugins in the Web UI.

If you wish to install it manually, simply edit your `eva.conf` file and add `web_ui_plugins` to the list of enabled plugins.

You can find the configuration file in any of the following locations:

* ~/eva.conf
* ~/.eva.conf
* ~/eva/eva.conf
* /etc/eva.conf
* /etc/eva/eva.conf

If you can't find the `eva.conf` file, simply create it in one of the locations mentioned above and add the following content:

    [eva]
    enabled_plugins = web_ui_plugins

NOTE: This will result in only the `web_ui_plugins` and it's dependencies being enabled on next Eva boot.

## Usage

Once installed, you will see a new menu item in the Web UI called `Plugins`.
On that page you will see two tables.

#### Plugins table

Lists all the plugins that have been downloaded and are available to be enabled/disabled or configured.
You should see information such as the plugin name, description, current version, and dependencies.

You should also see a `Config` button for every plugin, which will allow you to change plugin settings and view the README.md file for that plugin from inside the Web UI (if it exists).

You can enable/disable plugins by checking/unchecking them from the list and hitting the `Save` button below.

#### Available table

Lists all plugins that are available to be downloaded from the plugin repository configured.
The default plugin repository is the public [Eva Plugin Repository](https://github.com/edouardpoitras/eva-plugin-repository).

The plugin repository used can be set in the `eva.conf` file under the `plugin_repository` name.

You can download plugins by checking them and hitting the `Download` button bellow.
You can also view the individual plugin repositories by clicking the `View` buttons in the table.

## Developers

#### Triggers

The Web UI Plugins fires a few triggers to allow other plugins to alter the data in will display to ther user on the `/plugins` page.

`gossip.trigger('eva.web_ui_plugins.plugins_columns', plugins_cols=plugins_cols)`

This trigger is fired before sending the column data to the `plugins.html` template.
Other plugins should register to this trigger if they wish to add/remove columns from the `Plugins` table at `/plugins`.

Here's an example of a plugin adding a column to display the plugin path on disk:

```python
@gossip.register('eva.web_ui_plugins.plugins_columns')
def web_ui_plugins_columns(plugins_cols):
    plugins_cols.append('Plugin Path')
```

`gossip.trigger('eva.web_ui_plugins.plugins_row', plugin_id=plugin_id, row_data=row_data)`

Similar to the `eva.web_ui_plugins.plugins_columns` trigger except that it fires for every row in the table.
This would be used to fill in the column that was added in the `eva.web_ui_plugins.plugins_columns` trigger.

```python
@gossip.register('eva.web_ui_plugins.plugins_row')
def web_ui_plugins_row(plugin_id, row_data):
    """
    You need to have imported the conf array for this to work:
        from eva import conf
    """
    path = conf['plugins'][plugin_id]['info']['path']
    row_data.append(path)
```

`gossip.trigger('eva.web_ui_plugins.plugins_rows', rows=rows)`

Allows for one last chance at altering all of the rows of the `Plugins` table before being rendered in the template. Differs from `eva.web_ui_plugins.plugins_row` trigger in that it fires only once when the table is ready to be rendered (not on every row).

`gossip.trigger('eva.web_ui_plugins.available_columns', cols=cols)`

Same as `eva.web_ui_plugins.plugins_columns` trigger but alters the `Available` plugins table columns instead.

`gossip.trigger('eva.web_ui_plugins.available_row', plugin_id=plugin_id, row_data=row_data)`

Same as `eva.web_ui_plugins.plugins_row` trigger but alters individual `Available` plugins table rows instead.

`gossip.trigger('eva.web_ui_plugins.available_rows', rows=rows)`

Same as `eva.web_ui_plugins.plugins_rows` trigger but alters all `Available` plugins table rows instead.

`gossip.trigger('eva.web_ui_plugins.pre_plugins_table_markup', pre_plugins_table_markup=pre_plugins_table_markup)`

This trigger is fired in order to allow other plugins to insert HTML before the `Plugins` table.
The `pre_plugins_table_markup` variable is a list of HTML markup strings to which you can add items.

`gossip.trigger('eva.web_ui_plugins.post_plugins_table_markup', post_plugins_table_markup=post_plugins_table_markup)`

This trigger is fired in order to allow other plugins to insert HTML after the `Plugins` table.
The `post_plugins_table_markup` variable is a list of HTML markup strings to which you can add items.

`gossip.trigger('eva.web_ui_plugins.pre_available_table_markup', pre_available_table_markup=pre_available_table_markup)`

Same as `eva.web_ui_plugins.pre_plugins_table_markup` trigger but inserts before the `Available` plugins table instead.

`gossip.trigger('eva.web_ui_plugins.post_available_table_markup', post_available_table_markup=post_available_table_markup)`

Same as `eva.web_ui_plugins.post_plugins_table_markup` trigger but inserts before the `Available` plugins table instead.

## Configuration

None
