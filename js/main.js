const navToggle = document.getElementById("navToggle");
const navMenu = document.getElementById("navMenu");
const topSlider = document.querySelector(".top-slider");
const topSlides = document.querySelectorAll(".top-slide");
const sliderDots = document.querySelectorAll(".slider-dot");
const sliderPrev = document.getElementById("sliderPrev");
const sliderNext = document.getElementById("sliderNext");
const enquiryForms = document.querySelectorAll(".enquiry-form");
const currentYear = document.getElementById("currentYear");
const pickupDate = document.getElementById("pickupDate");
const heroTravelDate = document.getElementById("heroTravelDate");
const reviewForm = document.getElementById("reviewForm");
const reviewList = document.getElementById("reviewList");
const reviewSummary = document.getElementById("reviewSummary");
const reviewFeedback = document.getElementById("reviewFeedback");
const faqItems = document.querySelectorAll(".faq-item");
const reviewsStorageKey = "ramnagariTourismReviews";
const reviewsSeededKey = "ramnagariTourismReviewsSeeded";
const minimumReviewRating = 4;
const defaultReviews = [
    {
        id: 1704101400001,
        name: "Amit Sharma",
        rating: 5,
        message: "Ramnagari Tourism planned our Ayodhya trip very well. Cab was clean, driver was polite, and the whole family felt comfortable.",
        createdAt: "2026-04-18T10:30:00.000Z",
    },
    {
        id: 1704101400002,
        name: "Priya Verma",
        rating: 5,
        message: "Very smooth service for darshan and local sightseeing. The team responded quickly and helped us with hotel and cab details.",
        createdAt: "2026-04-21T12:15:00.000Z",
    },
    {
        id: 1704101400003,
        name: "Sandeep Gupta",
        rating: 4,
        message: "Good tour package and transparent pricing. Our Prayagraj route was managed nicely and pickup was on time.",
        createdAt: "2026-04-24T15:20:00.000Z",
    },
    {
        id: 1704101400004,
        name: "Neha Singh",
        rating: 5,
        message: "Best travel support for a family trip. Booking was simple and the driver knew the temple routes very well.",
        createdAt: "2026-04-27T09:10:00.000Z",
    },
];

let currentSlideIndex = 0;
let sliderIntervalId = null;

if (currentYear) {
    currentYear.textContent = new Date().getFullYear();
}

function setMinimumToday(dateField) {
    if (!dateField) {
        return;
    }

    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, "0");
    const day = String(today.getDate()).padStart(2, "0");
    dateField.min = `${year}-${month}-${day}`;
}

setMinimumToday(pickupDate);
setMinimumToday(heroTravelDate);

if (navToggle) {
    navToggle.addEventListener("click", () => {
        const isOpen = navMenu.classList.toggle("is-open");
        navToggle.setAttribute("aria-expanded", String(isOpen));
    });
}

document.querySelectorAll(".nav-menu a").forEach((link) => {
    link.addEventListener("click", () => {
        navMenu.classList.remove("is-open");
        navToggle?.setAttribute("aria-expanded", "false");
    });
});

function showSlide(index) {
    if (!topSlides.length) {
        return;
    }

    currentSlideIndex = (index + topSlides.length) % topSlides.length;

    topSlides.forEach((slide, slideIndex) => {
        slide.classList.toggle("is-active", slideIndex === currentSlideIndex);
    });

    sliderDots.forEach((dot, dotIndex) => {
        dot.classList.toggle("is-active", dotIndex === currentSlideIndex);
    });
}

function nextSlide() {
    showSlide(currentSlideIndex + 1);
}

function previousSlide() {
    showSlide(currentSlideIndex - 1);
}

function startSlider() {
    if (!topSlides.length) {
        return;
    }

    stopSlider();
    sliderIntervalId = window.setInterval(nextSlide, 3500);
}

function stopSlider() {
    if (sliderIntervalId) {
        window.clearInterval(sliderIntervalId);
        sliderIntervalId = null;
    }
}

