const API_PATH = 'http://43.204.81.69/fetch';

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
    $.ajax({
        type: 'POST',
        data: '',
        timeout: 60000,
        url: API_PATH,
    }).then((responses) => {
        console.log(responses);
        const noOfRecords = Object.keys(responses).length;
        for(let i = 1; i <= noOfRecords; i++) {
            const oid = responses[i][0];
            const name = responses[i][1];
            const mobno = responses[i][2];
            const prodid = responses[i][4];
            const qty = responses[i][5];
            const location = responses[i][7];
            let deliverystatus = responses[i][9];
            if(deliverystatus === 0){
                deliverystatus = "Not Delivered";
            }
            else {
                deliverystatus = "Delivered";
            }
            $('#admintable tbody').append("<tr><td>" + 
            oid + "</td><td>" + name + "</td><td>" +
            mobno+ "</td><td>" + prodid +  "</td><td>" +
            qty + "</td><td>" + location + "</td><td>" + deliverystatus + "</td></tr>");
        }
        $('#admintable').DataTable();
    });
    
});
