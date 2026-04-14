window.onload = function() {
    const menuBtn = document.getElementById('menuBtn');
    const sideScreen = document.getElementById('sideScreen');
    const overlay = document.getElementById('overlay');
    const langToggle = document.getElementById('langToggle');

    function toggleMenu() {
        if (!sideScreen || !overlay) return;
        sideScreen.classList.toggle('active');
        overlay.classList.toggle('active');
    }

    if (menuBtn && overlay) {
        menuBtn.addEventListener('click', toggleMenu);
        overlay.addEventListener('click', toggleMenu);
    } else {
        console.warn('Элементы не найдены. Проверьте ID в HTML!');
    }

    if (langToggle) {
        langToggle.addEventListener('click', function() {
            window.location.href = '/toggle-language';
        });
    }
};