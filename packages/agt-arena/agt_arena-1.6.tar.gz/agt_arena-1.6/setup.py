from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='agt_arena', 
    version='1.6',
    author='John Wu', 
    author_email='john_w_wu@brown.edu', 
    description='The AGT Docker Arena is a dockerized python platform designed to run and implement game environments that autonomous agents can connect to and compete in.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_data={'agt_server': ['configs/server_configs/*.json', 'configs/handin_configs/*.json']},
    packages=find_packages(exclude=["submissions"]),
    python_requires='>=3.10',
    install_requires=required,
)