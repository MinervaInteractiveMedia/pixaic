### pixaic

A small python program that applies photomosaic to a target image extracting tiles from a source image.
<img width="1920" height="2480" alt="yoyoyoy" src="https://github.com/user-attachments/assets/387353d6-3dc0-4a5e-b901-3dff5b4c4722" />

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
<img width="1920" height="1270" alt="yoo" src="https://github.com/user-attachments/assets/b23a01fb-7e8b-480a-b99f-e615277c16a9" />

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
