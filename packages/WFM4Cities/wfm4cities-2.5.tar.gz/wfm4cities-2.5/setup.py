from setuptools import setup, find_packages

# 使用 with 语句读取 README.md 文件
try:
    with open('README.md', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "Water-flooding Method for urban 3D-morphology"

setup(
    name='WFM4Cities',  # 包名
    version='2.5',  # 初始版本号
    packages=find_packages(),  # 自动发现包文件
    install_requires=[  # 列出你的依赖项
        'scipy==1.13.1',
        'scikit-learn==1.3.0',
        'matplotlib==3.9.4',
        'geopandas==0.13.1',
        'shapely==2.0.6',
        'pysal==24.1',
        'numpy==1.25.2',
    ],
    author='张祚, 江驭鲲, 王哲',
    author_email='jiangyukunccnu@163.com',
    description='Water-flooding Method for urban 3D-morphology',  # 简要的项目描述
    long_description=long_description,  # 使用变量而不是重新打开文件
    long_description_content_type='text/markdown',
    url='https://github.com/你的用户名/你的项目',  # 项目的 GitHub 链接
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # 或根据你选择的许可证
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
    ],
    python_requires='>=3.6',  # 指定 Python 版本要求

    # 配置入口点，使得运行 WFM4Cities 命令可以启动主程序
    entry_points={
        'console_scripts': [
            'WFM4Cities=WFM4Cities.Water_flooding_Model:main',  # 设置入口，调用 Water-flooding-Model.py 中的 main 函数
        ],
    },
)
