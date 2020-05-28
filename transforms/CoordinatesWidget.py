import ctk

class CoordinatesWidget:
    def __init__(self, decimals=0, coordinates=(0, 0, 0), step=1):
        self.widget = ctk.ctkCoordinatesWidget()
        self.widget.decimals = decimals
        self.widget.singleStep = step
        self.decimals = decimals
        self.setCoordinates(coordinates)

    def getCoordinates(self):
        return self._stringToCoords(self.widget.coordinates)

    def setCoordinates(self, coordinates):
        if not isinstance(coordinates, tuple):
            coordinates = 3 * (coordinates,)
        self.widget.coordinates = self._coordsToString(coordinates)

    def _coordsToString(self, coordinates):
        return ','.join(str(n) for n in coordinates)

    def _stringToCoords(self, string):
        cast = int if self.decimals == 0 else float
        return tuple([cast(n) for n in string.split(',')])
