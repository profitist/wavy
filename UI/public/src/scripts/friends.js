async function getFriends() {
    const token = localStorage.getItem('access_token');
    try {
        const response = await fetch("https://dospivosos.ru/friendships/", {
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
            }
        });
        if (!response.ok) throw new Error(await response.text());
        return await response.json();
    } catch (err) {
        console.error("Ошибка получения друзей:", err);
        alert("Не удалось загрузить друзей");
    }
}

function createFriendItem(friend, currentUsername) {
    const li = document.createElement("li");
    li.className = "friends-item";

    const img = document.createElement("img");
    img.className = "friends-avatar";
    img.alt = friend.username;

    const span = document.createElement("span");
    span.className = "friends-name";
    const { sender, receiver } = friend;
    img.src = `src/assets/avatars/mini_avatars/png/avatar_${(sender.username == currentUsername) ? receiver.user_picture_number : sender.user_picture_number}.png`;
    span.textContent = receiver.username == currentUsername ? sender.username : receiver.username;

    li.append(img, span);
    return li;
}

async function loadFriends() {
    const friendsList = document.querySelector(".friends-list");
    const currentUsername = localStorage.getItem('currentUsername');
    const friendships = await getFriends();
    if (!friendships) return;

    friendsList.innerHTML = "";
    friendships.forEach(friend => friendsList.appendChild(createFriendItem(friend, currentUsername)));
}

async function LoadPendingFriends() {
    const token = localStorage.getItem('access_token')
        try {
            const response = await fetch("https://dospivosos.ru/friendships/pending", {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            });

            if (!response.ok) throw new Error(await response.text());
            return await response.json();       
        } 
        catch (err) {
            console.error("Ошибка получения заявок в друзья:", err);
            alert("Упс, мы не смогли загрузить твоих новых друзей, но мы уверены что их куча");
        }
}

function createPendingFriendItem(username, avatarNumber) {
    const li = document.createElement('li');
    li.className = 'add-friend-item';

    li.innerHTML = `
        <img class="add-friend-avatar" src="src/assets/avatars/mini_avatars/png/avatar_${avatarNumber}.png" alt="${username}">
        <div class="add-friend-main">
            <div class="add-friend-name">${username}</div>
        </div>
        <div class="add-friend-icons">
            <button class="request-action request-action--accept" type="button" aria-label="Принять заявку">
                <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M18.6667 21.3333H9.33333C8.59696 21.3333 8 20.7364 8 20C8 19.2636 8.59695 18.6667 9.33333 18.6667H18.6667V9.33333C18.6667 8.59695 19.2636 8 20 8C20.7364 8 21.3333 8.59695 21.3333 9.33333V18.6667H30.6667C31.403 18.6667 32 19.2636 32 20C32 20.7364 31.403 21.3333 30.6667 21.3333H21.3333V30.6667C21.3333 31.403 20.7364 32 20 32C19.2636 32 18.6667 31.403 18.6667 30.6667V21.3333Z" fill="white"/>
                </svg>
            </button>
            <button class="request-action request-action--decline" type="button" aria-label="Отклонить заявку">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6 7H18" stroke="white" stroke-width="2" stroke-linecap="round"/>
                    <path d="M9 7V5H15V7" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M8 7L9 20H15L16 7" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M10 11V17" stroke="white" stroke-width="2" stroke-linecap="round"/>
                    <path d="M14 11V17" stroke="white" stroke-width="2" stroke-linecap="round"/>
                </svg>
            </button>
        </div>
    `;
    return li;
}

