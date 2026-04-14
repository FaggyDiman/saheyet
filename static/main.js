window.onload = function() {
    const menuBtn = document.getElementById('menuBtn');
    const sideScreen = document.getElementById('sideScreen');
    const overlay = document.getElementById('overlay');

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
};