let token = localStorage.getItem("token");

const chat = document.getElementById("chat");


// ---------------- UI ----------------
function addMessage(role, text, image = null) {
    const div = document.createElement("div");
    div.classList.add("msg", role);

    div.innerHTML = `
        <div class="bubble">
            <b>${role}</b><br>
            ${text || ""}
            ${image ? `<br><img src="${image}">` : ""}
        </div>
    `;

    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}


// ---------------- LOADER ----------------
function showLoader() {
    document.getElementById("loader").style.display = "flex";
}

function hideLoader() {
    document.getElementById("loader").style.display = "none";
}


// animated dots
setInterval(() => {
    const el = document.getElementById("dots");
    if (!el) return;

    let count = Math.floor(Date.now() / 500) % 4;
    el.innerText = "Generating" + ".".repeat(count);
}, 500);


// ---------------- LOGIN ----------------
async function login() {

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const form = new FormData();
    form.append("username", username);
    form.append("password", password);

    const res = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        body: form
    });

    const data = await res.json();

    if (data.access_token) {
        token = data.access_token;
        localStorage.setItem("token", token);
        alert("Login successful");
        loadHistory();
    } else {
        alert("Login failed");
    }
}


// ---------------- SEND IMAGE ----------------
async function send() {

    const file = document.getElementById("file").files[0];
    const prompt = document.getElementById("prompt").value;

    if (!file || !prompt) {
        alert("Upload image + prompt");
        return;
    }

    addMessage("user", prompt, URL.createObjectURL(file));

    const form = new FormData();
    form.append("image", file);
    form.append("prompt", prompt);

    showLoader();

    try {
        const res = await fetch("http://127.0.0.1:8000/edit-image", {
            method: "POST",
            headers: {
                "Authorization": "Bearer " + token
            },
            body: form
        });

        const data = await res.json();

        if (data.status === "success") {
            addMessage(
                "ai",
                "Done",
                "http://127.0.0.1:8000" + data.image
            );
        } else {
            addMessage("ai", "Error processing image");
        }

    } catch (err) {
        addMessage("ai", "Server error");
    }

    hideLoader();
}


// ---------------- LOAD HISTORY ----------------
async function loadHistory() {

    const res = await fetch("http://127.0.0.1:8000/chat-history", {
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    const data = await res.json();

    if (!data.history) return;

    data.history.forEach(item => {
        const [role, msg, img, out] = item;

        const image = role === "user" ? img : out;

        addMessage(
            role,
            msg,
            image ? "http://127.0.0.1:8000/" + image : null
        );
    });
}


// auto-load if token exists
if (token) {
    loadHistory();
}