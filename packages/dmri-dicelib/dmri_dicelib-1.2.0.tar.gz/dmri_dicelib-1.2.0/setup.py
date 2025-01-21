from setuptools import setup, find_packages, Extension, Command
from setuptools.command.build_ext import build_ext
from glob import glob
from numpy import get_include
from shutil import rmtree

# name of the package
package_name = 'dicelib'


def get_extensions():
    image = Extension(
        name=f'{package_name}.image',
        sources=[f'{package_name}/image.pyx'],
        include_dirs=[get_include()],
        extra_compile_args=['-w', '-std=c++11', '-g0'],
        language='c++'
    )
    streamline = Extension(
        name=f'{package_name}.streamline',
        sources=[f'{package_name}/streamline.pyx'],
        include_dirs=[get_include(), f'{package_name}/include'],
        extra_compile_args=['-w', '-std=c++11', '-g0'],
        language='c++'
    )
    tractogram = Extension(
        name=f'{package_name}.tractogram',
        sources=[f'{package_name}/tractogram.pyx'],
        include_dirs=[get_include()],
        extra_compile_args=['-w', '-std=c++11', '-g0'],
        language='c++'
    )
    clustering = Extension(
        name=f'{package_name}.clustering',
        sources=[f'{package_name}/clustering.pyx'],
        extra_compile_args=['-w', '-std=c++11'],
        language='c++',
    )
    connectivity = Extension(
        name=f'{package_name}.connectivity',
        sources=['dicelib/connectivity.pyx'],
        include_dirs=[get_include()],
        extra_compile_args=['-w', '-std=c++11'],
        language='c++',
    )
    tsf = Extension(
        name=f'{package_name}.tsf',
        sources=[f'{package_name}/tsf.pyx'],
        include_dirs=[get_include()],
        extra_compile_args=['-w', '-std=c++11'],
        language='c++',
    )

    return [image, streamline, tractogram, clustering, connectivity, tsf]


class CustomBuildExtCommand(build_ext):
    """build_ext command to use when numpy headers are needed"""

    def run(self):
        # Now that the requirements are installed, get everything from numpy
        from Cython.Build import cythonize
        from numpy import get_include
        from multiprocessing import cpu_count

        # Add everything requires for build
        self.swig_opts = None
        self.include_dirs = [get_include()]
        self.distribution.ext_modules[:] = cythonize(self.distribution.ext_modules, build_dir='build')

        # if not specified via '-j N' option, set compilation using max number of cores
        if self.parallel is None:
            self.parallel = cpu_count()
        print( f'Parallel compilation using {self.parallel} threads' )

        # Call original build_ext command
        build_ext.finalize_options(self)
        build_ext.run(self)


class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        rmtree('./build', ignore_errors=True)

setup(
    cmdclass={
        'build_ext': CustomBuildExtCommand,
        'clean': CleanCommand
    },
    ext_modules=get_extensions()
)