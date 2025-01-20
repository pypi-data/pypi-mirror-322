from setuptools import setup, find_packages

setup(
    name="syncverse",  
    version="0.1.3",  
    packages=find_packages(),  
    install_requires=[
        "watchdog",   
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib"
    ],
    include_package_data=True,  
    author="Maha Vishnu",
    author_email="mahavishnu55510@gmail.com",
    description="A Python package to sync files with Google Drive and locally.",
    long_description=open("README.md").read(),  
    long_description_content_type="text/markdown",
    url="https://github.com/vishnu55510/syncverse", 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6', 
)