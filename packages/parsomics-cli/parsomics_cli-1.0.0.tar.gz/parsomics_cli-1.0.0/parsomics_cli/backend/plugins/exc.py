class PluginManagerException(Exception):
    pass


class PluginDoesNotExistException(PluginManagerException):
    def __init__(self, plugin_name: str):
        message = f'plugin "{plugin_name}" does not exist'
        super().__init__(message)


class PluginAlreadyInstalledException(PluginManagerException):
    def __init__(self, plugin_name: str):
        message = f'plugin "{plugin_name}" is already installed'
        super().__init__(message)


class PluginNotInstalledException(PluginManagerException):
    def __init__(self, plugin_name: str):
        message = f"plugin {plugin_name} is not installed"
        super().__init__(message)
