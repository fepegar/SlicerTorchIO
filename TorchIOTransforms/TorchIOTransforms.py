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

TORCH_VERSION = '1.7.0'
TORCHVISION_VERSION = '0.8.1'


TRANSFORMS = [
  'RandomSpike',
  'RandomAffine',
  'RandomMotion',
  'RandomGhosting',
  'RandomBiasField',
  'RandomDownsample',
  'RandomElasticDeformation',
  'HistogramStandardization',
]


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
    docsUrl = 'https://torchio.readthedocs.io/slicer.html'
    linkText = f'See <a href="{docsUrl}">the documentation</a> for more information.'
    return linkText


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
      outputImage = self.currentTransform(inputVolumeNode, outputVolumeNode)
    except Exception as e:
      tb = traceback.format_exc()
      message = (
        f'TorchIO returned the error: {tb}'
        f'\n\nTransform kwargs:\n{kwargs}'
      )
      slicer.util.errorDisplay(message)
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


class TorchIOTransformsLogic(ScriptedLoadableModuleLogic):

  def pipInstallTorch(self, keepDialog=False):
    qt.QApplication.setOverrideCursor(qt.Qt.WaitCursor)
    slicer.util.pip_install(self.getTorchInstallLine())
    qt.QApplication.restoreOverrideCursor()
    kwargs = dict(autoCloseMsec=-1) if keepDialog else {}
    slicer.util.delayDisplay('PyTorch was installed successfully', **kwargs)

  def pipInstallTorchIO(self, keepDialog=False):
    qt.QApplication.setOverrideCursor(qt.Qt.WaitCursor)
    with self.peakPythonConsole():
      slicer.util.pip_install(self.getTorchIOInstallLine())
    qt.QApplication.restoreOverrideCursor()
    kwargs = dict(autoCloseMsec=-1) if keepDialog else {}
    slicer.util.delayDisplay('TorchIO was installed successfully', **kwargs)

  def isMac(self):
    return platform.system() == 'Darwin'

  def getTorchInstallLine(self):
    if self.isMac():
      args = ('torch', 'torchvision')
    else:
      args = (
        f'torch=={TORCH_VERSION}+cpu',
        f'torchvision=={TORCHVISION_VERSION}+cpu',
        '-f', 'https://download.pytorch.org/whl/torch_stable.html',
      )
    return ' '.join(args)

  def getTorchIOInstallLine(self):
    major = slicer.app.majorVersion
    if major < 4:
      slicer.util.errorDisplay('This Slicer is too old. Please use Slicer 4.X')
      return
    # Hack until Preview versio works again for macOS
    minor = slicer.app.minorVersion
    if minor <= 11 and self.isMac():
      return 'torchio==0.17.45'  # last version with SimpleITK 1
    return 'torchio'

  def checkTorchIO(self):
    try:
      import torchio
      # torchio is imported as "namespace" if the parent path of the repository
      # is in Slicer's sys.path (I think)
      version = torchio.__version__
    except (ImportError, AttributeError):
      message = (
        'This module requires the "torchio" Python package.'
        ' Click OK to download it now. It may take a few minutes.'
      )
      installTorchIO = slicer.util.confirmOkCancelDisplay(message)
      if installTorchIO:
        try:  # if torchvision is already installed
          import torchvision
          self.pipInstallTorchIO()
        except ImportError:
          qt.QApplication.restoreOverrideCursor()
          packages = '\n'.join(self.getTorchInstallLine().split())
          message = (
            'The following packages will be installed first:\n\n'
            f'{packages}'
            '\n\nIf you would like to install a different version, then click Cancel'
            ' and install your preferred version before using this module'
          )
          installTorch = slicer.util.confirmOkCancelDisplay(message)
          if installTorch:
            self.pipInstallTorch()
            self.pipInstallTorchIO()
          else:
            return
        finally:
          qt.QApplication.restoreOverrideCursor()
      import torchio
    logging.info(f'TorchIO version: {torchio.__version__}')
    return True

  def getPythonConsoleWidget(self):
    return slicer.util.mainWindow().pythonConsole().parent()

  @contextmanager
  def peakPythonConsole(self):
    console = self.getPythonConsoleWidget()
    pythonVisible = console.visible
    console.setVisible(True)
    yield
    console.setVisible(pythonVisible)

  def getTransform(self, transformName):
    import transforms
    return getattr(transforms, transformName)()

  def applyTransform(self, inputNode, outputNode, transformName):
    if outputNode is None:
      outputNode = slicer.mrmlScene.AddNewNodeByClass(inputNode.GetClassName())
    return self.getTransform(transformName)(inputNode, outputNode)

  def getNodesFromSubject(self, subject):
    nodes = {}
    for name, image in subject.get_images_dict(intensity_only=False).items():
      nodes[name] = self.getNodeFromImage(image, name=name)
    return nodes

  def getNodeFromImage(self, image, name=None):
    import torchio
    if image.type == torchio.LABEL:
      className = 'vtkMRMLLabelMapVolumeNode'
    else:
      className = 'vtkMRMLScalarVolumeNode'
    return su.PushVolumeToSlicer(image.as_sitk(), name=name, className=className)

  def getColin(self, version=1998):
    import torchio
    colin = torchio.datasets.Colin27(version=version)
    nodes = self.getNodesFromSubject(colin)
    if version == 1998:
      slicer.util.setSliceViewerLayers(
        background=nodes['t1'],
        label=nodes['brain'],
      )
    elif version == 2008:
      slicer.util.setSliceViewerLayers(
        background=nodes['t1'],
        foreground=nodes['t2'],
      )


class TorchIOTransformsTest(ScriptedLoadableModuleTest):
  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)
    logic = TorchIOTransformsLogic()
    logic.pipInstallTorch()
    logic.pipInstallTorchIO()

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

  def test_TorchIOTransforms(self):
    self.delayDisplay("Starting the test")
    import SampleData
    volumeNode = SampleData.downloadSample('MRHead')
    self.delayDisplay('Finished with download and loading')
    logic = TorchIOTransformsLogic()
    for transformName in TRANSFORMS:
      if transformName == 'HistogramStandardization':
        # This transform can't be run with default input parameters
        continue
      self.delayDisplay(f'Applying {transformName}...')
      logic.applyTransform(
        volumeNode,
        volumeNode,
        transformName,
      )
      self.delayDisplay(f'{transformName} passed!')
    self.delayDisplay('Test passed!')
