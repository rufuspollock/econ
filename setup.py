try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

import sys
sys.path.insert(0, '.')
import econ

setup(
    name='econ',
    version=econ.__version__,
    description=econ.__description__,
    long_description=econ.__long_description__,
    license='MIT',
    author='Rufus Pollock',
    author_email='rufus [at] rufuspollock [dot] org',
    url='http://www.openeconomics.net/',
    install_requires=[],
    packages=find_packages(exclude=['docs']),
    include_package_data=True,
    test_suite='nose.collector',
    zip_safe=False,
    package_data={'econ.www': ['i18n/*/LC_MESSAGES/*.mo']},
    # mx.Tidy (optional)
    # econ.data.tabular.HtmlWriter prettyPrint functionality depends on mx.Tidy
    # package (this functionality is disabled in normal used) 
    extras_require = {
        'www': ["Pylons>=0.9.6.1"],
        'test' : ['wsgi_intercept>=0.1'],
        },
    #message_extractors = {'econ.www': [
    #        ('**.py', 'python', None),
    #        ('public/**', 'ignore', None)]},
    entry_points="""
    [paste.app_factory]
    main = econ.www.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller

    [console_scripts]
    econ-admin=econ.cli:main
    """,
)
