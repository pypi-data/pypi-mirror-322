import os
import subprocess

from zenlog import log as logging

class Source:
    ''' '''
    pass

class LocalSource(Source):
    ''' '''

    def __init__(self, srcdir : str):
        ''' '''
        self.srcdir = srcdir

    def checkout(self, _target_dir: str, _flog) -> bool:
        return True

class GitSource(Source):
    ''' '''

    def __init__(self, url: str, branch: str, depth: int = 1, shallow_submodules: bool = False, recurse_submodules: bool = False) ->  None:
        ''' '''
        self.url = url
        self.branch = branch
        self.depth = depth
        self.shallow_submodules = shallow_submodules
        self.recurse_submodules = recurse_submodules

    def checkout(self, target_dir: str, flog) -> bool:
        ''' '''
        if os.path.exists(target_dir):
            logging.debug(f"   ==> refreshing git dir {target_dir}")
            #cmd = ['git', 'pull']
            return True

        logging.debug(f"   ==> checking out repo in {target_dir}")
        cmd = ['git', 'clone', self.url, '-b', self.branch, target_dir]
        if self.depth:
            cmd += ['--depth', str(self.depth)]
        if self.shallow_submodules:
            cmd.append('--shallow-submodules')
        if self.recurse_submodules:
            cmd.append('--recurse-submodules')

        proc = subprocess.run(cmd, stdout=flog, stderr=flog)
        return proc.returncode == 0
