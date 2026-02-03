### pixaic

A small python program that applies photomosaic to a target image extracting tiles from a source image.

---

## Quick Start

```bash
# Required
pip install pillow numpy
python pixaic.py
```

---

## What's Inside

| File | Role |
|---|---|
| `pixaic.py` | The main python script |
| `pixaic.app` | MACOS executable |


---

## Features

Load a target image (the image you want to recreate)
Load a tile image (the image whose tiles will be used)
Adjustable tile size (5-100 pixels)
Adjustable output width (200-3000 pixels)
Real-time preview of the generated photomosaic
Export to PNG or JPEG

---

## How to Use

Extracts random tiles from the source image (default: 1000 tiles)
Each tile's average RGB color is calculated
For each position in the target image, it finds the tile with the closest matching average color
Places that actual tile (not a tinted version)

New Settings:

Tiles to Extract: How many random tiles to grab from the source (100-10000)
Matching Mode:

"average" - Simple RGB distance
"weighted" - Perceptually weighted (gives more weight to green, which humans see better)



How to use:

Select your target image (what you want to recreate)
Select your source image (where tiles come from)
Adjust tile size and number of tiles to extract
Generate!
