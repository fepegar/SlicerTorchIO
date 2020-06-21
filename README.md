# TorchIO

This repository contains the code for a [3D Slicer](https://www.slicer.org/)
extension that can be used to experiment with the
[TorchIO](https://torchio.readthedocs.io/) Python package without any coding.

<table align="center">
    <tr>
        <td align="center">Original</td>
        <td align="center">
            <a href="http://torchio.rtfd.io/transforms/augmentation.html#randomblur">Random blur</a>
        </td>
    </tr>
    <tr>
        <td align="center"><img src="https://raw.githubusercontent.com/fepegar/torchio/master/docs/images/gifs_readme/1_Lambda_mri.png" alt="Original"></td>
        <td align="center">
            <a href="http://torchio.rtfd.io/transforms/augmentation.html#randomblur">
                <img src="https://raw.githubusercontent.com/fepegar/torchio/master/docs/images/gifs_readme/2_RandomBlur_mri.gif" alt="Random blur">
            </a>
        </td>
    </tr>
    <tr>
        <td align="center">
            <a href="http://torchio.rtfd.io/transforms/augmentation.html#randomflip">Random flip</a>
        </td>
        <td align="center">
            <a href="http://torchio.rtfd.io/transforms/augmentation.html#randomnoise">Random noise</a>
        </td>
    </tr>
    <tr>
        <td align="center">
            <a href="http://torchio.rtfd.io/transforms/augmentation.html#randomflip">
                <img src="https://raw.githubusercontent.com/fepegar/torchio/master/docs/images/gifs_readme/3_RandomFlip_mri.gif" alt="Random flip">
            </a>
        </td>
        <td align="center">
            <a href="http://torchio.rtfd.io/transforms/augmentation.html#randomnoise">
                <img src="https://raw.githubusercontent.com/fepegar/torchio/master/docs/images/gifs_readme/4_Compose_mri.gif" alt="Random noise">
            </a>
        </td>
    </tr>
    <tr>
        <td align="center">
            <a href="http://torchio.rtfd.io/transforms/augmentation.html#randomaffine">Random affine transformation</a>
        </td>
        <td align="center">
            <a href="http://torchio.rtfd.io/transforms/augmentation.html#randomelasticdeformation">Random elastic transformation</a>
        </td>
    </tr>
    <tr>
        <td align="center">
            <a href="http://torchio.rtfd.io/transforms/augmentation.html#randomaffine">
                <img src="https://raw.githubusercontent.com/fepegar/torchio/master/docs/images/gifs_readme/5_RandomAffine_mri.gif" alt="Random affine transformation">
            </a>
        </td>
        <td align="center">
            <a href="http://torchio.rtfd.io/transforms/augmentation.html#randomelasticdeformation">
                <img src="https://raw.githubusercontent.com/fepegar/torchio/master/docs/images/gifs_readme/6_RandomElasticDeformation_mri.gif" alt="Random elastic transformation">
            </a>
        </td>
    </tr>
    <tr>
        <td align="center">
            <a href="http://torchio.rtfd.io/transforms/augmentation.html#randombiasfield">Random bias field artifact</a>
        </td>
        <td align="center">
            <a href="http://torchio.rtfd.io/transforms/augmentation.html#randommotion">Random motion artifact</a>
        </td>
    </tr>
    <tr>
        <td align="center">
            <a href="http://torchio.rtfd.io/transforms/augmentation.html#randombiasfield">
                <img src="https://raw.githubusercontent.com/fepegar/torchio/master/docs/images/gifs_readme/7_RandomBiasField_mri.gif" alt="Random bias field artifact">
            </a>
        </td>
        <td align="center">
            <a href="http://torchio.rtfd.io/transforms/augmentation.html#randommotion">
                <img src="https://raw.githubusercontent.com/fepegar/torchio/master/docs/images/gifs_readme/8_RandomMotion_mri.gif" alt="Random motion artifact">
            </a>
        </td>
    </tr>
    <tr>
        <td align="center">
            <a href="http://torchio.rtfd.io/transforms/augmentation.html#randomspike">Random spike artifact</a>
        </td>
        <td align="center">
            <a href="http://torchio.rtfd.io/transforms/augmentation.html#randomghosting">Random ghosting artifact</a>
        </td>
    </tr>
    <tr>
        <td align="center">
            <a href="http://torchio.rtfd.io/transforms/augmentation.html#randomspike">
                <img src="https://raw.githubusercontent.com/fepegar/torchio/master/docs/images/gifs_readme/9_RandomSpike_mri.gif" alt="Random spike artifact">
            </a>
        </td>
        <td align="center">
            <a href="http://torchio.rtfd.io/transforms/augmentation.html#randomghosting">
                <img src="https://raw.githubusercontent.com/fepegar/torchio/master/docs/images/gifs_readme/10_RandomGhosting_mri.gif" alt="Random ghosting artifact">
            </a>
        </td>
    </tr>
</table>

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
