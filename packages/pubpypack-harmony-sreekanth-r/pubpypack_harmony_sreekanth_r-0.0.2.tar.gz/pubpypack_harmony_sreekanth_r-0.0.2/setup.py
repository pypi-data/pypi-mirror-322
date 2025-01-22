from setuptools import setup 

from Cython.Build import cythonize 

setup(
     name="pubpypack_harmony_sreekanth_r",
     ext_modules=cythonize("src/imppkg/harmonic_mean.pyx"),
)

