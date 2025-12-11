function createUser(userData) {
    const response = await fetch('http://212.193.27.136/user/'), {
          method: 'POST', // Метод запроса
          headers: {
            'Content-Type': 'application/json', // Указываем, что отправляем JSON
          },
          body: JSON.stringify(userData), // Преобразуем объект в строку JSON
        };

    if (!response.ok) {
          throw new Error(`Ошибка HTTP: ${response.status}`);
        }
    const newUser = await response.json();
    console.log('Новый пользователь:', newUser);
    return newUser;
}


const form = document.querySelector("reg-form");

document.getElementById("btn-register").addEventListener("click", () => {
    const formData = new FormData(form);

    const data = Object.fromEntries(formData.entries());
    console.log(data);

    if (data.password !== data.repeatPassword) {
            alert("Пароли не совпадают");
            return;
        }

    // переход после успешной регистрации
    createUser(data)
    goTo("screen-home.html");
});
