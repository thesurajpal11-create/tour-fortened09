# Bilingual Blog Update Report

Project root: `tour-fortened09`

## Goal

Add an in-page Hindi-English reading system to all blog pages, with Hindi as the default language and English available through a persistent toggle.

## Pages Updated

| Page | Status | Default Language | English Version | LocalStorage |
| --- | --- | --- | --- | --- |
| `ancient-ayodhya-history-archaeology.html` | Updated | Hindi | Added | `preferredBlogLanguage` |
| `ayodhya-itinerary-for-2-days.html` | Updated | Hindi | Added | `preferredBlogLanguage` |

## Language Toggle

Added a sticky language switcher near the top of each blog page.

Buttons:

- `हिंदी`
- `English`

Behavior:

- Hindi content is shown by default.
- English content appears when the English button is clicked.
- Hindi content appears again when the Hindi button is clicked.
- The selected language is saved in `localStorage` using the key `preferredBlogLanguage`.
- The same saved language is applied automatically across both blog pages.

## SEO Updates

Added hreflang alternates to both blog pages:

- `hreflang="hi-IN"`
- `hreflang="en-IN"`

The pages keep both language versions inside the same HTML file as requested. No separate language URLs were created.

## Content Updates

### Ancient Ayodhya: History, Archaeology and Spiritual Heritage

- Added a full Hindi reading version.
- Preserved the existing English heritage article.
- Kept article images, figures, captions, FAQ, CTA, schema, and internal links in place.
- English content remains written in a travel historian and local guide style.

### Ayodhya Itinerary for 2 Days

- Wrapped the existing Hindi/Hinglish itinerary content as the Hindi reading version.
- Added a natural English travel-guide version covering:
  - Two-day itinerary
  - Darshan flow
  - Saryu Aarti
  - Ram Mandir, Hanuman Garhi, Kanak Bhawan, Ram Ki Paidi
  - Cab and hotel guidance
  - FAQ
  - Related internal links
- Hid Hindi-only sticky WhatsApp and footer navigation while English mode is active.

## CSS Added

Updated `css/style.css` with:

- Sticky blog language switcher styling
- Active button highlight
- Responsive mobile layout
- Language content visibility rules

Main selectors added:

- `.blog-language-switcher`
- `.blog-language-switcher-inner`
- `.blog-language-label`
- `.blog-language-buttons`
- `.blog-lang-btn`
- `[data-lang-content]`
- `body[data-blog-lang="hi"] [data-lang-content="hi"]`
- `body[data-blog-lang="en"] [data-lang-content="en"]`

## JavaScript Added

Each blog page now includes a small language controller script that:

- Reads `preferredBlogLanguage` from `localStorage`
- Defaults to Hindi when no saved preference exists
- Switches visible content blocks
- Updates active button state
- Updates the page `lang` attribute between `hi-IN` and `en-IN`
- Saves the visitor's choice for other blog pages

## Internal Links

Internal links were preserved for:

- Ayodhya package
- Kashi package
- Prayagraj package
- Naimisharanya package
- Contact page

## Image and Schema Notes

- Existing images remain connected to the blog layout.
- Image paths were not broken by the bilingual update.
- FAQ and schema blocks remain available in the pages.
- No random stock images were added.

## Verification

Checked both pages for:

- Hindi and English content blocks
- Language toggle buttons
- `preferredBlogLanguage` usage
- Hindi and English hreflang tags
- Existing image path integrity

Final result: both required blog pages now support Hindi and English reading modes inside the same HTML file.
