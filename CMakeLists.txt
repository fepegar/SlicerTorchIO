cmake_minimum_required(VERSION 3.13.4)

project(TorchIO)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://torchio.readthedocs.io/slicer.html")
set(EXTENSION_CATEGORY "Utilities")
set(EXTENSION_CONTRIBUTORS "Fernando Perez-Garcia (University College London)")
set(EXTENSION_DESCRIPTION "TorchIO is a Python package containing a set of tools to efficiently read, preprocess, sample, augment, and write 3D medical images in deep learning applications written in PyTorch, including intensity and spatial transforms for data augmentation and preprocessing. Transforms include typical computer vision operations such as random affine transformations and also domain-specific ones such as simulation of intensity artifacts due to MRI magnetic field inhomogeneity or k-space motion artifacts.")
set(EXTENSION_ICONURL "https://raw.githubusercontent.com/fepegar/SlicerTorchIO/master/TorchIOTransforms/Resources/Icons/TorchIOTransforms.png")
set(EXTENSION_SCREENSHOTURLS "https://raw.githubusercontent.com/fepegar/SlicerTorchIO/master/Screenshots/TorchIO.png")
set(EXTENSION_DEPENDS "PyTorch") # Specified as a list or "NA" if no dependencies

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(TorchIOTransforms)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
