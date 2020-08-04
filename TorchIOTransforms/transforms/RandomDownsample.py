import slicer
import numpy as np

from .Transform import Transform
from .CoordinatesWidget import CoordinatesWidget


class RandomDownsample(Transform):
    def setup(self):
        self.axesLayout, self.axesDict = self.makeAxesLayout()
        self.layout.addRow('Axes: ', self.axesLayout)

        a, b = self.getDefaultValue('downsampling')
        self.downsamplingSlider = self.makeRangeWidget(
            1, a, b, 10, 0.01, 'downsampling')
        self.layout.addRow('Downsampling factor: ', self.downsamplingSlider)

    def getKwargs(self):
        kwargs = dict(
            axes=tuple([n for n in range(3) if self.axesDict[n].isChecked()]),
            downsampling=self.getSliderRange(self.downsamplingSlider),
        )
        return kwargs
