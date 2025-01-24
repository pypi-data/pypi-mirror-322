# setup.py
from setuptools import setup, find_packages

setup(
    name='dataanalysts',
    version='0.2.1',
    description='An advanced Python data analysis library with enhanced cleaning, transformation, and visualization.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Venkata Govind Neelapu',
    author_email='venkatagovindneelapu@gmail.com',
    license='MIT',
    url='https://github.com/yourusername/dataanalysts',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'scikit-learn',
        'seaborn'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)




