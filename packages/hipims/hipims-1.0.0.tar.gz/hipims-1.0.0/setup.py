from setuptools import setup, find_packages
from torch.utils.cpp_extension import BuildExtension, CUDAExtension
import os


this_directory = os.path.abspath(os.path.dirname(__file__))


# define cuda extensions
ext_modules = [
    CUDAExtension(
        name = 'hipims.euler_update', 
        sources = [
            'src/cuda/euler_update_Interface.cpp',
            'src/cuda/euler_update_Kernel.cu',
        ],
        # Extra compile arguments for both C++ and NVCC compilers
        extra_compile_args={
            'cxx': ['-g', f'-I{os.path.join(this_directory, "src", "cuda")}'],  # Debug information for C++
            'nvcc': ['-O2',
                    '-gencode=arch=compute_60,code=sm_60',  # Pascal architecture (e.g. GTX 1080)
                    '-gencode=arch=compute_70,code=sm_70',  # Volta (e.g. Tesla V100)
                    '-gencode=arch=compute_75,code=sm_75',  # Turing (e.g. RTX 2080)
                    '-gencode=arch=compute_80,code=sm_80',  # Ampere (e.g. RTX 3090)
                    '-gencode=arch=compute_80,code=compute_80',  # Ampere
                    '-gencode=arch=compute_86,code=compute_86']},

        include_dirs=[os.path.join(this_directory, 'src', 'cuda')]
    ),
    CUDAExtension(
        name = 'hipims.fluxCal_1stOrder', 
        sources = [
            'src/cuda/fluxCal_1stOrder_Interface.cpp',
            'src/cuda/fluxCal_1stOrder_Kernel.cu',
        ],
        extra_compile_args={
        'cxx': ['-g', f'-I{os.path.join(this_directory, "src", "cuda")}'],  # Debug information for C++
        'nvcc': ['-O2',
                '-gencode=arch=compute_60,code=sm_60',  # Pascal architecture (e.g. GTX 1080)
                '-gencode=arch=compute_70,code=sm_70',  # Volta (e.g. Tesla V100)
                '-gencode=arch=compute_75,code=sm_75',  # Turing (e.g. RTX 2080)
                '-gencode=arch=compute_80,code=sm_80',  # Ampere (e.g. RTX 3090)
                '-gencode=arch=compute_80,code=compute_80',  # Ampere
                '-gencode=arch=compute_86,code=compute_86']},
        include_dirs=[os.path.join(this_directory, 'src', 'cuda')]
    ),
    CUDAExtension(
        name = 'hipims.fluxCal_2ndOrder', 
        sources = [
            'src/cuda/fluxCal_2ndOrder_Interface.cpp',
            'src/cuda/fluxCal_2ndOrder_Kernel.cu',
        ],
        extra_compile_args={
            'cxx': ['-g', f'-I{os.path.join(this_directory, "src", "cuda")}'],  # Debug information for C++
            'nvcc': ['-O2',
                    '-gencode=arch=compute_60,code=sm_60',  # Pascal architecture (e.g. GTX 1080)
                    '-gencode=arch=compute_70,code=sm_70',  # Volta (e.g. Tesla V100)
                    '-gencode=arch=compute_75,code=sm_75',  # Turing (e.g. RTX 2080)
                    '-gencode=arch=compute_80,code=sm_80',  # Ampere (e.g. RTX 3090)
                    '-gencode=arch=compute_80,code=compute_80',  # Ampere
                    '-gencode=arch=compute_86,code=compute_86']},

        include_dirs=[os.path.join(this_directory, 'src', 'cuda')]
    ),
    CUDAExtension(
        name = 'hipims.fluxMask', 
        sources = [
            'src/cuda/fluxMask_Interface.cpp',
            'src/cuda/fluxMask_Kernel.cu',
        ],
        extra_compile_args={
            'cxx': ['-g', f'-I{os.path.join(this_directory, "src", "cuda")}'],  # Debug information for C++
            'nvcc': ['-O2',
                    '-gencode=arch=compute_60,code=sm_60',  # Pascal architecture (e.g. GTX 1080)
                    '-gencode=arch=compute_70,code=sm_70',  # Volta (e.g. Tesla V100)
                    '-gencode=arch=compute_75,code=sm_75',  # Turing (e.g. RTX 2080)
                    '-gencode=arch=compute_80,code=sm_80',  # Ampere (e.g. RTX 3090)
                    '-gencode=arch=compute_80,code=compute_80',  # Ampere
                    '-gencode=arch=compute_86,code=compute_86']},

        include_dirs=[os.path.join(this_directory, 'src', 'cuda')]
    ),
    CUDAExtension(
        name = 'hipims.frictionImplicit_andUpdate', 
        sources = [
            'src/cuda/frictionImplicit_andUpdate_Interface.cpp',
            'src/cuda/frictionImplicit_andUpdate_Kernel.cu',
        ],
        extra_compile_args={
            'cxx': ['-g', f'-I{os.path.join(this_directory, "src", "cuda")}'],  # Debug information for C++
            'nvcc': ['-O2',
                    '-gencode=arch=compute_60,code=sm_60',  # Pascal architecture (e.g. GTX 1080)
                    '-gencode=arch=compute_70,code=sm_70',  # Volta (e.g. Tesla V100)
                    '-gencode=arch=compute_75,code=sm_75',  # Turing (e.g. RTX 2080)
                    '-gencode=arch=compute_80,code=sm_80',  # Ampere (e.g. RTX 3090)
                    '-gencode=arch=compute_80,code=compute_80',  # Ampere
                    '-gencode=arch=compute_86,code=compute_86']},

        include_dirs=[os.path.join(this_directory, 'src', 'cuda')]
    ),
    CUDAExtension(
        name = 'hipims.infiltration_sewer', 
        sources = [
            'src/cuda/infiltration_sewer_Interface.cpp',
            'src/cuda/infiltration_sewer_Kernel.cu',
        ],
        extra_compile_args={
            'cxx': ['-g', f'-I{os.path.join(this_directory, "src", "cuda")}'],  # Debug information for C++
            'nvcc': ['-O2',
                    '-gencode=arch=compute_60,code=sm_60',  # Pascal architecture (e.g. GTX 1080)
                    '-gencode=arch=compute_70,code=sm_70',  # Volta (e.g. Tesla V100)
                    '-gencode=arch=compute_75,code=sm_75',  # Turing (e.g. RTX 2080)
                    '-gencode=arch=compute_80,code=sm_80',  # Ampere (e.g. RTX 3090)
                    '-gencode=arch=compute_80,code=compute_80',  # Ampere
                    '-gencode=arch=compute_86,code=compute_86']},

        include_dirs=[os.path.join(this_directory, 'src', 'cuda')]
    ),
    CUDAExtension(
        name = 'hipims.stationPrecipitation', 
        sources = [
           'src/cuda/stationPrecipitation_Interface.cpp',
           'src/cuda/stationPrecipitation_Kernel.cu',
        ],
        extra_compile_args={
            'cxx': ['-g', f'-I{os.path.join(this_directory, "src", "cuda")}'],  # Debug information for C++
            'nvcc': ['-O2',
                    '-gencode=arch=compute_60,code=sm_60',  # Pascal architecture (e.g. GTX 1080)
                    '-gencode=arch=compute_70,code=sm_70',  # Volta (e.g. Tesla V100)
                    '-gencode=arch=compute_75,code=sm_75',  # Turing (e.g. RTX 2080)
                    '-gencode=arch=compute_80,code=sm_80',  # Ampere (e.g. RTX 3090)
                    '-gencode=arch=compute_80,code=compute_80',  # Ampere
                    '-gencode=arch=compute_86,code=compute_86']},

        include_dirs=[os.path.join(this_directory, 'src', 'cuda')]
    ),
    CUDAExtension(
      name = 'hipims.timeControl', 
      sources = [
            'src/cuda/timeControl_Interface.cpp',
            'src/cuda/timeControl_Kernel.cu',],
      extra_compile_args={
            'cxx': ['-g', f'-I{os.path.join(this_directory, "src", "cuda")}'],  # Debug information for C++
            'nvcc': ['-O2',
                    '-gencode=arch=compute_60,code=sm_60',  # Pascal architecture (e.g. GTX 1080)
                    '-gencode=arch=compute_70,code=sm_70',  # Volta (e.g. Tesla V100)
                    '-gencode=arch=compute_75,code=sm_75',  # Turing (e.g. RTX 2080)
                    '-gencode=arch=compute_80,code=sm_80',  # Ampere (e.g. RTX 3090)
                    '-gencode=arch=compute_80,code=compute_80',  # Ampere
                    '-gencode=arch=compute_86,code=compute_86']},

      include_dirs=[os.path.join(this_directory, 'src', 'cuda')]
    )
]


# INSTALL_REQUIREMENTS = ['numpy', 'torch', 'torchvision', 'scikit-image', 'tqdm', 'imageio']
setup(

    ext_modules=ext_modules,
    cmdclass={
        'build_ext': BuildExtension.with_options(no_python_abi_suffix=True)
    },

    include_package_data=True,

    package_data={'hipims': ['sample/input/*'],},

    )

