from setuptools import setup, find_packages

setup(
    name="fpcli",
    version="0.1.6",
    description="A simple example package",
    author="Rohit kumar",
    packages=find_packages(include=["fpcli", "fpcli.*"]),
    install_requires=['typer'],  # Add dependencies here
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
