import nuke
import os
import re
import glob
import global_functions as gf
import config

n = nuke.menu('Nuke').addMenu('Mr. Wolf Tools')
n.addCommand('-', '-')
n.addCommand('Publish', 'nuke_quick_scripts.set_write_file_path()')
n.addCommand('-', '-')
n.addCommand('Open File Directory', 'nuke_quick_scripts.open_file_directory()', 'shift+e')
n.addCommand('Load File Path', 'nuke_quick_scripts.load_file_knob()', 'shift+r')
n.addCommand('-', '-')
n.addCommand('Reload Read Nodes', 'nuke_quick_scripts.reload_read_nodes()')
n.addCommand('Reset Viewers', 'nuke_quick_scripts.reset_viewer()', 'alt+q')
n.addCommand('Custom Framehold', 'nuke_quick_scripts.frame_hold()', 'shift+f')
n.addCommand('Custom Shuffle', 'nuke_quick_scripts.smart_shuffle()', '`')
n.addCommand('-', '-')
n.addCommand('Increment Save', 'nuke_quick_scripts.NukeVersionUp().nuke()', 'alt+shift+s')
n.addCommand('Create Read From Write', 'nuke_quick_scripts.read_from_write()', 'alt+r')
n.addCommand('Precomp Write Node', 'nuke_quick_scripts.pre_comp_write()', 'alt+f2')


def frame_hold():
    frame = nuke.frame()
    sel = nuke.selectedNodes()

    if sel:
        frame_hold_node = nuke.nodes.FrameHold()
        frame_hold_node.setInput(0,sel[-1])
        frame_hold_node['first_frame'].setValue(float(frame))
        [x.setSelected(False) for x in nuke.selectedNodes()]
        frame_hold_node['selected'].setValue(True)
        [x.setInput(z, frame_hold_node)for x in sel[-1].dependent() for z in range(x.inputs()) if x.input(z) == sel[-1]]
    else:
        frame_hold_node = nuke.createNode('FrameHold', 'first_frame %s' % frame)

    return frame_hold_node


def set_write_file_path():
    base_file = os.path.basename(nuke.Root().name())

    final_render_path = 'Z:/JOBS/{project}/{episode}/comp/_dailies/{shot_code}/{shot_code}_comp_{version}/{shot_code}_comp_{version}.%04d.dpx'
    edit_render_path = 'Z:/JOBS/{project}/{episode}/comp/_dailies/{shot_code}/{shot_code}_comp_{version}_lut_DNxHD.mov'
    h264_render_path = 'Z:/JOBS/{project}/{episode}/comp/_dailies/{shot_code}/{shot_code}_comp_{version}_lut_H264.mov'

    shot_code = base_file.rsplit('_', 2)[0]
    show, episode, seq, shot, task, version = gf.split_shot_code(base_file)[:6]
    version = 'v' + re.findall(pattern='\d+', string=version)[0]

    project = config.show_schema.get(show)

    final_render_path = final_render_path.format(project=project, episode=episode, shot_code=shot_code, version=version)
    edit_render_path = edit_render_path.format(project=project, episode=episode, shot_code=shot_code, version=version)
    h264_render_path = h264_render_path.format(project=project, episode=episode, shot_code=shot_code, version=version)

    nuke.toNode('FINAL')['file'].setValue(final_render_path)
    nuke.toNode('EDITORIAL_QT')['file'].setValue(edit_render_path)
    nuke.toNode('PRODUCER_QT')['file'].setValue(h264_render_path)


def reset_viewer():
    last_node_pos = sorted([(x.ypos(), x) for x in nuke.allNodes() if x.Class() != 'Viewer'])
    if last_node_pos:
        ypos, xpos = last_node_pos[-1][0] + 500, last_node_pos[-1][1].xpos()
    else:
        ypos, xpos = 0, 0

    for i, x in enumerate(nuke.allNodes('Viewer')):
        x['channels'].setValue('rgba')
        x.setXYpos(xpos, ypos + (50 * i))


def open_file_directory():
    """
        Quick script to open the folder location of nuke nodes that have a file knob
        :return: No return value
    """

    try:
        # Find nuke file path and open os window
        sel = nuke.selectedNode()
        file_path = None

        if sel.knob('file'):
            file_path = os.path.abspath(sel['file'].getValue())

        elif sel.knob('vfield_file'):
            file_path = sel['vfield_file'].getValue().replace('\\', '/')

        if file_path:
            folder_directory = os.path.dirname(file_path)
            os.startfile(folder_directory)

    except NameError:
        nuke.message('Node doesnt have a file path...')

    except ValueError:
        nuke.message('Please select a node with a file path...')

    except WindowsError:
        nuke.message('Folder Directory doesnt exist...')


