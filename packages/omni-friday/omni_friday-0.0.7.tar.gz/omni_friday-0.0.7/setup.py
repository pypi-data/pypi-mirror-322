
VERSION = "0.0.7"

from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()
setup(
    name = 'omni-friday',
    version = VERSION,
    author = 'Facundo Capua',
    author_email = 'capua.facundo@omni.pro',
    license = 'MIT License',
    description = 'FRIDAY is a console tool developed in Python that allows you to obtain and analyze key information from projects based on Adobe Commerce.',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/omni-pro/friday',
    py_modules = ['friday', 'app'],
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    entry_points = '''
        [console_scripts]
        friday=friday:cli
    '''
)