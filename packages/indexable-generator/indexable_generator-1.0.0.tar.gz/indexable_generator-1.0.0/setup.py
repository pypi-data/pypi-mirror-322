from setuptools import setup

setup(
    name='indexable_generator',
    version='1.0.0',
    description='python core functionalities',
    author='Tiago Simoes Beijoco',
    author_email='craft.uas@gmail.com',
    packages=['indexable_generator'],
    install_requires=[
        'requests',
        'importlib-metadata; python_version<"3.10"',
    ]
)