if (topSlider && topSlides.length) {
    showSlide(0);
    startSlider();

    sliderPrev?.addEventListener("click", () => {
        previousSlide();
        startSlider();
    });

    sliderNext?.addEventListener("click", () => {
        nextSlide();
        startSlider();
    });

    sliderDots.forEach((dot, index) => {
        dot.addEventListener("click", () => {
            showSlide(index);
            startSlider();
        });
    });

    topSlider.addEventListener("mouseenter", stopSlider);
    topSlider.addEventListener("mouseleave", startSlider);
}

function setFeedback(form, message, type) {
    const formFeedback = form.querySelector(".form-feedback");

    if (!formFeedback) {
        return;
    }

    formFeedback.textContent = message;
    formFeedback.className = `form-feedback ${type}`;
}

function validateField(field) {
    const value = field.value.trim();
    field.classList.remove("input-error");

    if (field.hasAttribute("required") && !value) {
        field.classList.add("input-error");
        return false;
    }

    if (field.type === "email" && value) {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(value)) {
            field.classList.add("input-error");
            return false;
        }
    }

    if (field.type === "tel" && value) {
        const digits = value.replace(/\D/g, "");
        if (digits.length < 10) {
            field.classList.add("input-error");
            return false;
        }
    }

    return true;
}

async function sendFormSubmitEmail(form) {
    const action = form.getAttribute("action");

    if (!action) {
        return false;
    }

    const response = await fetch(action, {
        method: "POST",
        body: new FormData(form),
        headers: {
            Accept: "application/json",
        },
    });

    return response.ok;
}

enquiryForms.forEach((enquiryForm) => {
    enquiryForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const fields = enquiryForm.querySelectorAll("input, select, textarea");
        const submitButton = enquiryForm.querySelector("button[type='submit']");
        let isValid = true;

        fields.forEach((field) => {
            const fieldIsValid = validateField(field);
            if (!fieldIsValid) {
                isValid = false;
            }
        });

        if (!isValid) {
            setFeedback(enquiryForm, "Please fill all required fields with valid details.", "error");
            return;
        }

        setFeedback(enquiryForm, "Submitting your enquiry...", "success");

        if (submitButton) {
            submitButton.disabled = true;
        }

        try {
            const emailSent = await sendFormSubmitEmail(enquiryForm);

            if (!emailSent) {
                throw new Error("FormSubmit did not confirm delivery.");
            }

            enquiryForm.reset();
            setFeedback(enquiryForm, "Thank you. Your enquiry has been sent successfully.", "success");
        } catch (error) {
            setFeedback(enquiryForm, "Sorry, your enquiry could not be sent. Please call or WhatsApp us.", "error");
        } finally {
            if (submitButton) {
                submitButton.disabled = false;
            }
        }
    });
});

function getSavedReviews() {
    try {
        const savedReviews = JSON.parse(localStorage.getItem(reviewsStorageKey) || "[]");
        const validReviews = Array.isArray(savedReviews) ? savedReviews : [];
        const approvedReviews = validReviews.filter((review) => Number(review.rating) >= minimumReviewRating);

        if (approvedReviews.length !== validReviews.length) {
            localStorage.setItem(reviewsStorageKey, JSON.stringify(approvedReviews));
        }

        return approvedReviews;
    } catch (error) {
        return [];
    }
}

function saveReviews(reviews) {
    localStorage.setItem(reviewsStorageKey, JSON.stringify(reviews));
}

function seedDefaultReviews() {
    if (localStorage.getItem(reviewsSeededKey) === "true") {
        return;
    }

    const savedReviews = getSavedReviews();
    const savedReviewIds = new Set(savedReviews.map((review) => review.id));
    const missingDefaultReviews = defaultReviews.filter((review) => !savedReviewIds.has(review.id));
    saveReviews([...missingDefaultReviews, ...savedReviews]);

    localStorage.setItem(reviewsSeededKey, "true");
}

function escapeReviewText(value) {
    return value.replace(/[&<>"']/g, (character) => {
        const entities = {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            "\"": "&quot;",
            "'": "&#039;",
        };
        return entities[character];
    });
}

