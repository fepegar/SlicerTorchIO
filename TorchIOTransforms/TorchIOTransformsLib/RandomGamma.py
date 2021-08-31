from .Transform import Transform


class RandomGamma(Transform):
    def setup(self):
        logs = self.getDefaultValue('log_gamma')
        self.logGammaSlider = self.makeRangeWidget(-2, *logs, 2, 0.01, 'log_gamma')
        self.layout.addRow('Log of gamma: ', self.logGammaSlider)

    def getKwargs(self):
        kwargs = dict(
            log_gamma=self.getSliderRange(self.logGammaSlider),
        )
        return kwargs
