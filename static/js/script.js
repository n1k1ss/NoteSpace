const form = document.getElementById("noteForm");
const loader = document.getElementById("loader");
const result = document.getElementById("result");

form.addEventListener("submit", async (event) => {

    event.preventDefault();

    const title = document.getElementById("title").value;
    const text = document.getElementById("text").value;

    try {
        loader.classList.remove("hidden");

        const response = await fetch("/api/notes/create", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                title: title,
                text: text
            })

        });

        const data = await response.json();

        result.textContent = data.message;

        form.reset();

    } catch (error) {
        result.textContent = "Something went wrong";
    }

    finally {
        loader.classList.add("hidden");
    }

    setTimeout(() => {
        result.textContent = ""
    }, 3000)

});