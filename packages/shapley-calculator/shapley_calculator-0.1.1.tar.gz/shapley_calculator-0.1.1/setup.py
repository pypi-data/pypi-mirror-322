from setuptools import setup, find_packages

setup(
    name='shapley_calculator',
    version='0.1.1',
    description='A library to calculate Shapley values for feature importance in machine learning models.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Andrew Alexeev',
    author_email='andrey.alekseev8996@gmail.com',
    url='https://github.com/AlekseevDS21/Shapley',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)