<!-- markdownlint-disable -->
<p align="center">
  <a href="http://torchio.rtfd.io/">
    <img src="https://raw.githubusercontent.com/fepegar/torchio/master/docs/source/favicon_io/for_readme_2000x462.png" alt="TorchIO logo">
  </a>
</p>
<!-- markdownlint-restore -->

> *Tools like TorchIO are a symptom of the maturation of medical AI research using deep learning techniques*.

Jack Clark, Policy Director
at [OpenAI](https://openai.com/) ([link](https://jack-clark.net/2020/03/17/)).

---

This repository contains the code for a [3D Slicer](https://www.slicer.org/)
extension that can be used to experiment with the
[TorchIO](https://torchio.readthedocs.io/) Python package without any coding.

<!-- markdownlint-disable -->
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
<!-- markdownlint-restore -->

## Installation

The extension can be installed using
[Extensions Manager](https://www.slicer.org/wiki/Documentation/4.10/SlicerApplication/ExtensionsManager).

## Continuous integration

The build status can be checked on [CDash](https://slicer.cdash.org/index.php?project=SlicerPreview&filtercount=1&showfilters=1&field1=buildname&compare1=63&value1=torchio).

## Credits

If you like this repository, please click on Star!

If you use this tool for your research, please cite our paper:

[F. Pérez-García, R. Sparks, and S. Ourselin. *TorchIO: a Python library for efficient loading, preprocessing, augmentation and patch-based sampling of medical images in deep learning*. Computer Methods and Programs in Biomedicine (June 2021), p. 106236. ISSN: 0169-2607.doi:10.1016/j.cmpb.2021.106236.](https://doi.org/10.1016/j.cmpb.2021.106236)

BibTeX entry:

```bibtex
@article{perez-garcia_torchio_2021,
    title = {TorchIO: a Python library for efficient loading, preprocessing, augmentation and patch-based sampling of medical images in deep learning},
    journal = {Computer Methods and Programs in Biomedicine},
    pages = {106236},
    year = {2021},
    issn = {0169-2607},
    doi = {https://doi.org/10.1016/j.cmpb.2021.106236},
    url = {https://www.sciencedirect.com/science/article/pii/S0169260721003102},
    author = {P{\'e}rez-Garc{\'i}a, Fernando and Sparks, Rachel and Ourselin, S{\'e}bastien},
}
```

This project is supported by the following institutions:

- [Engineering and Physical Sciences Research Council (EPSRC) & UK Research and Innovation (UKRI)](https://epsrc.ukri.org/)
- [EPSRC Centre for Doctoral Training in Intelligent, Integrated Imaging In Healthcare (i4health)](https://www.ucl.ac.uk/intelligent-imaging-healthcare/) (University College London)
- [Wellcome / EPSRC Centre for Interventional and Surgical Sciences (WEISS), University College London (UCL)](https://www.ucl.ac.uk/interventional-surgical-sciences/) (University College London)
- [School of Biomedical Engineering & Imaging Sciences (BMEIS), King's College London](https://www.kcl.ac.uk/bmeis) (King's College London)
