document.addEventListener("DOMContentLoaded", function() {
    if (document.body.id === "index") {
        console.log("yet to add any js");
    }

    // js for sign up page
    else if (document.body.id === "signup-page") {
        let form = document.querySelector("#signup");
        let username = document.querySelector("#username");
        let p = document.querySelector("#p");
        let p2 = document.querySelector("#p2");
        let submit = document.querySelector("#submit");
        let nameC = document.querySelector("#username + div");
        let notice = document.querySelector(".notice");

        form.addEventListener("input", async () => {
            let newForm = new FormData(form);

            let response = await fetch("/signupCheck", {
                    method: "POST",
                    body: newForm
                });
            let data = await response.json();
            notice.textContent = data.msg;
            console.log(data.msg);

            if (data.msg === "This username is not available") {
                nameC.textContent = data.msg;
                notice.textContent = "";
                submit.disabled = true;
            }
            else if (p2.value != p.value) {
                submit.disabled = true;
            }
            else {
                nameC.textContent = "";
                notice.textContent = "valid match";
                submit.disabled = false;
            }
           
            if (p2.value === "") {
                notice.textContent = "";
            }
        })
    }
    // js for login page
    else if (document.body.id === "login") {
        const form = document.querySelector("#signup");

        form.addEventListener("submit", async (e) => {
            let newForm = new FormData(form);

            try {
                let response = await fetch("/login", {
                    method: "POST",
                    body: newForm
                })
                let data = await response.json();
                console.log(JSON.stringify(data));
            }
            catch(error) {
                console.log(error);
            }
        })
    }
})