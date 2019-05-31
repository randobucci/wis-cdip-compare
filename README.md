# WIS-CDIP Comparisons  #

This repository contains python code to conduct comparisons between USACED WIS model and-CDIP buoys. The code are in form of interactive [Jupyter Notebooks](https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/What%20is%20the%20Jupyter%20Notebook.html). You can either: view code online or run interactively 

## View the code online ##

The links below will render the notebooks via the [nbviewer](http://nbviewer.jupyter.org/) service.

### Python Notebooks
* [1: WIS-CDIP-Test](https://nbviewer.jupyter.org/github/randobucci/wis-cdip-compare/blob/master/export/WIS-CDIP-Test.ipynb)
* [2: WIS-CDIP-Aggregate](https://nbviewer.jupyter.org/github/randobucci/wis-cdip-compare/blob/master/export/WIS-CDIP-Aggregate.ipynb)
* [3: WIS-CDIP-Compare](https://nbviewer.jupyter.org/github/randobucci/wis-cdip-compare/blob/master/export/WIS-CDIP-Aggregate.ipynb)

## Run the code interactively ##

Use git to [clone this repository](git clone https://github.com/randobucci/wis-cdip-compare.git). If you don't have git already on you computer, it is easy to install on all platforms following [these instructions](https://www.atlassian.com/git).

From the command line, run the command

```bash
git clone https://github.com/randobucci/wis-cdip-compare.git
```

Once you have the repository cloned, you can update it periodically to match master repo

```bash
git pull origin master
```

In order to execute the code in the notebooks, you need to have the necessary python packages installed.
The recommended way to do this is to install the [anaconda python distribution](https://www.anaconda.com/download/) together with the [conda package management utility](https://conda.io/docs/).
For more depth, you can read my [detailed intstructions for installing python](https://rabernat.github.io/research_computing/python.html).

This repository includes an [environment file](https://github.com/rabernat/intro_to_physical_oceanography/blob/master/phys_ocean_env.yml) which you can use to set up your python environment. To install this environment, type the following

```bash
cd wis-compare
conda env create -f phys_ocean_env.yml
```

This will create a new environment called `phys_ocean`. To activate this environment, type

```bash
source activate phys_ocean
```

The notebooks can be viewed and run using the [jupyter notebook](https://jupyter-notebook.readthedocs.io/en/stable/notebook.html) application. To launch the notebook interface, just type

```bash
jupyter notebook
```

When you are done working with the notebooks, close the notebook app and, if you wish, deactive the environment by typing

```bash
source deactivate
```

