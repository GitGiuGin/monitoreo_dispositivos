const adminCheck = document.getElementById('adminCheck');
    const adminFields = document.getElementById('adminFields');

    adminCheck.addEventListener('change', function() {
        if (this.checked) {
            adminFields.style.display = 'flex';
        } else {
            adminFields.style.display = 'none';
            // Limpiar valores al ocultar
            adminFields.querySelectorAll('input').forEach(input => input.value = '');
        }
    });