# Ayodhya Placeholder Image Review

Date: 2026-05-30

This report validates the four placeholder images used by the `ancient-ayodhya-history-archaeology` article. It checks file existence, sizes, dimensions, format, metadata files, manifest linkage, and current status.

## Summary

- All four placeholder files exist in `public/images/blog/ayodhya/`.
- Each placeholder has an accompanying metadata file and is referenced in `blog-assets/image-manifest.json` with `status: pending-generation`.

## Files

### 1) ancient-saket-map.webp
- Filename: `public/images/blog/ayodhya/ancient-saket-map.webp`
- File exists: Yes
- File size: 2802 bytes (2.74 KB)
- Dimensions: 1600 × 900
- Format: WEBP
- Metadata file exists: Yes (`public/images/blog/ayodhya/ancient-saket-map.metadata.json`)
- Manifest linked: Yes (referenced in `blog-assets/image-manifest.json`)
- Status: pending-generation

### 2) ayodhya-archaeology.webp
- Filename: `public/images/blog/ayodhya/ayodhya-archaeology.webp`
- File exists: Yes
- File size: 2662 bytes (2.60 KB)
- Dimensions: 1600 × 900
- Format: WEBP
- Metadata file exists: Yes (`public/images/blog/ayodhya/ayodhya-archaeology.metadata.json`)
- Manifest linked: Yes (referenced in `blog-assets/image-manifest.json`)
- Status: pending-generation

### 3) ayodhya-history-timeline.webp
- Filename: `public/images/blog/ayodhya/ayodhya-history-timeline.webp`
- File exists: Yes
- File size: 2664 bytes (2.60 KB)
- Dimensions: 1600 × 900
- Format: WEBP
- Metadata file exists: Yes (`public/images/blog/ayodhya/ayodhya-history-timeline.metadata.json`)
- Manifest linked: Yes (referenced in `blog-assets/image-manifest.json`)
- Status: pending-generation

### 4) ramayana-ayodhya-heritage.webp
- Filename: `public/images/blog/ayodhya/ramayana-ayodhya-heritage.webp`
- File exists: Yes
- File size: 2666 bytes (2.60 KB)
- Dimensions: 1600 × 900
- Format: WEBP
- Metadata file exists: Yes (`public/images/blog/ayodhya/ramayana-ayodhya-heritage.metadata.json`)
- Manifest linked: Yes (referenced in `blog-assets/image-manifest.json`)
- Status: pending-generation

## Notes & Recommendations

- The current placeholders are lightweight (small file sizes) for development. Replace with high-resolution generated assets (recommended source resolution 3584×2048) and convert to WebP at quality 80–85 for production.
- Keep the metadata `.metadata.json` files updated with `model`, `model_version`, `seed`, and `generation_date` after generation.
- Once final images are placed, update `blog-assets/image-manifest.json` `status` to `generated` and ensure `provenance_file` and `metadata_file` entries point to the correct JSON files.

Prepared by automation (Copilot)
