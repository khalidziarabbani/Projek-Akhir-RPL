// For editing the valur of the Cart
var updateBtns2 = document.getElementsByClassName('update-cart2')
for(var i = 0; i < updateBtns2.length; i++){
    updateBtns2[i].addEventListener('click', function(){
        var productId  = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'Action:', action)
        console.log('USER:', user)
        if(user == 'AnonymousUser'){
            console.log('Not logged in')
            alert('You need to login first to add items to your cart.')
        }else{
            updateUserOrder2(productId, action)
        }
    })
}

function updateUserOrder2(productId, action){
    console.log('User is logged in, sending data...')

    var url = '/update_item2/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId':productId, 'action':action})
    })

    .then((response) => {
        return response.json()
    })

    .then((response) => {
        console.log('data:', response)
        location.reload()
    })
}