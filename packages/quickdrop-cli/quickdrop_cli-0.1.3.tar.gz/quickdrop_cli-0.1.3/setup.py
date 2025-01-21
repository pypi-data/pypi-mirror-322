from setuptools import setup, find_packages

setup(
    name="quickdrop-cli",
    version="0.1.3",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
        "requests",
        "beautifulsoup4",
        "lxml",  # Adding this for better HTML parsing
    ],
    entry_points={
        "console_scripts": [
            "quickdrop=quickdrop.cli:cli",
        ],
    },
    author="Philip Marais",  # Update with your name
    author_email="philipmarais@gmail.com",  # Update with your email
    description="A simple deployment tool for quickdrop.host with automatic resource bundling",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/philipmarais/quickdrop-cli",  # Update with your repo
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
    ],
    python_requires=">=3.6",
)