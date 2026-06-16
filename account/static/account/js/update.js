function updateProfile(event) {
    event.preventDefault();
    const form = document.getElementById('updateForm');
    const formData = new FormData(form);

    fetch(form.dataset.url, {   // ← we'll pass URL via data attribute, cleaner
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const msg = document.getElementById('message');
        msg.innerText = data.message;
        msg.style.color = data.status === 'success' ? 'green' : 'red';
    });
}