def reload_read_nodes():
    for x in nuke.allNodes('Read'):
        x.setSelected(True)
        x['reload'].execute()


class NukeVersionUp(object):
    """
        Increments nuke script version and write nodes file paths...
        """
    pattern = r'(v\d{3})'

    def nuke(self):
        nuke_script_path = nuke.root().name()
        nuke.scriptSaveAs(self.increment_version(nuke_script_path))

        for write_node in nuke.allNodes('Write'):
            write_file_path = write_node['file'].getValue()
            write_node['file'].setValue(self.increment_version(write_file_path))

    def increment_version(self, file_path):
        dir_path, base_name = os.path.split(file_path)
        old_version = re.findall(pattern=self.pattern, string=base_name)

        if old_version:
            new_version = int(old_version[0][1:]) + 1
            new_version = 'v{:03d}'.format(new_version)

            new_file_path = os.path.join(dir_path, base_name).replace('\\', '/').replace(old_version[0], new_version)
            return new_file_path
        else:
            return file_path


def read_from_write():
    try:
        write_node = nuke.selectedNode()
        if write_node.Class() != 'Write':
            nuke.message('Please selected a write node')
            return False

        file_path = write_node['file'].getValue()
        x_pos, y_pos = write_node.xpos(), write_node.ypos()
        colorspace = write_node['colorspace'].getValue()

        if file_path.endswith('.mov') and os.path.exists(file_path):
            read_node = nuke.nodes.Read(xpos=x_pos, ypos=y_pos + 100)
            read_node['file'].fromUserText(file_path)

        else:
            glob_expression = file_path.replace('%04d', '*')
            frame_list = [v.rsplit('.', 2)[-2] for v in glob.glob(glob_expression)]
            min_frame, max_frame = min(frame_list), max(frame_list)

            read_node = nuke.nodes.Read(xpos=x_pos, ypos=y_pos + 100, file=file_path, first=min_frame, last=max_frame)
            read_node['colorspace'].setValue(int(colorspace))
        return read_node

    except ValueError:
        nuke.message('Error creating read from write...')
        pass


def pre_comp_write():
    """
    Create a pre comp write node based off user name input
    :return: Write node
    """
    try:
        name = nuke.getInput('Please state the name of the precomp render?')
        name = ''.join(['_' if x is ' ' else x for x in name])

        nuke_root_path = nuke.root().name()
        if nuke_root_path == 'Root':
            nuke.message('Please save nuke scene in a project directory...')
            return False

        shot_base_dir = nuke_root_path.split('comp/scripts', 1)[0]
        render_file_path = '{}precomp/{name}/{name}.%04d.exr'.format(shot_base_dir, name=name)

        pre_comp_node = nuke.createNode('Write', 'name {}_precomp channels all'.format(name))
        pre_comp_node['create_directories'].setValue(1), pre_comp_node['file'].setValue(render_file_path)
        return pre_comp_node

    except TypeError:
        nuke.message('No input entered...')
        return False


def load_file_knob():
    """
    Quick function to load the node file path for quick playback...

    """

    try:
        sel_file_path = nuke.selectedNode()['file'].getValue()

        if os.path.exists(sel_file_path):
            os.startfile(sel_file_path)

        else:
            dir_name = os.path.dirname(sel_file_path)
            dir_list = os.listdir(dir_name)
            sel_file_path = os.path.join(dir_name, dir_list[0])
            os.startfile(sel_file_path)

    except NameError:
        nuke.message('Could not find a file path on selected node, please selected the correct node!')

    except (WindowsError, IndexError):
        nuke.message('Error locating file path, please check file path!')

    return 1


def smart_shuffle():
    # Find active viewer and assign current layer
    active_viewer = nuke.activeViewer()
    if active_viewer:
        layer = active_viewer.node()['channels'].value()
    else:
        layer = 'rgba'

    # Create Shuffle Node with active layer
    shuffle_node = nuke.createNode('Shuffle', 'in {}'.format(layer))
    if layer != 'rgba':
        shuffle_node['alpha'].setValue(0)

