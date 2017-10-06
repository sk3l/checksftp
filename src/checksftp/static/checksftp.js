$(function(){

       $(".dropdown-menu").on('click', 'li a', function(){
                $(".dropdown-toggle").text($(this).text());
                $(".dropdown-toggle").val($(this).text());
                $('.dropdown-toggle').append('<span class="caret"></span>');
             });

});

function run_the_check(){
      $("#h2-title").text("Running check...");
      $("#div-result-status").show();

      let showtrace = false;
      let checkurl = 'runthecheck?';
      if ($("#chkbx-trace").is(':checked')) {
         showtrace = true;
         checkurl = checkurl + 'trace=true';
      }

      let port = $("#input-port").val()

      jQuery.ajax({
                  url     : checkurl,
                  type    : 'POST',
                  dataType: 'json',
                  success : function(data){
                                 alert("Success. Got the message:\n "+checkurl +"\n" + data.message)
                                 if (showtrace === true) {
                                    $("#panel-trace").show();
                                 }
                                 else {
                                    $("#panel-trace").hide();
                                 }
                                 $("#h2-title").text("Check Complete") 
                                 $("#div-result-status").hide();
                             }
              });
}
