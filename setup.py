from os.path import abspath, dirname, join, normpath

import setuptools

setuptools.setup(
    # Basic package information:
    name='pelican_cite',
    version='1.0.0',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},


    # Packaging options:
    include_package_data=True,

    # Package dependencies:
    install_requires=['pelican>=4.0', 'pybtex'],

    # Metadata for PyPI:
    author='Arvid Norlander',
    author_email='VorpalBlade@users.noreply.github.com',
    license='GPL-3.0',
    url='https://github.com/VorpalBlade/pelican-cite',
    keywords='pelican blog static bibtex citation',
    description='Allows the use of BibTeX citations within a Pelican site.',
    long_description=open(
        normpath(join(dirname(abspath(__file__)), 'README.md'))).read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Framework :: Pelican :: Plugins",
    ],
)
