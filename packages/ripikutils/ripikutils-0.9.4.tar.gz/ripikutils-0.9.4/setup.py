from setuptools import setup, find_packages

print(find_packages())
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
print(find_packages())
setup(
    name="ripikutils",
    version="0.9.4",
    author="Vaibhav Agarwal",
    author_email="vaibhav@ripik.ai",
    description="A utility package for AWS S3 and MongoDB operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ripiktech/ripikutils",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.10",
    install_requires=[
        "boto3",
        "pymongo",
        "certifi"
    ],
)
