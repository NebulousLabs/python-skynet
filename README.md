# Skynet Python SDK

> :warning: This repo has been archived and moved under the new [SkynetLabs](https://github.com/SkynetLabs) repo [here](https://github.com/SkynetLabs/python-skynet)

[![Version](https://img.shields.io/pypi/v/siaskynet)](https://pypi.org/project/siaskynet)
[![Python](https://img.shields.io/pypi/pyversions/siaskynet)](https://pypi.org/project/siaskynet)
[![Build Status](https://img.shields.io/github/workflow/status/NebulousLabs/python-skynet/Pull%20Request)](https://github.com/NebulousLabs/python-skynet/actions)
[![Contributors](https://img.shields.io/github/contributors/NebulousLabs/python-skynet)](https://github.com/NebulousLabs/python-skynet/graphs/contributors)
[![License](https://img.shields.io/pypi/l/siaskynet)](https://pypi.org/project/siaskynet)

An SDK for integrating Skynet into Python applications.

## Instructions

We recommend running your Python application using [pipenv](https://pipenv-searchable.readthedocs.io/basics.html).

You can use `siaskynet` by installing it with `pip`, adding it to your project's `Pipfile`, or by cloning this repository.

## Documentation

For documentation complete with examples, please see [the Skynet SDK docs](https://siasky.net/docs/?python#introduction).

## Contributing

### Requirements

In order to run lints and tests locally you will need to:

1. Check out the repository locally.
2. Make sure you have `make` installed (on Windows you can use [Chocolatey](https://chocolatey.org/) and run `choco install make`).

### Instructions

To run lints and tests on `python-skynet`, first install dependencies:

```
make install
```

Now you can run

```
pipenv run lint
```

or

```
pipenv run test
```
