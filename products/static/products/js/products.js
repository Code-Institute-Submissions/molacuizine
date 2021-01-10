$(document).ready(function(){
    // Function for product quantity selector //

    let val=parseInt($("#quantity").val());           
    $("#plus").click(function(){
        if(val<=19){
            val += 1;
            $("#quantity").val(val);
        }                       
    });    
    $("#minus").click(function(){ 
        if(val >=2){            
            val -= 1;
            $("#quantity").val(val);
        }      
    });
    
    // Required to add paceholders to store management form page //

    if($('#id_category').val()== ""){
            $('#id_category').css('color', '#aab7c4');            
        }    
    $('#id_category option:first-child').html('Category');
    $('#id_category').change(function(){
        if($('#id_category option:selected').val()== ""){
            $('#id_category').css('color', '#aab7c4');
        }
        else{
            $('#id_category').css('color', 'black');
        }          
    }) 

    // Required for customisable image upload button //

    $('#upload-button').click(function(){
        $('#id_image').click(); 
         
    })
    $('#id_image').hide();
    $('#id_image').change(function(){
        filename=$('#id_image').val().split('\\');      
        $('#filename-text').html(filename[filename.length-1]);
    }); 

    // Required to send store status data to context view to update model //

    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    $('#open').click(function(){       
        $.post('/bag/store_status/', {'csrfmiddlewaretoken': csrfToken,'status': 'open'})
        location.reload();                   
    })
    $('#close').click(function(){       
        $.post('/bag/store_status/', {'csrfmiddlewaretoken': csrfToken,'status': 'close'})
        location.reload();                   
    })    
});