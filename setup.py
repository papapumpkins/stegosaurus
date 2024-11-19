from setuptools import setup, find_packages

setup(
    name="stegosaurus", 
    version="0.1.0",  
    author="Neel", 
    author_email="neel@getparker.com", 
    description="A package to execute SQL queries and write to Google Sheets", 
    long_description=open("README.md").read(), 
    long_description_content_type="text/markdown",
    url="https://github.com/papapumpkins/stegosaurus",
    license="MIT", 
    packages=find_packages(), 
    install_requires=[
        "google-auth>=2.0.0",
        "google-auth-oauthlib>=0.4.0", 
        "google-api-python-client>=2.0.0", 
        "psycopg2-binary>=2.9.0", 
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "steg=stegosaurus.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
