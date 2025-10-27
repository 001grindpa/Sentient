document.addEventListener("DOMContentLoaded", function() {
    //js for landing page
    if (document.body.id === "landing") {
        let checkBox = document.querySelector("#learn");
        let contentCont = document.querySelector(".contentCont");
        let content = contentCont.querySelector(".content");

        contentCont.addEventListener("click", ()=> {
            if (checkBox.checked === true) {
                checkBox.checked = false;
            }
        });
        content.addEventListener("click", function(e) {
            e.stopPropagation();
        });
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
        });
    }
    // js for login page
    else if (document.body.id === "login") {
        const form = document.querySelector("#signup");
        let submit = document.querySelector("#submit");

        form.addEventListener("input", async (e) => {
            let newForm = new FormData(form);

            try {
                let response = await fetch("/loginCheck", {
                    method: "POST",
                    body: newForm
                })
                let data = await response.json();
                console.log(JSON.stringify(data));

                if (data.msg === "This account does not exist, please click 'sign up' to create an account") {
                    submit.disabled = true;
                }
                else {
                    submit.disabled = false;
                }
            }
            catch(error) {
                console.log(error);
            }
        });
    }
    // js for home page
    else if (document.body.id === "index") {
        let form = document.querySelector("#querry");
        let input = document.querySelector("#querry input");
        let btn = document.querySelector("#qBtn");
        let chatZone = document.querySelector(".chatZone");
        let info = document.querySelector(".infoArea div");

        form.addEventListener("submit", async (e) => {
            e.preventDefault();

            let newForm = new FormData(form);
            let queryText = newForm.get("q");
            input.value = "";
            console.log(queryText)

            let user = document.createElement("div");
            user.classList.add("userchat");
            let uDiv = document.createElement("div");
            user.appendChild(uDiv);
            uDiv.textContent = queryText;
            chatZone.appendChild(user);

            let r2 = document.createElement("div");
            r2.classList.add("r2Text");
            let img = document.createElement("img");
            img.src = "static/images/r2-w3_logo2.png";
            let gif = document.createElement("img");
            gif.classList.add("gif");
            gif.src = "static/gif/loading2.gif"
            gif.style.display = "block"
            r2.appendChild(gif);

            chatZone.appendChild(r2);
            chatZone.scrollTop = chatZone.scrollHeight;
            
            payload = {
                query: queryText
            };
            // response 1
            let response = await fetch("/assist1", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            })
            let data = await response.json();
            console.log(data.msg);
            // let response = await fetch("/test?q=" + queryText)
            // let data = await response.json();

            let r2T = document.createElement("div");
            r2T.classList.add("rText")
            let rDiv = document.createElement("div");
            r2T.appendChild(rDiv);
            rDiv.innerHTML = data.msg;


            setTimeout(() => {
                gif.style.display = "none";
                r2.appendChild(img);
                r2.appendChild(r2T);
                chatZone.scrollTop = chatZone.scrollHeight;
            }, 2000);
            
            // response 1
            let response2 = await fetch("/assist2", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            })
            let data2 = await response2.json();
            console.log(data2.msg);
            console.log(`length: ${(data2.msg).length}`);
            if ((data2.msg).length > 100) {
                info.innerHTML = data2.msg;
            }
            
            // console.log(data.msg);
        });
    }
})