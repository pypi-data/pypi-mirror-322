from dataclasses import dataclass
from importlib import metadata
import os
import pathlib
from shutil import rmtree
from typing import List, Literal, Optional, Union
import time

def get_version() -> str:
    try:
        version = metadata.version('dmri-dicelib')
    except metadata.PackageNotFoundError:
        version = 'not installed'
    return version

FileType = Literal['input', 'output']
@dataclass
class File:
    """File dataclass"""
    name: str
    type_: FileType
    path: pathlib.Path
    ext: Optional[Union[str, List[str]]] = None

    def __init__(self, name: str, type_: FileType, path: str, ext: Optional[Union[str, List[str]]] = None):
        self.name = name
        self.type_ = type_
        self.path = pathlib.Path(path)
        self.ext = ext

@dataclass
class Dir:
    """Dir dataclass"""
    name: str
    path: str

@dataclass
class Num:
    """Num dataclass"""
    name: str
    value: Union[int, float]
    min_: Optional[Union[int, float]] = None
    max_: Optional[Union[int, float]] = None
    include_min: Optional[bool] = True
    include_max: Optional[bool] = True
    
def check_params(files: Optional[List[File]]=None, dirs: Optional[List[Dir]]=None, nums: Optional[List[Num]]=None, force: bool=False):
    from dicelib.ui import setup_logger
    logger = setup_logger('utils')
    
    # files
    if files is not None:
        for file in files:
            if file.ext is not None:
                if isinstance(file.ext, str):
                    file.ext = [file.ext]
                suffixes = pathlib.Path(file.path).suffixes
                if len(suffixes) == 0:
                    logger.error(f'No extension for {file.name} file \'{file.path}\', must be {file.ext}')
                elif len(suffixes) > 1:
                    if suffixes[-1] == '.gz':
                        suffixes = suffixes[-2:]
                    else:
                        suffixes = suffixes[-1]
                suffix = ''.join(suffixes)
                if suffix not in file.ext or suffix == '':
                    exts = ' | '.join(file.ext)
                    logger.error(f'Invalid extension for {file.name} file \'{file.path}\', must be {exts}')
            if file.type_ == 'input':
                if not os.path.isfile(file.path):
                    logger.error(f'{file.name} file \'{file.path}\' not found')
            elif file.type_ == 'output':
                if force:
                    if os.path.isfile(file.path):
                        os.remove(file.path)
                else:
                    if os.path.isfile(file.path):
                        logger.error(f'{file.name} file \'{file.path}\' already exists, use --force to overwrite')

    # dirs
    if dirs is not None:
        for dir in dirs:
            if os.path.isdir(dir.path) and not force:
                logger.error(f'{dir.name} folder \'{dir.path}\' already exists, use --force to overwrite')

    # numeric
    if nums is not None:
        for num in nums:
            if num.min_ is not None and num.max_ is not None:
                if num.include_min and num.include_max:
                    if num.value < num.min_ or num.value > num.max_:
                        logger.error(f'\'{num.name}\' is not in the range ({num.min_}, {num.max_})')
                elif num.include_min and not num.include_max:
                    if num.value < num.min_ or num.value >= num.max_:
                        logger.error(f'\'{num.name}\' is not in the range [{num.min_}, {num.max_})')
                elif not num.include_min and num.include_max:
                    if num.value <= num.min_ or num.value > num.max_:
                        logger.error(f'\'{num.name}\' is not in the range ({num.min_}, {num.max_}]')
                elif not num.include_min and not num.include_max:
                    if num.value <= num.min_ or num.value >= num.max_:
                        logger.error(f'\'{num.name}\' is not in the range [{num.min_}, {num.max_}]')
            elif num.min_ is not None:
                if num.include_min:
                    if num.value < num.min_:
                        logger.error(f'\'{num.name}\' must be >= {num.min_}')
                else:
                    if num.value <= num.min_:
                        logger.error(f'\'{num.name}\' must be > {num.min_}')
            elif num.max_ is not None:
                if num.include_max:
                    if num.value > num.max_:
                        logger.error(f'\'{num.name}\' must be <= {num.max_}')
                else:
                    if num.value >= num.max_:
                        logger.error(f'\'{num.name}\' must be < {num.max_}')


def format_time(seconds):
    if seconds < 60:
        return f'{int(seconds):02d}s'
    elif seconds >= 60 and seconds < 3600:
        minutes, seconds = divmod(seconds, 60)
        minutes, seconds = int(minutes), int(seconds)
        return f'{minutes:02d}m{seconds:02d}s'
    elif seconds >= 3600:
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes, seconds = int(hours), int(minutes), int(seconds)
        return f'{hours:02d}h{minutes:02d}m{seconds:02d}s'
