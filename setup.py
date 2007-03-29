from setuptools import setup, find_packages

import sys
from econ import __version__

setup(
    name='econ',
    version=__version__,
    description='An open set of economics related tools, data and services.',
    license='GPL',
    author='Rufus Pollock',
    author_email='rufus@rufuspollock.org',
    url='http://www.knowledgeforge.net/project/econ/',
    install_requires=[],
    packages=find_packages(exclude=['docs']),
    include_package_data=True,
    package_data={'econ.www': ['i18n/*/LC_MESSAGES/*.mo']},
    extras_require = {
        'www': ["Pylons>=0.9.4,<=1.0"],
        },
    entry_points="""
        [paste.app_factory]
        main=econ.www:make_app
        [paste.app_install]
        main=paste.script.appinstall:Installer
    """,
)
