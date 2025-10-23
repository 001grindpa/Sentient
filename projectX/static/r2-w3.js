document.addEventListener("DOMContentLoaded", function() {
    if (document.body.id === "index") {
        console.log("yet to add any js")
    }

    // js for sign up page
    else if (document.body.id === "signup-page") {
        form = document.querySelector("#signup");

        form.addEventListener("submit", async (e) => {
            e.preventDefault()
            let newForm = new FormData(form)

            try {
                let response = await fetch("/signup", {
                    method: "POST",
                    body: newForm
                })
                let data = await response.json()
                console.log(data)
            }
            catch(error) {
                console.log(error)
            }
        })
    }
})