async function login(userData){
    try {
        const response = await fetch("http://212.193.27.136/tokens/tokens/", {
          method: "POST", // Метод запроса
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: new URLSearchParams(userData),
        });
    } catch (err) {
        console.error("Ошибка при создании пользователя:", err);
        // пробрасываем ошибку наверх, чтобы вызывающий код мог обработать её
        throw err;
    }
}

const form = document.querySelector(".reg-form.center-column.card");

document.getElementById("btn-login").addEventListener("click", async () => {
    console.log(form);
    const formData = new FormData(form);

    const data = Object.fromEntries(formData.entries());
    console.log(data);

    // переход после успешной регистрации
    try {
        await login(data);
        goTo("screen-home.html");
    } catch (err) {
        alert("Ошибка входа, проверьте консоль.");
    }
});