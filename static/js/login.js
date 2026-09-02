const form = document.getElementById("loginForm");
const loader = document.getElementById("loader");
const result = document.getElementById("result");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const result = document.getElementById("result");

    try {
        loader.classList.remove("hidden");

        const response = await fetch("/api/auth/login", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
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