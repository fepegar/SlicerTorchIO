import qt

from .Transform import Transform


class RandomMotion(Transform):
    def setup(self):
        degrees = self.getDefaultValue('degrees')
        self.degreesSlider = self.makeRangeWidget(
            -180, -degrees, degrees, 180, 1, 'degrees')
        self.layout.addRow('Degrees: ', self.degreesSlider)

        translation = self.getDefaultValue('translation')
        self.translationSlider = self.makeRangeWidget(
            -50, -translation, translation, 50, 1, 'translation')
        self.layout.addRow('Translation: ', self.translationSlider)

        self.numTransformsSpinBox = qt.QSpinBox()
        self.numTransformsSpinBox.maximum = 10
        self.numTransformsSpinBox.value = self.getDefaultValue('num_transforms')
        self.layout.addRow('Number of motions: ', self.numTransformsSpinBox)

        self.interpolationComboBox = self.makeInterpolationComboBox()
        self.layout.addRow('Interpolation: ', self.interpolationComboBox)

    def getKwargs(self):
        kwargs = dict(
            degrees=self.getSliderRange(self.degreesSlider),
            translation=self.getSliderRange(self.translationSlider),
            num_transforms=self.numTransformsSpinBox.value,
            image_interpolation=self.getInterpolation(),
        )
        return kwargs
