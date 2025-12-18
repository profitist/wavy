
function goTo(page) {
  window.location.href = page;
}

document.addEventListener('DOMContentLoaded', () => {
  const toggles = document.querySelectorAll('.settings-toggle');

  toggles.forEach((btn) => {
    btn.addEventListener('click', () => {
      const current = btn.getAttribute('aria-pressed') === 'true';
      btn.setAttribute('aria-pressed', (!current).toString());
    });
  });
});

function setShareStep(step) {
  const steps = document.querySelectorAll('.share-step');
  const target = String(step);

  steps.forEach((stepEl) => {
    const num = stepEl.getAttribute('data-step');
    stepEl.classList.toggle('active', num === target);
  });
} 

function openSharePopup(startStep = 0) {
  if (!document.getElementById('share-popup')) return;
  (document.getElementById('share-popup')).classList.add('active');
  setShareStep(startStep);
}

function closeSharePopup() {
  if (!document.getElementById('share-popup')) return;

  (document.getElementById('share-popup')).classList.remove('active');
}

document.addEventListener('DOMContentLoaded', () => {
  const overlay = document.getElementById('share-popup');
  if (!overlay) return; // Нет попапа — выходим

  const closeBtn = document.getElementById('share-popup-close');
  if (closeBtn) closeBtn.addEventListener('click', closeSharePopup);

  const goButtons = overlay.querySelectorAll('[data-go-step]');
  goButtons.forEach((btn) => {
    btn.addEventListener('click', () => {
      const step = btn.getAttribute('data-go-step');
      if (step) setShareStep(step);
    });
  });

  overlay.addEventListener('click', (event) => {
    if (event.target === overlay) closeSharePopup();
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeSharePopup();
  });
});

function openAddFriendPopup() {
  const overlay = document.getElementById('add-friend-popup');
  if (!overlay) return;

  overlay.classList.add('active');
}

function closeAddFriendPopup() {
  const overlay = document.getElementById('add-friend-popup');
  if (!overlay) return;

  overlay.classList.remove('active');
}

document.addEventListener('DOMContentLoaded', () => {
  const overlay = document.getElementById('add-friend-popup');
  if (!overlay) return; // Нет попапа — выходим

  const closeBtn = document.getElementById('add-friend-close');
  if (closeBtn) closeBtn.addEventListener('click', closeAddFriendPopup);

  overlay.addEventListener('click', (event) => {
    if (event.target === overlay) closeAddFriendPopup();
  });
});

function openFriendRequestsPopup() {
  const overlay = document.getElementById('new-friends-popup');
  if (!overlay) return;

  overlay.classList.add('active');
}

function closeFriendRequestsPopup() {
  const overlay = document.getElementById('new-friends-popup');
  if (!overlay) return;

  overlay.classList.remove('active');
}

document.addEventListener('DOMContentLoaded', () => {
  const overlay = document.getElementById('new-friends-popup');
  if (!overlay) return; // Нет попапа — выходим

  const closeBtn = document.getElementById('new-friends-popup-close');
  if (closeBtn) closeBtn.addEventListener('click', closeFriendRequestsPopup);

  overlay.addEventListener('click', (event) => {
    if (event.target === overlay) closeFriendRequestsPopup();
  });
});

function openChangeAvatarPopup() {
  const overlay = document.getElementById('avatar-popup');
  if (!overlay) return;

  overlay.classList.add('active');
}

function closeChangeAvatarPopup() {
  const overlay = document.getElementById('avatar-popup');
  if (!overlay) return;

  overlay.classList.remove('active');
  document.location.reload();
}

document.addEventListener('DOMContentLoaded', () => {
  const overlay = document.getElementById('avatar-popup');
  if (!overlay) return; // Нет попапа — выходим

  const closeBtn = document.getElementById('new-friends-popup-close');
  if (closeBtn) closeBtn.addEventListener('click', closeChangeAvatarPopup);

  overlay.addEventListener('click', (event) => {
    if (event.target === overlay) closeChangeAvatarPopup();
  });
});

