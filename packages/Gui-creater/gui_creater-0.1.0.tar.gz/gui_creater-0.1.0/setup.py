from setuptools import setup, find_packages
 
setup(
    name='Gui_creater',  # 包名
    version='0.1.0',    # 版本号
    packages=find_packages(),  # 自动查找包
    url='https://github.com/pysilver-8888/Gui_creater',  # 项目URL
    license='MIT',  # 许可证类型
    author='pysilver',  # 作者名
    author_email='19595263@qq.com',  # 作者邮箱
    description='A simple library to make useful Gui.',  # 短描述
    long_description=open('README.md').read(),  # 长描述，可以从README读取
    long_description_content_type="text/markdown",  # 说明文档类型
    keywords=['gui', 'example'],  # 关键词列表
    python_requires='>=3.6',  # Python版本要求
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)