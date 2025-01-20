import sys
import os
import subprocess
import requests
import tempfile


_sys_path_command = """
import sys
print('\\0'.join(sys.path))
"""
_sys_paths = {sys.executable : sys.path}
def _get_sys_path(executable):
    sys_path = _sys_paths.get(executable)
    if sys_path is None:
        sys_path = subprocess.run([executable, '-c', _sys_path_command], check=True, capture_output=True, text=True).stdout[:-1].split('\0')
        _sys_paths[executable] = sys_path
    return sys_path


def make_install_command(name, executable = sys.executable):
    return [executable, '-m', 'pip', 'install', name]


def install(name, executable = sys.executable, hide_output = False):
    subprocess.run(make_install_command(name, executable), check=True, capture_output=hide_output)


def make_uninstall_command(name, executable = sys.executable):
    return [executable, '-m', 'pip', 'uninstall', '-y', name]


def uninstall(name, executable = sys.executable, hide_output = False):
    subprocess.run(make_uninstall_command(name, executable), check=True, capture_output=hide_output)


try:
    import warnings
    warnings.filterwarnings('ignore', category=UserWarning, module='_distutils_hack')
    from pip._internal.metadata import get_environment
    from pip._vendor.packaging.utils import canonicalize_name
    warnings.filterwarnings('default', category=UserWarning, module='_distutils_hack')
    
    
    def exist(name, executable = sys.executable):
        env = get_environment(_get_sys_path(executable))
        installed = {dist.canonical_name: dist for dist in env.iter_all_distributions()}
        query_name = canonicalize_name(name)
        return query_name in installed
except ModuleNotFoundError:
    def exist(name, executable = sys.executable):
        try:
            subprocess.run([executable, '-m', 'pip', 'show', name], check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False


def _temp_walk(kind):
    temp_dir = tempfile.gettempdir()
    for root, dirs, filenames in os.walk(temp_dir):
        for dir_name in dirs:
            if dir_name.startswith(f"pip-{kind}-"):
                yield os.path.join(root, dir_name), filenames


def tempdirs(kind):
    return [dir_path for dir_path, _ in _temp_walk(kind)]


def find_temp_file_path(kind, filename):
    for dir_path, filenames in _temp_walk(kind):
        if filename in filenames:
            return os.path.join(dir_path, filename)


def config_get(key, scope = 'global', executable = sys.executable):
    try:
        process = subprocess.run([executable, '-m', 'pip', 'config', 'get', f'{scope}.{key}'], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError:
        return None
    return process.stdout[:-1]


def config_set(key, value, scope = 'global', executable = sys.executable):
    subprocess.run([executable, '-m', 'pip', 'config', 'set', f'{scope}.{key}', value], capture_output=True)


def config_unset(key, scope = 'global', executable = sys.executable):
    subprocess.run([executable, '-m', 'pip', 'config', 'unset', f'{scope}.{key}'], capture_output=True)


def get_cache_dir(executable = sys.executable):
    return subprocess.run([executable, '-m', 'pip', 'cache', 'dir'], capture_output=True, text=True).stdout[:-1]


def get_latest_version(package_name):
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        latest_version = data['info']['version']
        return latest_version
    return None