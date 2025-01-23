from setuptools import setup, find_packages

setup(
    name='sigmaex',
    version='0.1.2',
    description='A python package for checking the gaussian histogram of data array.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Mingyu Li',
    author_email='lmytime@hotmail.com',
    url='https://github.com/lmytime/sigmaex',
    license='GPL3',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'astropy',
        'tifffile',
        'matplotlib',
        'lmfit'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'sigmaex = sigmaex.sigmaex:main',  # 设置命令行入口
        ],
    },
    python_requires='>=3.6',
)