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
    let stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
    let clientSecret = $('#id_client_secret').text().slice(1, -1);
    
    let stripe = Stripe(stripePublicKey);
        let elements = stripe.elements();
        let style = {
            base: {
                color: '#000',
                fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
                fontSmoothing: 'antialiased',
                fontSize: '16px',
                '::placeholder': {
                    color: '#aab7c4'
                }
            },
            invalid: {
                color: '#dc3545',
                iconColor: '#dc3545'
            }
        };
        let card = elements.create('card', {style: style});
        card.mount('#card-element');

    // Handle realtime validation errors on the card element
    
    card.addEventListener('change', function (event) {
        var errorDiv = document.getElementById('card-errors');
        if (event.error) {
            var html = `
                <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                </span>
                <span>${event.error.message}</span>
            `;
            $(errorDiv).html(html);
        } else {
            errorDiv.textContent = '';
        }
    });
}); 