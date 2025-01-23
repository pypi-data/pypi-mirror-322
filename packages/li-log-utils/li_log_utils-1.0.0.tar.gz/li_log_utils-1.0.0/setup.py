from setuptools import setup, find_packages

from pkg_resources import parse_requirements

with open("requirements.txt", encoding="utf-8") as fp:
    install_requires = [str(requirement) for requirement in parse_requirements(fp)]

setup(
    name="li_log_utils",
    version="1.0.0",
    author="lirongxuan",
    author_email="24868371772@qq.com",
    description="用于数据格式转换",
    long_description=open('README.md', encoding='utf-8').read(),
    license="Apache License, Version 2.0",
    url="https://gitlab.chehejia.com/xuyang7/mindgpt_dataloop_common_tools/data_process_utils",

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    include_package_data=True,  # 一般不需要
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'data-process-utils = data_process_utils.log_utils.py:save_json'
        ]
    })
