from .Transform import Transform


class RandomBlur(Transform):
    def setup(self):
        stds = self.getDefaultValue('std')
        self.stdSlider = self.makeRangeWidget(0, *stds, 5, 0.01, 'std')
        self.layout.addRow('Standard deviation: ', self.stdSlider)

    def getKwargs(self):
        kwargs = dict(
            std=self.getSliderRange(self.stdSlider),
        )
        return kwargs
