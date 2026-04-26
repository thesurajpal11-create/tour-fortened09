function getYouTubeEmbedUrl(url) {
    if (!url) {
        return "";
    }

    const trimmed = url.trim();
    const patterns = [
        /youtube\.com\/watch\?v=([^&]+)/i,
        /youtu\.be\/([^?&]+)/i,
        /youtube\.com\/embed\/([^?&]+)/i
    ];

    for (const pattern of patterns) {
        const match = trimmed.match(pattern);
        if (match?.[1]) {
            return `https://www.youtube.com/embed/${match[1]}`;
        }
    }

    return "";
}

document.querySelectorAll("[data-gallery-upload]").forEach((galleryBlock) => {
    const input = galleryBlock.querySelector("[data-gallery-input]");
    const preview = galleryBlock.querySelector("[data-gallery-preview]");

    if (!input || !preview) {
        return;
    }

    input.addEventListener("change", () => {
        preview.innerHTML = "";

        const files = Array.from(input.files || []);
        if (!files.length) {
            return;
        }

        files.forEach((file) => {
            if (!file.type.startsWith("image/")) {
                return;
            }

            const item = document.createElement("div");
            item.className = "upload-preview-item";

            const image = document.createElement("img");
            image.src = URL.createObjectURL(file);
            image.alt = file.name || "Uploaded destination preview";
            image.addEventListener("load", () => URL.revokeObjectURL(image.src), { once: true });

            item.appendChild(image);
            preview.appendChild(item);
        });
    });
});

document.querySelectorAll(".video-section-grid").forEach((videoBlock) => {
    const fileInput = videoBlock.querySelector("[data-video-file-input]");
    const linkInput = videoBlock.querySelector("[data-video-link-input]");
    const filePreview = videoBlock.querySelector("[data-video-file-preview]");
    const youtubePreview = videoBlock.querySelector("[data-youtube-preview]");

    if (fileInput && filePreview) {
        fileInput.addEventListener("change", () => {
            filePreview.innerHTML = "";

            const file = fileInput.files?.[0];
            if (!file || !file.type.startsWith("video/")) {
                return;
            }

            const video = document.createElement("video");
            video.controls = true;
            video.src = URL.createObjectURL(file);
            video.addEventListener("loadeddata", () => URL.revokeObjectURL(video.src), { once: true });
            filePreview.appendChild(video);
        });
    }

    if (linkInput && youtubePreview) {
        const updateEmbed = () => {
            youtubePreview.innerHTML = "";

            const embedUrl = getYouTubeEmbedUrl(linkInput.value);
            if (!embedUrl) {
                youtubePreview.innerHTML = '<div class="video-preview-placeholder">Paste a YouTube link to preview it here.</div>';
                return;
            }

            const iframe = document.createElement("iframe");
            iframe.src = embedUrl;
            iframe.title = "Destination YouTube preview";
            iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
            iframe.allowFullscreen = true;
            youtubePreview.appendChild(iframe);
        };

        linkInput.addEventListener("input", updateEmbed);
        updateEmbed();
    }
});
