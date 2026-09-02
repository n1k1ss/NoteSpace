const form = document.getElementById("registerForm");
const loader = document.getElementById("loader");
const result = document.getElementById("result");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    const result = document.getElementById("result");

    if (password !== confirmPassword) {
        result.textContent = "Passwords do not match";
        return;
    }

    try {
        loader.classList.remove("hidden");

        const response = await fetch("/api/auth/register", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                username: username,
                email: email,
                password: password
            })
        });

        const data = await response.json();

        result.textContent = data.message;

        form.reset();

        if (response.ok && data.redirect) {
            setTimeout(() => {
                window.location.href = data.redirect;
            }, 1000);
        }

    } catch (error) {
        result.textContent = "Something went wrong";
    }

    finally {
        loader.classList.add("hidden");
    }
});