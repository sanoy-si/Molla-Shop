
var numberInput = document.getElementsByClassName('myNumberInput');
for (var i = 0; i<=updateBtns.length; i++){

    numberInput[i].addEventListener('change', function() {
    var value = this.value;
    var productId = this.dataset.product
    var action = 'set'
    console.log('New value:', value,productId);
    updateCart2(productId,action,value)
    // Perform any desired actions based on the new value
});
}
function updateCart2(productId, action,value) {
    var url = '/setcart/';
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productId': productId, 'action': action,'value':value})
    })
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            console.log('data:', data);
            location.reload();
        });
}