from setuptools import setup, find_packages

setup(
    name="kuzco",
    version="0.1.19",
    author="Yakov Perets",
    author_email="yakov.perets@gmail.com",
    description="Tool for managing Python monorepos",
    # long_description=open('README.md').read(),
    long_description_content_type="text/markdown",  # Specify Markdown format
    url="https://gitlab.com/yakov.perets/kuzco",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    install_requires=[
        "click","watchdog"
    ],
    entry_points={
        "console_scripts": [
            "kuzco=kuzco.cli.cli:cli",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

# PIP editable mode
### pip install -e .
# PYPI
## build pip package
### python setup.py sdist bdist_wheel
## upload pip package
### twine upload -u __token__ -p  dist/* --verbose 
