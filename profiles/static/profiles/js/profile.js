$(document).ready(function(){    

    // Required to add paceholders to profile form page //
    if($('#id_town').val()== ""){
            $('#id_town').css('color', '#aab7c4');            
        }    
    $('#id_town option:first-child').html('Town');
    $('#id_town').change(function(){
        if($('#id_town option:selected').val()== ""){
            $('#id_town').css('color', '#aab7c4');
        }
        else{
            $('#id_town').css('color', 'black');
        }          
    });     
}); 