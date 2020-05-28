# SlicerTorchIO

## Installation

If this repo is in `~/git/SlicerTorchIO`, write in `~/.slicerrc.py`:

```python
from pathlib import Path

modulePath = Path('~/git/SlicerTorchIO/TorchIO.py').expanduser()
moduleFactory = slicer.app.moduleManager().factoryManager()
moduleFactory.registerModule(qt.QFileInfo(str(modulePath)))
moduleFactory.loadModules([modulePath.stem])
```

And open 3D Slicer.
