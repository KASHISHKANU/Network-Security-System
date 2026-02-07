const spot = document.querySelector(".cursor-spot");

document.addEventListener("mousemove", e => {
    if (!spot) return;
    spot.style.left = e.clientX + "px";
    spot.style.top = e.clientY + "px";
});

const form = document.querySelector("form");
const loader = document.getElementById("loader");

if (form && loader) {
    form.addEventListener("submit", () => {
        loader.classList.remove("hidden");
    });
}

document.querySelectorAll(".threat-table tbody tr").forEach(row => {
    const rowText = row.innerText;

    if (rowText.includes("MALICIOUS")) {
        row.classList.add("tr-malicious");
    }

    if (rowText.includes("SAFE")) {
        row.classList.add("tr-safe");
    }
});

document.addEventListener("DOMContentLoaded", () => {
});
