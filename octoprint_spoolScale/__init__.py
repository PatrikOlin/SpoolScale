#!/usr/bin/env python3
# coding=utf-8
from __future__ import absolute_import, unicode_literals

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
from octoprint.util import RepeatedTimer
from .libs.scale import Scale

class SpoolscalePlugin(octoprint.plugin.SettingsPlugin,
                       octoprint.plugin.AssetPlugin,
		       octoprint.plugin.StartupPlugin,
                       octoprint.plugin.TemplatePlugin):

	def __init__(self):
		self.scale = Scale()
		self._checkWeightTimer = None

	def on_after_startup(self):
		self._logger.info('Spoolscale loaded (more: %s)' %self._settings.get(["spoolweight"]))
		interval = 5.0
		self.start_weight_timer(interval)

	def start_weight_timer(self, interval):
		self._checkWeightTimer = RepeatedTimer(interval, self.update_spool_weight, run_first=True)
		self._checkWeightTimer.start()

	def update_spool_weight(self):
		weight = self.scale.get_weight()
		self._plugin_manager.send_plugin_message(self._identifier, dict(spoolweight=weight))

	##~~ SettingsPlugin mixin

	def get_settings_defaults(self):
		return dict(
			spoolweight=self.scale.get_weight()
		)

	def get_template_configs(self):
		return [
			# dict(type="navbar", custom_bindings=False )
		]

	##~~ AssetPlugin mixin

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/spoolScale.js"],
		)

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
		# for details.
		return dict(
			spoolScale=dict(
				displayName="Spoolscale Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="PatrikOlin",
				repo="SpoolScale",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/PatrikOlin/SpoolScale/archive/{target_version}.zip"
			)
		)


__plugin_name__ = "Spoolscale"
__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_implementation__ = SpoolscalePlugin()
