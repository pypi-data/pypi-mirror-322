from typing import Optional, Union, Iterable, Dict, overload
import re
import os
import shutil
from zipfile import ZipFile
from .type import Data


class ZipDirname(str): ...
class ZipFilename(str): ...


_suffix_pattern = r'(?P<suffix>\.(?:[a-zA-Z0-9]+)(?:\.(?=[a-zA-Z0-9]*(?=.*[a-zA-Z]))[a-zA-Z0-9]+)*)$'
def filename_suffix(filename):
    match = re.search(_suffix_pattern, filename)
    if match is not None:
        suffix = match.group('suffix')
        if suffix is None:
            suffix = ''
    else:
        suffix = ''
    return suffix


def _get_zip_filelist_with_dirname(zip_file: ZipFile, dirname):
    for file in zip_file.filelist:
        filename = file.filename
        if filename.startswith(dirname):
            filename = filename[len(dirname):]
            if filename == '/':
                continue
            else:
                filename = filename[1:]
        else:
            continue
        yield file.is_dir(), filename


def iterdir(zip_file: ZipFile, dirname: str = ''):
    if dirname is None or dirname == '':
        filelist_iter = ((file.is_dir(), file.filename) for file in zip_file.filelist)
    else:
        filelist_iter = _get_zip_filelist_with_dirname(zip_file, dirname)
    for is_dir, filename in filelist_iter:
        if is_dir:
            yield ZipDirname(filename[:-1])
        elif '/' not in filename:
            yield ZipFilename(filename)


def listdir(zip_file: ZipFile, dirname: str = ''):
    return list(iterdir(zip_file, dirname))


def extract(zip_file: ZipFile, src: str, dst: str, password: Optional[str] = None):
    with zip_file.open(src, pwd=password) as source, open(dst, "wb") as target:
        shutil.copyfileobj(source, target)


def extract_to(zip_file: ZipFile, src: str, dir: str, password: Optional[str] = None):
    dst = os.path.join(dir, os.path.basename(src))
    extract(zip_file, src, dst, password)


def write_data(zip_file: ZipFile, src: str, data: Data):
    return zip_file.writestr(src, data)


def _replace_map(zip_file: ZipFile, replacement: Dict[str, Data]):
    filename = zip_file.filename
    suffix = filename_suffix(filename)
    prefix = filename[:-len(suffix)]
    temp_filename = f'{prefix}_temp{suffix}'
    with ZipFile(temp_filename, 'w', compression=zip_file.compression, compresslevel=zip_file.compresslevel) as temp_zip:
        for file_path in zip_file.namelist():
            to_be_replaced = replacement.get(file_path)
            if to_be_replaced is None:
                with zip_file.open(file_path) as f:
                    temp_zip.writestr(file_path, f.read())
            else:
                temp_zip.writestr(file_path, to_be_replaced)
        temp_zip.setpassword(zip_file.pwd)
    zip_file.close()
    os.remove(filename)
    os.rename(temp_filename, filename)
    zip_file.open(filename, zip_file.mode, zip_file.pwd)
    


def _replace_list(zip_file: ZipFile, path: Union[str, Iterable[str]], data: Union[Data, Iterable[Data]]):
    if isinstance(path, str):
        path = [path]
        data = [data]
    replacement = {file_path : content for file_path, content in zip(path, data)}  
    _replace_map(zip_file, replacement)


@overload
def replace(zip_file: ZipFile, replacement: Dict[str, Data]):
    ...


@overload
def replace(zip_file: ZipFile, path: Union[str, Iterable[str]], data: Union[Data, Iterable[Data]]):
    ...


def replace(zip_file: ZipFile, *args, **kwargs):
    replacement = kwargs.get('replacement')
    path = kwargs.get('path')
    if path is None:
        if replacement is None:
            args_length = len(args)
            if args_length == 1:
                if isinstance(args[0], Dict):
                    func = _replace_map
                else:
                    func = _replace_list
            elif args_length == 2:
                func = _replace_list
            else:
                if isinstance(args[0], Dict):
                    func = _replace_map
                else:
                    func = _replace_list
        else:
            func = _replace_map
    else:
        func = _replace_list
    return func(zip_file, *args, **kwargs)