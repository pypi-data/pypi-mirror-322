from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext
import subprocess
import os

class CustomInstallCommand(build_ext):
    def run(self):
        # Ensure Graphviz is installed
        try:
            print("Installing Graphviz with Homebrew...")
            subprocess.check_call(["brew", "install", "graphviz"])
        except Exception as e:
            print(f"Error installing Graphviz: {e}")
            raise

        # Set environment variables for Graphviz
        os.environ["CFLAGS"] = "-I/usr/local/include"
        os.environ["LDFLAGS"] = "-L/usr/local/lib"
        os.environ["GRAPHVIZ_CFLAGS"] = "-I/usr/local/include"
        os.environ["GRAPHVIZ_LDFLAGS"] = "-L/usr/local/lib"

        # Run the original build_ext command
        super().run()

setup(
    name="nnViewer",
    version="0.1.0",
    author="PBDESG",
    author_email="pbdesg@gmail.com",
    description="A neural network visualization tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/PBDESG/nnViewer",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "torch==2.2.2",
        "pygraphviz==1.14",
        "PyQt5==5.15.11",
    ],
    cmdclass={
        "build_ext": CustomInstallCommand,
    },
)
