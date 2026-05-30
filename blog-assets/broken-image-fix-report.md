# Broken Image Fix Report

Date: 2026-05-30

File checked: `ancient-ayodhya-history-archaeology.html`

## Summary

- All image `src` paths in the article were scanned.
- All current `img src` files exist in the project.
- All responsive `source srcset` WEBP candidates exist in the project.
- The visible article image `src` values were changed to clean local WEBP paths where possible.
- Fallback `onerror` handlers were added to article images.
- Broken-image layout protection was added in `css/style.css` with `min-height`, background styling, and fallback-state styling.

## Image Src Fixes

| Section name | Image alt | Old src | New src | File exists |
| --- | --- | --- | --- | --- |
| Header logo | Ayodhya Ramnagri Tourism logo | `images/logo.jpeg` | `images/logo.jpeg` | Yes |
| Hero Section | Shri Ram Mandir Ayodhya temple architecture and pilgrims | `images/ayodhya.jpg` | `images/ayodhya-heritage.webp` | Yes |
| Introduction | Shri Ram Mandir Ayodhya temple facade with carved stone details | `images/ram_temple_1694583470615_1694583503125.jpg` | `images/ram-mandir-ayodhya.webp` | Yes |
| Temple Architecture | Hanuman Garhi temple in Ayodhya with pilgrims and temple entrance | `images/Hanuman_Garhi_Mandir_Ayodhya.jpg` | `images/hanuman-garhi-ayodhya.webp` | Yes |
| Temple Architecture | Kanak Bhawan temple courtyard in Ayodhya | `images/kanak-bhawan.png` | `images/kanak-bhawan-ayodhya.webp` | Yes |
| Did You Know Facts | Ayodhya local market lanes near pilgrimage routes | `images/AYODHYA MARKET.jpg` | `images/ayodhya-market.webp` | Yes |

## Responsive Source Paths Checked

| Section name | Source path | File exists |
| --- | --- | --- |
| Hero Section | `images/ayodhya-heritage-480.webp` | Yes |
| Hero Section | `images/ayodhya-heritage-768.webp` | Yes |
| Hero Section | `images/ayodhya-heritage-1200.webp` | Yes |
| Hero Section | `images/ayodhya-heritage.webp` | Yes |
| Introduction | `images/ram-mandir-ayodhya-480.webp` | Yes |
| Introduction | `images/ram-mandir-ayodhya.webp` | Yes |
| Temple Architecture | `images/hanuman-garhi-ayodhya-480.webp` | Yes |
| Temple Architecture | `images/hanuman-garhi-ayodhya-768.webp` | Yes |
| Temple Architecture | `images/hanuman-garhi-ayodhya.webp` | Yes |
| Temple Architecture | `images/kanak-bhawan-ayodhya-480.webp` | Yes |
| Temple Architecture | `images/kanak-bhawan-ayodhya-768.webp` | Yes |
| Temple Architecture | `images/kanak-bhawan-ayodhya-1200.webp` | Yes |
| Temple Architecture | `images/kanak-bhawan-ayodhya.webp` | Yes |
| Did You Know Facts | `images/ayodhya-market-480.webp` | Yes |
| Did You Know Facts | `images/ayodhya-market.webp` | Yes |

## Notes

- Paths are relative to `ancient-ayodhya-history-archaeology.html`, which is in the project root.
- The final paths work for local Live Server when serving `tour-fortened09` as the site root.
- The final paths also work after deployment if the `images/` folder is deployed beside the HTML file.
- No random stock image paths were introduced.
