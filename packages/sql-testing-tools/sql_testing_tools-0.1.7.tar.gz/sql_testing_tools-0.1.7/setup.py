from setuptools import setup, find_packages

with open("sql_testing_tools/README.md", "r") as fh:
    description = fh.read()


setup(
    name='sql_testing_tools',
    version='0.1.7',
    packages=find_packages(),
    install_requires=[
        'sqlparse>=0.5.1',
        'requests>=2.32.3'
    ],
    long_description=description,
    long_description_content_type="text/markdown"
)