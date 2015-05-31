import os
from setuptools import setup, find_packages

install_requires = [
    "metayaml",
    "attrdict",
    "evernote",
    "sqlitedict",
]

dependency_links = [
    #Use direct link to Github because pypi version doesn't install at all
    #On the date 2015 May 30
    "https://github.com/evernote/evernote-sdk-python3/archive/master.zip#egg=evernote"
]

fiefar_dependencies = [
    "PyYAML",
]
install_requires.extend(fiefar_dependencies)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

packages = find_packages(".")
setup(
    name="efa",
    version="0.0.1",  # TODO read from version
    author="ASD Technologies",
    author_email="detijazzz@gmail.com",
    description="API backend server for the BOSS project",
    license="Public",
    url="https://github.com/deti/efa",
    packages=packages,
    package_data={
        '': ['*.sh', '*.ini', '*.pem', '*.txt'],
        'configs': ['*.yaml']},
    install_requires=install_requires,
    dependency_links=dependency_links,
    entry_points={
        'console_scripts':
        [
            'efa = efa:main',
            'efa.py = efa:main',
        ]
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Web Environment",
        "License :: Other/Proprietary License",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.4",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Server",
        "Topic :: Multimedia :: Video :: Display",
    ],
)
