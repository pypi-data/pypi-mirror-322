from setuptools import setup, find_packages

# 读取 README 文件内容
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pyjokers',
    version='0.2.0',
    packages=find_packages(),
    description='A simple joke generator',
    long_description=long_description,
    long_description_content_type='text/markdown',  # 指定描述文件的格式
    author='tianhukj',
    author_email='tianhukj@outlook.com',
    url='https://github.com/tianhukj/pyjokers',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        # 当前没有依赖项
    ],
    entry_points={
        'console_scripts': [
            'pyjoke=pyjokers.pyjokers:main',
        ],
    },
)
