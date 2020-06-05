import qt
import slicer
import numpy as np

from .Transform import Transform
from .CoordinatesWidget import CoordinatesWidget


class RandomGhosting(Transform):
    def setup(self):
        self.numGhostsSpinBox = qt.QSpinBox()
        self.numGhostsSpinBox.maximum = 50
        default = int(np.mean(self.getDefaultValue('num_ghosts')))
        self.numGhostsSpinBox.value = default
        self.layout.addRow('Ghosts: ', self.numGhostsSpinBox)

        self.axesLayout, self.axesDict = self.makeAxesLayout()
        self.layout.addRow('Axes: ', self.axesLayout)

        self.intensitySlider = slicer.qMRMLSliderWidget()
        self.intensitySlider.singleStep = 0.01
        self.intensitySlider.maximum = 1
        self.intensitySlider.value = np.mean(self.getDefaultValue('intensity'))
        self.layout.addRow('Intensity: ', self.intensitySlider)

    def getKwargs(self):
        kwargs = dict(
            num_ghosts=self.numGhostsSpinBox.value,
            axes=tuple([n for n in range(3) if self.axesDict[n].isChecked()]),
            intensity=2 * (self.intensitySlider.value,),
        )
        return kwargs
