$(document).ready(function(){
    // Code to allow quantity selection on bag page //
    // medium and large screens //
    $(".plus").click(function(){ 
        let plus=$(this).attr("id");
        let newPlus=plus.split("-");
        let val=parseInt($("#quantity-"+newPlus[1]).val());         
        if(val<=49){
            val += 1;
            $("#quantity-"+newPlus[1]).val(val);
        }                       
    });    
    $(".minus").click(function(){
        let minus=$(this).attr("id");
        let newMinus=minus.split("-");
        let val=parseInt($("#quantity-"+newMinus[1]).val()); 
        if(val >=2){            
            val -= 1;
            $("#quantity-"+newMinus[1]).val(val);
        }      
    }); 
    
    // Medium and lower screens //
    /* Add new id to differentiate from large screens */
    $(".plus-small").click(function(){ 
        let plus=$(this).attr("id");
        let newPlus=plus.split("-");
        let val=parseInt($("#quantity-small-"+newPlus[2]).val());        
        if(val<=49){
            val += 1;
            $("#quantity-small-"+newPlus[2]).val(val);
        }                       
    });    
    $(".minus-small").click(function(){
        let minus=$(this).attr("id");
        let newMinus=minus.split("-");
        let val=parseInt($("#quantity-small-"+newMinus[2]).val()); 
        if(val >=2){            
            val -= 1;
            $("#quantity-small-"+newMinus[2]).val(val);
        }      
    });

    // Remove item and reload on click
    $('.delete-item').click(function(){
        let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();        
        let itemId = $(this).attr('id');       
        let spice_index = $(this).attr('data-name');            
        let url = `/bag/delete/${itemId}/`;        
        var data = {'csrfmiddlewaretoken': csrfToken, 'spice_index': spice_index};       
       
        $.post(url, data)
         .done(function() {
             location.reload();
         });
    });
});