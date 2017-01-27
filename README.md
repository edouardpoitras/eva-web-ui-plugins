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

Note that this will result in only the web_ui_plugins and it's dependencies being enabled on next Eva boot.

## Configuration

None
