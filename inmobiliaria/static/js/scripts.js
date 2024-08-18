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
