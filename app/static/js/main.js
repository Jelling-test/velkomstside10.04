// Funktion til at håndtere sletning af menupunkter via JavaScript POST
function deleteMenuItem(itemId, itemName) {
    if (confirm(`Er du sikker på, at du vil slette "${itemName}"?`)) {
        // Opret en formular dynamisk
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/admin/delete_menu_item/${itemId}`;
        document.body.appendChild(form);
        form.submit();
    }
}

// Funktion til at håndtere sletning af bager-produkter
function deleteBakeryItem(itemId, itemName) {
    if (confirm(`Er du sikker på, at du vil slette "${itemName}"?`)) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/admin/delete_bakery_item/${itemId}`;
        document.body.appendChild(form);
        form.submit();
    }
}

// Funktion til at håndtere sletning af arrangementer
function deleteEvent(eventId, eventTitle) {
    if (confirm(`Er du sikker på, at du vil slette "${eventTitle}"?`)) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/admin/delete_event/${eventId}`;
        document.body.appendChild(form);
        form.submit();
    }
}

// Funktion til at håndtere sletning af kampagner
function deletePromotion(promotionId, promotionTitle) {
    if (confirm(`Er du sikker på, at du vil slette "${promotionTitle}"?`)) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/admin/delete_promotion/${promotionId}`;
        document.body.appendChild(form);
        form.submit();
    }
}

// Funktion til at opdatere antal-feltet i rundstykkebestillinger
function updateQuantity(id, change) {
    const inputElement = document.getElementById(`quantity_${id}`);
    let value = parseInt(inputElement.value) || 0;
    value = Math.max(0, value + change);
    inputElement.value = value;
}

// Funktion til at validere rundstykkebestillingsformularen
function validateBakeryOrderForm() {
    let hasItems = false;
    const quantityInputs = document.querySelectorAll('input[name^="quantity_"]');
    
    quantityInputs.forEach(input => {
        if (parseInt(input.value) > 0) {
            hasItems = true;
        }
    });
    
    if (!hasItems) {
        alert('Du skal vælge mindst én vare.');
        return false;
    }
    
    return true;
}

// Initialiser tooltips og popovers når dokumentet er klar
document.addEventListener('DOMContentLoaded', function() {
    // Initialiser Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialiser Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Tilføj validering til rundstykkebestillingsformularen hvis den findes
    const bakeryOrderForm = document.getElementById('bakeryOrderForm');
    if (bakeryOrderForm) {
        bakeryOrderForm.addEventListener('submit', function(event) {
            if (!validateBakeryOrderForm()) {
                event.preventDefault();
            }
        });
    }
});
