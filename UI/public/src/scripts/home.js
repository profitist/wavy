async function loadTracks() {
    try {
        const response = await fetch("https://dospivosos.ru/tracks/", {
            method: "GET",
        });
        if (!response.ok) throw new Error("Ошибка загрузки треков");
        return await response.json();
    } catch (err) {
        console.error("Ошибка при загрузке треков:", err);
        return [];
    }
}

async function searchTrackByName(name) {
    try {
        const response = await fetch(
            `https://dospivosos.ru/tracks/?q=${name}`,
            { method: "GET" }
        );

        if (!response.ok) return [];
        return await response.json();
    } catch (err) {
        console.error("Ошибка поиска:", err);
        return [];
    }
}

async function sendTrack(track, description) {
    const token = localStorage.getItem('access_token')
    try {
        const response = await fetch("https://dospivosos.ru/shared_track/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
            },
            body: JSON.stringify({ track, description }),
        });

        if (!response.ok) throw new Error(await response.text());
        return await response.json();
    } catch (err) {
        console.error("Ошибка отправки трека:", err);
        alert("Не удалось отправить трек.");
    }
}

async function loadFeed() {
    const token = localStorage.getItem("access_token");

    try {
        const response = await fetch("https://dospivosos.ru/feed/", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
            },
        });

        if (!response.ok) {
            throw new Error("Ошибка загрузки уведомлений");
        }

        return await response.json();
    } catch (err) {
        console.error("Ошибка при загрузке feed:", err);
        return [];
    }
}

function createNotificationItem(item) {
    const li = document.createElement("li");
    li.className = "home-notification-item";

    li.innerHTML = `
        <div class="home-notification-left" type = "button" data-link = "${item.track.external_link}">
            <div class="home-notification-cover">
                <svg fill="none" height="52" viewBox="0 0 52 52" width="52" xmlns="http://www.w3.org/2000/svg">
                    <rect fill="#7F7F7F" height="52" rx="11" width="52"></rect>
                </svg>
                <div class="home-notification-play">▶️</div>
            </div>
        </div>

        <div class="home-notification-main">
            <div class="home-notification-title">
                ${item.track.title}
            </div>
            <div class="home-notification-artist">
                ${item.track.author}
            </div>
        </div>

        <div class="home-notification-right">
            <img
                class="home-notification-avatar"
                src="src/assets/avatars/mini_avatars/png/avatar_${item.sender.user_picture_number}.png"
                alt="${item.sender.username}"
            />
            <div class="home-notification-sender">
                ${item.sender.username}
            </div>
        </div>
    `;

    return li;
}

async function renderFeed() {
    const list = document.querySelector(".home-notifications");
    if (!list) return;

    list.innerHTML = "";

    const feed = await loadFeed();

    if (!feed.length) {
        list.innerHTML = `<li class="home-notification-item">Пока нет уведомлений</li>`;
        return;
    }

    feed.forEach(item => {
        list.appendChild(createNotificationItem(item));
    });
}


document.addEventListener("DOMContentLoaded", async () => {
    renderFeed();
    const searchInput = document.querySelector(".share-search-input");
    const list = document.querySelector(".share-track-list");

    const selectedCard = document.querySelector(".share-selected-track");
    const selectedTitle = selectedCard?.querySelector(".share-item-title");
    const selectedAuthor = selectedCard?.querySelector(".share-item-subtitle");


    const sendBtnStep3 = document.querySelector('[data-step="2"] .share-btn-primary');

    if (!searchInput || !list) return;

    let selectedTrack = null;

    const allTracks = await loadTracks();

    function createTrackElement(track) {
        const li = document.createElement("li");
        li.classList.add("share-list-item");

        li.innerHTML = `
            <div class="share-cover"></div>
            <div class="share-item-main">
                <div class="share-item-title">${track.title}</div>
                <div class="share-item-subtitle">${track.author}</div>
            </div>
            <button class="share-radio" type="button"></button>
        `;

        li.querySelector(".share-radio").addEventListener("click", () => {
            [...list.children].forEach(el => el.classList.remove("active"));
            li.classList.add("active");
            selectedTrack = track;
        });

        return li;
    }

    function renderFirstThree() {
        list.innerHTML = "";
        allTracks.slice(0, 3).forEach(t => list.appendChild(createTrackElement(t)));
    }

    renderFirstThree();

    searchInput.addEventListener("input", async () => {
        const query = searchInput.value.trim();

        if (query === "") {
            selectedTrack = null;
            return renderFirstThree();
        }

        const results = await searchTrackByName(query);
        list.innerHTML = "";

        if (!results?.length) {
            list.innerHTML = `<li class="share-list-item">Не найдено</li>`;
            selectedTrack = null;
            return;
        }

        results.forEach(track => {
            list.appendChild(createTrackElement(track));
            list.firstChild.classList.add("active");
        })
    });

    const step1NextBtn = document.querySelector('[data-step="1"] [data-go-step="2"]');

    step1NextBtn?.addEventListener("click", () => {
        if (!selectedTrack) {
            alert("Выберите трек!");
            return;
        }

        selectedTitle.textContent = selectedTrack.title;
        selectedAuthor.textContent = selectedTrack.author;
    });

    sendBtnStep3?.addEventListener("click", async () => {
        if (!selectedTrack) {
            alert("Ошибка: трек не выбран.");
            return;
        }

        await sendTrack(selectedTrack, "");
        //alert("Трек успешно отправлен!");
    });

    document.addEventListener("click",async(event) => {
        const shareBtn = event.target.closest('.home-notification-left');
        if (!shareBtn){
            return;
        }
        window.location.href = shareBtn.dataset.link;
    })
});
