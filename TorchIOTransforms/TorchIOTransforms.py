import logging
import platform
import importlib
import traceback
from pathlib import Path

import numpy as np
import SimpleITK as sitk

import vtk, qt, ctk, slicer
import sitkUtils as su
from slicer.ScriptedLoadableModule import (
  ScriptedLoadableModule,
  ScriptedLoadableModuleWidget,
  ScriptedLoadableModuleLogic,
  ScriptedLoadableModuleTest,
)

WINDOWS_TORCH_INSTALL = 'torch===1.5.0 torchvision===0.6.0 -f https://download.pytorch.org/whl/torch_stable.html'



class TorchIOTransforms(ScriptedLoadableModule):

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = 'TorchIO Transforms'
    self.parent.categories = ['Utilities']
    self.parent.dependencies = []
    self.parent.contributors = [
      'Fernando Perez-Garcia'
      ' (University College London, King\'s College London)'
    ]
    self.parent.helpText = (
      'This module can be used to quickly visualize the effect of each'
      ' transform parameter. That way, users can have an intuitive feeling of'
      ' what the output of a transform looks like without any coding at all.\n\n'
    )
    self.parent.helpText += self.getDefaultModuleDocumentationLink(
      docPage='https://torchio.readthedocs.io/slicer.html')
    self.parent.acknowledgementText = (
      'This work is supported by the EPSRC-funded UCL Centre for Doctoral'
      ' Training in Medical Imaging (EP/L016478/1). This publication represents'
      ' in part independent research commissioned by the Wellcome Trust Health'
      ' Innovation Challenge Fund (WT106882). The views expressed in this'
      ' publication are those of the authors and not necessarily those of the'
      ' Wellcome Trust.'
    )


class TorchIOTransformsWidget(ScriptedLoadableModuleWidget):

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)
    self.logic = TorchIOTransformsLogic()
    if not self.logic.checkTorchIO():
      return
    self.transforms = []
    self.currentTransform = None
    self.makeGUI()
    self.onVolumeSelectorModified()
    slicer.torchio = self
    self.backgroundNode = None

  def makeGUI(self):
    self.addNodesButton()
    self.addTransformButton()
    self.addTransforms()
    self.addToggleApplyButtons()
    # Add vertical spacer
    self.layout.addStretch(1)

  def addNodesButton(self):
    self.nodesButton = ctk.ctkCollapsibleButton()
    self.nodesButton.text = 'Volumes'
    self.layout.addWidget(self.nodesButton)
    nodesLayout = qt.QFormLayout(self.nodesButton)

    self.inputSelector = slicer.qMRMLNodeComboBox()
    self.inputSelector.nodeTypes = ['vtkMRMLVolumeNode']
    self.inputSelector.addEnabled = False
    self.inputSelector.removeEnabled = True
    self.inputSelector.noneEnabled = False
    self.inputSelector.setMRMLScene(slicer.mrmlScene)
    self.inputSelector.currentNodeChanged.connect(self.onVolumeSelectorModified)
    nodesLayout.addRow('Input volume: ', self.inputSelector)

    self.outputSelector = slicer.qMRMLNodeComboBox()
    self.outputSelector.nodeTypes = ['vtkMRMLScalarVolumeNode']
    self.outputSelector.addEnabled = False
    self.outputSelector.removeEnabled = True
    self.outputSelector.noneEnabled = True
    self.outputSelector.setMRMLScene(slicer.mrmlScene)
    self.outputSelector.noneDisplay = 'Create new volume'
    self.outputSelector.currentNodeChanged.connect(self.onVolumeSelectorModified)
    nodesLayout.addRow('Output volume: ', self.outputSelector)

  def addTransformButton(self):
    self.transformsButton = ctk.ctkCollapsibleButton()
    self.transformsButton.text = 'Transforms'
    self.layout.addWidget(self.transformsButton)
    self.transformsLayout = qt.QFormLayout(self.transformsButton)

    self.transformsComboBox = qt.QComboBox()
    self.transformsLayout.addWidget(self.transformsComboBox)

  def addTransforms(self):
    transformNames = [
      'RandomSpike',
      'RandomAffine',
      'RandomMotion',
      'RandomGhosting',
      'RandomBiasField',
      'RandomElasticDeformation',
      'HistogramStandardization',
    ]
    self.transformsComboBox.addItems(transformNames)
    for transformName in transformNames:
      klass = getattr(importlib.import_module('transforms'), transformName)
      transform = klass()
      self.transforms.append(transform)
      transform.hide()
      self.transformsLayout.addWidget(transform.groupBox)
    self.transformsComboBox.currentIndex = -1
    self.transformsComboBox.currentIndexChanged.connect(self.onTransformsComboBox)

  def addToggleApplyButtons(self):
    toggleApplyFrame = qt.QFrame()
    toggleApplyLayout = qt.QHBoxLayout(toggleApplyFrame)

    self.toggleButton = qt.QPushButton('Toggle volumes')
    self.toggleButton.clicked.connect(self.onToggleButton)
    self.toggleButton.setDisabled(True)
    toggleApplyLayout.addWidget(self.toggleButton)

    self.applyButton = qt.QPushButton('Apply transform')
    self.applyButton.clicked.connect(self.onApplyButton)
    self.applyButton.setDisabled(True)
    toggleApplyLayout.addWidget(self.applyButton)

    self.layout.addWidget(toggleApplyFrame)

  def onTransformsComboBox(self):
    transformName = self.transformsComboBox.currentText
    for transform in self.transforms:
      if transform.name == transformName:
        self.currentTransform = transform
        transform.show()
      else:
        transform.hide()
    self.onVolumeSelectorModified()

  def onVolumeSelectorModified(self):
    self.applyButton.setDisabled(
      self.inputSelector.currentNode() is None
      or self.currentTransform is None
    )
    self.toggleButton.setEnabled(
      self.inputSelector.currentNode() is not None
      and self.outputSelector.currentNode() is not None
    )

  def onToggleButton(self):
    inputNode = self.inputSelector.currentNode()
    outputNode = self.outputSelector.currentNode()
    if self.backgroundNode is None:
      self.backgroundNode = inputNode
    self.backgroundNode = outputNode if self.backgroundNode is inputNode else inputNode
    foregroundNode = outputNode if self.backgroundNode is inputNode else inputNode
    slicer.util.setSliceViewerLayers(
      background=self.backgroundNode,
      foreground=foregroundNode,
      foregroundOpacity=0,
    )

  def onApplyButton(self):
    inputVolumeNode = self.inputSelector.currentNode()
    outputVolumeNode = self.outputSelector.currentNode()

    if outputVolumeNode is None:
      name = f'{inputVolumeNode.GetName()} {self.currentTransform.name}'
      outputVolumeNode = slicer.mrmlScene.AddNewNodeByClass(
        inputVolumeNode.GetClassName(),
        name,
      )
      outputVolumeNode.CreateDefaultDisplayNodes()
      self.outputSelector.currentNodeID = outputVolumeNode.GetID()
    try:
      kwargs = self.currentTransform.getKwargs()
      logging.info(f'Transform args: {kwargs}')
      outputImage = self.currentTransform(inputVolumeNode)
    except Exception as e:
      tb = traceback.format_exc()
      message = (
        f'TorchIO returned the error: {tb}'
        f'\n\nTransform kwargs:\n{kwargs}'
      )
      slicer.util.errorDisplay(message)
      return
    su.PushVolumeToSlicer(outputImage, targetNode=outputVolumeNode)
    inputColorNodeID = inputVolumeNode.GetDisplayNode().GetColorNodeID()
    outputVolumeNode.GetDisplayNode().SetAndObserveColorNodeID(inputColorNodeID)
    slicer.util.setSliceViewerLayers(background=outputVolumeNode)


