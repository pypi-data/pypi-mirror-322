from setuptools import setup, find_packages

setup(
    name="sqlitelib",
    version="1.0.4",
    author="Jun Ke",
    author_email="kejun91@gmail.com",
    description="A sqlite lib that encapsulate common sqlite operations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kejun91/sqlitelib",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
