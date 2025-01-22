from setuptools import setup, find_packages

setup(
    name="mytower_sftp_package",
    version="1.0.0",
    description="A reusable SFTP client package for Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="moustapha.cheikh",
    author_email="bounesadava@gmail.com",
    url="https://github.com/yourusername/sftp_package",  # Replace with your repository URL
    packages=find_packages(),
    install_requires=[
        "paramiko",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
