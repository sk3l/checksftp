$(function(){

       $(".dropdown-menu").on('click', 'li a', function(){
                $(".dropdown-toggle").text($(this).text());
                $(".dropdown-toggle").val($(this).text());
                $('.dropdown-toggle').append('<span class="caret"></span>');
             });

});

function run_the_check(){
      $("#h1-title").text("Running check...");
      $("#div-result-status").show();

      let showtrace = false;

      let host = $(".dropdown-toggle").text()
      let port = $("#input-port").val()

      let checkurl = 'runthecheck?host=' + host + '&port=' + port;

      if ($("#chkbx-trace").is(':checked')) {
         showtrace = true;
         checkurl = checkurl + '&trace=true';
      }

      jQuery.ajax({
                  url     : checkurl,
                  type    : 'POST',
                  dataType: 'json',
                  success : function(data){
                                 alert("Success. Got the message:\n "+checkurl +"\n" + data.message)
gc
                                 $("#div-result-summary").text(data.msg);

                                 $("#div-result-img").show();
                                 let result = data.result;
                                 if (result === 0) {
                                    $("#div-result-img").html(
                                       '<img alt="succcess!" src="static/images/web-check.png"></img>');
                                 }
                                 else {
                                    $("#div-result-img").html(
                                       '<img alt="fail" src="static/images/web-x.png"></img>');
                                 }

                                 $("#div-result-text").show()

                                 if (showtrace === true) {
                                    $("#panel-trace").show();
                                 }
                                 else {
                                    $("#panel-trace").hide();
                                 }
                                 $("#h1-title").text("Check Complete")gc
                                 $("#div-result-status").hide();
                             }
              });
}