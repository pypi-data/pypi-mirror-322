from setuptools import setup, find_packages

setup(
    name="run_protocol",
    version="0.1.0",
    description="A Python library to control the Opentrons OT-2 and FLEX robot via HTTP API.",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/run_protocol",
    packages=find_packages(),
    install_requires=["requests"],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)