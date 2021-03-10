#-----------------------------------------------------------------------------
set(MODULE_NAME TorchIOTransforms)

#-----------------------------------------------------------------------------
set(MODULE_PYTHON_SCRIPTS
  ${MODULE_NAME}.py
  ${MODULE_NAME}Lib/__init__
  ${MODULE_NAME}Lib/CoordinatesWidget
  ${MODULE_NAME}Lib/HistogramStandardization
  ${MODULE_NAME}Lib/RandomAffine
  ${MODULE_NAME}Lib/RandomBlur
  ${MODULE_NAME}Lib/RandomBiasField
  ${MODULE_NAME}Lib/RandomAnisotropy
  ${MODULE_NAME}Lib/RandomElasticDeformation
  ${MODULE_NAME}Lib/RandomGhosting
  ${MODULE_NAME}Lib/RandomMotion
  ${MODULE_NAME}Lib/RandomSpike
  ${MODULE_NAME}Lib/Transform
  )

set(MODULE_PYTHON_RESOURCES
  Resources/Icons/${MODULE_NAME}.png
  )

#-----------------------------------------------------------------------------
slicerMacroBuildScriptedModule(
  NAME ${MODULE_NAME}
  SCRIPTS ${MODULE_PYTHON_SCRIPTS}
  RESOURCES ${MODULE_PYTHON_RESOURCES}
  WITH_GENERIC_TESTS
  )

#-----------------------------------------------------------------------------
if(BUILD_TESTING)

  # Register the unittest subclass in the main script as a ctest.
  # Note that the test will also be available at runtime.
  slicer_add_python_unittest(SCRIPT ${MODULE_NAME}.py)

  # Additional build-time testing
  add_subdirectory(Testing)
endif()
