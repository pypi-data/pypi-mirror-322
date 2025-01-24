from setuptools import setup, find_packages

setup(
    name='A_STT',
    version='0.1',
    author='Prime Vivek',
    author_email='vivekbadiger666@gmail.com',
    description='This is a speech-to-text package created by Prime Vivek. It helps with voice commands and more.',
    packages=find_packages(),
    install_requires=[
        'selenium',
        'webdriver-manager',
    ],
    python_requires='>=3.6',  # or any other version you want
)
