setTimeout(function() {
    const message = document.getElementById('auto-hide-message');
    if (message) {
        message.style.display = 'none';
    }
}, 5000);


document.addEventListener('DOMContentLoaded', function() {
    const rutInput = document.getElementById('id_rut');

    rutInput.addEventListener('input', function() {
        let value = this.value;
        if (value.length > 0 && value[value.length - 1].toLowerCase() === 'k') {
            this.value = value.slice(0, -1) + 'K';
        }
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


document.addEventListener('DOMContentLoaded', function () {
    const regionSelect = document.getElementById('region');
    const comunaSelect = document.getElementById('commune');

    if (regionSelect) {
        regionSelect.addEventListener('change', function () {
            const regionId = this.value;
            comunaSelect.innerHTML = '<option value="">Seleccione una comuna</option>';

            if (regionId) {
                fetch(`/get_comunas/${regionId}/`)
                    .then(response => response.json())
                    .then(data => {
                        data.forEach(comuna => {
                            const option = document.createElement('option');
                            option.value = comuna.id;
                            option.textContent = comuna.name;
                            comunaSelect.appendChild(option);
                        });
                    })
                    .catch(error => console.error('Error fetching comunas:', error));
            }
        });
    }
});


function confirmDelete(propertyId) {
    if (confirm("¿Estás seguro de que deseas eliminar esta propiedad?")) {
        fetch(`/property/delete/${propertyId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            } else {
                alert('Error al eliminar la propiedad.');
            }
        });
    }
}
