import os
import subprocess
import glob
import config
from platform import system


def dev_env():
    """
    Setting the nuke development system environments...
    """

    nuke_env = 'd:/pipeline/feature/nuke'
    python_paths = \
        [
            'd:/pipeline/feature',
            config.drive() + '/.pipeline/python/python27/lib/site-packages',
        ]

    return nuke_env, python_paths


def pipeline_env():
    """
    Setting the nuke pipeline system environments...
    """

    nuke_env = config.drive() + '.pipeline/feature/nuke'
    python_paths = \
        [
            config.drive() + '.pipeline/feature',
            config.drive() + '.pipeline/python/python27/lib/site-packages',
        ]

    return nuke_env, python_paths


def nuke_env_setter(script='', dev=False):
    """
    Nuke environment setter, set the pipeline setting to
    allow nuke to launcher with pipeline python scripts
    system environments...
    """

    nuke_env, env = dev_env() if dev else pipeline_env()

    if system() == 'Windows':
        env = ';'.join(env)
        nuke_glob_expr = 'C:/Program Files/Nuke*/Nuke*.exe'
        nuke_path_list = glob.glob(nuke_glob_expr)

        if isinstance(script, list):
            script = ' '.join(script)

        cmd = '"{}" --nukex {}'.format(nuke_path_list[-1], script)

    elif system() == 'Darwin':
        env = ':'.join(env)
        nuke_glob_expr = '/Applications/Nuke*/NukeX*.app/Nuke*'
        nuke_path_list = filter(lambda x: 'Non' not in x, glob.glob(nuke_glob_expr))

        if isinstance(script, str):
            cmd = [nuke_path_list[-1], '--nukex', script]

        else:
            cmd = [nuke_path_list[-1], '--nukex'] + script

    elif system() == 'Linux':
        env = ':'.join(env)
        nuke_glob_expr = '/usr/local/Nuke*/Nuke*'
        nuke_path_list = glob.glob(nuke_glob_expr)

        if isinstance(script, str):
            script = [script]

        cmd = [nuke_path_list[-1], '--nukex'] + script

    else:
        return 0

    os.environ['NUKE_PATH'] = nuke_env
    os.environ['PYTHONPATH'] = env
    p = subprocess.Popen(cmd)

    return p


if __name__ == '__main__':
    nuke_env_setter(dev=True)


