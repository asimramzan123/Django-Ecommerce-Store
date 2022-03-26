

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
            // console.log('User is not authenticated')
            addCookieItem(productId, action)
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

function addCookieItem(productId, action){
    console.log('User is not Logged In')


    // // what actually addCookieItem is trying to come up with
    // cart ={
    //     // 1 is productId and then how much quantity is available
    //     1 : {"quantity":4},
    //     3 : {"quantity":2},
    // }

    // check the action
    if (action == 'add'){
        // if cart is empty or undefined then create cart
		if (cart[productId] == undefined){

		cart[productId] = {'quantity':1}

		}
        // if already there then go ahead and incrrease quantity
        else{
			cart[productId]['quantity'] += 1
		}
	}

    // decreasing quantity or removing the item

	if (action == 'remove'){
        // reduce by 1
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}

    // check cart value
    console.log('Cart',cart)
    // overwrite whatever cookies has set to the cart
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'

    // to check whether location gets updated
    location.reload()

}
