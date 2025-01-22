from setuptools import setup, find_packages

setup(
    name="dualkey",
    version="1.0.5",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "dualkey=dualkey.main:main"
        ],
    },
    author="Tanner McMullen",
    description="A seedphrase encryption/decryption tool",
    license="MIT",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ilovespectra/dualkey",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

