import qt
import slicer
import numpy as np

from .Transform import Transform


class RandomSpike(Transform):
    def setup(self):
        self.numSpikesSpinBox = qt.QSpinBox()
        self.numSpikesSpinBox.maximum = 10
        self.numSpikesSpinBox.value = self.getDefaultValue('num_spikes')
        self.layout.addRow('Spikes: ', self.numSpikesSpinBox)

        self.intensitySlider = slicer.qMRMLSliderWidget()
        self.intensitySlider.singleStep = 0.01
        self.intensitySlider.maximum = 5
        self.intensitySlider.value = np.mean(self.getDefaultValue('intensity'))
        self.layout.addRow('Intensity: ', self.intensitySlider)

    def getKwargs(self):
        kwargs = dict(
            num_spikes=self.numSpikesSpinBox.value,
            intensity=self.intensitySlider.value,
        )
        return kwargs
