# Project Root Fix Report

Date: 2026-05-30

Single project root used:

`/tour-fortened09/`

## Files Moved

No file move was needed. The only HTML file found outside `/tour-fortened09/` was already present inside the project root with the same SHA256 hash.

## Duplicate Files Removed

| Removed duplicate | Canonical file kept | Result |
| --- | --- | --- |
| `../ayodhya-itinerary-for-2-days.html` | `ayodhya-itinerary-for-2-days.html` | Removed outside duplicate after hash match |

## Links Fixed

| File | Fix |
| --- | --- |
| `index.html` | Changed root-relative favicon path from `/favicon.ico` to `favicon.ico` |
| `index.html` | Changed root-relative guide card image paths from `/images/ayodhya-heritage.webp` to `images/ayodhya-heritage.webp` |
| `ayodhya-itinerary-for-2-days.html` | Changed breadcrumb `/` to `index.html` |
| `ayodhya-itinerary-for-2-days.html` | Changed `/blog.html` to `blog.html` |
| `ayodhya-itinerary-for-2-days.html` | Changed package links such as `/packages/ayodhya-package.html` to `packages/ayodhya-package.html` |
| `ayodhya-itinerary-for-2-days.html` | Changed `/ayodhya-cab-service.html`, `/kashi-tour-package.html`, and `/char-dham-yatra/index.html` to relative paths |
| `ancient-ayodhya-history-archaeology.html` | Changed root-relative favicon path from `/favicon.ico` to `favicon.ico` |
| `ancient-ayodhya-history-archaeology.en.html` | Changed breadcrumbs, image paths, and related tour links from root-relative paths to project-relative paths |
| `blog.html` | Changed root-relative favicon path from `/favicon.ico` to `favicon.ico` |
| `blogs/*.html` | Changed root-relative favicon paths from `/favicon.ico` to `../favicon.ico` |

## Image Paths Fixed

| File | Fix |
| --- | --- |
| `index.html` | `srcset="/images/ayodhya-heritage.webp"` to `srcset="images/ayodhya-heritage.webp"` |
| `index.html` | `src="/images/ayodhya-heritage.webp"` to `src="images/ayodhya-heritage.webp"` |
| `ancient-ayodhya-history-archaeology.en.html` | `/public/images/blog/ayodhya/*.webp` to `public/images/blog/ayodhya/*.webp` |
| `ancient-ayodhya-history-archaeology.en.html` | `/images/*.webp` to `images/*.webp` |

## Sitemap

`sitemap.xml` uses final live URLs on:

`https://www.ramnagritourism.com/`

No localhost sitemap URLs were found.

## Verification

Outside-project HTML scan:

`OK - no HTML files remain outside /tour-fortened09/`

Root-relative internal path scan:

`OK - no internal href="/...", src="/...", or srcset="/..." paths remain in project HTML files`

Required page checks:

| Page | Local path check |
| --- | --- |
| `/tour-fortened09/index.html` | OK |
| `/tour-fortened09/ancient-ayodhya-history-archaeology.html` | OK |
| `/tour-fortened09/ayodhya-itinerary-for-2-days.html` | OK |

## Final Page URLs

| Page | Final live URL |
| --- | --- |
| Home | `https://www.ramnagritourism.com/` |
| Ancient Ayodhya Heritage Article | `https://www.ramnagritourism.com/ancient-ayodhya-history-archaeology.html` |
| Ayodhya 2 Day Itinerary | `https://www.ramnagritourism.com/ayodhya-itinerary-for-2-days.html` |
