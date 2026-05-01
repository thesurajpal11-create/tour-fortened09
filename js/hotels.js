const API_BASE_URL = "http://127.0.0.1:8000";

const destinationSelect = document.getElementById("hotelDestinationSelect");
const categorySelect = document.getElementById("hotelCategorySelect");
const hotelFilterForm = document.getElementById("hotelFilterForm");
const hotelOptionsGrid = document.getElementById("hotelOptionsGrid");
const hotelStatus = document.getElementById("hotelStatus");

function formatRupees(value) {
    return new Intl.NumberFormat("en-IN", {
        style: "currency",
        currency: "INR",
        maximumFractionDigits: 0,
    }).format(value || 0);
}

function setHotelStatus(message, type = "") {
    hotelStatus.textContent = message;
    hotelStatus.className = `hotel-status ${type}`.trim();
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

function hotelOptionTemplate(option) {
    const amenities = option.amenities?.length
        ? option.amenities.map((amenity) => `<span>${escapeHtml(amenity)}</span>`).join("")
        : "<span>Comfort stay</span>";

    return `
        <article class="hotel-option-card">
            <div class="hotel-card-topline">
                <span class="hotel-category-pill">${escapeHtml(option.category)}</span>
                <strong>${formatRupees(option.selling_price_per_room)} / room</strong>
            </div>
            <h2>${escapeHtml(option.display_name)}</h2>
            <div class="hotel-facts">
                <span>${escapeHtml(option.rooms_available)} rooms available</span>
                <span>${escapeHtml(option.distance_from_tour_km)} km from tour place</span>
                <span>${escapeHtml(option.nearby_place || "Near main sightseeing area")}</span>
            </div>
            <div class="hotel-amenities">${amenities}</div>
            <div class="hotel-card-footer">
                <span>Check-in ${escapeHtml(option.check_in_time)}</span>
                <span>Check-out ${escapeHtml(option.check_out_time)}</span>
            </div>
            <a href="booking.html" class="btn btn-primary">Book Now</a>
        </article>
    `;
}

async function loadDestinations() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/catalog/destinations`);
        if (!response.ok) {
            throw new Error("Could not load destinations");
        }
        const destinations = await response.json();
        destinationSelect.innerHTML = destinations
            .map((destination) => `<option value="${destination.id}">${escapeHtml(destination.name)}</option>`)
            .join("");

        if (destinations.length) {
            await loadHotelOptions();
        } else {
            setHotelStatus("No destinations are available right now.", "error");
        }
    } catch (error) {
        destinationSelect.innerHTML = '<option value="">Backend not connected</option>';
        setHotelStatus("Start the backend at http://127.0.0.1:8000 to show live hotel prices.", "error");
    }
}

async function loadHotelOptions() {
    const destinationId = destinationSelect.value;
    const category = categorySelect.value;

    if (!destinationId) {
        setHotelStatus("Select a destination to view hotel options.");
        hotelOptionsGrid.innerHTML = "";
        return;
    }

    setHotelStatus("Loading hotel options...");
    hotelOptionsGrid.innerHTML = "";

    const params = new URLSearchParams({ destination_id: destinationId });
    if (category) {
        params.set("category", category);
    }

    try {
        const response = await fetch(`${API_BASE_URL}/api/catalog/hotel-options?${params.toString()}`);
        if (!response.ok) {
            throw new Error("Could not load hotel options");
        }
        const options = await response.json();

        if (!options.length) {
            setHotelStatus("No hotel options found for this destination and type.", "error");
            return;
        }

        setHotelStatus(`${options.length} hotel option${options.length > 1 ? "s" : ""} available.`, "success");
        hotelOptionsGrid.innerHTML = options.map(hotelOptionTemplate).join("");
    } catch (error) {
        setHotelStatus("Unable to load hotel options. Please check backend server.", "error");
    }
}

if (hotelFilterForm) {
    hotelFilterForm.addEventListener("submit", (event) => {
        event.preventDefault();
        loadHotelOptions();
    });
}

loadDestinations();
