# TorchIO

> *Tools like TorchIO are a symptom of the maturation of medical AI research using deep learning techniques*.

Jack Clark, Policy Director
at [OpenAI](https://openai.com/) ([link](https://jack-clark.net/2020/03/17/)).

---

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

### Option 1: Extensions Manager

The extension can be installed using
[Extensions Manager](https://www.slicer.org/wiki/Documentation/4.10/SlicerApplication/ExtensionsManager).

### Option 2: cloning this repository

If you would like to apply changes to the module locally, you can clone this
repository and add the path to the Slicer modules.

#### Add module programmatically

If this repo is in `~/git/SlicerTorchIO`, add this to `~/.slicerrc.py`:

```python
from pathlib import Path

repoDir = Path('~/git/SlicerTorchIO/').expanduser()
moduleDir = repoDir / 'TorchIOTransforms'
modulePath = moduleDir / 'TorchIO.py'
moduleFactory = slicer.app.moduleManager().factoryManager()
moduleFactory.registerModule(qt.QFileInfo(str(modulePath)))
moduleFactory.loadModules([modulePath.stem])
```

and open 3D Slicer. You can search the modules hitting `Ctrl + F` and typing
`TorchIO`.

#### In Slicer settings

Add the module to the additional module paths, as explained in the
[Slicer wiki](https://www.slicer.org/wiki/Documentation/4.10/SlicerApplication/ApplicationSettings#Additional_module_paths).

## Credits

If you like this repository, please click on Star!

If you use this tool for your research, please cite the paper:

> [Pérez-García, F., Sparks, R., Ourselin, S.: TorchIO: a Python library for efficient
loading, preprocessing, augmentation and patch-based sampling of medical images
in deep learning. arXiv:2003.04696 [cs, eess, stat] (Mar 2020), http://arxiv.org/abs/2003.04696, arXiv: 2003.04696](http://arxiv.org/abs/2003.04696)

BibTeX entry:

```bibtex
@article{perez-garcia_torchio_2020,
    title = {{TorchIO}: a {Python} library for efficient loading, preprocessing, augmentation and patch-based sampling of medical images in deep learning},
    shorttitle = {{TorchIO}},
    url = {http://arxiv.org/abs/2003.04696},
    urldate = {2020-03-11},
    journal = {arXiv:2003.04696 [cs, eess, stat]},
    author = {P{\'e}rez-Garc{\'i}a, Fernando and Sparks, Rachel and Ourselin, Sebastien},
    month = mar,
    year = {2020},
    note = {arXiv: 2003.04696},
    keywords = {Computer Science - Computer Vision and Pattern Recognition, Electrical Engineering and Systems Science - Image and Video Processing, Computer Science - Machine Learning, Computer Science - Artificial Intelligence, Statistics - Machine Learning},
}
```
