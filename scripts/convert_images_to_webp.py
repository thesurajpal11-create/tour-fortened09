#!/usr/bin/env python3
"""Batch convert selected images to WEBP for the site.

Run from repository root:
  python scripts/convert_images_to_webp.py

Requires Pillow: pip install pillow
"""
from pathlib import Path
from PIL import Image

CONVERSIONS = {
    'images/ram_temple_1694583470615_1694583503125.jpg': 'images/ram-mandir-ayodhya.webp',
    'images/ayodhya.jpg': 'images/ayodhya-heritage.webp',
    'images/Hanuman_Garhi_Mandir_Ayodhya.jpg': 'images/hanuman-garhi-ayodhya.webp',
    'images/kanak-bhawan.png': 'images/kanak-bhawan-ayodhya.webp',
    'images/Nageshwarnath-Temple.jpg': 'images/nageshwarnath-temple-ayodhya.webp',
    'images/Dashrath-Mahal-Ayodhya-2.jpg': 'images/dashrath-mahal-ayodhya.webp',
    'images/AYODHYA MARKET.jpg': 'images/ayodhya-market.webp',
    'images/heritage.jpg': 'images/ayodhya-heritage-illustration.webp',
}

ROOT = Path(__file__).resolve().parents[1]

def convert_all():
    for src_rel, dst_rel in CONVERSIONS.items():
        src = ROOT / src_rel
        dst = ROOT / dst_rel
        if not src.exists():
            print(f'Missing source: {src_rel}')
            continue
        if dst.exists():
            print(f'Already exists: {dst_rel}')
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            with Image.open(src) as img:
                img = img.convert('RGB')
                img.save(dst, 'WEBP', quality=85, method=6)
            print(f'Converted {src_rel} -> {dst_rel}')
        except Exception as e:
            print(f'Error converting {src_rel}: {e}')

if __name__ == '__main__':
    convert_all()
