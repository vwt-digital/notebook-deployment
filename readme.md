# Notebook deployment

This project helps you set up a GCP project containing a jupyter notebook within the Operational Data Hub of Volkerwessels Telecom

## Getting Started

### Prerequisites

To create all the configuration files a [Cookiecutter](https://cookiecutter.readthedocs.io/) has been created.

Install Cookiecutter using:

```
pip install cookiecutter
```

## Generate the config files

Open a terminal in the folder where you want to output the generated files, a new directory will be created.

To generate the config files using the Cookiecutter execute the following command:

```
cookiecutter https://github.com/vwt-digital/notebook-deployment.git
```

This will use this repository as a template. If you want to use the development branch use:

```
cookiecutter https://github.com/vwt-digital/notebook-deployment.git --checkout develop
```

## Use the generated files

Follow the instructions that are in the readme.md of the generated folder.
