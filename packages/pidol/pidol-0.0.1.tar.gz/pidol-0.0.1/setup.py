# coding=utf-8
# author=UlionTse

import re
import pathlib
import setuptools


NAME = 'pidol'
PACKAGE = 'pidol'
AUTHOR = 'UlionTse'
AUTHOR_EMAIL = 'uliontse@outlook.com'
HOMEPAGE_URL = 'https://github.com/uliontse/pidol'
DESCRIPTION = 'Pidol is a library that includes many models of CTR Prediction & Recommender System by Paddle.'
LONG_DESCRIPTION = pathlib.Path('README.md').read_text(encoding='utf-8')
VERSION = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', pathlib.Path('pidol/__init__.py').read_text(), re.M).group(1)


setuptools.setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license='Apache-2.0',
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_dir={'pidol': 'pidol'},
    url=HOMEPAGE_URL,
    project_urls={
        'Source': 'https://github.com/UlionTse/pidol',
        'Changelog': 'https://github.com/UlionTse/pidol/blob/main/change_log.txt',
        'Documentation': 'https://github.com/UlionTse/pidol/blob/main/README.md',
    },
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords=['Machine Learning', 'Deep Learning', 'CTR Prediction', 'Recommender System'],
    install_requires=[
        'numpy>=1.26.4',
        'paddlepaddle>=2.6.2',
    ],
    python_requires='>=3.9',
    extras_require={'pypi': ['build>=1.2.2', 'twine>=6.0.1']},
    zip_safe=False,
)














