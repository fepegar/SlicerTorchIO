cmake_minimum_required(VERSION 3.13.4)

project(TorchIO)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://www.slicer.org/wiki/Documentation/Nightly/Extensions/TorchIO")
set(EXTENSION_CATEGORY "Utilities")
set(EXTENSION_CONTRIBUTORS "Fernando Pérez-García (University College London)")
set(EXTENSION_DESCRIPTION "TorchIO is a Python package containing a set of tools to efficiently read, preprocess, sample, augment, and write 3D medical images in deep learning applications written in PyTorch, including intensity and spatial transforms for data augmentation and preprocessing. Transforms include typical computer vision operations such as random affine transformations and also domain-specific ones such as simulation of intensity artifacts due to MRI magnetic field inhomogeneity or k-space motion artifacts.")
set(EXTENSION_ICONURL "http://www.example.com/Slicer/Extensions/TorchIO.png")
set(EXTENSION_SCREENSHOTURLS "http://www.example.com/Slicer/Extensions/TorchIO/Screenshots/1.png")
set(EXTENSION_DEPENDS "NA") # Specified as a list or "NA" if no dependencies

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(TorchIO)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
