# Final Image Report

Date: 2026-05-30

## Summary

- Article: `/ancient-ayodhya-history-archaeology.html`
- Image folders scanned: `/public/images`, `/public/assets`, `/assets/images`, `/images`
- Random stock images: not added
- Blank placeholder images: not used in the article
- Final custom missing image: `images/ayodhya-archaeology-layers.webp`
- Missing image action: prompt generated and documented in `image-manifest.json`, `blog-assets/image-manifest.json`, and `blog-assets/metadata/ayodhya-archaeology-layers.metadata.json`

## Reused WEBP Assets

| File | Article section | Status |
| --- | --- | --- |
| `images/ayodhya-heritage.webp` | Hero banner and social preview | Reused and optimized |
| `images/ram-mandir-ayodhya.webp` | Introduction | Reused and optimized |
| `images/hanuman-garhi-ayodhya.webp` | Temple Architecture | Reused and optimized |
| `images/kanak-bhawan-ayodhya.webp` | Temple Architecture | Reused and optimized |
| `images/ayodhya-market.webp` | Did You Know Facts | Reused and optimized |

## Responsive WEBP Versions Generated

| Source | Generated versions |
| --- | --- |
| `images/ayodhya-heritage.webp` | `images/ayodhya-heritage-480.webp`, `images/ayodhya-heritage-768.webp`, `images/ayodhya-heritage-1200.webp` |
| `images/ram-mandir-ayodhya.webp` | `images/ram-mandir-ayodhya-480.webp` |
| `images/hanuman-garhi-ayodhya.webp` | `images/hanuman-garhi-ayodhya-480.webp`, `images/hanuman-garhi-ayodhya-768.webp` |
| `images/kanak-bhawan-ayodhya.webp` | `images/kanak-bhawan-ayodhya-480.webp`, `images/kanak-bhawan-ayodhya-768.webp`, `images/kanak-bhawan-ayodhya-1200.webp` |
| `images/ayodhya-market.webp` | `images/ayodhya-market-480.webp` |

## Optimization Notes

- `scripts/process_final_images.py` was run with `blog-assets/image-manifest.json`.
- `scripts/optimize_images.py` was run against the reused image manifest.
- Main hero image reduced from about 542 KB to about 260 KB.
- Kanak Bhawan image reduced from about 194 KB to about 133 KB.
- All article images use WEBP sources, SEO alt text, captions, and lazy loading except the above-the-fold hero, which uses `fetchpriority="high"`.

## Prompt-Ready Missing Image

Filename: `images/ayodhya-archaeology-layers.webp`

Prompt:
Documentary-style educational illustration of Ayodhya archaeology, showing a clean excavation trench, layered soil section, pottery sherds, old brickwork, measured grid strings, and a subtle Saryu river reference in the background. Use warm natural light, no people in focus, no text, no watermark, no modern fantasy elements.
