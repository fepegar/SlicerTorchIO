import qt
import slicer

from .Transform import Transform


class RandomBiasField(Transform):
    def setup(self):
        self.coefficientsSlider = slicer.qMRMLSliderWidget()
        self.coefficientsSlider.singleStep = 0.01
        self.coefficientsSlider.maximum = 2
        self.coefficientsSlider.value = self.getDefaultValue('coefficients')
        self.layout.addRow('Coefficients: ', self.coefficientsSlider)

        self.orderSpinBox = qt.QSpinBox()
        self.orderSpinBox.maximum = 6
        self.orderSpinBox.value = self.getDefaultValue('order')
        self.layout.addRow('Polynomial order: ', self.orderSpinBox)

    def getKwargs(self):
        kwargs = dict(
            coefficients=self.coefficientsSlider.value,
            order=self.orderSpinBox.value,
        )
        return kwargs
