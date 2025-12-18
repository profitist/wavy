export async function login(userData) {
    try {
        const response = await fetch("http://212.193.27.136/users/token", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams(userData),
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('refresh_token', data.refresh_token);
            return data;
        }
        else {
            throw new Error('Login failed');
        }

    } catch (err) {
        console.error("Ошибка входа:", err);
        throw err;
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".reg-form.center-column.card");
    const btn = document.getElementById("btn-login");

    if (!form || !btn) return;

    btn.addEventListener("click", async () => {
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        try {
            await login(data);
            goTo("screen-home.html");
        } catch (err) {
            alert("Ошибка входа, проверьте консоль.");
        }
    });
});
