import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="siaskynet",
    version="2.1.0",
    author="Peter-Jan Brone",
    author_email="peterjan.brone@gmail.com",
    description="Skynet SDK",
    url="https://github.com/NebulousLabs/python-skynet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
        'responses',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
