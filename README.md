# PixelBox

Application to measure desktop objects by dragging yellow rectangles that measure width and height in pixels.

[![Commit activity](https://img.shields.io/github/commit-activity/m/travisseymour/pixelbox)](https://img.shields.io/github/commit-activity/m/travisseymour/pixelbox)
[![License](https://img.shields.io/github/license/travisseymour/pixelbox)](https://img.shields.io/github/license/travisseymour/pixelbox)

The PixelBox application makes it easy to measure the extent of rectangular regions on your displays by using your mouse to draw dimension labeled yellow boxes. If you have multiple monitors, you can use the left/right arrow keys to move the drawing areas between monitors. In addition, you can use the number keys 1, 2, 3, 4 to move the PixelBox title window to the upper-left, upper-right, lower-left, and lower-right corners of the display. This is useful to measure areas that the title window obstructs.

Using the righ-click menu, you can clear the last box, all boxes, or save the box drawings to a PNG image on disk.

![gif of pixelbox usage](pixelbox/resources/pixelbox.gif)

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
