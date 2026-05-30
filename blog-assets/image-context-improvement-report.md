# Image Context Improvement Report

Date: 2026-05-30

File updated:

`ancient-ayodhya-history-archaeology.html`

## Summary

- Every article image is now wrapped in a semantic `<figure class="blog-figure">`.
- Every article image has a `<figcaption>`.
- Every article image has a related explanatory paragraph using `.image-note`.
- Normal content images are constrained to `max-width: 720px` and centered.
- The hero image remains full width through `.blog-figure-hero`.
- A WEBP version of the local Deepotsav/Ram Ki Paidi image was generated: `images/saryu-deepotsav-riverfront.webp`.
- Header logo is not treated as a blog image and remains in the navbar.

## Image Blocks Added Or Improved

| Section | Image | Caption purpose | Explanation purpose |
| --- | --- | --- | --- |
| Hero Section | `images/ayodhya-heritage.webp` | Frames Ayodhya as a modern pilgrimage skyline | Explains that the article views Ayodhya through architecture, ritual, history and travel experience |
| Introduction / Saryu | `images/saryu-deepotsav-riverfront.webp` | Shows the Saryu riverfront ritual atmosphere | Explains why the Saryu is a natural starting point for understanding Ayodhya |
| Historical Background | `public/images/blog/ayodhya/ancient-saket-map.webp` | Places Ancient Saket in sacred geography | Explains why map context matters for Ayodhya's historical identity |
| Archaeology | `public/images/blog/ayodhya/ayodhya-archaeology.webp` | Connects the section to layers and material evidence | Explains stratigraphy and why archaeology must be read carefully in a living city |
| Temple Architecture | `images/hanuman-garhi-ayodhya.webp` | Shows Hanuman Garhi as a key temple site | Explains its raised approach, gateway feeling and devotional sequence before Ram Mandir |
| Legends & Katha | `images/kanak-bhawan-ayodhya.webp` | Places Kanak Bhawan in Sita-Rama local memory | Explains why Kanak Bhawan belongs with storytelling, not archaeology |
| Travel Experience | `images/saryu-deepotsav-riverfront.webp` | Shows Ram Ki Paidi evening atmosphere | Explains why Ram Ki Paidi is a felt travel experience, not only a photo stop |
| Pilgrim Guide | `images/ayodhya-market.webp` | Shows market lanes used by pilgrims | Explains how prasad, food, directions and pauses are part of practical pilgrimage |
| CTA | `assets/images/vehicles/tempo-traveller-ayodhya.jpg` | Shows group/family travel support | Explains why a reliable vehicle matters for relaxed Ayodhya sightseeing |

## CSS Added

Added styles for:

- `.blog-figure`
- `.blog-figure-hero`
- `.blog-figure img`
- `.blog-figure figcaption`
- `.image-note`
- `.hero-image-note`

## Validation

Image path check:

`Paths checked: 23`

Missing image paths:

`None`

Article image structure:

- Blog figure blocks: 9
- Image explanation notes: 9
- Header logo excluded from blog image count
