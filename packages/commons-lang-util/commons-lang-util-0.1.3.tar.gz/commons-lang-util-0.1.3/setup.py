from setuptools import setup

setup(
    name='commons-lang-util',
    version='0.1.3',
    packages=['commons_lang_util'],
    install_requires=[],
    author='JiaBao Gao',
    author_email='gaojiabao1991@gmail.com',
    description='A utility package for common language operations',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/gaojiabao1991/commons_lang_util',
    classifiers = [
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    python_requires='>=3.0',
) 

