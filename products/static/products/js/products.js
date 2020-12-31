$(document).ready(function(){    
    let val=0;           
    $("#plus").click(function(){
        if(val<=9 && val >=0){
            val += 1;
            $("#quantity").val(val);
        }                       
    });    
    $("#minus").click(function(){ 
        if(val<=10 && val >=1){            
            val -= 1;
            $("#quantity").val(val);
        }      
    });         
});