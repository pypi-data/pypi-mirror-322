from setuptools import setup, find_packages

setup(
    name='luca-llai',
    version='0.1.0',
    author='LearnableLoopAI.com',
    author_email='kobus78@gmail.com',
    description='A brief description of the luca package.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/luca_project',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'pymdp',
        # add other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'luca=luca.luca:main',
        ],
    },
)
