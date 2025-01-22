from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setup(
    name="serbian-text-converter",
    version="0.1.5",
    description="A utility package for converting Serbian text between Cyrillic and Latin scripts, and generating slugs.",
    long_description=long_description,
    long_description_content_type="text/markdown", 
    author="mladjom",
    author_email="mladenmilentijevic@gmail.com",
    url="https://github.com/mladjom/serbian-text-converter",
    packages=find_packages(),
    install_requires=[
        "Django>=3.2",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",        
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "Framework :: Django :: 3.2"
    ],
    python_requires=">=3.1",
)