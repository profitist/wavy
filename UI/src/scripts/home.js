
async function loadTracks() {
    try {
        const response = await fetch("http://212.193.27.136/tracks/", {
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
            `http://212.193.27.136/tracks/?title=${name}`,
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
        const response = await fetch("http://212.193.27.136/shared_track/", {
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

document.addEventListener("DOMContentLoaded", async () => {
    const searchInput = document.querySelector(".share-search-input");
    const list = document.querySelector(".share-track-list");

    const selectedCard = document.querySelector(".share-selected-track");
    const selectedTitle = selectedCard?.querySelector(".share-item-title");
    const selectedAuthor = selectedCard?.querySelector(".share-item-subtitle");

    const sendBtnStep3 = document.querySelector('[data-step="2"] .share-btn-primary');

    // Если этих элементов нет — значит это НЕ страница "share"
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

        const found = results[0];
        selectedTrack = found;

        list.appendChild(createTrackElement(found));
        list.firstChild.classList.add("active");
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
        alert("Трек успешно отправлен!");
    });
});
