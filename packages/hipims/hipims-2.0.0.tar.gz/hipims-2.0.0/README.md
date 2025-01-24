# High-Performance Integrated hydrodynamic Modelling System ***hybrid***

This is a beta version inhouse code of Hemlab used for high-performance flooding simulation.


## About
HiPIMS names for High-Performance Integrated hydrodynamic Modelling System. It uses state-of-art numerical schemes (Godunov-type finite volume) to solve the 2D shallow water equations for flood simulations. To support high-resolution flood simulations, HiPIMS is implemented on multiple GPUs (Graphics Processing Unit) using CUDA/C++ languages to achieve high-performance computing. To find out how to use the model, please see the wiki.

### Contributing
HiPIMS is maintained by the Hydro-Environmental Modelling Labarotory [URL](https://www.hemlab.org/), a research hub for technological innovation and interdisciplinary collaboration. We warmly welcome the hydro-environmental modelling community to contribute to the project, believing that this project will benefit the whole community.

 [Qiuhua Liang](https://www.lboro.ac.uk/departments/abce/staff/qiuhua-liang/), ([Q.Liang@lboro.ac.uk](mailto:Q.Liang@lboro.ac.uk)) is the Head of HEMLab.

#### Authors
Jiaheng Zhao, HemLab ([jiaheng.zhao@fmglobal.com](mailto:jiaheng.zhao@fmglobal.comk))

Xue Tong, Loughborough University ([x.tong2@lboro.ac.uk](mailto:x.tong2@lboro.ac.uk))  
  
## License
This is a beta version inhouse code of Hemlab and can only be used and extended if you are a ***member of hemlab***. If not, please contact Qiuhua Liang (q.liang@lboro.ac.uk) for more information.

## Requirements
HiPMS deployment requires the following software to be installed on the build machine.
- GCC and G++ >= 10
- Python >= 3.8
- pip
- The CUDA Toolkit 12.1 (see https://developer.nvidia.com/cuda-12-1-0-download-archive)
- torch for CUDA 12.1(pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121)

## Install
cd .../HiPIMS_2024
pip install .
