# setup.py

from setuptools import setup, find_packages

setup(
    name='magic_thumbnail',
    version='0.1.0',
    description='A Python library to generate multiple thumbnails from high-resolution images.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Atharva Wankhede',
    author_email='atharvaw007@gmail.com',
    url='https://github.com/aths7/magic_thumbnail',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'Pillow>=10.0.0',
        'requests>=2.0.0',
        'python-dotenv>=0.19.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
