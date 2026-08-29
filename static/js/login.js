const form = document.getElementById("loginForm");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const result = document.getElementById("result");

    try {
        const response = await fetch("/api/login", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                username: username,
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
});