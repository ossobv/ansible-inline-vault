#!/usr/bin/env python3
from distutils.core import setup


long_description = 'FIXME'


setup(
    name='ansible-inline-vault',
    version='v0.1_rc1',
    scripts=['ansible-inline-vault'],
    data_files=[
        ('share/ansible-inline-vault/playbooks/filter_plugins', [
            'filter_plugins/decrypt.py'])],
    description=(
        'Decrypt files with inline ansible vault secrets'),
    long_description=long_description,
    author='Walter Doekes, OSSO B.V.',
    author_email='wjdoekes+ansible@osso.nl',
    url='https://github.com/ossobv/ansible-inline-vault',
    license='GPLv3+',
    platforms=['linux'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        ('License :: OSI Approved :: GNU General Public License v3 '
         'or later (GPLv3+)'),
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'cryptography>=2.8',
    ],
)

# vim: set ts=8 sw=4 sts=4 et ai tw=79:
