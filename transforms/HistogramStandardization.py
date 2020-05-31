import qt
import slicer

from .Transform import Transform
from .CoordinatesWidget import CoordinatesWidget


class HistogramStandardization(Transform):
    def setup(self):
        self.landmarksLineEdit = qt.QLineEdit()
        self.layout.addRow('Path to landmarks: ', self.landmarksLineEdit)

    def getArgs(self):
        path = arg = self.landmarksLineEdit.text
        if path.endswith('.npy'):  # I should modify the transform to accept this
            import numpy as np
            arg = {'img': np.load(path)}
        return arg,
