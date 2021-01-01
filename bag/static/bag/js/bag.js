$(document).ready(function(){
    // Code to allow selection on bag page //

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
});