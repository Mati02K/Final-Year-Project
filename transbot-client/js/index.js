const API_PATH = 'https://quasarcommunity.org/drobotAPI/retreive.php';

const connect = (postData) => {
    const jsonData = JSON.stringify(postData);
    return $.ajax({
        type: 'POST',
        data: {
            myData: jsonData,
        },
        timeout: 60000,
        url: API_PATH,
    }).then((response) => response);
};

$(() => {
    connect('').then((response) => {
        response = JSON.parse(response);
        const products = response.Items;
        let i = 0;
        let productContainer = '';
        while(i < products.length) {
            let j = 0;
            productContainer += '<div class="row">';
            while( j < 3 && j < products.length){
                const product = products[i];
                const available = product.available;
                if(available) {
                    const productName = product.pname;
                    const productPrice = product.price;
                    const productImage = product.image_url;
                    productContainer += `<div class="col-sm-4">
                    <div class="card"> <div class="imgBox">`
                    + `<img class="mouse" src="${productImage}" alt="${productName}">`
                    + `</div>
                    <div class="contentBox">
                    <h3>${productName}</h3>
                    <h2 class="price"> &#8377; ${productPrice}</h2>
                    <a href="checkout.html?pid=${product.pid}&price=${productPrice}&name=${productName}" class="buy">Buy Now</a>
                </div>
                </div>
                </div>`;
                j++;
                }  
                i++;
            }
            productContainer += '</div>';
        }
        $('#products').append(productContainer);
    });
});