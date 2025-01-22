# 2adif

[![CI](https://github.com/uiolee/2adif/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/uiolee/2adif/actions/workflows/ci.yml)
[![Publish](https://github.com/uiolee/2adif/actions/workflows/publish.yml/badge.svg)](https://github.com/uiolee/2adif/actions/workflows/publish.yml)

Convert tables to [ADIF](https://adif.org/) format.

## Feat

- [x] convert `csv` to `adi` format.
- [ ] convert `xlsx` to `adi` format.
- [ ] convert `ods` to `adi` format.

## Usage

[![PyPI - Version](https://img.shields.io/pypi/v/2adif)](https://pypi.org/p/2adif/#history)
[![PyPI - Status](https://img.shields.io/pypi/status/2adif)](https://pypi.org/p/2adif)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/2adif)](https://pypi.org/p/2adif)
[![PyPI - Format](https://img.shields.io/pypi/format/2adif)](https://pypi.org/p/2adif/#files)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/2adif)](https://pypi.org/p/2adif/#files)
[![PyPI - License](https://img.shields.io/pypi/l/2adif)](./LICENSE)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/2adif)](https://pypi.org/p/2adif)

### pipx

#### Install

```bash
pipx install 2adif
```

#### convert `csv` to `adi`

- Convert the specified `csv` file

  ```bash
  2adif ./test/test.csv
  ```

- Convert all csv files in the specified directory

  ```bash
  2adif ./test/
  ```

### source

<details>
<summary>source</summary>

#### Python

see [./src/main.py](./src/main.py#L140) for more.

</details>

## Develop Env

```plain
Python 3.11.9
```
