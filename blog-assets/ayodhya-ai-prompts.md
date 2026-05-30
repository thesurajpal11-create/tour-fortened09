# Ayodhya AI Image Prompts (ready-to-use)

This file contains production-ready prompts and engine parameters for generating hero / OG / thumbnail images for the `ancient-ayodhya-history-archaeology` article. Use the sections for Midjourney, Stable Diffusion (txt2img), or DALL·E as appropriate. Save outputs using the suggested filenames, convert to WEBP (quality 80–85, method 6) and place in `/images`.

---

## General guidance
- Save final images as: `ayodhya-hero-16x9.webp`, `ayodhya-og-1200x630.webp`, `ayodhya-thumb-1x1.webp`.
- Include people only as silhouettes or background figures; avoid generating identifiable faces for safety/consent reasons.
- Prefer warm golden-hour light, natural textures and a slightly documentary editorial look for authenticity.
- After generation: run `scripts/convert_images_to_webp.py` or use an image editor to export WebP and optimize.

---

## 1) Midjourney (V5+/parameters)

Hero (16:9 editorial)
Prompt:
"Aerial view of Ayodhya at sunrise showing the Saryu river curve, temple spires, and low-rise heritage buildings; warm golden light, slight morning mist, editorial magazine cover, ultra-detailed, filmic color grading --ar 16:9 --v 5 --q 2 --stylize 1000"

OG (1200x630 focus)
Prompt:
"Evening Saryu aarti at Ram Ki Paidi, priests with diyas and reflected lamps on the water, silhouettes of pilgrims watching, cinematic warm tones, shallow depth, high contrast --ar 1200:630 --v 5 --q 2 --stylize 800"

Thumbnail (1:1 detail)
Prompt:
"Close-up carved stone temple panel with floral motifs, warm sandstone colors, high microdetail, studio-soft light --ar 1:1 --v 5 --q 2 --stylize 600"

Notes:
- Use `--no text, watermark` to avoid embedded labels. If you need an illustration style, add `--style raw` or append `illustration, vector-friendly` to the prompt.

---

## 2) Stable Diffusion (txt2img) — recommended parameters

Hero (1600x900)
Prompt:
"Aerial view of Ayodhya at sunrise showing the Saryu river, temple spires and heritage buildings, warm golden light, morning mist, editorial photography, natural colors, high detail"

Negative prompt (recommended):
"(blurred, lowres, watermark, text, logo, extra fingers, deformed, mutated, ugly)"

Suggested sampler/params:
- Sampler: `Euler a` or `DDIM`
- Steps: 28–40
- CFG scale: 6.5–8.5
- Size: `1600x900` (hero), `1200x630` (og), `800x800` (thumb)
- Seed: leave blank for variety or set integer for reproducibility.

Post-process:
- Minor color-grade (warmth +10), sharpen 0.4, crop for safety margins.
- Run an upscaler (GFPGAN/ESRGAN) only if faces are present and you have rights to process them.

---

## 3) DALL·E / OpenAI Image (short prompts)

Hero:
"Aerial sunrise view of Ayodhya and the Saryu river, temple spires, warm golden light, editorial photography"

OG:
"Evening river aarti at Ayodhya with floating diyas and reflections, cinematic lighting, pilgrims in silhouette"

Notes:
- Keep prompts concise for DALL·E; use image edits/variations to fine-tune composition.

---

## 4) Illustration / Vector option (for banners)
Prompt:
"Minimalist illustrated skyline of Ayodhya featuring the Saryu river curve and iconic temple spires, warm palette (saffron, gold, sandstone), flat shading, negative space for headline, vector-friendly"

Export: SVG + PNG at 3000x1688, then convert to WebP.

---

## 5) Filenames and alt text (SEO-ready)
- `images/ayodhya-hero-16x9.webp` -> "Aerial view of Ayodhya and the Saryu river at sunrise"
- `images/ayodhya-og-1200x630.webp` -> "Saryu Aarti at Ram Ki Paidi, Ayodhya — evening ritual with floating lamps"
- `images/ayodhya-thumb-1x1.webp` -> "Stone carving detail from Ayodhya temple"

---

## 6) Licensing & usage notes
- Verify the image provider's license allows commercial reuse if you publish under a brand.
- For AI-generated images, store the prompt and seed as metadata (in `blog-assets/ayodhya-ai-prompts.md`) for provenance.
- When using stock photography, prefer a vendor that provides model/property releases for crowds or faces.

---

If you want, I can also prepare a ZIP (`blog-assets/ai-image-package.zip`) containing these prompts as `.txt` files and the placeholder images; tell me and I'll create it next. 

---

## Priority: Missing images — A/B/C prompt variations
The following assets are not present in the project and have three prompt variations (A/B/C) each. Use these with Midjourney / Stable Diffusion / DALL·E. Filenames suggested below; after generation, convert to WebP and place in `/images`.

1) Ancient Saket Map
- Filename: `images/ayodhya-ancient-saket-map.webp`
	- A: "Antique-style map of Ancient Saket (Ayodhya) showing river Saryu, temple clusters, and labelled neighborhood names in a parchment texture, hand-drawn cartographic style, muted ochre palette, high detail — map legend and compass rose, vintage engraving look."
	- B: "Stylized historical map of Ayodhya (Saket) combining topographic river curve and temple icons, sepia tones, aged paper texture, clear labels for key sites (Ram Mandir, Kanak Bhawan, Hanuman Garhi), 300 DPI, editorial cartography style."
	- C: "Minimalist illustrated heritage map of Saket showing Saryu river, pilgrimage route and key monuments, soft watercolor wash, inked outlines, high legibility for hero banner, warm palette."

