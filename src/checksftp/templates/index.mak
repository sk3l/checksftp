<!DOCTYPE html>
<html lang="en">
<head>
   <meta name="generator" content=
   "HTML Tidy for HTML5 for Linux version 5.2.0">
   <meta charset="utf-8">
   <meta http-equiv="X-UA-Compatible" content="IE=edge">
   <meta name="viewport" content=
   "width=device-width, initial-scale=1">
   <meta name="description" content="">
   <meta name="author" content="">
   <title>checksftp</title><!-- Bootstrap core CSS -->
   <link href=
   "${request.static_url('checksftp:static/bootstrap/css/bootstrap.min.css')}"
   rel="stylesheet">
   <!-- Just for debugging purposes. Don't actually copy these 2 lines! -->
   <!--[if lt IE 9]><script src="../../assets/js/ie8-responsive-file-warning.js"></script><![endif]-->
   <!--<link href='https://fonts.googleapis.com/css?family=Exo' rel=
      'stylesheet' type='text/css'>-->
   <link href=
   "${request.static_url('checksftp:static/css/custom.css')}" rel=
   "stylesheet">
   <script type="text/javascript" src=
   "${request.static_url('checksftp:static/jquery-3.2.1.min.js')}">
   </script>
   <script type="text/javascript" src=
   "${request.static_url('checksftp:static/checksftp.js')}">
   </script>
   <!--<script src="../../assets/js/ie-emulation-modes-warning.js">-->
   <!--</script>-->
   <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
   <!--[if lt IE 9]>
                                                                                 <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
                                                                                       <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
                                                                                           <![endif]-->
</head>
<body>
   <div id="window">
      <nav id="navbar-top">
         <div id="div-nav">
            <div class="navbar-header">
               <a id="navbar-link" href="/" class=
               "navbar-brand">checksftp</a>
            </div>
            <div id="navbar" class="navbar-collapse collapse">
               <span id="span-nav" class=
               "navbar-text navbar-right">Bloomberg SFTP test
               utility</span>
            </div>
         </div>
      </nav><!--<div id="banner"></div>-->
      <div id="container">
         <!--<div class="row">-->
         <div id="sidebar">
            <h3>Parameters</h3>
            <form id="form-params" name="form-params">
               <hr>
               <div class="form-group form-group-endpoint">
                  <div>
                     <label>Select an endpoint</label>
                  </div><label for="hostSelection" class=
                  "form-label-endpoint">Host</label>
                  <div class="dropdown">
                     <ul class="nav nav-pills" role="tablist">
                        <li role="presentation" class="dropdown">
                           <a href="#" class="dropdown-toggle" id=
                           "dropdwn-host" data-toggle="dropdown"
                           role="button" aria-haspopup="true"
                           aria-expanded="false">Select Host</a>
                           <ul class="dropdown-menu" id="menu-host"
                           aria-labelledby="dropdwn-host">
                              <li>
                                 <a href="#">foobar</a>
                              </li>
                              <li>
                                 <a href="#">localhost</a>
                              </li>
                           </ul>
                        </li>
                     </ul>
                  </div>
               </div>
               <div class="form-group form-group-endpoint">
                  <label for="input-port" class=
                  "form-label-endpoint">Port</label> <input type=
                  "text" class="form-control" id="input-port"
                  placeholder="Enter port" required="">
               </div>
               <hr>
               <div class="form-group form-group-endpoint">
                  <label for="hostSelection">Select the check
                  type</label>
                  <div class="radio">
                     <label><input type="radio" name=
                     "optionsRadios" id="optionsRadios1" value=
                     "option1" checked>Simple</label>
                  </div>
                  <div class="radio">
                     <label><input type="radio" name=
                     "optionsRadios" id="optionsRadios2" value=
                     "option2">Continuous</label>
                  </div>
                  <div class="radio">
                     <label><input type="radio" name=
                     "optionsRadios" id="optionsRadios3" value=
                     "option3"> Full</label>
                  </div>
               </div>
               <hr>
               <div class="checkbox">
                  <label><input type="checkbox" id=
                  "chkbx-trace">Show trace info</label>
               </div><button type="button" onclick=
               "run_the_check()" class="btn btn-default">Run
               Check</button>
            </form>
         </div>
         <div id="main">
            <div id="div-pics" class="row">
               <div id="col-left" class="col-xs-4">
               <div class="div-label-img">
                  <span class=
                  "label label-default label-img">Source</span>
                  <div class="div-url">
                     <span id="span-target-src">web server</span>
                  </div>
               </div><img alt="Source" src=
               "${request.static_url('checksftp:static/images/web-home.png')}"></div>
               <div id="col-middle" class="col-xs-4">
                  <div id="div-result-title">
                     <h1 id="h1-title">Ready to Check</h1>
                  </div>
                  <div id="div-result-img" style="display:none;">
                  </div>
                  <div id="div-result-outcome" style=
                  "display:none;">
                     <h2 id="h2-outcome"></h2>
                  </div>
                  <div id="div-result-status" style=
                  "display: none;">
                     <div class="loader"></div>
                  </div>
                  <div id="div-result-text" style="display: none;">
                     <div id="div-result-summary"></div>
                  </div>
               </div>
               <div id="col-right" class="col-xs-4">
               <div class="div-label-img">
                  <span class=
                  "label label-default label-img" id="span-target-lbl">Target</span>
                  <div class="div-url">
                     <span id="span-target-host">host</span>
                     <span id="span-target-port">:port</span>
                  </div>
               </div><img alt="Destination" src=
               "${request.static_url('checksftp:static/images/web-server.png')}"></div>
            </div>
            <div class="panel panel-default" id="panel-trace"
            style="display: none;">
               <div class="panel-heading">
                  <h3 class="panel-title">Trace Info</h3>
               </div>
               <div id="panel-trace-dtl" class="panel-body">
                  detailed results
               </div>
            </div>
         </div><!--</div>-->
         <!--</div>-->
      </div>
      <!-- Placed at the end of the document so the pages load faster -->
      <script src=
      "https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js">
      </script>
      <script src=
      "${request.static_url('checksftp:static/bootstrap/js/bootstrap.min.js')}">
      </script>
      <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->

      <!--<script src="/bootstrap/js/ie10-viewport-bug-workaround.js">-->
       <!--</script>-->
   </div>
</body>
</html>
