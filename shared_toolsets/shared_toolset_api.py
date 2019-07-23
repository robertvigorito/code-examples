# import nuke
# import nukescripts
import os
import scandir
import nuke

VERSION = nuke.NUKE_VERSION_STRING
PLUGIN_PATHS = nuke.pluginPath()


def find_toolset_path():
    """
    Look through the nuke plugin path and find the base folder
    directory of the assigned toolset directory....

    :return: base toolset path
    """

    for path in PLUGIN_PATHS:
        toolset_dir = os.path.join(path, 'ToolSets').replace('\\', '/')

        if not os.path.exists(toolset_dir) or VERSION in toolset_dir:
            continue

        for base, folder, files in scandir.walk(toolset_dir):
            yield base


def refresh_toolset():
    """
    Refresh nukes default toolset and new create menu and
    refresh item...

    :return:
    """
    import nukescripts
    nukescripts.toolsets.refreshToolsetsMenu()

    m = nuke.menu('Nodes').addMenu('ToolSets')
    m.addCommand('Create', 'shared_toolsets.create_ui.run()', 'ToolsetCreate.png')
    m.addCommand('Refresh', 'shared_toolsets.api.refresh_toolset()')
    m.addCommand('Custom Delete', 'shared_toolsets.delete_ui.run()')
