import os
import sys
from pathlib import Path

from setuptools import setup


try:
    from sphinx.setup_command import BuildDoc
except ImportError:
    BuildDoc = None

from explorer import get_version


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...

name = "django-sql-explorer"
version = get_version(True)
release = get_version()


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


if sys.argv[-1] == 'build':
    os.system('python setup.py sdist bdist_wheel')
    print(f"Built release {release} (version {version})")
    sys.exit()

if sys.argv[-1] == 'release':
    os.system('twine upload --skip-existing dist/*')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version:")
    os.system(f"git tag -a {version} -m 'version {version}'")
    os.system("git push --tags")
    sys.exit()

this_directory = Path(__file__).parent
long_description = (this_directory / "README.rst").read_text()

setup(
    name=name,
    version=version,
    author="Chris Clark",
    author_email="chris@untrod.com",
    maintainer='Mark Walker',
    maintainer_email='theshow@gmail.com',
    description=("A pluggable app that allows users (admins) to execute SQL,"
                 " view, and export the results."),
    license="MIT",
    keywords="django sql explorer reports reporting csv database query",
    url="https://github.com/groveco/django-sql-explorer",
    project_urls={
      'Changes': 'https://django-sql-explorer.readthedocs.io/en/latest/history.html',
      'Documentation': 'https://django-sql-explorer.readthedocs.io/en/latest/',
      'Issues': 'https://github.com/groveco/django-sql-explorer/issues'
    },
    packages=['explorer'],
    long_description=long_description,
    long_description_content_type='text/x-rst',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Utilities',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only',
    ],
    python_requires='>=3.8',
    install_requires=[
        'Django>=3.2.12',
        'sqlparse>=0.4.0',
    ],
    extras_require={
        "charts": [
            "matplotlib<4",
            "seaborn<0.12"
        ],
        "snapshots": [
            "boto3>=1.20.0",
            "celery>=4.0"
        ],
        "xls": [
            'xlsxwriter>=1.3.6'
        ]
    },
    cmdclass={
        'build_sphinx': BuildDoc,
    },
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'release': ('setup.py', release),
            'source_dir': ('setup.py', 'docs'),
            'build_dir': ('setup.py', './docs/_build')
        }
    },
    include_package_data=True,
    zip_safe=False,
)
