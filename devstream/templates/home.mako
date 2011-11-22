<%inherit file="base.mako"/>

<%block name="additional_js">
<script src="${h.assets_url(request, '/js/libs/underscore.min.js')}"></script>
<script src="${h.assets_url(request, '/js/libs/backbone.js')}"></script>
<script src="${h.assets_url(request, '/js/stream.js')}"></script>

<script type="text/template" charset="utf-8" id="stream-item-template">
  <div class="row">
    <div class="span9 stream-item">
      <div class="row meta">
        <div class="span8 author">
          <a href="javascript:void(0)" class="author-name"><%= title %></a>
          <span class="label success">Git</span>
        </div>
        <div class="span2 date">23 Oct 2011</div>
      </div>
      <div class="content"><%= content %></div>
    </div>
  </div>
</script>

<script type="text/template" charset="utf-8" id="stream-template">
  <div class="stream-items">
  </div>
</script>
</%block>

<%block name="content_inner">
<form id="post-box" action="" method="post">
  <div class="clearfix">
    <div class="input">
      <textarea class="xxlarge" id="status" name="status" rows="2"></textarea>
      <input type="submit" value="Update" class="btn large primary" />
      <span class="help-block">
        Type whatever you want to say.
      </span>
    </div>
  </div>
</form>

<div id="stream-widget" class="row stream">
  <div class="span10 stream-inner">

    <div class="row">
      <div class="span9 stream-item">
        <div class="row meta">
          <div class="span8 author">
            <a href="javascript:void(0)" class="author-name">Marconi</a>
            <span class="label success">Git</span>
          </div>
          <div class="span2 date">23 Oct 2011</div>
        </div>
        <div class="content">
          The quick brown fox jumps over the lazy dog.
        </div>
      </div>
    </div>

    <div class="row">
      <div class="span9 stream-item last">
        <div class="row meta">
          <div class="span8 author">
            <a href="javascript:void(0)" class="author-name">Marconi</a>
            <span class="label warning">Status</span>
          </div>
          <div class="span2 date">23 Oct 2011</div>
        </div>
        <div class="content">
          The quick brown fox jumps over the lazy dog.
        </div>
      </div>
    </div>

  </div> <!-- /stream-inner -->
</div> <!-- /stream -->
</%block>

<%block name="sidebar">
<div id="team-status">
  <h3>Online Members</h3>
  <ul>
    <li>
      <a href="#">Marconi Moreto</a>
    </li>
    <li>
      <a href="#">Mark Abuda</a>
    </li>
    <li>
      <a href="#">Mark Abuda</a>
    </li>
  </ul>
</div>
</%block>