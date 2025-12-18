async function createUser(userData) {
    console.log(JSON.stringify(userData))
    try {
        const response = await fetch("http://212.193.27.136/users/", {
          method: "POST",
          headers: {
            "Content-Type" : "application/json",
          },
          body: JSON.stringify(userData),
        });

        if (!response.ok) {
          throw new Error(`Ошибка HTTP: ${response.status}`);
        }
        const newUser = await response.json();
        console.log("Новый пользователь:", newUser);
    } catch (err) {
        console.error("Ошибка при создании пользователя:", err);
        throw err;
    }
}

const form = document.querySelector(".reg-form");

document.getElementById("btn-register").addEventListener("click", async () => {
    console.log(form);
    const formData = new FormData(form);

    const data = Object.fromEntries(formData.entries());
    console.log(data);
//
//    if (data.password !== data.repeatPassword) {
//            alert("Пароли не совпадают");
//            return;
//    }

    try {
        await createUser(data);
        goTo("screen-home.html");
    } catch (err) {
        alert("Ошибка регистрации, проверьте консоль.");
    }
});
