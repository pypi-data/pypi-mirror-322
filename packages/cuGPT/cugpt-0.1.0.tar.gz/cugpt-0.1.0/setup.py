from setuptools import setup, find_packages
from torch.utils.cpp_extension import BuildExtension, CUDAExtension
import os

# Define the root directory
root = os.path.dirname(os.path.abspath(__file__))

# Path to the CUDA source file
relu_source = os.path.join('cuGPT', 'kernels', 'relu.cu')

setup(
    name='cuGPT',
    version='0.1.0',
    author='A. Zeer',
    description='PyTorch CUDA extension package.',
    long_description=open(os.path.join(root, 'README.md')).read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    ext_modules=[
        CUDAExtension(
            name='cuGPT.kernels.relu_ext',
            sources=[relu_source],
            extra_compile_args={
                'cxx': ['-O3'],
                'nvcc': [
                    '-O3',
                    '-U__CUDA_NO_HALF_CONVERSIONS__',
                    '-U__CUDA_NO_HALF_OPERATORS__',
                    '-U__CUDA_NO_HALF2_OPERATORS__',
                    '-U__CUDA_NO_BFLOAT16_CONVERSIONS__',
                    '-U__CUDA_NO_BFLOAT16_OPERATORS__',
                    '--expt-relaxed-constexpr',
                    '--expt-extended-lambda',
                    '--use_fast_math',
                ],
            },
            language='c++',
        )
    ],
    cmdclass={
        'build_ext': BuildExtension
    },
    install_requires=[
        'torch',
    ],
)
