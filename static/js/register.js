const form = document.getElementById("registerForm");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    if (password !== confirmPassword) {
        document.getElementById("result").textContent =
            "Passwords do not match";

        return;
    }

    console.log({
        username,
        email,
        password
    });
});