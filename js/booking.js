const BOOKING_API_BASE_URL = window.RAMNAGARI_API_BASE_URL || "http://127.0.0.1:8000";

const state = {
    token: localStorage.getItem("ramnagari_customer_token") || "",
    user: JSON.parse(localStorage.getItem("ramnagari_customer_user") || "null"),
    estimate: null,
    booking: null,
};

const loginTab = document.getElementById("loginTab");
const signupTab = document.getElementById("signupTab");
const loginForm = document.getElementById("loginForm");
const signupForm = document.getElementById("signupForm");
const bookingForm = document.getElementById("bookingForm");
const estimateButton = document.getElementById("estimateButton");
const bookingSummary = document.getElementById("bookingSummary");

function field(id) {
    return document.getElementById(id);
}

function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>"']/g, (character) => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        "\"": "&quot;",
        "'": "&#39;",
    }[character]));
}

function formatRupees(value) {
    return new Intl.NumberFormat("en-IN", {
        style: "currency",
        currency: "INR",
        maximumFractionDigits: 0,
    }).format(value || 0);
}

function showMessage(id, message, type = "success") {
    const element = field(id);
    element.textContent = message;
    element.className = `booking-message ${type}`;
}

function authHeaders() {
    return {
        "Content-Type": "application/json",
        Authorization: `Bearer ${state.token}`,
    };
}

async function api(path, options = {}) {
    if (!BOOKING_API_BASE_URL) {
        throw new Error("Online booking is unavailable because the backend is not deployed.");
    }

    const response = await fetch(`${BOOKING_API_BASE_URL}${path}`, {
        ...options,
        headers: {
            ...(options.auth ? authHeaders() : { "Content-Type": "application/json" }),
            ...(options.headers || {}),
        },
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
        throw new Error(data.detail || "Request failed. Please try again.");
    }
    return data;
}

function setAuthMode(mode) {
    const isLogin = mode === "login";
    loginTab.classList.toggle("is-active", isLogin);
    signupTab.classList.toggle("is-active", !isLogin);
    loginForm.classList.toggle("is-hidden", !isLogin);
    signupForm.classList.toggle("is-hidden", isLogin);
    showMessage("authMessage", "");
}

function saveSession(result) {
    state.token = result.access_token;
    state.user = result.user;
    localStorage.setItem("ramnagari_customer_token", state.token);
    localStorage.setItem("ramnagari_customer_user", JSON.stringify(state.user));
}

function buildBookingPayload() {
    return {
        destination_id: Number(field("destinationSelect").value),
        hotel_category: field("hotelCategorySelect").value,
        cab_type: field("cabTypeSelect").value,
        tourists: Number(field("touristsInput").value),
        stay_days: Number(field("stayDaysInput").value),
        hotel_option_id: field("hotelOptionSelect").value ? Number(field("hotelOptionSelect").value) : null,
    };
}

function renderEstimate(estimate, paymentOrder = null) {
    const paymentBlock = paymentOrder
        ? `
            <div class="summary-payment">
                <strong>Payment Order Ready</strong>
                <span>Advance: ${formatRupees(paymentOrder.amount)}</span>
                <button type="button" class="btn btn-primary" id="payNowButton">Pay Now</button>
            </div>
        `
        : "";

    bookingSummary.innerHTML = `
        <h2>Estimate</h2>
        <div class="summary-list">
            <div><span>Tour</span><strong>${escapeHtml(estimate.tour)}</strong></div>
            <div><span>Hotel</span><strong>${escapeHtml(estimate.display_name)}</strong></div>
            <div><span>Cab</span><strong>${escapeHtml(estimate.cab)}</strong></div>
            <div><span>Tourists</span><strong>${escapeHtml(estimate.tourists)}</strong></div>
            <div><span>Rooms</span><strong>${escapeHtml(estimate.rooms)}</strong></div>
            <div><span>Days</span><strong>${escapeHtml(estimate.days)}</strong></div>
            <div><span>Cab Total</span><strong>${formatRupees(estimate.cab_total)}</strong></div>
            <div><span>Hotel Total</span><strong>${formatRupees(estimate.hotel_total)}</strong></div>
            <div><span>Service Charge</span><strong>${formatRupees(estimate.service_charge)}</strong></div>
            <div class="summary-total"><span>Total</span><strong>${formatRupees(estimate.total_amount)}</strong></div>
            <div class="summary-total"><span>Advance Payment</span><strong>${formatRupees(estimate.advance_payment_amount)}</strong></div>
        </div>
        ${paymentBlock}
    `;

    const payNowButton = document.getElementById("payNowButton");
    if (payNowButton && paymentOrder) {
        payNowButton.addEventListener("click", () => openRazorpay(paymentOrder));
    }
}

async function loadDestinations() {
    const destinations = await api("/api/catalog/destinations");
    field("destinationSelect").innerHTML = destinations
        .map((destination) => `<option value="${destination.id}">${escapeHtml(destination.name)}</option>`)
        .join("");
}

async function loadCabs() {
    const cabs = await api("/api/catalog/cab-types");
    field("cabTypeSelect").innerHTML = cabs
        .map((cab) => `<option value="${escapeHtml(cab.cab_type)}">${escapeHtml(cab.cab_type)} - ${cab.capacity} seats</option>`)
        .join("");
}

async function loadHotelOptions() {
    const destinationId = field("destinationSelect").value;
    const category = field("hotelCategorySelect").value;
    const hotelOptionSelect = field("hotelOptionSelect");

    if (!destinationId || !category) {
        hotelOptionSelect.innerHTML = "<option value=\"\">Best available option</option>";
        return;
    }

    const params = new URLSearchParams({ destination_id: destinationId, category });
    const options = await api(`/api/catalog/hotel-options?${params.toString()}`);
    hotelOptionSelect.innerHTML = [
        "<option value=\"\">Best available option</option>",
        ...options.map((option) => (
            `<option value="${option.hotel_option_id}">${escapeHtml(option.display_name)} - ${formatRupees(option.selling_price_per_room)}</option>`
        )),
    ].join("");
}

async function estimateTrip() {
    const estimate = await api("/api/catalog/estimate", {
        method: "POST",
        body: JSON.stringify(buildBookingPayload()),
    });
    state.estimate = estimate;
    state.booking = null;
    renderEstimate(estimate);
    return estimate;
}

async function createBooking() {
    if (!state.token) {
        throw new Error("Please login or sign up before creating a booking.");
    }

    const booking = await api("/api/bookings/", {
        method: "POST",
        auth: true,
        body: JSON.stringify(buildBookingPayload()),
    });
    state.booking = booking;
    state.estimate = booking;
    renderEstimate(booking);
    return booking;
}

async function createPaymentOrder(bookingId) {
    return api(`/api/bookings/${bookingId}/payment/order`, {
        method: "POST",
        auth: true,
    });
}

function openRazorpay(order) {
    if (!window.Razorpay) {
        showMessage("bookingMessage", "Razorpay checkout could not load. Check your internet connection.", "error");
        return;
    }

    const checkout = new window.Razorpay({
        key: order.key_id,
        amount: Math.round(order.amount * 100),
        currency: order.currency,
        name: "Ramnagari Tourism",
        description: `Advance payment for booking #${order.booking_id}`,
        order_id: order.razorpay_order_id,
        prefill: {
            name: state.user?.name || "",
            email: state.user?.email || "",
            contact: state.user?.phone || "",
        },
        handler: async (response) => {
            try {
                await api("/api/bookings/payment/verify", {
                    method: "POST",
                    auth: true,
                    body: JSON.stringify({
                        razorpay_order_id: response.razorpay_order_id,
                        razorpay_payment_id: response.razorpay_payment_id,
                        razorpay_signature: response.razorpay_signature,
                    }),
                });
                showMessage("bookingMessage", "Payment verified. Your booking is pending admin approval.");
            } catch (error) {
                showMessage("bookingMessage", error.message, "error");
            }
        },
        modal: {
            ondismiss: () => showMessage("bookingMessage", "Payment window closed before completion.", "error"),
        },
    });
    checkout.open();
}

loginTab.addEventListener("click", () => setAuthMode("login"));
signupTab.addEventListener("click", () => setAuthMode("signup"));

loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    showMessage("authMessage", "Logging in...");
    try {
        const result = await api("/api/auth/login", {
            method: "POST",
            body: JSON.stringify({
                email: field("loginEmail").value.trim(),
                password: field("loginPassword").value,
            }),
        });
        saveSession(result);
        showMessage("authMessage", `Logged in as ${result.user.name}.`);
    } catch (error) {
        showMessage("authMessage", error.message, "error");
    }
});

signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    showMessage("authMessage", "Creating account...");
    try {
        await api("/api/auth/signup", {
            method: "POST",
            body: JSON.stringify({
                name: field("signupName").value.trim(),
                email: field("signupEmail").value.trim(),
                phone: field("signupPhone").value.trim() || null,
                password: field("signupPassword").value,
            }),
        });
        const result = await api("/api/auth/login", {
            method: "POST",
            body: JSON.stringify({
                email: field("signupEmail").value.trim(),
                password: field("signupPassword").value,
            }),
        });
        saveSession(result);
        setAuthMode("login");
        showMessage("authMessage", `Account created. Logged in as ${result.user.name}.`);
    } catch (error) {
        showMessage("authMessage", error.message, "error");
    }
});

estimateButton.addEventListener("click", async () => {
    showMessage("bookingMessage", "Calculating estimate...");
    try {
        await estimateTrip();
        showMessage("bookingMessage", "Estimate ready.");
    } catch (error) {
        showMessage("bookingMessage", error.message, "error");
    }
});

bookingForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    showMessage("bookingMessage", "Creating booking...");
    try {
        const booking = await createBooking();
        showMessage("bookingMessage", "Booking created. Preparing payment...");
        const paymentOrder = await createPaymentOrder(booking.id);
        renderEstimate(booking, paymentOrder);
        showMessage("bookingMessage", "Payment order ready. Click Pay Now.");
    } catch (error) {
        showMessage("bookingMessage", error.message, "error");
    }
});

field("destinationSelect").addEventListener("change", () => {
    loadHotelOptions().catch((error) => showMessage("bookingMessage", error.message, "error"));
});
field("hotelCategorySelect").addEventListener("change", () => {
    loadHotelOptions().catch((error) => showMessage("bookingMessage", error.message, "error"));
});

Promise.all([loadDestinations(), loadCabs()])
    .then(loadHotelOptions)
    .then(() => {
        if (state.user) {
            showMessage("authMessage", `Logged in as ${state.user.name}.`);
        }
    })
    .catch((error) => showMessage("bookingMessage", error.message, "error"));
