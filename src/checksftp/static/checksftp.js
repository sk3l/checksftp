function run_the_check(){
       jQuery.ajax({
                  url     : 'runthecheck',
                  type    : 'POST',
                  dataType: 'json',
                  success : function(data){
                                 alert("Success. Got the message:\n "+ data.message)
                             }
              });
}
