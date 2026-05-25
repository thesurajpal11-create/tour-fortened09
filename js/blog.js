const blogSearch = document.getElementById("blogSearch");
const blogCards = Array.from(document.querySelectorAll(".blog-card"));
const blogFilters = Array.from(document.querySelectorAll(".blog-filter"));
const blogEmpty = document.getElementById("blogEmpty");

let activeBlogFilter = "all";

function normalizeText(value) {
    return value.trim().toLowerCase();
}

function getBlogHaystack(card) {
    return normalizeText([
        card.dataset.title || "",
        card.dataset.keywords || "",
        card.textContent || "",
    ].join(" "));
}

function filterBlogs() {
    const query = normalizeText(blogSearch?.value || "");
    let visibleCount = 0;

    blogCards.forEach((card) => {
        const categories = (card.dataset.category || "").split(" ");
        const matchesFilter = activeBlogFilter === "all" || categories.includes(activeBlogFilter);
        const matchesSearch = !query || getBlogHaystack(card).includes(query);
        const isVisible = matchesFilter && matchesSearch;

        card.hidden = !isVisible;
        if (isVisible) {
            visibleCount += 1;
        }
    });

    if (blogEmpty) {
        blogEmpty.hidden = visibleCount !== 0;
    }
}

blogSearch?.addEventListener("input", filterBlogs);

blogFilters.forEach((button) => {
    button.addEventListener("click", () => {
        activeBlogFilter = button.dataset.filter || "all";
        blogFilters.forEach((filterButton) => {
            filterButton.classList.toggle("is-active", filterButton === button);
        });
        filterBlogs();
    });
});
