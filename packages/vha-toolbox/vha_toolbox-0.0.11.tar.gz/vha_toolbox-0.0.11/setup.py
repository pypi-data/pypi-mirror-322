import pathlib

import setuptools

long_description = (pathlib.Path(__file__).parent.resolve() / 'README.md').read_text(encoding='utf-8')

setuptools.setup(
    name='vha-toolbox',
    version='0.0.11',
    author='Victor Hachard',
    author_email='31635811+VictorHachard@users.noreply.github.com',
    url='https://github.com/VictorHachard/vha-toolbox',
    description='My personal Python toolbox',
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Source": "https://github.com/VictorHachard/vha-toolbox",
        "Bug Tracker": "https://github.com/VictorHachard/vha-toolbox/issues"
    },
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12"
    ],
    packages=['vha_toolbox'],
    install_requires=[
        'Unidecode==1.3.8'
    ],
)
