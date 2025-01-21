from setuptools import setup
import re

def read_requirements(filename):
    requirements = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # 跳过注释和空行
            if not line or line.startswith('#'):
                continue
            # 处理-r或--requirement参数
            if line.startswith('-r ') or line.startswith('--requirement '):
                continue
            # 移除行内注释
            line = line.split('#')[0].strip()
            # 处理环境标记
            if ';' in line:
                line = line.split(';')[0].strip()
            # 处理版本号
            requirements.append(re.sub(r'==|>=|<=|~=|>|<', '>=', line))
    return requirements



setup(
    name='commons-lang-util',
    version='0.1.5',
    packages=['commons_lang_util'],
    install_requires=read_requirements("requirements.txt"),
    author='JiaBao Gao',
    author_email='gaojiabao1991@gmail.com',
    description='A utility package for common language operations',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/gaojiabao1991/commons_lang_util',
    classifiers = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    python_requires='>=3.0',
) 

