const form = document.getElementById("noteForm");
const result = document.getElementById("result");

form.addEventListener("submit", async (event) => {

    event.preventDefault();

    const title = document.getElementById("title").value;
    const text = document.getElementById("text").value;

    const response = await fetch("/api/notes", {

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

    setTimeout(() => {
        result.textContent = ""
    }, 1000)

});