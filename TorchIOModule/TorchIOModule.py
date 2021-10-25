import logging
from pathlib import Path
from contextlib import contextmanager

import numpy as np
import SimpleITK as sitk

import qt, slicer
import sitkUtils as su
from slicer.ScriptedLoadableModule import (
  ScriptedLoadableModule,
  ScriptedLoadableModuleLogic,
)

import PyTorchUtils


MRML_LABEL = 'vtkMRMLLabelMapVolumeNode'
MRML_SCALAR = 'vtkMRMLScalarVolumeNode'


class TorchIOModule(ScriptedLoadableModule):

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = 'TorchIO Abstract Module'
    self.parent.categories = []
    self.parent.dependencies = []
    self.parent.contributors = [
      "Fernando Perez-Garcia (University College London and King's College London)"
    ]
    self.parent.helpText = (
      'This module can be used to quickly visualize the effect of each'
      ' transform parameter. That way, users can have an intuitive feeling of'
      ' what the output of a transform looks like without any coding at all.\n\n'
    )
    self.parent.helpText += self.getDefaultModuleDocumentationLink()
    self.parent.acknowledgementText = (
      'This work was was funded by the Engineering and Physical Sciences'
      ' Research Council (EPSRC) and supported by the UCL Centre for Doctoral'
      ' Training in Intelligent, Integrated Imaging in Healthcare, the UCL'
      ' Wellcome / EPSRC Centre for Interventional and Surgical Sciences (WEISS),'
      ' and the School of Biomedical Engineering & Imaging Sciences (BMEIS)'
      " of King's College London."
    )

  def getDefaultModuleDocumentationLink(self):
    docsUrl = 'https://torchio.readthedocs.io/slicer.html'
    linkText = f'See <a href="{docsUrl}">the documentation</a> for more information.'
    return linkText


class TorchIOModuleLogic(ScriptedLoadableModuleLogic):
  def __init__(self):
    self._torchio = None
    self.torchLogic = PyTorchUtils.PyTorchUtilsLogic()

  @property
  def torchio(self):
    if self._torchio is None:
      logging.info('Importing torchio...')
      self._torchio = self.importTorchIO()
    return self._torchio

  def importTorchIO(self):
    if not self.torchLogic.torchInstalled():
      logging.info('PyTorch module not found')
      torch = self.torchLogic.installTorch(askConfirmation=True)
      if torch is None:
        slicer.util.errorDisplay(
          'PyTorch needs to be installed to use the TorchIO extension.'
          ' Please reload this module to install PyTorch.'
        )
        return
    try:
      import torchio
    except ModuleNotFoundError:
      with self.showWaitCursor(), self.peakPythonConsole():
        torchio = self.installTorchIO()
    logging.info(f'TorchIO {torchio.__version__} imported correctly')
    return torchio

  @staticmethod
  def installTorchIO(confirm=True):
    if confirm:
      install = slicer.util.confirmOkCancelDisplay(
        'TorchIO will be downloaded and installed now. The process might take some minutes.'
      )
      if not install:
        logging.info('Installation of TorchIO aborted by user')
        return None
    slicer.util.pip_install('torchio')
    import torchio
    logging.info(f'TorchIO {torchio.__version__} installed correctly')
    return torchio

  def getTorchIOImageFromVolumeNode(self, volumeNode):
    image = su.PullVolumeFromSlicer(volumeNode)
    tio = self.torchio
    if volumeNode.IsA('vtkMRMLScalarVolumeNode'):
      image = sitk.Cast(image, sitk.sitkFloat32)
      class_ = tio.ScalarImage
    elif volumeNode.IsA('vtkMRMLLabelMapVolumeNode'):
      class_ = tio.LabelMap
    tensor, affine = tio.io.sitk_to_nib(image)
    return class_(tensor=tensor, affine=affine)

  def getVolumeNodeFromTorchIOImage(self, image, outputVolumeNode=None):
    tio = self.torchio
    kwargs = {}
    if outputVolumeNode is None:
      kwargs = {'className': MRML_LABEL if isinstance(image, tio.LabelMap) else MRML_SCALAR}
    else:
      kwargs = {'targetNode': outputVolumeNode}
    su.PushVolumeToSlicer(image.as_sitk(), **kwargs)
    return outputVolumeNode

  def getPythonConsoleWidget(self):
    return slicer.util.mainWindow().pythonConsole().parent()

  @contextmanager
  def peakPythonConsole(self, show=True):
    if slicer.app.testingEnabled():
      show = False
    if show:
      console = self.getPythonConsoleWidget()
      pythonVisible = console.visible
      console.setVisible(True)
    yield
    if show:
      console.setVisible(pythonVisible)

  @contextmanager
  def showWaitCursor(self, show=True):
    if show:
      qt.QApplication.setOverrideCursor(qt.Qt.WaitCursor)
    yield
    if show:
      qt.QApplication.restoreOverrideCursor()

  def getNodesFromSubject(self, subject):
    nodes = {}
    for name, image in subject.get_images_dict(intensity_only=False).items():
      nodes[name] = self.getVolumeNodeFromTorchIOImage(image, name=name)
    return nodes

  def getColin(self, version=1998):
    colin = self.torchio.datasets.Colin27(version=version)
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
        label=nodes['cls'],
      )
