# Ayodhya Image Upload Checklist

Date: 2026-05-30

This checklist verifies the final image upload pipeline for the `ancient-ayodhya-history-archaeology` article.

## Pipeline status

- Final image upload folder: `blog-assets/final-images/`
- Folder exists: No
- Ready for replacement: No

> The final upload directory does not exist yet, so no final images are currently available for replacement.

## Expected final images

| Expected filename | Accepted formats | Destination path | Placeholder found? | Ready for replacement? |
|---|---|---|---|---|
| `ancient-saket-map` | `jpg`, `png`, `webp` | `public/images/blog/ayodhya/ancient-saket-map.webp` | Yes | No |
| `ayodhya-archaeology` | `jpg`, `png`, `webp` | `public/images/blog/ayodhya/ayodhya-archaeology.webp` | Yes | No |
| `ayodhya-history-timeline` | `jpg`, `png`, `webp` | `public/images/blog/ayodhya/ayodhya-history-timeline.webp` | Yes | No |
| `ramayana-ayodhya-heritage` | `jpg`, `png`, `webp` | `public/images/blog/ayodhya/ramayana-ayodhya-heritage.webp` | Yes | No |

## Placeholder verification

All four destination placeholders currently exist in `public/images/blog/ayodhya/` and are ready to be replaced once final assets arrive.

## Upload checklist

1. Create or verify the directory: `blog-assets/final-images/`
2. Upload these final image files into that folder with matching stems:
   - `ancient-saket-map.jpg` or `.png` or `.webp`
   - `ayodhya-archaeology.jpg` or `.png` or `.webp`
   - `ayodhya-history-timeline.jpg` or `.png` or `.webp`
   - `ramayana-ayodhya-heritage.jpg` or `.png` or `.webp`
3. Optionally upload provenance JSON files into `blog-assets/provenance-examples/` named:
   - `ancient-saket-map.json`
   - `ayodhya-archaeology.json`
   - `ayodhya-history-timeline.json`
   - `ramayana-ayodhya-heritage.json`
4. After upload, run the final processing script:

```bash
python scripts/process_final_images.py \
  --final-dir blog-assets/final-images \
  --manifest blog-assets/image-manifest.json \
  --provenance-dir blog-assets/provenance-examples \
  --report blog-assets/final-image-report.md
```

## Required upload summary

Upload exactly these files into `/blog-assets/final-images/`:
- `ancient-saket-map.jpg` or `.png` or `.webp`
- `ayodhya-archaeology.jpg` or `.png` or `.webp`
- `ayodhya-history-timeline.jpg` or `.png` or `.webp`
- `ramayana-ayodhya-heritage.jpg` or `.png` or `.webp`

No other changes are needed until these final images are available.
