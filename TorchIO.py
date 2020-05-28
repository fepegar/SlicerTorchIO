import importlib
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


try:
  import torchio
except ImportError:
  slicer.util.pip_install('torchio')
  import torchio


class TorchIO(ScriptedLoadableModule):

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "TorchIO"
    self.parent.categories = ["Utilities"]
    self.parent.dependencies = []
    self.parent.contributors = [
      "Fernando Perez-Garcia (University College London)",
    ]
    self.parent.helpText = """[This is the help text.]
    """
    self.parent.helpText += self.getDefaultModuleDocumentationLink(
      docPage='https://github.com/fepegar/SlicerTorchIO')
    self.parent.acknowledgementText = """
    University College London.
    """


class TorchIOWidget(ScriptedLoadableModuleWidget):

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)
    self.logic = TorchIOLogic()
    # self.logic.installRepository()
    self.transforms = []
    self.currentTransform = None
    self.makeGUI()
    self.onInputNodeModified()
    slicer.torchio = self
    import SampleData
    SampleData.downloadSample('MRHead')


  def makeGUI(self):
    self.addNodesButton()
    self.addTransformButton()
    self.addTransforms()
    self.addApplyButton()
    # Add vertical spacer
    self.layout.addStretch(1)

  def addNodesButton(self):
    self.nodesButton = ctk.ctkCollapsibleButton()
    self.nodesButton.text = 'Volumes'
    self.layout.addWidget(self.nodesButton)
    nodesLayout = qt.QFormLayout(self.nodesButton)

    self.inputSelector = slicer.qMRMLNodeComboBox()
    self.inputSelector.nodeTypes = ['vtkMRMLScalarVolumeNode']
    self.inputSelector.addEnabled = False
    self.inputSelector.removeEnabled = True
    self.inputSelector.noneEnabled = False
    self.inputSelector.setMRMLScene(slicer.mrmlScene)
    self.inputSelector.currentNodeChanged.connect(self.onInputNodeModified)
    nodesLayout.addRow('Input volume: ', self.inputSelector)

    self.outputSelector = slicer.qMRMLNodeComboBox()
    self.outputSelector.nodeTypes = ['vtkMRMLScalarVolumeNode']
    self.outputSelector.removeEnabled = True
    self.outputSelector.noneEnabled = True
    self.outputSelector.setMRMLScene(slicer.mrmlScene)
    self.outputSelector.noneDisplay = 'Create new volume'
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
      'RandomAffine',
      'RandomMotion',
      'RandomGhosting',
      'RandomElasticDeformation',
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

  def addApplyButton(self):
    self.applyButton = qt.QPushButton('Apply')
    self.applyButton.clicked.connect(self.onApplyButton)
    self.applyButton.setDisabled(True)
    self.layout.addWidget(self.applyButton)

  def onTransformsComboBox(self):
    transformName = self.transformsComboBox.currentText
    for transform in self.transforms:
      if transform.name == transformName:
        self.currentTransform = transform
        transform.show()
      else:
        transform.hide()

  def onInputNodeModified(self):
    self.applyButton.setDisabled(self.inputSelector.currentNode() is None)

  def onApplyButton(self):
    inputVolumeNode = self.inputSelector.currentNode()
    outputVolumeNode = self.outputSelector.currentNode()

    if outputVolumeNode is None:
      name = f'{inputVolumeNode.GetName()} {self.currentTransform.name}'
      outputVolumeNode = slicer.mrmlScene.AddNewNodeByClass(
        'vtkMRMLScalarVolumeNode',
        name,
      )
      self.outputSelector.currentNodeID = outputVolumeNode.GetID()
    try:
      outputImage = self.currentTransform(inputVolumeNode)
    except Exception as e:
      message = (
        f'TorchIO returned the error: {e}'
        f'\n\nTransform kwargs:\n{self.currentTransform.getKwargs()}'
      )
      slicer.util.errorDisplay(message)
      return
    su.PushVolumeToSlicer(outputImage, targetNode=outputVolumeNode)
    slicer.util.setSliceViewerLayers(background=outputVolumeNode)


class TorchIOLogic(ScriptedLoadableModuleLogic):

  def installRepository(self):
    box = qt.QMessageBox()
    box.setStandardButtons(0)
    box.setText('Importing TorchIO Python module...')
    box.show()
    slicer.app.processEvents()
    slicer.util.pip_install('torchio')
    import torchio
    box.accept()

  def applyTransform(self, inputNode, outputNode, transformName, args, kwargs):
    pass


class TorchIOTest(ScriptedLoadableModuleTest):
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
    self.test_TorchIO1()

  def test_TorchIO1(self):
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
