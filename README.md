# PixelBox

Application to measure desktop objects by dragging yellow rectangles that measure width and height in pixels.

[![Commit activity](https://img.shields.io/github/commit-activity/m/travisseymour/pixelbox)](https://img.shields.io/github/commit-activity/m/travisseymour/pixelbox)
[![License](https://img.shields.io/github/license/travisseymour/pixelbox)](https://img.shields.io/github/license/travisseymour/pixelbox)

This tool uses the Textual framework to display a scrollable table of search results from [flatpak](https://flatpak.org/). Use the arrow keys to select an entry and press ENTER to be prompted for installation.

- **Github repository**: <https://github.com/travisseymour/pixelbox/>

---

![gif of pixelbox usage](images/pixelbox.gif)

---

## Installation

### Preparation

1. Make sure you have [uv (preferred)](https://docs.astral.sh/uv/) or [PipX](https://pipx.pypa.io/stable/) installed.

2. Make sure you have Python 3.9 or higher installed. If you need to install a version of Python, you can use `uv` to do this, for example:
   
    To check to see which versions of Python you already have
   
   ```bash
   uv python list
   ```
   
    To install Python 3.11
   
   ```bash
   uv python install 3.11
   ```

### Installation

```bash
uv tool install git+https://github.com/travisseymour/pixelbox.git
```

or

```bash
pipx install git+https://github.com/travisseymour/pixelbox.git
```

### Upgrade

```bash
uv tool upgrade pixelbox
```

or

```bash
pipx upgrade pixelbox
```

### Removal

```bash
uv tool uninstall pixelbox
```

or 

```bash
pipx uninstall pixelbox
```