class TorchIOTransformsLogic(ScriptedLoadableModuleLogic):

  def pipInstallTorchIO(self):
    qt.QApplication.setOverrideCursor(qt.Qt.WaitCursor)
    slicer.util.pip_install('torchio')
    qt.QApplication.restoreOverrideCursor()
    slicer.util.delayDisplay('TorchIO was installed successfully', autoCloseMsec=-1)

  def checkTorchIO(self):
    try:
      import torchio
    except ImportError:
      message = (
        'This module requires the "torchio" Python package.'
        ' Click OK to download it now. It may take a few minutes.'
      )
      installTorchIO = slicer.util.confirmOkCancelDisplay(message)
      if installTorchIO:
        if platform.system() == 'Windows':
          try:  # if torchvision is already installed
            import torchvision
            self.pipInstallTorchIO()
          except ImportError:
            qt.QApplication.restoreOverrideCursor()
            message = (
              'The following packages will be installed:\n'
              'torch===1.5.0 torchvision===0.6.0 -f https://download.pytorch.org/whl/torch_stable.html'
              '\n\nIf you would like to install a different version, then click Cancel'
              ' and install your preferred version before using this module'
            )
            installTorchWindows = slicer.util.confirmOkCancelDisplay(message)
            if installTorchWindows:
              qt.QApplication.setOverrideCursor(qt.Qt.WaitCursor)
              slicer.util.pip_install(WINDOWS_TORCH_INSTALL)
              self.pipInstallTorchIO()
            else:
              return
          finally:
            qt.QApplication.restoreOverrideCursor()
        else:
          self.pipInstallTorchIO()
      import torchio
    logging.info(f'TorchIO version: {torchio.__version__}')
    return True

  def applyTransform(self, inputNode, outputNode, transformName, args, kwargs):
    pass


class TorchIOTransformsTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_TorchIOTransforms1()

  def test_TorchIOTransforms1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import SampleData
    SampleData.downloadFromURL(
      nodeNames='FA',
      fileNames='FA.nrrd',
      uris='http://slicer.kitware.com/midas3/download?items=5767',
      checksums='SHA256:12d17fba4f2e1f1a843f0757366f28c3f3e1a8bb38836f0de2a32bb1cd476560')
    self.delayDisplay('Finished with download and loading')
    volumeNode = slicer.util.getNode(pattern="FA")
    self.delayDisplay('Test passed!')
