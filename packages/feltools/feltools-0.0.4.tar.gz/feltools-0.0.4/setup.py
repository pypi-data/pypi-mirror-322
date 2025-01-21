from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
print(long_description)
setup(
    name='feltools',
    version='0.0.4',
    author="Felix Reiter",
    author_email='sbody1113@gmail.com',
    description='A collection of simple tools in Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    packages=find_packages(include=['feltools','feltools.*']),
    classifiers=[],
    install_requires=[]
)