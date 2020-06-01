import qt
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

    def getKwargs(self):
        kwargs = dict(
            num_ghosts=self.numGhostsSpinBox.value,
            axes=tuple([n for n in range(3) if self.axesDict[n].isChecked()]),
        )
        return kwargs
