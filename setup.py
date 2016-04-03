#-*- coding: utf-8 -*-

"""Polaris setup

By default will install to /opt/polaris, to install to a different folder 
set POLARIS_INSTALL_PREFIX env before running "python3 setup.py install"
"""

import os
import sys
import inspect
import shutil
import setuptools


VERSION = '0.4.0'


def main():
   # setup packages
    setuptools.setup(
        version=VERSION,
        author='Anton Gavrik',    
        name='polaris-gslb',
        description=('An extendable Global Server Load Balancing(GSLB) '
                     'solution, DNS-based traffic manager.'),
        packages = setuptools.find_packages('.'),
        install_requires=[
            'pyyaml',
            'python-memcached', 
            'python-daemon-3K'
        ],
        license='BSD 3-Clause',
        url='https://github.com/polaris-gslb/polaris-gslb',
        download_url=('https://github.com/polaris-gslb/polaris-gslb/tarball/v{}'
                      .format(VERSION)),
        classifiers=[
            'Programming Language :: Python :: 3',
        ]
    )

    # use value from POLARIS_INSTALL_PREFIX env if set
    try:
        install_prefix = os.environ['POLARIS_INSTALL_PREFIX']
    except KeyError:
        install_prefix = os.path.join(os.sep, 'opt', 'polaris')

    # determine the directory where setup.py is located
    pwd = os.path.abspath(
        os.path.split(inspect.getfile(inspect.currentframe()))[0])
 
    print('Creating directory topology...')
    for path in [ 
        os.path.join(install_prefix, 'etc'),
        os.path.join(install_prefix, 'bin'),
        os.path.join(install_prefix, 'run'),        
            ]:
        try:
            os.makedirs(path)
        except FileExistsError:
            continue

    print('Copying dist configuration and executables...')
    for dirname in [ 'etc', 'bin' ]:
        copy_files(os.path.join(pwd, dirname), 
                   os.path.join(install_prefix, dirname))


    print('Creating /etc/default/polaris...')    
    py3_bin = which('python3')
    py3_path = ''
    if py3_bin is None:
        print('Unable to find Python3 executable in the $PATH, '
              'add the path manually to /etc/default/polaris')
    else:
        py3_path = os.path.split(py3_bin)[0]

    with open(os.path.join(os.sep, 'etc', 'default', 'polaris'), 'w') as f:
        f.write('export PATH=$PATH:{}\n'.format(py3_path))
        f.write('export POLARIS_INSTALL_PREFIX={}\n'
                .format(install_prefix))
         

def copy_files(src_dir, dst_dir):
    """Copy all files from src_dir to dst_dir""" 
    src_files = os.listdir(src_dir)
    for file_name in src_files:
        full_file_name = os.path.join(src_dir, file_name)
        if (os.path.isfile(full_file_name)):
            shutil.copy(full_file_name, dst_dir)


def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ['PATH'].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


if __name__ == '__main__':
    main()

