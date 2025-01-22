from setuptools import setup, find_packages

setup(
    name="bathini",
    version="0.1.0",
    packages=find_packages(),
    description="A package that introduces Bathini, a Computer Vision Scientist",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Bathini",
    author_email="your.email@example.com",  # Replace with your email
    url="https://github.com/bathini/bathini",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)