$(document).ready(function(){
    // Required to display toasts //    
    $('.toast').toast('show');
    
    // Required to add paceholders to registration page //
    $('#id_first_name').attr('placeholder', "Firstname"); 
    $('#id_last_name').attr('placeholder', "Lastname");    
}); 