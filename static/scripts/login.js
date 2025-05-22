document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.getElementById("signin");

    if (loginForm) {
        loginForm.addEventListener("submit", function(event) {
            event.preventDefault();
            document.getElementById("loading").style.display = "flex"; // Показываем загрузку
            
            setTimeout(() => {
                loginForm.submit();
            }, 1000); // Ждем перед отправкой
        });
    }
});
