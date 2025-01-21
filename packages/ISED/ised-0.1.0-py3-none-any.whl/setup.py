# setup.py
from setuptools import setup, find_packages

# Read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='ISED',
    version='0.1.0',  # Use semantic versioning
    description='Temporal smoothness embedding learning via the ISED approach',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Wenjun Bai',
    author_email='wjbai@atr.jp',
    url='https://github.com/LeonBai/ISED',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    package_data={
        'ised': ['data/*.pkl'],
    },
    install_requires=[
        'numpy>=1.21.6',
        'tensorflow>=2.11.0',
        'scipy>=1.7.3',
        'scikit-learn>=0.24.0',
        'scikit-dimension>=0.3.4',
        'scikit-image>=0.17.2',
    ],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='embedding learning temporal smoothness ISED',
)
