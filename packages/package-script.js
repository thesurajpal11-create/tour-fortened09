const brochureGeneratedAt = new Date().getFullYear();

document.documentElement.style.setProperty("--brochure-year", `"${brochureGeneratedAt}"`);

document.querySelectorAll("[data-print-package]").forEach((button) => {
  button.addEventListener("click", () => {
    window.print();
  });
});
