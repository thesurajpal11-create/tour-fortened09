# Ayodhya image prompts and alt text

This file lists the images available in the repository that will be reused for the heritage article, and image-generation prompts for any missing hero/OG images (use for stock/AI generation if needed).

## Existing images to reuse (source file -> suggested webp filename -> alt text)
- images/ayodhya.jpg -> images/ayodhya-heritage.webp -> "Aerial view of Ayodhya and the Saryu river at dawn"
- images/ram_temple_1694583470615_1694583503125.jpg -> images/ram-mandir-ayodhya.webp -> "Ram Mandir Ayodhya aerial view"
- images/Hanuman_Garhi_Mandir_Ayodhya.jpg -> images/hanuman-garhi-ayodhya.webp -> "Hanuman Garhi temple entrance, Ayodhya"
- images/kanak-bhawan.png -> images/kanak-bhawan-ayodhya.webp -> "Kanak Bhawan inner courtyard and shrine"
- images/Nageshwarnath-Temple.jpg -> images/nageshwarnath-temple-ayodhya.webp -> "Nageshwarnath Temple, Ayodhya"
- images/Dashrath-Mahal-Ayodhya-2.jpg -> images/dashrath-mahal-ayodhya.webp -> "Dashrath Mahal, Ayodhya"
- images/AYODHYA MARKET.jpg -> images/ayodhya-market.webp -> "Ayodhya street market and pilgrims"
- images/heritage.jpg -> images/ayodhya-heritage-illustration.webp -> "Heritage illustration: Ayodhya temple silhouette"

## Missing or recommended hero/OG images (prompts)

1) Hero aerial illustration (wide, editorial):
"A wide aerial view of Ayodhya at sunrise showing the Saryu river, temple spires, and low-rise heritage buildings; warm golden light, slight morning mist, high detail, editorial photography style, 16:9, color graded for heritage magazine cover."

2) Intimate temple detail (Kanak Bhawan carved panel close-up):
"Close-up photograph of ornate sandstone carving and floral motifs on a North Indian temple façade, soft-side lighting, 50mm, high detail, natural colors."

3) Saryu Aarti scene (evening):
"Evening river aarti at Ram Ki Paidi: priests with diyas, reflected flames on water, pilgrims watching, cinematic warm tones, shallow depth of field."

4) Market & craft scene:
"Ayodhya local market scene with sweet vendors, colorful stalls, and pilgrims; candid documentary style, natural lighting, high detail."

---

## Additional hero / OG prompt variations (editorial + social)

- Hero editorial (16:9, magazine cover):
	"A wide aerial view of Ayodhya at sunrise showing the Saryu river, temple spires and low-rise heritage buildings; warm golden light, slight morning mist, high detail, editorial photography style, 16:9 aspect ratio, color graded for a heritage magazine cover. Include space on the right for a headline overlay."

- Social OG (1200x630 px, attention-focused):
	"Close-in composition of the Ram ghats at dusk during the aarti — floating diyas, reflected flames and silhouettes of pilgrims; dramatic warm lighting, shallow depth of field, high contrast, crop-safe for 1200x630."

- Square thumbnail (social feed, 1:1):
	"Textural close-up of carved stone detail from a temple façade with warm tones and natural shadows; crop to 1:1, high-detail, non-photoreal illustration or photograph acceptable."

- Illustration option (stylized, vector-friendly):
	"Minimalist illustrated skyline of Ayodhya featuring the Saryu river curve and iconic temple spires, warm palette (saffron, gold, sandstone), flat shading suitable for hero banners and svg export, include negative space for title text."

## OG alt text and filename suggestions

- images/ayodhya-hero-16x9.webp -> "Aerial view of Ayodhya and the Saryu river at sunrise"
- images/ayodhya-og-1200x630.webp -> "Saryu Aarti at Ram Ki Paidi, Ayodhya — evening ritual with floating lamps"
- images/ayodhya-thumb-1x1.webp -> "Stone carving detail from Ayodhya temple"

## Usage notes

- For article pages use the 16:9 hero (`ayodhya-hero-16x9.webp`) as the in-article banner and the 1200x630 OG image for social meta tags.
- All generated images must be converted to WEBP, optimized with quality ~80–85, and saved with descriptive filenames.
- Provide `alt` text as above; add `loading="lazy"` to in-article `<img>` tags and include `decoding="async"` where supported.

## Conversion instructions (local):
- Use the provided Python script `scripts/convert_images_to_webp.py` (recommended) to batch convert the listed source images to the suggested webp filenames with quality 85 and method 6.

## Alt text generation (SEO-ready)
- Use the alt texts listed above; keep alt text descriptive, 6–12 words, include 'Ayodhya' when the subject is place-specific.
