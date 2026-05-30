# Ayodhya Image Audit

Date: 2026-05-30

## Summary

This audit lists images used or planned for the `ancient-ayodhya-history-archaeology` article and verifies placeholders, SEO coverage, and next steps to accept externally-generated images without code changes.

## Existing images reused

- `public/images/blog/ayodhya/ancient-saket-map.webp` — placeholder exists (status: placeholder/pending-generation).
- `public/images/blog/ayodhya/ayodhya-archaeology.webp` — placeholder exists (status: placeholder/pending-generation).
- `public/images/blog/ayodhya/ayodhya-history-timeline.webp` — placeholder exists (status: placeholder/pending-generation).
- `public/images/blog/ayodhya/ramayana-ayodhya-heritage.webp` — placeholder exists (status: placeholder/pending-generation).

## Missing images

None — all four target filenames exist as placeholders in `/public/images/blog/ayodhya/`.

## Placeholder status

- All four assets are lightweight placeholders and are referenced by the article and `blog-assets/image-manifest.json` with `status: pending-generation` and provenance pointers in `blog-assets/provenance-examples/`.

## SEO alt text coverage

- `ancient-saket-map.webp`: alt provided — "Antique-style map of Ancient Saket (Ayodhya) showing Saryu river and key heritage sites".
- `ayodhya-archaeology.webp`: alt provided — "Archaeological cross-section illustration showing stratified layers at Ayodhya".
- `ayodhya-history-timeline.webp`: alt provided — "Historical timeline of Ayodhya showing major periods from ancient Saket to modern heritage".
- `ramayana-ayodhya-heritage.webp`: alt provided — "Dawn view of Ayodhya skyline with temple spires and the Saryu river, heritage mood".

All key images have descriptive alt text present in `blog-assets/image-manifest.json` and are embedded in the article — alt coverage is complete.

## Recommended image dimensions

- Hero / OG: 1792x1024 (16:9) — suitable for hero banners and social sharing.
- OG fallback: 1200x630 for Twitter and Facebook card previews.
- Thumbnail/square: 800x800 or 1200x1200 for high-res thumbnails.

When exporting, produce original PNG/JPEG at 2x target resolution (e.g., 3584x2048) if you plan to crop/retouch, then convert to WebP at quality 80–85.

## WEBP optimization notes

- Use `scripts/convert_images_to_webp.py` with method 6 and quality 80–85 for a good quality/size tradeoff.
- Strip EXIF where not needed. Keep minimal IPTC/XMP metadata for provenance if desired, but also save a separate `.metadata.json` file in `blog-assets/provenance-examples/`.

## Drop-in workflow (no code changes required)

1. Generate images externally using prompts in `blog-assets/dalle_payloads/`.
2. Save outputs to temporary folder, convert to WebP (quality 80–85), and name exactly as the `output_filename` in payloads (e.g., `public/images/blog/ayodhya/ramayana-ayodhya-heritage.webp`).
3. Place image files in `/public/images/blog/ayodhya/` overwriting placeholders.
4. Create/update a provenance JSON next to the image in `blog-assets/provenance-examples/` containing `model`, `model_version`, `seed`, and `generation_date`.
5. Update `blog-assets/image-manifest.json` status to `generated` and set `provenance_file` to the provenance JSON path.

## Notes & risks

- Ensure the image provider's license permits the intended use (commercial/editorial). Retain prompt and seed metadata for provenance.
- Avoid adding embedded visible text to images; instead add captions in HTML where needed.

Prepared by: Automation script (Copilot)
