from setuptools import setup, find_packages

setup(
    name='pyjzq',
    version='0.1',
    author='tianhukj',
    author_email='tianhukj@outlook.com',
    description='A command-line tic-tac-toe game',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/tianhukj/pyjzq',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        # 添加依赖包，如有需要
    ],
    entry_points={
        'console_scripts': [
            'pyjzq=pyjzq.game:main',
        ],
    },
)
