<!doctype html>
<!--[if lt IE 7 ]> <html class="no-js ie6" lang="en"> <![endif]-->
<!--[if IE 7 ]>    <html class="no-js ie7" lang="en"> <![endif]-->
<!--[if IE 8 ]>    <html class="no-js ie8" lang="en"> <![endif]-->
<!--[if (gte IE 9)|!(IE)]><!--> <html class="no-js" lang="en"> <!--<![endif]-->
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">

    <title><%block name="title">${_("DevStream")}</%block></title>
    <meta name="description" content="">
    <meta name="author" content="">

    <META HTTP-EQUIV="CACHE-CONTROL" CONTENT="${h.get_settings(request, 'meta_cache_control', 'PUBLIC')}">
    <META HTTP-EQUIV="EXPIRES" CONTENT="${h.get_settings(request, 'meta_expires', '1d')}">

    <link rel="shortcut icon" href="${h.assets_url(request, '/favicon.ico')}">

    <link rel="stylesheet" href="${h.assets_url(request, '/css/bootstrap.min.css')}" type="text/css" />
    <link rel="stylesheet" href="${h.assets_url(request, '/css/styles.css')}" type="text/css" />

    <script src="${h.assets_url(request, '/js/libs/modernizr-1.7.min.js')}"></script>
    <script src="${request.static_url('devstream:static/js/libs/socketio/socket.io.js')}"></script>

    <%block name="head"></%block>

</head>

<body>

  <div class="topbar">
      <div class="fill">
        <div class="container">
          <a class="brand" href="#">${_("DevStream")}</a>
          <ul class="nav">
            <li class="active"><a href="#">${_("Dashboard")}</a></li>
            <li><a href="#about">${_("About")}</a></li>
            <li><a href="#contact">${_("Contact")}</a></li>
          </ul>
          <form action="" class="pull-right">
            <input class="input-small" type="text" placeholder="${_('Username')}">
            <input class="input-small" type="password" placeholder="${_('Password')}">
            <button class="btn" type="submit">${_("Sign-in")}</button>
          </form>
        </div>
      </div>
    </div> <!-- /topbar -->


    <div class="container">

      <div class="content">
        <%block name="page_header">
        </%block>

        <div class="row">
          <%block name="content">
          </%block>
        </div>
      </div>

      <footer>
        <p>${_("&copy; Company 2011") | n}</p>
      </footer>

    </div> <!-- /container -->


    <script src="${h.assets_url(request, '/js/libs/jquery.min.js')}"></script>
    <%block name="additional_js"></%block>

    <!-- scripts concatenated and minified via ant build script-->
    <script src="${h.assets_url(request, '/js/plugins.js')}"></script>
    <script src="${h.assets_url(request, '/js/script.js')}"></script>
    <!-- end scripts-->


    <!--[if lt IE 7 ]>
        <script src="${h.assets_url(request, '/js/libs/dd_belatedpng.js')}"></script>
        <script>DD_belatedPNG.fix("img, .png_bg");</script>
    <![endif]-->

</body>
</html>