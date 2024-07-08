document.getElementById('loginButton').addEventListener('click', async function () {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (username && password) {
        try {
            const response = await fetch('/api/v1/login/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            if (response.ok) {
                const data = await response.json();
                // Save the JWT token in local storage or cookie
                localStorage.setItem('jwtToken', data.token);
                // Redirect or do something after successful login
                alert('Login successful!');
            } else {
                alert('Login failed. Please check your credentials.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }
    } else {
        alert('Please fill in both fields.');
    }
});
