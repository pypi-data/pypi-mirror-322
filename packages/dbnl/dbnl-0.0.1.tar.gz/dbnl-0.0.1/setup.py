from setuptools import setup
from setuptools.command.build_py import build_py


class fail(build_py):
    def run(self):
        raise Exception(
            "This package should not be installed from PyPI."
            " Please refer to the documentation for installation instructions:"
            " https://docs.dbnl.com/how-to-use-distributional/getting-started#installing-distributional"
        )


setup(cmdclass={"build_py": fail})
