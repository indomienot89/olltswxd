const tg = window.Telegram.WebApp;
tg.expand();

tg.SettingsButton.hide();

const theme = tg.colorScheme; // "light" atau "dark"

// Cek apakah benar dibuka lewat WebApp
if (!tg.initDataUnsafe || !tg.initDataUnsafe.user) {
    document.getElementById("loading").innerText =
        "❗ Harus dibuka melalui Telegram Mini App, bukan lewat browser.";
    throw new Error("Not inside Telegram WebApp");
}

const user = tg.initDataUnsafe.user;

// Lanjut: fetch ke server
fetch("/membershipcheck", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: user.id })
})
.then(res => res.json())
.then(data => {
    document.getElementById("loading").style.display = "none";
    document.getElementById("result").style.display = "block";

    document.getElementById("uid").innerText = data.user_id;
    document.getElementById("fname").innerText = data.full_name;
    document.getElementById("uname").innerText = "@" + data.username;

    const list = document.getElementById("membership-list");
    list.innerHTML = "";

    data.membership_data.forEach(item => {
        const li = document.createElement("li");
        li.className = "list-group-item d-flex justify-content-between";
        li.innerHTML = `<span><b>${item.group}</b></span><span>${item.status}</span>`;
        list.appendChild(li);
    });

    document.getElementById("result").style.display = "block";
});