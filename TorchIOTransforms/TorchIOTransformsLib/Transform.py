import inspect
import importlib

import qt
import ctk
import slicer
import numpy as np
import sitkUtils as su

import torch
import torchio


class Transform:
    def __init__(self):
        self.groupBox = qt.QGroupBox('Parameters')
        self.layout = qt.QFormLayout(self.groupBox)
        self.setup()

    def getHelpLink(self):
        docs = 'https://torchio.readthedocs.io'
        type_ = self.transformType
        return f'{docs}/transforms/{self.transformType}.html#torchio.transforms.{self.name}'

    def setup(self):
        raise NotImplementedError

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def transformType(self):
        return 'augmentation' if self.name.startswith('Random') else 'preprocessing'

    def show(self):
        self.groupBox.show()

    def hide(self):
        self.groupBox.hide()

    def getTransformClass(self):
        klass = getattr(importlib.import_module('torchio'), self.name)
        return klass

    def getArgs(self):
        return ()

    def getKwargs(self):
        return {}

    def getTransform(self):
        klass = self.getTransformClass()
        args = self.getArgs()
        kwargs = self.getKwargs()
        return klass(*args, **kwargs)

    def makeInterpolationComboBox(self):
        from torchio.transforms.interpolation import Interpolation
        values = [key.name.lower().capitalize() for key in Interpolation]
        comboBox = qt.QComboBox()
        comboBox.addItems(values)
        comboBox.setCurrentIndex(1)  # linear
        comboBox.setToolTip(self.getArgDocstring('image_interpolation'))
        return comboBox

    def getInterpolation(self):
        return self.interpolationComboBox.currentText.lower()

    def makeRangeWidget(self, minimum, minimumValue, maximumValue, maximum, step, name):
        slider = slicer.qMRMLRangeWidget()
        slider.minimum = minimum
        slider.maximum = maximum
        slider.minimumValue = minimumValue
        slider.maximumValue = maximumValue
        slider.singleStep = step
        slider.setToolTip(self.getArgDocstring(name))
        slider.symmetricMoves = True
        return slider

    def makeAxesLayout(self):
        layout = qt.QHBoxLayout()
        axesDict = {n: qt.QCheckBox(str(n)) for n in range(3)}
        for widget in axesDict.values():
            widget.setChecked(True)
            layout.addWidget(widget)
        return layout, axesDict

    def getSignature(self):
        klass = self.getTransformClass()
        return inspect.signature(klass)

    def getDefaultValue(self, kwarg):
        signature = self.getSignature()
        return signature.parameters[kwarg].default

    def getDocstring(self):
        return inspect.getdoc(self.getTransformClass())

    def getArgDocstring(self, arg):
        # TODO: learn regex
        lines = self.getDocstring().splitlines()
        line = [line for line in lines if line.startswith(f'    {arg}:')][0]
        index = lines.index(line)
        line = line.replace(f'{arg}: ', '')
        argLines = [line]
        for line in lines[index + 1:]:
            if line.startswith(8 * ' '):
                break
            argLines.append(line)
        return '\n'.join(argLines)

    def getSliderRange(self, slider):
        return slider.minimumValue, slider.maximumValue

    def __call__(self, inputVolumeNode, outputVolumeNode):
        image = su.PullVolumeFromSlicer(inputVolumeNode)
        data, affine = torchio.utils.sitk_to_nib(image)
        tensor = torch.from_numpy(data.astype(np.float32))  # why do I need this? Open a TorchIO issue?
        if inputVolumeNode.IsA('vtkMRMLScalarVolumeNode'):
            image = torchio.ScalarImage(tensor=tensor, affine=affine)
        elif inputVolumeNode.IsA('vtkMRMLLabelMapVolumeNode'):
            image = torchio.LabelMap(tensor=tensor, affine=affine)
        transformed = self.getTransform()(image)
        image = torchio.utils.nib_to_sitk(transformed.data, transformed.affine)
        su.PushVolumeToSlicer(image, targetNode=outputVolumeNode)
        return outputVolumeNode
