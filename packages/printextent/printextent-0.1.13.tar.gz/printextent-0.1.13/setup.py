from setuptools import find_packages, setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='printextent',
    version='0.1.13',
    packages=find_packages(),
    install_requires=[],
    description='Printing made for the creativity.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Thomas Kyrouac',
    author_email='thomaskkyrouac@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)