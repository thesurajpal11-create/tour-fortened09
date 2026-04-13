const navToggle = document.getElementById("navToggle");
const navMenu = document.getElementById("navMenu");
const topSlider = document.querySelector(".top-slider");
const topSlides = document.querySelectorAll(".top-slide");
const sliderDots = document.querySelectorAll(".slider-dot");
const sliderPrev = document.getElementById("sliderPrev");
const sliderNext = document.getElementById("sliderNext");
const enquiryForm = document.getElementById("enquiryForm");
const formFeedback = document.getElementById("formFeedback");
const currentYear = document.getElementById("currentYear");
const pickupDate = document.getElementById("pickupDate");

let currentSlideIndex = 0;
let sliderIntervalId = null;

if (currentYear) {
    currentYear.textContent = new Date().getFullYear();
}

if (pickupDate) {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, "0");
    const day = String(today.getDate()).padStart(2, "0");
    pickupDate.min = `${year}-${month}-${day}`;
}

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

function setFeedback(message, type) {
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

if (enquiryForm) {
    enquiryForm.addEventListener("submit", (event) => {
        event.preventDefault();

        const fields = enquiryForm.querySelectorAll("input, select, textarea");
        let isValid = true;

        fields.forEach((field) => {
            const fieldIsValid = validateField(field);
            if (!fieldIsValid) {
                isValid = false;
            }
        });

        if (!isValid) {
            setFeedback("Please fill all required fields with valid details.", "error");
            return;
        }

        setFeedback("Your enquiry has been submitted. Our team will contact you soon.", "success");
        enquiryForm.reset();

        if (pickupDate) {
            const today = new Date();
            const year = today.getFullYear();
            const month = String(today.getMonth() + 1).padStart(2, "0");
            const day = String(today.getDate()).padStart(2, "0");
            pickupDate.min = `${year}-${month}-${day}`;
        }
    });
}