2) Ayodhya Archaeology Illustration
- Filename: `images/ayodhya-archaeology-illustration.webp`
	- A: "Cross-section archaeological illustration of Ayodhya showing stratified layers: ancient habitation, medieval rebuilds, recent temple foundations; labeled strata, archaeological tools at work, educational diagram aesthetic, clear colors and annotations."
	- B: "Isometric archaeological site drawing of Ayodhya excavations with archaeologists, trenches, pottery sherds and brick foundations visible; realistic documentary style, high detail, natural earth tones."
	- C: "Infographic-style archaeology illustration highlighting material finds (pottery, beads, brickwork) with magnified insets and captions, clean vector diagrams, museum-educational look."

3) Historical Ayodhya Timeline
- Filename: `images/ayodhya-historical-timeline.webp`
	- A: "Horizontal timeline banner illustrating Ayodhya's key periods: Vedic/early, classical Saket, medieval, modern reconstruction — include dated markers, iconic small illustrations (temple, river, fort) on parchment background, elegant serif labels."
	- B: "Vertical infographic timeline for Ayodhya showing centuries with short captions and illustrative icons, warm heritage palette, suitable for article inset and printable poster."
	- C: "Stylized illustrated timeline with layered panels and illustrated vignettes of daily life across eras (pottery, rituals, temple building), hand-painted textures and clean captions for each era."

4) Ancient Ayodhya Heritage Artwork
- Filename: `images/ayodhya-heritage-artwork.webp`
	- A: "Painterly heritage artwork of Ayodhya's skyline at dawn with temple spires, Saryu reflections and a gentle halo of light — warm saffron palette, painterly brushstrokes, high-resolution for hero banner."
	- B: "Contemporary mixed-media collage combining archival sketches, temple relief photos, and watercolor washes representing Ayodhya's living heritage; layered textures, editorial art direction."
	- C: "Traditional Indian miniature-inspired artwork depicting a procession along the Saryu with temple backdrop, intricate details, gold highlights and rich colors, royalty-free illustration style."

Usage note: If an existing photo or illustration in `/images` closely matches the asset you need, prefer reusing it and update `image-manifest.json` status to `exists`.

---

## DALL·E 3 (ready-to-send payloads)
Use these exact prompts and the general negative prompt above when submitting to DALL·E 3. Payload JSON files are provided under `blog-assets/dalle_payloads/` and set canvas size to 1792x1024 (closest 16:9). Request PNG/JPEG output if the API cannot deliver WebP and then convert to WebP using `scripts/convert_images_to_webp.py`.

1) ancient-saket-map.webp (DALL·E payload)
- Prompt: "Antique-style cartographic map of Ancient Saket (Ayodhya) on aged parchment, showing the Saryu river, clusters of temple icons, labelled key sites (Ram Mandir, Kanak Bhawan, Hanuman Garhi) — hand-drawn engraving look, subtle color washes, compass rose, scale bar, high detail, documentary historical style."
- Negative prompt: (apply general negative prompt)

2) ayodhya-archaeology.webp (DALL·E payload)
- Prompt: "Cross-section archaeological illustration of Ayodhya showing stratified layers: ancient habitation, medieval rebuilds, recent temple foundations; labeled strata, archaeological tools, and insets of pottery sherds — clear educational diagram, museum-quality."
- Negative prompt: (apply general negative prompt)

3) ayodhya-history-timeline.webp (DALL·E payload)
- Prompt: "Horizontal timeline banner illustrating Ayodhya's major periods: Vedic/early, classical Saket, medieval, and modern reconstruction — include dated markers and small illustrative icons (temple, river, pottery), elegant museum-style serif labels, warm parchment background."
- Negative prompt: (apply general negative prompt)

4) ramayana-ayodhya-heritage.webp (DALL·E payload)
- Prompt: "Painterly heritage artwork of Ayodhya's skyline at dawn with temple spires, gentle mist over the Saryu river, warm saffron light, painterly brushstrokes, documentary editorial quality — no modern skyline, historically inspired."
- Negative prompt: (apply general negative prompt)

Store the exact prompt, model name and any `seed` or `variation` metadata alongside the final image file for provenance. After generation, move the images to `/public/images/blog/ayodhya/` and update the site manifest.

---

## DALL·E 3 payload files (JSON)
The following JSON payload files are available and ready for upload to your DALL·E 3 workflow. They live in `blog-assets/dalle_payloads/` and include the full prompt, negative prompt note, recommended `size` (1792x1024), `output_filename`, `alt_text`, `seo_caption`, `placement_section`, `license_provenance_note`, and `manifest_status` (pending-generation). After generation, save outputs using the `output_filename` and replace the placeholder files in `/public/images/blog/ayodhya/`.

- `blog-assets/dalle_payloads/ancient-saket-map.json`
- `blog-assets/dalle_payloads/ayodhya-archaeology.json`
- `blog-assets/dalle_payloads/ayodhya-history-timeline.json`
- `blog-assets/dalle_payloads/ramayana-ayodhya-heritage.json`

Usage tip:
- Upload the JSON payload directly via your DALL·E 3 client if it supports JSON payloads, or copy the `prompt`/`size` fields into the API UI. Save any returned `seed`/`variation`/`model_version` values into a small provenance JSON next to the final image (example: `public/images/blog/ayodhya/ramayana-ayodhya-heritage.metadata.json`).

When ready, tell me and I will update `blog-assets/image-manifest.json` statuses from `pending-generation` to `generated` and attach the provenance metadata.
