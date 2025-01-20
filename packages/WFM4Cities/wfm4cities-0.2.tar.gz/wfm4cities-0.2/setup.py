from setuptools import setup, find_packages

# 使用 with 语句读取 README.md 文件
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='WFM4Cities',  # 包名
    version='0.2',  # 初始版本号
    packages=find_packages(),  # 自动发现包文件
    install_requires=[  # 列出你的依赖项
        'scipy>=1.5.0',
        'sklearn>=0.24',
        'matplotlib>=3.3',
        'tkinter',  # Tkinter 通常是 Python 的标准库，不需要安装
        'geopandas>=0.9.0',
        'shapely>=1.7.1',
        'pysal>=2.0',
        'numpy>=1.19',
    ],
    author='张祚、 江驭鲲、 王哲',
    author_email='jiangyukunccnu@163.com',
    description='Water-flooding Method for urban 3D-morphology',  # 简要的项目描述
    long_description=long_description,  # 使用变量而不是重新打开文件
    long_description_content_type='text/markdown',
    url='https://github.com/你的用户名/你的项目',  # 项目的 GitHub 链接
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # 或根据你选择的许可证
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # 指定 Python 版本要求
)


