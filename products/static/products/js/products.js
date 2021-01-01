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
});