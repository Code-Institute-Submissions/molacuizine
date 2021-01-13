$(document).ready(function(){
    // Required to display toasts //    
    $('.toast').toast('show');
    
    // Required to add paceholders to registration page //
    $('#id_first_name').attr('placeholder', "Firstname"); 
    $('#id_last_name').attr('placeholder', "Lastname");
    
    $('.product-submit').click(function(){''
        $(".fa-shopping-bag").css('font-size', '40px');
        $(".fa-shopping-bag").css('color', 'green');
        $(".header-link").hide();
    })
}); 