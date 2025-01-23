from setuptools import setup, find_packages

setup(
    name='ant_auto_tool_1',  # 包的名字
    version='0.1.1',  # 版本号
    author='Pingchuan ZHONG',
    author_email='zhongpingchuan.zpc@antgroup.com',
    description='A tool for ant auto',
    long_description=open('README.md').read(),  # 从README读取长描述
    long_description_content_type='text/markdown',
    url='',  # 项目的主页
    packages=find_packages(),  # 自动发现所有包和子包
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5',  # 指定支持的Python版本
)
