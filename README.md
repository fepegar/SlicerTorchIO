# TorchIO

This repository contains the code for a 3D Slicer extension that can be used to
experiment with the [TorchIO](https://torchio.readthedocs.io/) Python package.

## Installation

### Extensions Manager

In the near future, it will be possible to install the extension using the
[Extensions Manager](https://www.slicer.org/wiki/Documentation/4.10/SlicerApplication/ExtensionsManager).

### Cloning this repository

If this repo is in `~/git/SlicerTorchIO`, write in `~/.slicerrc.py`:

```python
from pathlib import Path

modulePath = Path('~/git/SlicerTorchIO/TorchIO.py').expanduser()
moduleFactory = slicer.app.moduleManager().factoryManager()
moduleFactory.registerModule(qt.QFileInfo(str(modulePath)))
moduleFactory.loadModules([modulePath.stem])
```

and open 3D Slicer. You can search the modules hitting `Ctrl + F` and typing
`TorchIO`.
