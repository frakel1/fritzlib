from setuptools import setup, find_packages

setup(
    name='fritzbox-library',
    version='0.1.0',
    author='Franz Keller',
    author_email='frakel1@outlook.com',
    description='A library for interacting with Fritzbox devices.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/fritzbox-library',
    packages=find_packages(),
    install_requires=[
        'requests',
        'tkinter',  # tkinter is included with Python, but you can specify it if needed
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)