"""
# 1. remove old temp folders
rm -rf dist build

# 2. then, build
python setup.py sdist bdist_wheel

# 3. finally, upload
twine upload dist/*

rm -rf dist build && python setup.py sdist bdist_wheel && twine upload dist/*
"""

import os

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def _process_requirements():
    packages = open('requirements.txt').read().strip().split('\n')
    requires = []
    for pkg in packages:
        if pkg.startswith('git+ssh'):
            return_code = os.system('pip install {}'.format(pkg))
            assert return_code == 0, 'error, status_code is: {}, exit!'.format(return_code)
        else:
            requires.append(pkg)
    return requires


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            if filename.endswith('yaml'):
                paths.append(os.path.join('..', path, filename))
    return paths


extra_files = package_files('memoryscope')

setuptools.setup(
    name="memoryscope-ai",
    version="0.1.1.0",
    description="MemoryScope is a powerful and flexible long term memory system for LLM chatbots. It consists of a "
                "memory database and three customizable system operations, which can be flexibly combined to provide "
                "robust long term memory services for your LLM chatbot.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/memoryscope/memoryscope",
    project_urls={
        "Bug Tracker": "https://github.com/memoryscope/memoryscope/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    package_data={"": extra_files},
    include_package_data=True,
    entry_points={
        'console_scripts': ['memoryscope-ai=memoryscope:cli'],
    },
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.10",
    install_requires=_process_requirements(),
)
