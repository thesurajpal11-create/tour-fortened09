#!/usr/bin/env python3
"""
Process final images: replace placeholders, optimize, generate responsive versions,
update manifests and metadata, and write a final report.

Place final images (any common image format) in `blog-assets/final-images/`.
Provide optional provenance JSON files in `blog-assets/provenance-examples/` named
the same as the image stem (e.g., `ancient-saket-map.json`) containing model, seed, etc.

Run:
  python scripts/process_final_images.py --final-dir blog-assets/final-images \
    --manifest blog-assets/image-manifest.json \
    --provenance-dir blog-assets/provenance-examples \
    --report blog-assets/final-image-report.md

This script will NOT run unless you invoke it. It will overwrite placeholders in
`public/images/blog/ayodhya/` with optimized WebP images and create responsive
variants `-480.webp`, `-768.webp`, `-1200.webp`.
"""

import argparse
import json
from pathlib import Path
import shutil
from datetime import datetime

# Reuse optimize function from optimize_images (copied here to avoid import issues)
from PIL import Image
import io


def optimize_image_bytes(img: Image.Image, target_width: int, target_kb: int, quality_start=85, quality_min=50):
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
        if size <= target_kb * 1024:
            buf.seek(0)
            return buf.read(), size, (resized.width, resized.height), quality
        last_bytes = (buf.getvalue(), size, quality, (resized.width, resized.height))
        quality -= 5

    if last_bytes:
        data, size, q, dims = last_bytes
        return data, size, dims, q

    buf = io.BytesIO()
    resized.save(buf, format='WEBP', quality=quality_start, method=6)
    return buf.getvalue(), buf.tell(), (resized.width, resized.height), quality_start


def run(final_dir: Path, manifest_path: Path, provenance_dir: Path, report_path: Path, dry_run=False):
    final_dir.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    report_rows = []

    for entry in manifest:
        status = entry.get('status','pending-generation')
        if status != 'pending-generation':
            continue
        filename = entry.get('filename')
        if not filename:
            continue
        dest = Path(filename)
        stem = dest.stem

        # find a file in final_dir matching stem
        candidates = list(final_dir.glob(stem + '.*'))
        if not candidates:
            # no final image provided for this entry
            report_rows.append({'filename': filename, 'processed': False, 'reason': 'no final upload'})
            continue

        src = candidates[0]
        # copy to destination (overwrite placeholder)
        if dry_run:
            copied = False
        else:
            shutil.copy2(src, dest)
            copied = True

        # open image
        img = Image.open(src).convert('RGB')
        orig_size = src.stat().st_size
        orig_dims = img.size

        # determine role
        section = entry.get('section','').lower()
        is_hero = 'hero' in section or 'banner' in section
        target_kb = 250 if is_hero else 150

        # optimize original (keep same filename, WebP)
        optimized_bytes, opt_size, opt_dims, opt_quality = optimize_image_bytes(img, orig_dims[0], target_kb)
        if not dry_run:
            dest.write_bytes(optimized_bytes)

        responsive_files = []
        for w in [480, 768, 1200]:
            if w >= orig_dims[0]:
                continue
            data, size, dims, q = optimize_image_bytes(img, w, target_kb)
            out_path = dest.with_name(f"{stem}-{w}{dest.suffix}")
            if not dry_run:
                out_path.write_bytes(data)
            responsive_files.append({'file': str(out_path), 'size': size, 'dimensions': dims, 'quality': q})

        # provenance
        prov_file = provenance_dir / f"{stem}.json"
        prov = {}
        if prov_file.exists():
            try:
                prov = json.loads(prov_file.read_text(encoding='utf-8'))
            except Exception:
                prov = {}

        # update metadata in public images folder
        metadata_path = dest.with_suffix(dest.suffix + '.metadata.json')
        metadata = {}
        if metadata_path.exists():
            try:
                metadata = json.loads(metadata_path.read_text(encoding='utf-8'))
            except Exception:
                metadata = {}

        # fill metadata fields with provenance
        metadata.update({
            'filename': str(dest).replace('\\','/'),
            'status': 'generated',
            'model': prov.get('model',''),
            'model_version': prov.get('model_version',''),
            'seed': prov.get('seed',''),
            'generation_date': prov.get('generation_date',''),
            'prompt': prov.get('prompt',''),
            'negative_prompt': prov.get('negative_prompt',''),
            'resolution': f"{opt_dims[0]}x{opt_dims[1]}",
            'format': 'webp',
            'license': prov.get('license', metadata.get('license','Website use only')),
            'created_for': metadata.get('created_for','Ayodhya Ramnagri Tourism'),
            'page': metadata.get('page','/ancient-ayodhya-history-archaeology.html')
        })

        if not dry_run:
            metadata_path.write_text(json.dumps(metadata, indent=2), encoding='utf-8')

        # update blog-assets provenance example
        prov_example_path = provenance_dir / f"{stem}.json"
        prov_example = prov.copy()
        prov_example.update({'filename': str(dest).replace('\\','/'), 'status': 'generated', 'resolution': metadata['resolution']})
        if not dry_run:
            prov_example_path.write_text(json.dumps(prov_example, indent=2), encoding='utf-8')

        # update manifest entry
        entry['status'] = 'generated'
        entry['provenance_file'] = str(prov_example_path).replace('\\','/')
        entry['metadata_file'] = str(metadata_path).replace('\\','/')

        report_rows.append({
            'filename': str(dest).replace('\\','/'),
            'original_size': orig_size,
            'optimized_size': opt_size,
            'compression_pct': 100.0 * (1 - (opt_size / orig_size)) if orig_size else 0,
            'dimensions': opt_dims,
            'alt_text': entry.get('alt_text',''),
            'provenance_status': 'attached' if prov else 'missing',
            'responsive': responsive_files
        })

    # write updated manifest
    if not dry_run:
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')

    # write report
    lines = [f"# Final Image Report\n\nDate: {datetime.utcnow().isoformat()}Z\n\n"]
    for r in report_rows:
        lines.append(f"## {r['filename']}\n")
        lines.append(f"- Original size: {r['original_size']} bytes\n")
        lines.append(f"- Optimized size: {r['optimized_size']} bytes\n")
        lines.append(f"- Compression: {r['compression_pct']:.1f}%\n")
        lines.append(f"- Dimensions: {r['dimensions'][0]}x{r['dimensions'][1]}\n")
        lines.append(f"- Alt text: {r['alt_text']}\n")
        lines.append(f"- Provenance: {r['provenance_status']}\n")
        if r['responsive']:
            lines.append(f"- Responsive files:\n")
            for rf in r['responsive']:
                lines.append(f"  - {rf['file']}: {rf['size']} bytes, {rf['dimensions'][0]}x{rf['dimensions'][1]}\n")
        lines.append('\n')

    if not dry_run:
        report_path.write_text('\n'.join(lines), encoding='utf-8')
    else:
        print('\n'.join(lines))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--final-dir', required=True)
    parser.add_argument('--manifest', required=True)
    parser.add_argument('--provenance-dir', required=True)
    parser.add_argument('--report', required=True)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    run(Path(args.final_dir), Path(args.manifest), Path(args.provenance_dir), Path(args.report), dry_run=args.dry_run)


if __name__ == '__main__':
    main()
