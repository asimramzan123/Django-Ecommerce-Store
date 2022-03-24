

// query all the cart items buttons by update-cart items

var UpdateButtons = document.getElementsByClassName('update-cart')


// looping through all buttons then add event listners to get prod id and action on click
for( i=0; i <UpdateButtons.length; i++){

    UpdateButtons[i].addEventListener('click', function(){

        // response on click
        // this is like self in python(item that clicked on)
        var productId = this.dataset.product
        var action = this.dataset.action

        console.log('Product_id:', productId, 'Action:', action)
    // checking if user is authenticated or not.
        console.log('User:',user )
        if (user == 'AnonymousUser'){
            console.log('User is not authenticated')
        }
        else{
            updateUserOrder(productId, action)
        }

        

    })
}

function updateUserOrder(productId, action){
    console.log('User is authenticated. sending data...')
    console.log("csrf=============")
    console.log(csrftoken)
    // adding up fetch call using POST method so that we could send data to update_item view
    var url = '/update_item/'
    fetch(url, {
        method:'POST',
        headers:{

            'Content-Type': 'application/json',
            // 'Accept': 'application/json',
            'X-CSRFTOKEN': csrftoken
        },
        // sending string to backend in this fetch api
        body: JSON.stringify({'productId': productId, 'action': action})
    })

    // response after we send the data to view, convert these values into json data.
    .then((response)=> {
        console.log("succes then")
        return response.json();
    })

    // print out the data
    .then((data)=> {
        // console.log('Data:',data)
        // to reload page to get new data
        location.reload()   
    });

}




