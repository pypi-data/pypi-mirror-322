from setuptools import setup, find_packages

setup(
    name="nustify",  # New unique name for your package
    version="0.1.0",
    author="Abdul Rehman",
    author_email="abrehman.bsai24seecs@seecs.edu.pk",
    description="A Python package for exploring BSAI at SEECS.",
    url="https://github.com/AbdulRehmanOK/nustify",  # Change the URL to reflect the correct repo name
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  
)
