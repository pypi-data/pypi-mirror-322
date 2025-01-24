from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='py_to_pyd',
    version='0.0.1',
    description='Py To Pyd',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='huang yi yi',
    author_email='363766687@qq.com',
    packages=['PyToPyd'],  # 自动查找所有包
    include_package_data=True,  # 包括其他文件
    entry_points={
        'console_scripts': [
            'py-to-pyd=PyToPyd.main:main', 
            'pytopyd=PyToPyd.main:main', 
        ],
    },
    python_requires='>=3.6',
    install_requires=[
        "Cython>=3.0.10.post1",
    ],
)