window.addEventListener('load', function () {
    const menuBtn = document.getElementById('menuBtn');
    const sideScreen = document.getElementById('sideScreen');
    const overlay = document.getElementById('overlay');
    const langToggle = document.getElementById('langToggle');
    const mainsheet = document.getElementById('mainsheet');
    const locationContainer = document.getElementById('locationContainer');
    const appendContainer = document.getElementById('appendContainer');

    function toggleMenu() {
        if (!sideScreen || !overlay) return;
        sideScreen.classList.toggle('active');
        overlay.classList.toggle('active');
    }

    if (menuBtn && overlay) {
        menuBtn.addEventListener('click', toggleMenu);
        overlay.addEventListener('click', toggleMenu);
    }

    if (langToggle) {
        langToggle.addEventListener('click', function (event) {
            event.preventDefault();
            window.location.href = '/toggle-language';
        });
    }

    async function fetchLocationContent(name) {
        const response = await fetch(`/location/${encodeURIComponent(name)}`);
        if (!response.ok) {
            throw new Error(`Не удалось загрузить локацию ${name}`);
        }
        return response.text();
    }

    async function saveLocationState(mainLocation, extraLocation) {
        try {
            await fetch('/location/save', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    main_location: mainLocation,
                    extra_location: extraLocation || null,
                }),
            });
        } catch (error) {
            console.warn('Не удалось сохранить состояние локаций на сервере.', error);
        }
    }

    async function renderLocation(name, append = false) {
        if (!locationContainer || !appendContainer) return;

        const content = await fetchLocationContent(name);
        if (append) {
            const wrapper = document.createElement('section');
            wrapper.className = 'location-card appended-location';
            wrapper.dataset.locationName = name;
            wrapper.innerHTML = content;
            appendContainer.appendChild(wrapper);
        } else {
            locationContainer.innerHTML = '';
            appendContainer.innerHTML = '';
            const wrapper = document.createElement('section');
            wrapper.className = 'location-card active-location';
            wrapper.dataset.locationName = name;
            wrapper.innerHTML = content;
            locationContainer.appendChild(wrapper);
        }

        const mainLocation = append ? locationContainer.querySelector('[data-location-name]')?.dataset.locationName || name : name;
        const extraLocation = append ? name : '';

        await saveLocationState(mainLocation, extraLocation);
    }

    function bindLocationButtons() {
        document.addEventListener('click', async function (event) {
            const button = event.target.closest('[data-location-name]');
            if (!button) return;
            if (button.tagName !== 'BUTTON') return;

            event.preventDefault();
            const name = button.dataset.locationName;
            const action = button.dataset.locationAction;
            if (!name || !action) return;
            await renderLocation(name, action === 'append');
        });
    }

    function initSideNav() {
        const navBtns = document.querySelectorAll('.side-nav-btn');
        const views = document.querySelectorAll('.side-view');
        const titleDisplay = document.getElementById('side-view-title');

        navBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const targetView = btn.dataset.view;
                const viewName = btn.dataset.name;
                
                navBtns.forEach(b => b.classList.remove('active'));
                views.forEach(v => v.classList.remove('active'));

                btn.classList.add('active');
                const view = document.getElementById(`side-view-${targetView}`);
                if (view) view.classList.add('active');
                
                if (titleDisplay && viewName) {
                    titleDisplay.textContent = viewName;
                }
            });
        });
    }

    async function init() {
        bindLocationButtons();
        initSideNav();
        if (!mainsheet) return;
        const defaultLocation = mainsheet.dataset.defaultLocation || 'loc1';
        const extraLocation = mainsheet.dataset.extraLocation;
        try {
            await renderLocation(defaultLocation, false);
            if (extraLocation) {
                await renderLocation(extraLocation, true);
            }
        } catch (error) {
            if (locationContainer) {
                locationContainer.innerHTML = '<p class="location-error">Ошибка загрузки локации.</p>';
            }
            console.error(error);
        }
    }

    init();
});