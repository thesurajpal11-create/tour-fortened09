const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const requiredPaths = [
  "index.html",
  "404.html",
  "vercel.json",
  "CNAME",
  "sitemap.xml",
  "css/style.css",
  "js/main.js",
  "js/booking.js",
  "js/hotels.js",
  "ancient-kashi-history-archaeology.html",
  "ancient-ayodhya-history-archaeology.html",
  "blog.html",
  "pages/destinations.html",
  "pages/tour-packages.html",
  "pages/hotels.html",
  "pages/booking.html",
  "pages/cab.html",
  "pages/contact.html",
];

const missingRequired = requiredPaths.filter((item) => !fs.existsSync(path.join(root, item)));
if (missingRequired.length) {
  console.error("Missing required static files:");
  missingRequired.forEach((item) => console.error(`- ${item}`));
  process.exit(1);
}

function walk(dir, files = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if ([".git", "node_modules"].includes(entry.name)) {
        continue;
      }
      walk(fullPath, files);
    } else if (entry.name.endsWith(".html")) {
      files.push(fullPath);
    }
  }
  return files;
}

function isExternal(value) {
  return /^(https?:|\/\/|mailto:|tel:|javascript:|data:|#)/i.test(value);
}

function stripUrlParts(value) {
  return value.split("#")[0].split("?")[0];
}

function existsAsStaticFile(target) {
  if (fs.existsSync(target)) {
    return true;
  }
  if (!path.extname(target) && fs.existsSync(path.join(target, "index.html"))) {
    return true;
  }
  return false;
}

const attrPattern = /\b(?:href|src|action)=["']([^"']+)["']/gi;
const missingLinks = [];

for (const htmlFile of walk(root)) {
  const html = fs.readFileSync(htmlFile, "utf8");
  let match;

  while ((match = attrPattern.exec(html))) {
    const raw = match[1].trim();
    const clean = stripUrlParts(raw);
    if (!clean || isExternal(clean)) {
      continue;
    }

    const target = clean.startsWith("/")
      ? path.join(root, clean)
      : path.resolve(path.dirname(htmlFile), clean);

    if (!target.startsWith(root) || !existsAsStaticFile(target)) {
      missingLinks.push(`${path.relative(root, htmlFile)} -> ${raw}`);
    }
  }
}

if (missingLinks.length) {
  console.error("Missing internal links or assets:");
  missingLinks.forEach((item) => console.error(`- ${item}`));
  process.exit(1);
}

console.log("Static site verification passed.");
