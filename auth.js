// Authentication functions
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');

    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    if (signupForm) {
        signupForm.addEventListener('submit', handleSignup);
    }
});

async function handleLogin(e) {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('token', data.access_token);
            localStorage.setItem('user', JSON.stringify(data.user));
            showMessage('loginMessage', 'Login successful! Redirecting...', 'success');
            setTimeout(() => {
                window.location.href = '../index.html';
            }, 2000);
        } else {
            showMessage('loginMessage', data.detail || 'Login failed', 'error');
        }
    } catch (error) {
        console.error('Login error:', error);
        showMessage('loginMessage', 'Error logging in. Please try again.', 'error');
    }
}

async function handleSignup(e) {
    e.preventDefault();

    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm_password').value;

    if (password !== confirmPassword) {
        showMessage('signupMessage', 'Passwords do not match', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/auth/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: name,
                email: email,
                phone: phone,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            showMessage('signupMessage', 'Signup successful! Redirecting to login...', 'success');
            setTimeout(() => {
                window.location.href = 'login.html';
            }, 2000);
        } else {
            showMessage('signupMessage', data.detail || 'Signup failed', 'error');
        }
    } catch (error) {
        console.error('Signup error:', error);
        showMessage('signupMessage', 'Error creating account. Please try again.', 'error');
    }
}
