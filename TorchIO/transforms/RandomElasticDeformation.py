import qt

from .Transform import Transform
from .CoordinatesWidget import CoordinatesWidget


class RandomElasticDeformation(Transform):
    def setup(self):
        self.controlPointsWidget = CoordinatesWidget(
            decimals=0,
            coordinates=self.getDefaultValue('num_control_points'),
        )
        self.layout.addRow('Control points: ', self.controlPointsWidget.widget)

        self.maxDisplacementWidget = CoordinatesWidget(
            decimals=2,
            coordinates=self.getDefaultValue('max_displacement'),
            step=0.1,
        )
        self.layout.addRow('Maximum displacement: ', self.maxDisplacementWidget.widget)

        self.lockedBordersSpinBox = qt.QSpinBox()
        self.lockedBordersSpinBox.maximum = 2
        self.lockedBordersSpinBox.value = self.getDefaultValue('locked_borders')
        self.layout.addRow('Locked borders: ', self.lockedBordersSpinBox)

        self.interpolationComboBox = self.makeInterpolationComboBox()
        self.layout.addRow('Interpolation: ', self.interpolationComboBox)

        # arg = 'default_pad_value'
        # self.padLineEdit = qt.QLineEdit(self.getDefaultValue(arg))
        # self.padLineEdit.setToolTip(self.getArgDocstring(arg))
        # self.layout.addRow('Padding: ', self.padLineEdit)

    # def getPadArg(self):
    #     text = self.padLineEdit.text
    #     try:
    #         value = float(text)
    #     except ValueError:
    #         value = text
    #     return value

    def getKwargs(self):
        kwargs = dict(
            num_control_points=self.controlPointsWidget.getCoordinates(),
            max_displacement=self.maxDisplacementWidget.getCoordinates(),
            locked_borders=self.lockedBordersSpinBox.value,
            image_interpolation=self.getInterpolation(),
            # default_pad_value=self.getPadArg(),
        )
        return kwargs
