from setuptools import setup, find_packages

setup(
    name='fritzlib',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A library for managing Fritzbox devices and login operations.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/fritzlib',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'tkinter',  # tkinter is included with Python, but you can specify it if needed
    ],
)