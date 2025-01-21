from setuptools import setup, find_packages

setup(
    name="opensubmarine",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    
    # Metadata
    author="OpenSubmarine Team",
    author_email="hello@nautilus.sh",
    description="A library for secure smart contract development on Algorand",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/NautilusOSS/opensubmarine-contracts",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security",
    ],
    python_requires=">=3.7",
    install_requires=[
        "py-algorand-sdk",
        # Add other dependencies as needed
    ],
) 