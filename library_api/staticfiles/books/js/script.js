// JavaScript for interactivity
document.addEventListener("DOMContentLoaded", () => {
    const toggleButton = document.getElementById("toggleTheme");
    toggleButton?.addEventListener("click", () => {
        document.body.classList.toggle("dark-mode");
    });
});