async function AcceptFriend(username) {
    const token = localStorage.getItem('access_token');

    try {
        const response = await fetch(`https://dospivosos.ru/friendships/accept/${username}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
            },
            body : username
        });
        if (!response.ok) throw new Error(await response.text());           
        } 
        catch (err) {
            console.error("Ошибка принятия заявки:", err);
            alert("Упс, может он передумал?");
        }
}

async function RejectFriend(username) {
    const token = localStorage.getItem('access_token');

    try {
        const response = await fetch(`https://dospivosos.ru/friendships/reject/${username}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
            },
            body : username
        });
        if (!response.ok) throw new Error(await response.text());           
        } 
        catch (err) {
            console.error("Ошибка удаления заявки:", err);
            alert("Упс, повод передумать?");
        }
}

function createAddFriendItem(username, avatarNumber) {
  const li = document.createElement('li');
  li.className = 'add-friend-item';

  li.innerHTML = `
    <img
      src="src/assets/avatars/mini_avatars/png/avatar_${avatarNumber}.png"
      alt="${username}"
      class="add-friend-avatar"
    />
    <div class="add-friend-main">
      <div class="add-friend-name">${username}</div>
    </div>
    <button class="add-friend-plus" type="button">
      <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M18.6667 21.3333H9.33333C8.59696 21.3333 8 20.7364 8 20C8 19.2636 8.59695 18.6667 9.33333 18.6667H18.6667V9.33333C18.6667 8.59696 19.2636 8 20 8C20.7364 8 21.3333 8.59695 21.3333 9.33333V18.6667H30.6667C31.403 18.6667 32 19.2636 32 20C32 20.7364 31.403 21.3333 30.6667 21.3333H21.3333V30.6667C21.3333 31.403 20.7364 32 20 32C19.2636 32 18.6667 31.403 18.6667 30.6667V21.3333Z" fill="white"/>
      </svg>
    </button>
  `;

  return li;
}

async function FindUser(username) {
    const token = localStorage.getItem('access_token');

    try {
        const response = await fetch(`https://dospivosos.ru/users/${username}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
            },
        });      
        if (!response.ok) throw new Error();
        return response.json();
        } 
        catch (err) {
        }
}

async function SendRequest(username) {
        const token = localStorage.getItem('access_token');
    try {
        const response = await fetch(`https://dospivosos.ru/friendships/send/${username}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
            },
            body : username
        });      
        if (!response.ok) throw new Error();
        return response.json();
        } 
    catch (err) {
    }
}

loadFriends();

document.addEventListener("DOMContentLoaded", async() => {
    const popup = document.querySelector(".add-friend-list");
    popup.innerHTML = "";
    const pendingFriends = await LoadPendingFriends(); 
    pendingFriends.forEach(friendship => popup.appendChild(createPendingFriendItem(friendship.sender.username, friendship.sender.user_picture_number)));
    
    popup.addEventListener("click", async(event) => {
    const declineBtn = event.target.closest('.request-action--decline');
    const acceptBtn = event.target.closest('.request-action--accept');

    if (acceptBtn) {
        const parentItem = acceptBtn.closest('.add-friend-item');
        username = parentItem.querySelector('.add-friend-name').textContent;
        await AcceptFriend(username);
        parentItem.remove();
    }

    else if (declineBtn) {   
        const parentItem = declineBtn.closest('.add-friend-item');
        username = parentItem.querySelector('.add-friend-name').textContent;
        await RejectFriend(username);
        parentItem.remove();
    }
    })

    const sendPopup = document.querySelector(".potential-friend-list");
    sendPopup.innerHTML = "";
    sendPopup.addEventListener("click", async(event) => {
        const send = event.target.closest('.add-friend-item');
        if (send){
            const parentItem = send.closest('.add-friend-item');
            username = parentItem.querySelector('.add-friend-name').textContent;
            await SendRequest(username);
            parentItem.remove();
        }
    })
    const search = document.querySelector(".share-search-bar");
    search.addEventListener("input", async (event) =>{
        sendPopup.innerHTML = "";
        const value = event.target.value;
        const user = await FindUser(value);
        if (user != null){
            sendPopup.appendChild(createAddFriendItem(user.username,user.user_picture_number));
        }
    })
});
