from setuptools import setup, find_packages

setup(
    name='capsify',
    version='0.2',
    packages=find_packages(),
    install_requires=[],  # Add any dependencies here
    python_requires='>=3.6',  # Specify Python version requirements
    author='',  # Add your name
    author_email='',  # Add your email
    description='',  # Add a short description
    long_description=open('README.md').read(),  # Assuming you have a README file
    long_description_content_type='text/markdown',
    url='',  # Add your project's URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)