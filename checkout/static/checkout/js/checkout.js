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
    });
    
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
        let errorDiv = document.getElementById('card-errors');
        if (event.error) {
            let html = `
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
    
    // Handle form submit

    let form = document.getElementById('payment-form');

    // https://stackoverflow.com/questions/1085801/get-selected-value-in-dropdown-list-using-javascript
    let town = document.getElementById('id_town');    
     
    form.addEventListener('submit', function(ev){
        /* Prevents form from being submitted to view and instead runs the following function */
        ev.preventDefault();
        
        card.update({ 'disabled': true});    
        $('#submit-button').attr('disabled', true);
        $('#payment-form').fadeToggle(100);
        $('#loading-overlay').fadeToggle(100);

        
        let saveInfo = Boolean($('#id-save-info').attr('checked'));        
        let requestInfo = form.request.value;

        // From using {% csrf_token %} in the form
        let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        let postData = {
            'csrfmiddlewaretoken': csrfToken,
            'client_secret': clientSecret,
            'save_info': saveInfo,
            'request': requestInfo,
        };
        let url = '/checkout/cache_checkout_data/';
        
        $.post(url, postData).done(function () {            
            // https://stripe.com/docs/js/payment_intents/confirm_card_payment#stripe_confirm_card_payment-clientSecret
            stripe.confirmCardPayment(clientSecret, {
                    payment_method: {                    
                    card: card,                    
                    billing_details: {
                        name: $.trim(form.full_name.value),
                        phone: $.trim(form.phone_number.value),
                        email: $.trim(form.email.value),
                        address:{
                            line1: $.trim(form.street_address.value),                        
                            city: $.trim(town.options[town.selectedIndex].text),                            
                            postal_code: $.trim(form.postcode.value),
                        }
                    }
                },                
                shipping: {
                    name: $.trim(form.full_name.value),
                    phone: $.trim(form.phone_number.value),                
                    address: {
                        line1: $.trim(form.street_address.value),                    
                        city: $.trim(town.options[town.selectedIndex].text),                    
                        postal_code: $.trim(form.postcode.value),                    
                    }
                },
            }).then(function(result) {
                if (result.error) {
                    var errorDiv = document.getElementById('card-errors');
                    var html = `
                        <span class="icon" role="alert">
                        <i class="fas fa-times"></i>
                        </span>
                        <span>${result.error.message}</span>`;
                    $(errorDiv).html(html);
                    $('#payment-form').fadeToggle(100);
                    $('#loading-overlay').fadeToggle(100);
                    card.update({ 'disabled': false});
                    $('#submit-button').attr('disabled', false);
                } else {
                    if (result.paymentIntent.status === 'succeeded'){                        
                        form.submit();
                    }
                }
            });
        }).fail(function () {            
            location.reload();
        });
    });    
});
