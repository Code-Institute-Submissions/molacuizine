$(document).ready(function(){
    // Code to allow selection on bag page //

    $(".plus").click(function(){ 
        let plus=$(this).attr("id");
        let val=parseInt($("#quantity-"+plus).val()); 
        console.log(val)
        if(val<=49){
            val += 1;
            $("#quantity-"+plus).val(val);
        }                       
    });    
    $(".minus").click(function(){
        let minus=$(this).attr("id");
        let val=parseInt($("#quantity-"+minus).val()); 
        if(val >=2){            
            val -= 1;
            $("#quantity-"+minus).val(val);
        }      
    });         
});