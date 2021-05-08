from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='qt-widgets',
    version='0.0.1-dev3',
    author='flegac',
    description='Qt widgets library',

    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/flegac/qt-widgets",
    project_urls={
        "Bug Tracker": "https://github.com/flegac/qt-widgets/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=[line for line in open('requirements.txt')],
    python_requires=">=3.7",
    include_package_data=True
)
