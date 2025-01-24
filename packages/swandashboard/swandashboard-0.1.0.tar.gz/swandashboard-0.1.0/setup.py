from setuptools import setup, find_packages

setup(
    name="swandashboard",
    version="0.1.0",
    packages=find_packages(),
    description="A package to open SWAN Dashboard",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Shivdutt Choubey",
    author_email="shivduttchoubey@gmail.com",  # Replace with your email
    url="https://github.com/shivduttchoubey/swan.github.io",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)