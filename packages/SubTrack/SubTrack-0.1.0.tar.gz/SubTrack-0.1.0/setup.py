from setuptools import setup, find_packages

setup(
    name='SubTrack',  
    version='0.1.0',  
    author='Anatoly',  
    author_email='tolagvozdev@gmail.com',  
    description='A library for tracking subscribers and managing unsubscribed profiles.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/anatolygg/SubTrack',  
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pandas',
        'openpyxl',
        'beautifulsoup4',
    ], 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7', 
)