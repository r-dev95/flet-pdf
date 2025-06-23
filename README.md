<!-- ============================================================
  Project Image
 ============================================================ -->
<div align=center>
  <img
    src='docs/image/demo.gif'
    alt='Project Image.'
    width=500
  />
</div>

<!-- ============================================================
  Overview
 ============================================================ -->
# :book:Overview

<!-- [![English](https://img.shields.io/badge/English-018EF5.svg?labelColor=d3d3d3&logo=readme)](./README.md) -->
<!-- [![Japanese](https://img.shields.io/badge/Japanese-018EF5.svg?labelColor=d3d3d3&logo=readme)](./README_JA.md) -->
[![English](https://img.shields.io/badge/English-018EF5.svg?labelColor=d3d3d3&logo=readme)](./README.md)
[![license](https://img.shields.io/github/license/r-dev95/flet-pdf-app)](./LICENSE)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

[![Python](https://img.shields.io/badge/Python-3776AB.svg?labelColor=d3d3d3&logo=python)](https://github.com/python)
[![Sphinx](https://img.shields.io/badge/Sphinx-000000.svg?labelColor=d3d3d3&logo=sphinx&logoColor=000000)](https://github.com/sphinx-doc/sphinx)
[![Pytest](https://img.shields.io/badge/Pytest-0A9EDC.svg?labelColor=d3d3d3&logo=pytest)](https://github.com/pytest-dev/pytest)
[![Pydantic](https://img.shields.io/badge/Pydantic-ff0055.svg?labelColor=d3d3d3&logo=pydantic&logoColor=ff0055)](https://github.com/pydantic/pydantic)

This repository is an app using [Flet][flet] to merge, split and extract pages from pdf files.

[flet]: https://flet.dev/

<!-- ============================================================
  Features
 ============================================================ -->
## :desktop_computer:Features

<div align=center>
  <img
    src='docs/image/app.png'
    alt='The App screen.'
    width=500
  />
</div>

|Item                            |Feature                              |
| ---                            | ---                                 |
|Select button                   |Select files.                        |
|Delete button                   |Delete all files.                    |
|Merge button                    |Merge files.                         |
|Split button                    |Split all pages of the file.         |
|Extract button                  |Enter the pages you want to extract. |
|Text area (top right of screen) |Extract pages from the file.         |
|Text area (File Path List)      |Display the selected file.           |
|Text area (Log)                 |Display the logs.                    |

> [!note]
> **Text area (top right of screen)**
>
> You can enter numbers separated by commas.
>
> You can also use hyphens to connect consecutive numbers.
>
> You can enter numbers connected with multiple hyphens, such as `10-5-15`, which is the same as `5-15`.
>
> Correct Example:
>
> ``` None
> 1,5,10-15,20,40-35,50-55-45
> ```
>
> Incorrect Example:
>
> ``` None
> 1,
> ```
>
> ``` None
> ,1
> ```
>
> ``` None
> 10-
> ```
>
> ``` None
> -10
> ```

<!-- ============================================================
  Usage
 ============================================================ -->
## :keyboard:Usage

### Install

```bash
git clone https://github.com/r-dev95/flet-pdf-app.git
```

### Build virtual environment

You need to install `uv`.

If you don't have a python development environment yet, see [here](https://github.com/r-dev95/env-python).

```bash
cd flet-pdf-app/
uv sync
```

### Run

```bash
cd src
uv run flet run app.py       # In Desktop mode
uv run flet run app.py --web # In Web mode
```

- Press the `Select` button and select files.

  When a file is selected, the `File Path List` displays the selected file and a corresponding :wastebasket: button.

  Files displayed in the `File Path List` can be reordered by drag and drop.

  Pressing the :wastebasket: button will delete the corresponding file.

- Press the `Merge` button and all files will be merged.

- Pressing the `Split` button will split all pages from the file.

- Pressing the `Extract` button will extract pages from the file.

  Enter the form (`Number of pages to Extract`) to select the pages you want to extract.

- Pressing the `Delete` button at the top of the screen will delete all files displayed in the `File Path List` (, not directory).

> [!note]
> **In Web mode:**
>
> When selecting a file, the file path cannot be obtained, so the selected file must be in the same directory as `app.py`.
>
> **In Desktop mode:**
>
> When selecting a file, you can get the file path, so it doesn't matter where the file is located.
>
> However, this doesn't work well when launching the app in a virtual environment like WSL.

<!-- ============================================================
  Structure
 ============================================================ -->
## :bookmark_tabs:Structure

<div align=center>
  <img
    src='docs/image/classes.png'
    alt='classes.'
  />
</div>

<!-- ============================================================
  License
 ============================================================ -->
## :key:License

This repository is licensed under the [BSD 3-Clause](LICENSE).
