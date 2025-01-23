import json
import subprocess
import sys
from datetime import datetime
from importlib.metadata import distributions
from importlib.resources import files
from pathlib import Path

from pydantic import BaseModel

from .exc import (
    PluginAlreadyInstalledException,
    PluginDoesNotExistException,
    PluginNotInstalledException,
)


class PluginMetadata(BaseModel):
    name: str
    pypi_package: str
    date_added: datetime
    official: bool
    description: str
    url: str
    tool_url: str
    license: str


class PackageManager(BaseModel):
    @classmethod
    def _run_pip(cls, subcommand, *args):
        command = [sys.executable, "-m", "pip", subcommand, *args, "--quiet"]
        subprocess.check_call(command)

    @classmethod
    def install_package(cls, *package_names) -> None:
        cls._run_pip("install", *package_names)

    @classmethod
    def uninstall_package(cls, *package_names) -> None:
        cls._run_pip("uninstall", *package_names, "--yes")

    @classmethod
    def list_installed_packages(cls) -> list[str]:
        installed_packages = []
        for package in distributions():
            installed_packages.append(package.metadata["Name"])
        return installed_packages


class PluginManager(BaseModel):
    available_plugin_index: dict[str, PluginMetadata] = {}
    installed_plugin_index: dict[str, PluginMetadata] = {}

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self.load_plugins_metadata()

    def load_plugins_metadata(self):
        package_dir = str(files("parsomics_cli"))
        plugins_json = (
            Path(package_dir) / Path("parsomics-registry") / Path("plugins.json")
        )
        with open(plugins_json, "r") as file:
            data = json.load(file)
            for d in data["plugins"]:
                plugin_metadata = PluginMetadata.model_validate(d)
                self.available_plugin_index[plugin_metadata.name] = plugin_metadata

    def is_plugin_installed(self, plugin_name: str):
        installed_packages = PackageManager.list_installed_packages()
        plugin_metadata = self.available_plugin_index[plugin_name]

        # Check if the plugin package is installed
        plugin_installed = False
        if plugin_metadata.pypi_package in installed_packages:
            plugin_installed = True

        return plugin_installed

    def list_plugins(self):
        installed_plugins = []
        for plugin_name in self.available_plugin_index:
            if self.is_plugin_installed(plugin_name):
                installed_plugins.append(
                    {
                        "name": plugin_name,
                        "installed": True,
                    }
                )
            else:
                installed_plugins.append(
                    {
                        "name": plugin_name,
                        "installed": False,
                    }
                )
        return installed_plugins

    def check_plugin_installable(self, plugin_name: str):
        # Raise exception if plugin does not exist
        if not plugin_name in self.available_plugin_index:
            raise PluginDoesNotExistException(plugin_name)

        # Raise exception if the plugin is already installed
        if self.is_plugin_installed(plugin_name):
            raise PluginAlreadyInstalledException(plugin_name)

    def install_plugin(self, plugin_name: str):
        # Raise exception if the plugin is not installable
        self.check_plugin_installable(plugin_name)

        plugin_metadata: PluginMetadata = self.available_plugin_index[plugin_name]
        PackageManager.install_package(plugin_metadata.pypi_package)

    def check_plugin_uninstallable(self, plugin_name: str):
        # Raise exception if plugin does not exist
        if not plugin_name in self.available_plugin_index:
            raise PluginDoesNotExistException(plugin_name)

        # Raise exception if the plugin is not installed
        if not self.is_plugin_installed(plugin_name):
            raise PluginNotInstalledException(plugin_name)

    def uninstall_plugin(self, plugin_name: str):
        # Raise exception if the plugin is not uninstallable
        self.check_plugin_uninstallable(plugin_name)

        plugin_metadata: PluginMetadata = self.available_plugin_index[plugin_name]
        PackageManager.uninstall_package(plugin_metadata.pypi_package)
