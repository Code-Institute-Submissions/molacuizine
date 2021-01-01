$(document).ready(function(){
    // Code to allow selection on bag page //
    // medium and large screens //
    $(".plus").click(function(){ 
        let plus=$(this).attr("id");
        let newPlus=plus.split("-")
        let val=parseInt($("#quantity-"+newPlus[1]).val()); 
        console.log(val)
        if(val<=49){
            val += 1;
            $("#quantity-"+newPlus[1]).val(val);
        }                       
    });    
    $(".minus").click(function(){
        let minus=$(this).attr("id");
        let newMinus=minus.split("-")
        let val=parseInt($("#quantity-"+newMinus[1]).val()); 
        if(val >=2){            
            val -= 1;
            $("#quantity-"+newMinus[1]).val(val);
        }      
    }); 
    
    // Medim and lower screens //
    $(".plus-small").click(function(){ 
        let plus=$(this).attr("id");
        let newPlus=plus.split("-")
        let val=parseInt($("#quantity-small-"+newPlus[2]).val()); 
        console.log(val)
        if(val<=49){
            val += 1;
            $("#quantity-small-"+newPlus[2]).val(val);
        }                       
    });    
    $(".minus-small").click(function(){
        let minus=$(this).attr("id");
        let newMinus=minus.split("-")
        let val=parseInt($("#quantity-small-"+newMinus[2]).val()); 
        if(val >=2){            
            val -= 1;
            $("#quantity-small-"+newMinus[2]).val(val);
        }      
    })
});