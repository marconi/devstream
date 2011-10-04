<%inherit file="base.mako"/>

<%block name="content_inner">
    <div class="grid_11 alpha">
        <div id="stream">
            <form id="stream-form" action="" method="post">
                <div class="form-field">
                    <textarea name="status" rows="3" cols="60"></textarea>
                </div>
                <div class="form-submit">
                    <input class="awesome large orange" type="submit" value="Submit" />
                </div>
            </form>
            <div id="stream-inner">
                <div class="stream-item">
                    <div class="mugshot">
                        <a href="#"></a>
                    </div>
                    <div class="status-info">
                        <div class="status-meta">
                            <a href="#">Marconi Moreto</a> <span class="time-ago">about 2 hours ago</span>
                        </div>
                        <div class="status">
                            The quick brown fox jumps over the lazy dog.
                        </div>
                    </div>
                </div>
                <div class="stream-item">
                    <div class="mugshot">
                        <a href="#"></a>
                    </div>
                    <div class="status-info">
                        <div class="status-meta">
                            <a href="#">Marconi Moreto</a> <span class="time-ago">about 2 hours ago</span>
                        </div>
                        <div class="status">
                            The quick brown fox jumps over the lazy dog.
                        </div>
                    </div>
                </div>
                <div class="stream-item last">
                    <div class="mugshot">
                        <a href="#"></a>
                    </div>
                    <div class="status-info">
                        <div class="status-meta">
                            <a href="#">Marconi Moreto</a> <span class="time-ago">about 2 hours ago</span>
                        </div>
                        <div class="status">
                            The quick brown fox jumps over the lazy dog.
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="grid_5 omega">
        <div id="sidebar">
            <div id="agenda" class="block">
                <h3 class="block-title">${"Today's Agenda"}</h3>
                <div class="content">
                    hee
                </div>
            </div>
            <div id="dev-status" class="block">
                <h3 class="block-title">${"Dev Status"}</h3>
                <div class="content">
                    <div class="latest-status-item">
                        <div class="status-light offline"></div>
                        <div class="status-info">
                            <div class="status-meta">
                                <a href="#">Marconi Moreto</a>
                            </div>
                            <div class="status">
                                <span class="time">[0:12]</span>
                                The quick brown fox jumps over the lazy dog.
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</%block>