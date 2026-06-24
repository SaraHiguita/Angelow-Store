document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.alert-dismissible').forEach(function (alert) {
        setTimeout(function () {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    document.addEventListener('click', function (e) {
        var target = e.target.closest('[data-confirm]');
        if (target) {
            if (!confirm(target.dataset.confirm || '¿Estás seguro?')) {
                e.preventDefault();
            }
        }
    });
});

// HTMX: actualizar contador del carrito después de cada request
document.addEventListener('htmx:afterSwap', function () {
    var countEl = document.getElementById('cart-count-value');
    if (countEl) {
        var count = parseInt(countEl.textContent, 10) || 0;
        var alpineEl = document.querySelector('[x-data]');
        if (alpineEl && alpineEl.__x) {
            alpineEl.__x.$data.cartCount = count;
        }
    }
});

document.addEventListener('htmx:beforeSwap', function (evt) {
    if (evt.detail.xhr.status === 401) {
        window.location.href = '/accounts/login/';
    }
});

document.addEventListener('htmx:responseError', function (evt) {
    var message = evt.detail.xhr.responseText || 'Error del servidor';
    var container = document.getElementById('messages-container');
    if (container) {
        var alert = document.createElement('div');
        alert.className = 'alert alert-danger alert-dismissible fade show';
        alert.innerHTML = message + '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>';
        container.appendChild(alert);
    }
});
