// API Base URL
const API_BASE_URL = 'http://localhost:8000/api';

// Check if user is logged in
function checkAuthStatus() {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');
    const authButtons = document.getElementById('authButtons');
    const userProfile = document.getElementById('userProfile');

    if (token && user) {
        if (authButtons) authButtons.style.display = 'none';
        if (userProfile) userProfile.style.display = 'block';
    } else {
        if (authButtons) authButtons.style.display = 'block';
        if (userProfile) userProfile.style.display = 'none';
    }
}

// Logout function
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    checkAuthStatus();
    window.location.href = '../index.html';
}

// Load featured destinations
async function loadFeaturedDestinations() {
    try {
        const response = await fetch(`${API_BASE_URL}/destinations`);
        const destinations = await response.json();
        
        const container = document.getElementById('featuredDestinations');
        if (!container) return;

        container.innerHTML = '';
        destinations.slice(0, 3).forEach(dest => {
            const card = createDestinationCard(dest);
            container.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading destinations:', error);
    }
}

// Create destination card element
function createDestinationCard(destination) {
    const card = document.createElement('div');
    card.className = 'destination-card';
    card.innerHTML = `
        <div class="destination-image">${destination.name.charAt(0)}</div>
        <div class="destination-content">
            <h3>${destination.name}</h3>
            <p>${destination.short_description}</p>
            <div class="destination-rating">
                <span class="stars">★★★★★ ${destination.rating}</span>
            </div>
            <a href="pages/destination-detail.html?id=${destination.id}" class="btn-primary">View Details</a>
        </div>
    `;
    return card;
}

// Load all destinations
async function loadAllDestinations() {
    try {
        const response = await fetch(`${API_BASE_URL}/destinations`);
        const destinations = await response.json();
        
        const container = document.getElementById('allDestinations');
        if (!container) return;

        container.innerHTML = '';
        destinations.forEach(dest => {
            const card = createDestinationCard(dest);
            container.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading destinations:', error);
    }
}

// Load destinations dropdown for booking
async function loadDestinationsDropdown() {
    try {
        const response = await fetch(`${API_BASE_URL}/destinations`);
        const destinations = await response.json();
        
        const select = document.getElementById('destination');
        if (!select) return;

        destinations.forEach(dest => {
            const option = document.createElement('option');
            option.value = dest.id;
            option.textContent = dest.name;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading destinations:', error);
    }
}

// Show message
function showMessage(elementId, message, type) {
    const element = document.getElementById(elementId);
    if (!element) return;

    element.textContent = message;
    element.className = type; // 'success' or 'error'
    element.style.display = 'block';
    
    setTimeout(() => {
        element.style.display = 'none';
    }, 5000);
}

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    checkAuthStatus();
    
    if (document.getElementById('featuredDestinations')) {
        loadFeaturedDestinations();
    }
    
    if (document.getElementById('allDestinations')) {
        loadAllDestinations();
    }
    
    if (document.getElementById('destination')) {
        loadDestinationsDropdown();
    }
});
