const chatBox = document.getElementById("chatBox");

async function sendMessage() {

    const file = document.getElementById("fileInput").files[0];
    const prompt = document.getElementById("prompt").value;

    if (!file) return alert("Upload image first");

    addMsg("user", prompt, URL.createObjectURL(file));

    showTyping();

    const form = new FormData();
    form.append("image", file);
    form.append("prompt", prompt);

    const res = await fetch("/edit-image", {
        method: "POST",
        body: form
    });

    const data = await res.json();

    hideTyping();

    if (data.status === "success") {
        addMsg("ai", "Result", null, "/" + data.result);
    }

}

function addMsg(role, text, img = null, result = null) {

    const div = document.createElement("div");
    div.className = role === "user" ? "msg user" : "msg ai";

    let html = "";

    if (text) html += `<p>${text}</p>`;
    if (img) html += `<img src="${img}">`;
    if (result) html += `<img src="${result}">`;

    div.innerHTML = html;
    chatBox.appendChild(div);

    chatBox.scrollTop = chatBox.scrollHeight;
}

function showTyping() {
    const div = document.createElement("div");
    div.id = "typing";
    div.className = "msg ai";
    div.innerHTML = "AI is processing...";
    chatBox.appendChild(div);
}

function hideTyping() {
    const t = document.getElementById("typing");
    if (t) t.remove();
}