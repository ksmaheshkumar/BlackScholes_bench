# Copyright (C) 2019 Intel Corporation
#
# SPDX-License-Identifier: MIT


import base_bs_erf


def build_ext():
  try:
    from distutils.core import setup
    from Cython.Build import cythonize
    import os, subprocess, numpy

    subprocess.call(['icc', '--version'])
  except:
    print("error building the extension module: Cython and Intel compiler are required")
    return False
  else:
    os.environ['CC'] = "icc"
    os.environ['LDSHARED'] = "icc -shared"
    # use high accuracy precision
    os.environ['CFLAGS'] = "-fimf-precision=high -prec-sqrt -qopt-report=5 -fno-alias -xhost -qopenmp -pthread -fno-strict-aliasing"

    setup(
        name = "bs_erf_cython_impl",
        ext_modules = cythonize("bs_erf_cython_impl.pyx"),
        include_dirs = [numpy.get_include()],
        script_args = ["build_ext", "--inplace"]
    )
    import bs_erf_cython_impl as bsc
    return bsc


try:
    import bs_erf_cython_impl as bsc
except:
    bsc = build_ext()

if not bsc:
    print("Skipping Cython version")
else:
    base_bs_erf.run("Cython-parallel", bsc.black_scholes_par, pass_args=True)
    base_bs_erf.run("Cython-serial", bsc.black_scholes_ser, pass_args=True)
