let checktype = "simple";
let timer = null;

$(function(){

     $(".dropdown-menu").on('click', 'li a', function(){
              $(".dropdown-toggle").text($(this).text());
              $(".dropdown-toggle").val($(this).text());
              $(".dropdown-toggle").append('<span class="caret"></span>');
              $("#span-target-host").text($(this).text());
           });

     $("#input-port").on('blur', function(e){
             $("#span-target-port").text(":" + $("#input-port").val());
           });

      $("input[name='optionsRadios']").change(function(){
         checktype = $(this).val();
         if (checktype === 'continuous') {
            $("#div-cont-int").show();
         }
         else {
            $("#div-cont-int").hide();
            if (timer !== null) {
               clearInterval(timer);
               timer = null;
            }
         }
      });

});

function run_the_check() {

   check_with_server();
   if (checktype === 'continuous' && timer === null) {
      interval =  $("#input-cont-int").val();
      interval *= 1000;
      timer = setInterval(run_the_check, interval);
   }
}

function check_with_server(){

    $("#div-host-err").hide();
    $("#div-port-err").hide();

    let isValid = true;
    if ($(".dropdown-toggle").text() === "Select Host") {
       $("#div-host-err").show();
       isValid = false;
    }

    if ($.isNumeric($("#input-port").val()) === false) {
       $("#div-port-err").show();
       isValid = false;
    }

    if (isValid === false)
       return;

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

    $("#div-result-summary").hide();
    $("#div-result-img").hide()
    $("#div-result-outcome").hide();
    $("#div-result-text").hide()
    $("#panel-trace").hide();
    $("#panel-trace-dtl").html('');

    jQuery.ajax({
       url     : checkurl,
       type    : 'POST',
       dataType: 'json',
       success : function(data){
          alert("Success. Got the message:\n "+checkurl +"\n" + data.message)

          $("#div-result-summary").text(data.msg);

          $("#div-result-img").show();
          let result = data.result;
          if (result === 0) {
             $("#div-result-img").html(
               '<img alt="succcess!" src="static/images/web-check-sml.png"></img>');
             $("#h2-outcome").text("Success");
             $("#h2-outcome").css("color", "green");
             $("#span-target-lbl").attr("class", "label label-success label-img");
             $("#span-target-host").css("color", "green");
             $("#span-target-port").css("color", "green");
          }
          else {
             $("#div-result-img").html(
                '<img alt="fail" src="static/images/web-x-sml.png"></img>');
             $("#h2-outcome").text("Failure");
             $("#h2-outcome").css("color", "red");
             $("#span-target-lbl").attr("class", "label label-danger label-img");
             $("#span-target-host").css("color", "red");
             $("#span-target-port").css("color", "red");
          }

          $("#div-result-text").show()

          if (showtrace === true) {
             $("#panel-trace-dtl").html(data.trace);
             $("#panel-trace").show();
          }
          else {
             $("#panel-trace").hide();
          }

          $("#h1-title").text("Check Complete");
          $("#div-result-outcome").show();
          $("#div-result-summary").show();
          $("#div-result-status").hide();


       }
    });
}

