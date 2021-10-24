import logging
import platform
import traceback
from pathlib import Path
from contextlib import contextmanager

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

from TorchIOModule import TorchIOModuleLogic


TRANSFORMS = list(sorted([
  'RandomBlur',
  'RandomSpike',
  'RandomAffine',
  'RandomGamma',
  'RandomMotion',
  'RandomGhosting',
  'RandomBiasField',
  'RandomAnisotropy',
  'RandomElasticDeformation',
  'HistogramStandardization',
]))


class TorchIOTransforms(ScriptedLoadableModule):

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = 'TorchIO Transforms'
    self.parent.categories = ['Utilities']
    self.parent.dependencies = []
    self.parent.contributors = [
      'Fernando Perez-Garcia'
      ' (University College London and King\'s College London)'
    ]
    self.parent.helpText = (
      'This module can be used to quickly visualize the effect of each'
      ' transform parameter. That way, users can have an intuitive feeling of'
      ' what the output of a transform looks like without any coding at all.\n\n'
    )
    self.parent.helpText += self.getDefaultModuleDocumentationLink()
    self.parent.acknowledgementText = (
      'This work is supported by the EPSRC-funded UCL Centre for Doctoral'
      ' Training in Medical Imaging (EP/L016478/1). This publication represents'
      ' in part independent research commissioned by the Wellcome Trust Health'
      ' Innovation Challenge Fund (WT106882). The views expressed in this'
      ' publication are those of the authors and not necessarily those of the'
      ' Wellcome Trust.'
    )

  def getDefaultModuleDocumentationLink(self):
    docsUrl = 'https://torchio.readthedocs.io/interfaces/index.html#d-slicer-gui'
    linkText = f'See <a href="{docsUrl}">the documentation</a> for more information.'
    return linkText


class TorchIOTransformsWidget(ScriptedLoadableModuleWidget):

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)
    self.logic = TorchIOTransformsLogic()
    if self.logic.torchio is None: # make sure PyTorch and TorchIO are installed
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

    goToSampleDataButton = qt.QPushButton('Go to Sample Data module')
    goToSampleDataButton.clicked.connect(lambda: slicer.util.selectModule('SampleData'))
    nodesLayout.addWidget(goToSampleDataButton)

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
    self.outputSelector.selectNodeUponCreation = False
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
    self.transformsComboBox.addItems(TRANSFORMS)
    for transformName in TRANSFORMS:
      transform = self.logic.getTransform(transformName)
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
      self.currentTransform(inputVolumeNode, outputVolumeNode)
    except:
      message = 'Error applying the transform.'
      detailedText = (
        f'Transform kwargs:\n{kwargs}\n\n'
        f'Error details:\n{traceback.format_exc()}'
      )
      slicer.util.errorDisplay(message, detailedText=detailedText)
      return
    inputDisplayNode = inputVolumeNode.GetDisplayNode()
    inputColorNodeID = inputDisplayNode.GetColorNodeID()
    outputDisplayNode = outputVolumeNode.GetDisplayNode()
    outputDisplayNode.SetAndObserveColorNodeID(inputColorNodeID)
    if outputVolumeNode.IsA('vtkMRMLLabelMapVolumeNode'):
      slicer.util.setSliceViewerLayers(label=outputVolumeNode)
    else:
      outputDisplayNode.SetAutoWindowLevel(False)
      wmin, wmax = inputDisplayNode.GetWindowLevelMin(), inputDisplayNode.GetWindowLevelMax()
      outputDisplayNode.SetWindowLevelMinMax(wmin, wmax)
      slicer.util.setSliceViewerLayers(background=outputVolumeNode)


class TorchIOTransformsLogic(TorchIOModuleLogic):
  def getTransform(self, transformName):
    import TorchIOTransformsLib
    return getattr(TorchIOTransformsLib, transformName)()

  def applyTransform(self, inputNode, outputNode, transformName):
    if outputNode is None:
      outputNode = slicer.mrmlScene.AddNewNodeByClass(inputNode.GetClassName())
    transform = self.getTransform(transformName)
    with self.showWaitCursor():
      transform(inputNode, outputNode)


class TorchIOTransformsTest(ScriptedLoadableModuleTest):
  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)
    logic = TorchIOTransformsLogic()
    logic.installTorchIO(confirm=False)
    self.landmarksPath = Path(slicer.util.tempDirectory()) / 'landmarks.npy'
    landmarks = np.array(
      [3.55271368e-15, 7.04965436e-02, 5.11962268e-01, 8.81293798e-01,
       1.08523250e+00, 1.51833266e+00, 3.08140233e+00, 1.15454687e+01,
       2.78108498e+01, 3.42262691e+01, 3.99556984e+01, 5.26837071e+01,
       1.00000000e+02]
    )
    np.save(self.landmarksPath, landmarks)
    # Landmarks unused for now

  def tearDown(self):
    self.landmarksPath.unlink()

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_TorchIOTransforms()
    self.tearDown()

  def _delayDisplay(self, message):
    if not slicer.app.testingEnabled():
      self.delayDisplay(message)

  def test_TorchIOTransforms(self):
    self._delayDisplay("Starting the test")
    import SampleData
    volumeNode = SampleData.downloadSample('MRHead')
    self._delayDisplay('Finished with download and loading')
    logic = TorchIOTransformsLogic()
    for transformName in TRANSFORMS:
      if transformName == 'HistogramStandardization':
        # This transform can't be run with default input parameters
        continue
      self._delayDisplay(f'Applying {transformName}...')
      logic.applyTransform(
        volumeNode,
        volumeNode,
        transformName,
      )
      self._delayDisplay(f'{transformName} passed!')
    self._delayDisplay('Test passed!')
