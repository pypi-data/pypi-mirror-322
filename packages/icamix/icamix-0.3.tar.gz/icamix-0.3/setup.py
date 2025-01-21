from setuptools import setup, find_packages

setup(
    name='icamix',
    version='0.3',
    author='fzpy',
    author_email='690799557@qq.com',
    description='A package for amplitude mixing',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/rqfzpy/icamix',
    packages=find_packages(),
    install_requires=[
        'torch',  # Add torch as a dependency
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        # Add more classifiers as needed
    ],
)