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
    $('#otpcheck').on('click', function() {
        // Validating card details
        const orderid = $('#orderid').val();
        const onetimepass = $('#otp').val();
        if (orderid && onetimepass) {
            const otpDetails = {
                oid : orderid,
                otp : onetimepass,
            };
            $.ajax({
                type: 'POST',
                data: otpDetails,
                timeout: 60000,
                url: API_PATH,
            }).then((response) => {
                if(response == 'Success'){
                    alert('Success, the OTP is correct, you will receive the order by the Drobot');
                }
                else {
                    alert('Entered OTP is incorrect');
                }
            });
        }
    });
});