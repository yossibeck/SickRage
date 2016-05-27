"""
Use setup tools to install sickrage
"""
import os
from setuptools import find_packages, setup

try:
    from babel.messages import frontend as babel
except ImportError:
    babel = None

ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__)))

with open(os.path.join(ROOT, 'readme.md'), 'r') as r:
    long_description = r.read()

setup(
    name="sickrage",
    version="0.0.1",

    description="Automatic Video Library Manager for TV Shows",
    long_description=long_description,

    url='https://sickrage.github.io',
    download_url='https://github.com/SickRage/SickRage.git',

    author='miigotu',
    author_email='miigotu@gmail.com',

    license='GPLv2',

    include_package_data=True,
    zip_safe=False,

    package_data = {'sickrage': ['gui/**']},
    packages=['sickrage', 'sickbeard'],

    install_requires=[
        'pytz',
        'pygithub',
        'requests',
        'mako',
        'babelfish',
        'subliminal',
        'validators',
        'tornado',
        'xmltodict',
        'cachecontrol',
        'oauth',
        'oauth2',
        'setuptools-git',
        'send2trash',
        'jsonrpclib',
        'html5lib',
        'hachoir_core',
        'hachoir_metadata',
        'hachoir_parser',
        'feedparser',
        'bencode',
        'imdbpy',
        'gntp==0.4',
        'pynma',
        'lockfile',
        'twitter',
        'configobj',
        'markdown2'
    ],

    test_suite="tests",
    tests_require=[
        'coveralls',
        'nose',
        'rednose',
        'mock',
        'vcrpy',
        'vcrpy-unittest',
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Multimedia :: Video',
    ],

    cmdclass={
        'compile_catalog': babel.compile_catalog,
        'extract_messages': babel.extract_messages,
        'init_catalog': babel.init_catalog,
        'update_catalog': babel.update_catalog
    } if babel else {},

    message_extractors={
        'gui': [
            ('**/views/**.mako', 'mako', {'input_encoding': 'utf-8'}),
            # @OmgImAlexis
            # Need to move *.js into a separate dir than *.min.js,
            # running gettext on minified js conflicts with _()
            # ('**/js/**.js', 'javascript', {'input_encoding': 'utf-8'})
        ],
        'sickrage': [('**.py', 'python', None)],
        'sickbeard': [('**.py', 'python', None)],
    },

    scripts=['SickBeard.py']
)
