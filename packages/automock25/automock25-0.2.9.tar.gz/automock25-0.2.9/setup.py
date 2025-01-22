
from setuptools import setup, find_packages

setup(
    name='automock25',  # 包的名称
    version='0.2.9',           # 包的版本号
    packages=find_packages(),  # 自动查找所有包和子包
    install_requires=[        # 项目依赖的其他包
        # 'numpy>=1.18.5',
        'requests>=2.24.0',
        'flask>=2.0.0',  # 你可以根据需要调整 Flask 的版本号
        'DataRecorder>=3.6.2',
        'DrissionPage>=4.1.0.17',


    ],
    author='peak',        # 作者名称
    author_email='your.email@example.com',  # 作者邮箱
    description='自动模拟充值',  # 简短描述
    # long_description=open('README.md').read(),  # 详细描述，通常从 README 文件读取
    long_description_content_type='text/markdown',  # 描述内容的格式
    #url='https://github.com/yourusername/your_package_name',  # 项目主页或仓库地址
    classifiers=[  # 分类器，用于描述项目的特性
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',

    ],
    python_requires='>=3.6',  # 支持
    include_package_data=True,  # 包含包数据（如静态文件）
    #  entry_points={  # 可选，用于创建命令行工具
    #     'console_scripts': [
    #         'your_command=your_package.module:main_function',
    #     ],
    # },
    # include_package_data=True,  # 包含包数据（如静态文件）
    # package_data={  # 可选，指定包含的数据文件
    #     'your_package': ['data/*.dat'],
    # },
    # exclude_package_data={  # 可选，指定排除的数据文件
    #     'your_package': ['data/exclude_this.dat'],
    # },
    # zip_safe=False,  # 可选，指定是否可以安全地以 zip 形式安装
)