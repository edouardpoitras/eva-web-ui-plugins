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

Once installed, you will see a new tab in the Web UI called `Plugins`.
On that page you will see some action buttons and two tables.

#### Check For Updates button

This button fires a job in the background that will check all plugins for updates.
If a plugin requires an update, it will appear in the `Plugins` table (this could take a few minutes depending on the number of plugins to check and your internet connection).

#### Undo Last Update button

This button is used when the user wishes to un-do the previous update.

NOTE: As of version 0.1.0, This only works for the last applied update - you can't undo more than one update at a time.

#### Plugins table

Lists all the plugins that have been downloaded and are available to be enabled/disabled or configured.
You should see information such as the plugin name, description, current version, dependency, and status.

You should see a `Config` button for every plugin in order to change it's settings, and an `Update` button will appear when new updates are available.

You can enable/disable plugins by checking/unchecking them from the list and hitting the `Save` button below.

#### Available table

Lists all plugins that are available to be downloaded from the plugin repository configured.
The default plugin repository is the public [Eva Plugin Repository](https://github.com/edouardpoitras/eva-plugin-repository).

The plugin repository used can be set in the `eva.conf` file under the `plugin_repository` name.

You can download plugins by checking them and hitting the `Download` button bellow.
You can also view the individual plugin repositories by clicking the `View` buttons in the table.

## Configuration

None
