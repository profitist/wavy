function showScreen(id) {
  const screens = document.querySelectorAll('.screen');

  screens.forEach(screen => {
    screen.classList.remove('active');
  });

  const target = document.getElementById(id);
  if (target) {
    target.classList.add('active');
  }
}

// находим все переключатели
document.addEventListener('DOMContentLoaded', () => {
  const toggles = document.querySelectorAll('.settings-toggle');

  toggles.forEach((btn) => {
    btn.addEventListener('click', () => {
      const current = btn.getAttribute('aria-pressed') === 'true';
      btn.setAttribute('aria-pressed', (!current).toString());
    });
  });
});

// ======================
// Попап "Поделиться"
// ======================

function setShareStep(step) {
  const steps = document.querySelectorAll('.share-step');
  const target = String(step);

  steps.forEach((stepEl) => {
    const stepNum = stepEl.getAttribute('data-step');
    if (stepNum === target) {
      stepEl.classList.add('active');
    } else {
      stepEl.classList.remove('active');
    }
  });
}

function openSharePopup(startStep) {
  const overlay = document.getElementById('share-popup');
  if (!overlay) return;

  overlay.classList.add('active');
  // если не передали шаг — по умолчанию 0
  setShareStep(startStep != null ? startStep : 0);
}

function closeSharePopup() {
  const overlay = document.getElementById('share-popup');
  if (!overlay) return;

  overlay.classList.remove('active');
}

// вешаем обработчики после загрузки DOM
document.addEventListener('DOMContentLoaded', () => {
  const overlay = document.getElementById('share-popup');
  if (!overlay) return;

  // крестик закрытия
  const closeBtn = document.getElementById('share-popup-close1');
  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      closeSharePopup();
    });
  }

  // переходы по шагам: кнопки с data-go-step
  const goButtons = overlay.querySelectorAll('[data-go-step]');
  goButtons.forEach((btn) => {
    btn.addEventListener('click', () => {
      const targetStep = btn.getAttribute('data-go-step');
      if (targetStep != null) {
        setShareStep(targetStep);
      }
    });
  });

  // закрытие по клику вне окна (по фону)
  overlay.addEventListener('click', (event) => {
    if (event.target === overlay) {
      closeSharePopup();
    }
  });

  // закрытие по Esc
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      closeSharePopup();
    }
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
  if (!overlay) return;

  const closeBtn = document.getElementById('add-friend-close');
  if (closeBtn) {
    closeBtn.addEventListener('click', closeAddFriendPopup);
  }

  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) {
      closeAddFriendPopup();
    }
  });
});