function renderReviews() {
    if (!reviewList || !reviewSummary) {
        return;
    }

    const reviews = getSavedReviews();

    if (!reviews.length) {
        reviewSummary.textContent = "No reviews yet.";
        reviewList.innerHTML = "";
        return;
    }

    const averageRating = reviews.reduce((total, review) => total + review.rating, 0) / reviews.length;
    reviewSummary.textContent = `${averageRating.toFixed(1)} out of 5 from ${reviews.length} review${reviews.length === 1 ? "" : "s"}`;
    reviewList.innerHTML = reviews
        .map((review) => {
            const reviewDate = new Date(review.createdAt).toLocaleDateString("en-IN", {
                day: "numeric",
                month: "short",
                year: "numeric",
            });

            return `
                <article class="review-card">
                    <div class="review-card-header">
                        <h3>${escapeReviewText(review.name)}</h3>
                        <span class="review-stars" aria-label="${review.rating} out of 5 stars">${review.rating}/5</span>
                    </div>
                    <p>${escapeReviewText(review.message)}</p>
                    <span class="review-date">${reviewDate}</span>
                </article>
            `;
        })
        .join("");
}

if (reviewForm) {
    seedDefaultReviews();
    renderReviews();

    reviewForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const nameInput = reviewForm.querySelector("#reviewName");
        const ratingInput = reviewForm.querySelector("#reviewRating");
        const messageInput = reviewForm.querySelector("#reviewMessage");
        const submitButton = reviewForm.querySelector("button[type='submit']");
        const fields = [nameInput, ratingInput, messageInput];
        let isValid = true;

        fields.forEach((field) => {
            if (field && !validateField(field)) {
                isValid = false;
            }
        });

        if (!isValid) {
            if (reviewFeedback) {
                reviewFeedback.textContent = "Please write your name, rating, and review.";
                reviewFeedback.className = "form-feedback error";
            }
            return;
        }

        const rating = Number(ratingInput.value);

        if (rating < minimumReviewRating) {
            if (reviewFeedback) {
                reviewFeedback.textContent = "Please choose a rating of 4 stars or higher.";
                reviewFeedback.className = "form-feedback error";
            }
            return;
        }

        const reviews = getSavedReviews();
        reviews.unshift({
            id: Date.now(),
            name: nameInput.value.trim(),
            rating,
            message: messageInput.value.trim(),
            createdAt: new Date().toISOString(),
        });
        saveReviews(reviews);
        renderReviews();

        if (reviewFeedback) {
            reviewFeedback.textContent = "Review saved. Sending to Ramnagari Tourism...";
            reviewFeedback.className = "form-feedback success";
        }

        if (submitButton) {
            submitButton.disabled = true;
        }

        try {
            const emailSent = await sendFormSubmitEmail(reviewForm);

            if (reviewFeedback) {
                reviewFeedback.textContent = emailSent
                    ? "Review saved and sent to Ramnagari Tourism."
                    : "Review saved on this device.";
                reviewFeedback.className = "form-feedback success";
            }
        } catch (error) {
            if (reviewFeedback) {
                reviewFeedback.textContent = "Review saved on this device. Email sending could not be confirmed.";
                reviewFeedback.className = "form-feedback success";
            }
        } finally {
            reviewForm.reset();

            if (submitButton) {
                submitButton.disabled = false;
            }
        }
    });
}

faqItems.forEach((item) => {
    const question = item.querySelector(".faq-question");
    const answer = item.querySelector(".faq-answer");

    if (!question || !answer) {
        return;
    }

    question.addEventListener("click", () => {
        const isOpen = item.classList.contains("is-open");

        faqItems.forEach((otherItem) => {
            const otherQuestion = otherItem.querySelector(".faq-question");
            const otherAnswer = otherItem.querySelector(".faq-answer");

            otherItem.classList.remove("is-open");
            otherQuestion?.setAttribute("aria-expanded", "false");

            if (otherAnswer) {
                otherAnswer.style.maxHeight = "0";
            }
        });

        if (!isOpen) {
            item.classList.add("is-open");
            question.setAttribute("aria-expanded", "true");
            answer.style.maxHeight = `${answer.scrollHeight}px`;
        }
    });
});
