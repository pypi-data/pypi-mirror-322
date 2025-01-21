# BioProcessNexus
The BioProcessNexus is a project to enable free sharing of techno economic process models and life cycle analsis via surrogate models. The heartpieces of the project are an open-source python software for the generation and analysis of surrogate models and a data repository containing Monte-Carlo data from original models as well as pre-trained surrogate models.

For more information visit the [documentation](https://bioprocessnexus.readthedocs.io/en/latest/)!

## Installation

### Executable

The BioProcessNexus can be launched directly by downloading bioprocess.exe from [here](https://drive.boku.ac.at/d/3e0e8e499c7c402190de/).

### PyPi

You can install the development version of the BioProcessNexus from PyPi with:

```
pip install bioprocessnexus
```

All dependencies can be found in the requirements.txt file and be installed with:

```
pip install -r path/to/requirements.txt
```

after downloading the file.

The GUI can the be launched by importing the bioprocessnexus and running bioprocessnexus.launch_nexus() in python:

``` python
import bioprocessnexus
bioprocessnexus.launch_nexus()
```

