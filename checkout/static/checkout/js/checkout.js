$(document).ready(function(){    

    // Required to add paceholders to profile form page //

    if($('#id_town').val()== ""){
            $('#id_town').css('color', '#aab7c4');            
        }    
    $('#id_town option:first-child').html('Town *');
    $('#id_town').change(function(){
        if($('#id_town option:selected').val()== ""){
            $('#id_town').css('color', '#aab7c4');
        }
        else{
            $('#id_town').css('color', 'black');
        }          
    })
    
    // Stripe Core logic  for payment //
    // let stripePublicKey = $('#stripe_public_key').val()
    // let clientSecret = $('#client_secret').val()
    var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
    var clientSecret = $('#id_client_secret').text().slice(1, -1);
    // var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
    // var clientSecret = $('#id_client_secret').text().slice(1, -1);
    // console.log(clientSecret)
    console.log(stripePublicKey)
    
    console.log(clientSecret)
    console.log('zahur')

}); 