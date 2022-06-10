const getProductDetails = (urlString) => {
    const paramString = urlString.split('?')[1];
    const queryString = new URLSearchParams(paramString);
    let productDetails = {};
    let itr = 1;
    for(let pair of queryString.entries()) {
        if(itr == 1){
            productDetails['pid'] = pair[1];
        }
        else if(itr == 2){
            productDetails['price'] = pair[1];
        }
        else if(itr == 3){
            productDetails['name'] = pair[1];
        }
        itr += 1;
    }
    return productDetails;
};

const parseData = (productDetails) => {
    $('#pid').text(productDetails.pid);
    $('#pname').text(productDetails.name);
    $('#pamt').html(`&#8377;${productDetails.price}`);
    $('#tamt').html(`&#8377;${productDetails.price}`);
};

$(() => {
    const API_PATH = 'https://quasarcommunity.org/drobotAPI/checkout.php';
    const productDetails = getProductDetails(window.location.href);
    const pid = parseInt(productDetails.pid);
    const priceAmt = parseInt(productDetails.price);
    parseData(productDetails);
    $('#buy').on('click', function() {

        // Validating card details
        const cname = $('#cardname').val();
        const cardno = $('#cardno').val();
        const exp = $('#exp').val();
        const cvv = $('#cvv').val();


        if (cname && cardno && exp && cvv && cname.length > 5 && 
            cardno.length > 0 && exp.length > 0 && cvv.length > 0) {

            // Get the Location Details
            const showPosition = (position) => {
                const lat = position.coords.latitude;
                const long = position.coords.longitude;
                const locationDetails = lat + ',' + long;
                console.log(locationDetails);
                const fname = $('#firstName').val();
                const lname = $('#lastName').val();
                const email = $('#email').val();
                const phone = $('#mobno').val();
                const price = priceAmt;
                const qty = parseInt($('#qty').val());
                const orderDetails = {
                    pid : pid,
                    name : fname + ' ' + lname,
                    email : email,
                    mobno : phone,
                    amt : price,
                    quantity : qty,
                    location : locationDetails,
                };
                $.ajax({
                    type: 'POST',
                    data: orderDetails,
                    timeout: 60000,
                    url: API_PATH,
                }).then((response) => {
                    // console.log(response);
                    // console.log(response === 'Success');
                    location.replace('placed.html');
                    // if (response === 'Success') {
                    //     location.replace('placed.html');
                    // }
                    // else {
                    //     alert('Order failed. Please check your entered details or try again after some time.');
                    //     console.log("Order failed");
                    // }
                });
            };
                    
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(showPosition);
            } else {
                console.log("Geolocation is not supported by this browser.");
            }
        }
        else {
            alert("Please fill the card details to proceed");
        }
    });
});
