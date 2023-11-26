var updateBtns = document.getElementsByClassName('update-cart');

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log('productId:', productId, 'Action:', action);
        console.log('USER:', user);

        updateUserOrder(productId, action);
    })
}

function updateUserOrder(productId, action) {
    console.log('User is authenticated, sending data...');

    var url = '/update_item/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ 'productId': productId, 'action': action })
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log('Data:', data);

        var clickedButton = document.querySelector('.update-cart[data-product="' + productId + '"][data-action="' + action + '"]');
        var container = clickedButton.closest('.cart-row');

        document.querySelector('.cart-total').innerText = data.cartItems;

        var itemQuantityElement = document.querySelector('.quantity'); 
        if (itemQuantityElement) {
            itemQuantityElement.innerText = data.itemQuantity;

			if (data.itemQuantity <= 0) {
                var cartRow = itemQuantityElement.closest('.cart-row');
                if (cartRow) {
                    cartRow.remove();
                }
            }
        }

		var totalItemsElement = document.querySelector('.total-items');
        var totalAmountElement = document.querySelector('.total-amount');

        if (totalItemsElement && totalAmountElement) {
            totalItemsElement.innerText = data.cartItems;
            totalAmountElement.innerText = '$' + data.cartTotal.toFixed(2); 
        }

        var itemTotalElement = container.querySelector('.item-total');
        if (itemTotalElement) {
            itemTotalElement.innerText = '$' + data.itemTotal.toFixed(2);
        }
    });
    //location.reload();
}
