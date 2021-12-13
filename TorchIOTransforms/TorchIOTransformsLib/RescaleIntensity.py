import qt

from .Transform import Transform


class RescaleIntensity(Transform):
    def setup(self):
        outMinMax = self.getDefaultValue('out_min_max')
        self.outMinMaxSlider = self.makeRangeWidget(-1, *outMinMax, 1, 0.01, 'out_min_max')
        self.layout.addRow('Output range: ', self.outMinMaxSlider)

        percentiles = self.getDefaultValue('percentiles')
        self.percentilesSlider = self.makeRangeWidget(0, *percentiles, 100, 0.01, 'percentiles')
        self.layout.addRow('Cut-off percentiles: ', self.percentilesSlider)

        # inMinMax = self.getDefaultValue('in_min_max')
        # self.inMinMaxSlider = self.makeRangeWidget(-1, *inMinMax, 1, 0.01, 'in_min_max')
        # self.layout.addRow('inMinMax: ', self.inMinMaxSlider)

    def getKwargs(self):
        kwargs = dict(
            out_min_max=self.getSliderRange(self.outMinMaxSlider),
            percentiles=self.getSliderRange(self.percentilesSlider),
            # in_min_max=self.getSliderRange(self.inMinMaxSlider),
        )
        return kwargs
