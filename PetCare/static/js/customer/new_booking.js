function showProviders(serviceId) {
    document.querySelectorAll('.service-card').forEach(card =>
        card.classList.remove('active')
    );

    document.querySelectorAll('.provider-list').forEach(list =>
        list.classList.remove('active')
    );

    event.currentTarget.classList.add('active');
    document.getElementById(serviceId).classList.add('active');
}

function searchProviders() {
    const input = document.getElementById('searchInput').value.toLowerCase();
    const activeList = document.querySelector('.provider-list.active');
    if (!activeList) return;

    activeList.querySelectorAll('.provider-card').forEach(card => {
        const text = card.innerText.toLowerCase();
        card.style.display = text.includes(input) ? 'block' : 'none';
    });
}
