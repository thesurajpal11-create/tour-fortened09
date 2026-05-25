const fs = require("fs");
const path = require("path");

const siteUrl = "https://www.ramnagritourism.com";
const today = new Date().toISOString().slice(0, 10);

const pages = [
  { loc: "/", changefreq: "weekly", priority: "1.0" },
  { loc: "/blog.html", changefreq: "weekly", priority: "0.9" },
  { loc: "/blogs/ram-mandir-ayodhya-travel-guide-2026.html", changefreq: "monthly", priority: "0.88" },
  { loc: "/blogs/ayodhya-2-day-tour-plan.html", changefreq: "monthly", priority: "0.86" },
  { loc: "/blogs/ayodhya-to-kashi-tour-guide.html", changefreq: "monthly", priority: "0.86" },
  { loc: "/blogs/prayagraj-sangam-tour-guide.html", changefreq: "monthly", priority: "0.84" },
  { loc: "/blogs/chitrakoot-tour-guide.html", changefreq: "monthly", priority: "0.84" },
  { loc: "/ayodhya-tour-package.html", changefreq: "weekly", priority: "0.9" },
  { loc: "/kashi-tour-package.html", changefreq: "weekly", priority: "0.9" },
  { loc: "/prayagraj-tour-package.html", changefreq: "weekly", priority: "0.9" },
  { loc: "/chitrakoot-tour-package.html", changefreq: "weekly", priority: "0.85" },
  { loc: "/naimisharanya-tour-package.html", changefreq: "weekly", priority: "0.85" },
  { loc: "/ayodhya-cab-service.html", changefreq: "weekly", priority: "0.9" },
  { loc: "/pages/destinations.html", changefreq: "weekly", priority: "0.82" },
  { loc: "/pages/tour-packages.html", changefreq: "weekly", priority: "0.82" },
  { loc: "/pages/hotels.html", changefreq: "weekly", priority: "0.8" },
  { loc: "/pages/cab.html", changefreq: "weekly", priority: "0.8" },
  { loc: "/pages/booking.html", changefreq: "weekly", priority: "0.8" },
  { loc: "/pages/contact.html", changefreq: "monthly", priority: "0.75" },
  { loc: "/destinations/ayodhya/", changefreq: "monthly", priority: "0.8" },
  { loc: "/destinations/varanasi/", changefreq: "monthly", priority: "0.8" },
  { loc: "/destinations/prayagraj/", changefreq: "monthly", priority: "0.8" },
  { loc: "/destinations/chitrakoot/", changefreq: "monthly", priority: "0.8" },
  { loc: "/destinations/mathura/", changefreq: "monthly", priority: "0.74" },
  { loc: "/destinations/vindhyachal/", changefreq: "monthly", priority: "0.72" },
];

const urlEntries = pages
  .map(({ loc, changefreq, priority }) => {
    return [
      "    <url>",
      `        <loc>${siteUrl}${loc}</loc>`,
      `        <lastmod>${today}</lastmod>`,
      `        <changefreq>${changefreq}</changefreq>`,
      `        <priority>${priority}</priority>`,
      "    </url>",
    ].join("\n");
  })
  .join("\n");

const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urlEntries}
</urlset>
`;

fs.writeFileSync(path.join(__dirname, "..", "sitemap.xml"), sitemap);
console.log(`Generated sitemap.xml with ${pages.length} URLs and lastmod ${today}`);
