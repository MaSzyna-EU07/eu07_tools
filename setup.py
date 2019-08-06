import sys
import fnmatch
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py as build_py_orig

excluded = []

if "--devonly" not in sys.argv:
      excluded = [
            "eu07_tools/e3d/input.py",
            "eu07_tools/t3d/input.py",
            # temporary it's useless
            "eu07_tools/mat"
      ] 
else:
      sys.argv.remove("--devonly")

class build_py(build_py_orig):
    def find_package_modules(self, package, package_dir):
        modules = super().find_package_modules(package, package_dir)
        return [
            (pkg, mod, file)
            for (pkg, mod, file) in modules
            if not any(fnmatch.fnmatchcase(file, pat=pattern) for pattern in excluded)
        ]

setup(name='eu07_tools',
      packages=find_packages(),
      cmdclass={'build_py': build_py},
      version='1.0',
      description='Helpful tools for editing MaSzyna Train Simulator assets',
      url='https://gitlab.com/krzysiuup/eu07_tools',
      author='Balaclava',
      author_email='krzysiuup@gmail.com',
      license='MIT',
      python_requires='>=3.7',

)
