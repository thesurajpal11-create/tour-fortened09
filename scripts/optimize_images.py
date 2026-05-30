#!/usr/bin/env python3
"""
Optimize images for the Ayodhya blog images.

Usage:
  python scripts/optimize_images.py --input-dir public/images/blog/ayodhya \
    --manifest blog-assets/image-manifest.json \
    --report blog-assets/image-optimization-report.md [--dry-run]

This script:
- Reads `image-manifest.json` to find images and their roles (hero vs content).
- For each image present, produces responsive WebP sizes: 480, 768, 1200, and optimized original.
- Attempts to compress images to target sizes (hero: <=250KB, content: <=150KB) by reducing quality.
- Preserves aspect ratio and writes files alongside the originals using suffixes like `-768.webp`.
- Preserves per-image metadata files (does not modify them).

Note: Run this after you replace placeholders with final generated images.
"""

import argparse
import json
from pathlib import Path
from PIL import Image
import io
import sys


def sizeof_fmt(num):
    for unit in ['B','KB','MB','GB']:
        if abs(num) < 1024.0:
            return f"{num:.0f} {unit}"
        num /= 1024.0
    return f"{num:.0f} TB"


def optimize_image(src_path: Path, dst_path: Path, target_width: int, target_kb: int, quality_start=85, quality_min=50):
    img = Image.open(src_path).convert('RGB')
    w, h = img.size
    if target_width >= w:
        resized = img
    else:
        ratio = target_width / float(w)
        new_h = int(h * ratio)
        resized = img.resize((target_width, new_h), Image.LANCZOS)

    quality = quality_start
    last_bytes = None
    while quality >= quality_min:
        buf = io.BytesIO()
        resized.save(buf, format='WEBP', quality=quality, method=6)
        size = buf.tell()
        # target_kb is in KB
        if size <= target_kb * 1024:
            buf.seek(0)
            dst_path.write_bytes(buf.read())
            return size, (resized.width, resized.height), quality
        last_bytes = (size, quality, buf)
        quality -= 5

    # if we did not meet target, save last attempt
    if last_bytes:
        size, q, buf = last_bytes
        buf.seek(0)
        dst_path.write_bytes(buf.read())
        return size, (resized.width, resized.height), q
    # fallback save with default quality
    buf = io.BytesIO()
    resized.save(buf, format='WEBP', quality=quality_start, method=6)
    buf.seek(0)
    dst_path.write_bytes(buf.read())
    return buf.tell(), (resized.width, resized.height), quality_start


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', required=True)
    parser.add_argument('--manifest', required=True)
    parser.add_argument('--report', required=True)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    manifest_path = Path(args.manifest)
    report_path = Path(args.report)

    if not manifest_path.exists():
        print('Manifest not found:', manifest_path)
        sys.exit(1)

    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))

    results = []

    for entry in manifest:
        filename = entry.get('filename')
        if not filename:
            continue
        src = Path(filename)
        if not src.exists():
            results.append({'filename': filename, 'exists': False})
            continue

        # Determine role
        section = entry.get('section','').lower()
        is_hero = 'hero' in section or 'banner' in section
        target_kb = 250 if is_hero else 150

        # sizes to generate (widths)
        widths = [480, 768, 1200]

        # record original
        orig_size = src.stat().st_size
        with Image.open(src) as im:
            orig_dims = im.size
            orig_format = im.format

        optimized_original_path = src  # overwrite original when not dry-run

        entry_result = {
            'filename': filename,
            'original_size': orig_size,
            'original_dimensions': orig_dims,
            'optimized_original_size': None,
            'optimized_dimensions': None,
            'responsive_files': [],
            'status': entry.get('status','pending-generation')
        }

        if args.dry_run:
            # don't write files, but simulate
            entry_result['note'] = 'dry-run: no files written'
            results.append(entry_result)
            continue

        # Optimize and overwrite original aiming for target_kb
        try:
            opt_size, dims, q = optimize_image(src, optimized_original_path, orig_dims[0], target_kb)
            entry_result['optimized_original_size'] = opt_size
            entry_result['optimized_dimensions'] = dims
            entry_result['optimized_quality'] = q
        except Exception as e:
            entry_result['error'] = str(e)

        # Create responsive sizes
        for w in widths:
            if w >= orig_dims[0]:
                continue
            dst = src.with_name(f"{src.stem}-{w}{src.suffix}")
            try:
                size, dims, q = optimize_image(src, dst, w, target_kb)
                entry_result['responsive_files'].append({'file': str(dst), 'size': size, 'dimensions': dims, 'quality': q})
            except Exception as e:
                entry_result.setdefault('responsive_errors', []).append({'width': w, 'error': str(e)})

        results.append(entry_result)

    # write report
    lines = [f"# Image Optimization Report\n\nDate: \n\n"]
    for r in results:
        lines.append(f"## {r.get('filename')}\n")
        lines.append(f"- Original size: {sizeof_fmt(r.get('original_size',0))}\n")
        if r.get('optimized_original_size'):
            lines.append(f"- Optimized original size: {sizeof_fmt(r.get('optimized_original_size'))}\n")
            pct = 100.0 * (1 - (r['optimized_original_size'] / r['original_size'])) if r['original_size'] else 0
            lines.append(f"- Compression: {pct:.1f}%\n")
        if r.get('original_dimensions'):
            lines.append(f"- Dimensions: {r['original_dimensions'][0]} x {r['original_dimensions'][1]}\n")
        lines.append(f"- Status: {r.get('status')}\n")
        if r.get('responsive_files'):
            lines.append(f"- Responsive files:\n")
            for rf in r['responsive_files']:
                lines.append(f"  - {rf['file']}: {sizeof_fmt(rf['size'])}, {rf['dimensions'][0]}x{rf['dimensions'][1]}\n")
        lines.append('\n')

    report_path.write_text('\n'.join(lines), encoding='utf-8')
    print('Wrote report to', report_path)


if __name__ == '__main__':
    main()
