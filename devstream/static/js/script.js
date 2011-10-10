$(document).ready(function() {

    /**
     * Helper function for display field errors
     */
    function displayFieldError(field, errormsg, wheretoappend) {
        var error = document.createElement("div");
        error.innerHTML = errormsg;
        error.className = 'error';
        $(field).siblings(".error").remove();
        $(field).addClass("error-field");
        if (wheretoappend !== undefined) {
            $(wheretoappend).after(error);
        }
        else {
            $(field).after(error);
        }
        return field;
    }

    /**
     * Connect to SocketIO
     */
    var socket = new io.Socket('localhost', {transports: ['websocket', 'flashsocket', 'htmlfile', 'xhr-multipart', 'xhr-polling', 'jsonp-polling']});
    socket.on('connect', function() {
        var newDate = new Date;
        var random_uid = newDate.getTime();
        socket.send({type: 'connect', uid: random_uid});
    });
    socket.on('message', function(obj) {
        console.log(obj);
    });
    socket.on('error', function(obj) {
        console.log(obj);
    });
    socket.on('disconnect', function() {
        console.log('Disconnected');
    });
    // socket.connect();


    $("#stream-form .form-submit input").click(function(e) {
        var url = $("#stream-form").attr("action");
        var csrfToken = $("#stream-form input[name=_csrf]").val();
        var status = $("#stream-form textarea[name=status]").val();

        // clear errors and messages
        $("#stream-form .error, #stream-form .message").remove();

        $.ajax({
            type: 'POST',
            url: url,
            data: {status: status, _csrf: csrfToken},
            dataType: 'json',
            statusCode: {
                // successful post
                200: function (data, textStatus, jqXHR) {
                    
                },
                // validation errors
                400: function (data, textStatus, jqXHR) {
                    response = JSON.parse(data.responseText);
                    displayFieldError($("#stream-form textarea[name=status]"),
                                      response.status).focus();
                },
                // csrf token retry
                403: function (data, textStatus, jqXHR) {
                    
                }
            },
            complete: function(data, status) {
                response = JSON.parse(data.responseText);
                if (response.message !== undefined) {
                    message = document.createElement('p');
                    message.className = "message";

                    if (data.status == 200) {
                        message.className += " info";
                    }

                    message.innerHTML = response.message;
                    $("#stream-form").prepend(message);
                }

                // reset status textarea
                $("#stream-form textarea[name=status]").val("").focus();
            }
        });

        e.preventDefault();
    });

    /**
     * Stream widget
     */
    function Stream(widget, visible_items) {
        this.widget = (widget.length === 1) ? widget[0] : widget;
        this.items = [];
        this.visible_items = visible_items || 10;
    }
    
    Stream.prototype.addItem = function(item) {
        // add the new item
        this.items.unshift(item);

        // then slice the items up-to visible_items
        this.items = this.items.slice(0, this.visible_items);
    }
    Stream.prototype.render = function() {
        var stream = this;

        // reverse it first so it renders the last one
        stream.items.reverse();

        $.each(stream.items, function(i, val) {
            // hide it by default
            var item = val.renderItem();
            item.className += " hidden";

            // append it
            $("#stream-inner").prepend(item);

            // then show it after appending
            $(item).show("fast", function() {
                $(this).removeClass("hidden");

                // add class 'last' to last item
                var stream_items = $(stream.widget).find(".stream-item");
                $(stream_items).removeClass("last");
                $(stream_items[stream_items.length-1]).addClass("last");
            });
        });

        // then reverse it back to descending
        stream.items.reverse();
    }

    function streamItem(name, mugshot_url, profile_url, time_ago, status) {
        this.name = name;
        this.mugshot_url = mugshot_url;
        this.profile_url = profile_url;
        this.time_ago = time_ago;
        this.status = status;
    }
    streamItem.prototype.renderItem = function() {
        // mugshot
        var mugshot_img = document.createElement("img");
        mugshot_img.setAttribute("src", this.mugshot_url);
        var mugshot_link = document.createElement("a");
        mugshot_link.setAttribute("href", this.profile_url);
        mugshot_link.appendChild(mugshot_img);
        var mugshot = document.createElement("div");
        mugshot.className = "mugshot";
        mugshot.appendChild(mugshot_link);

        var name = document.createElement("a");
        name.setAttribute("href", this.profile_url);
        name.innerHTML = this.name;

        var time_ago = document.createElement("span");
        time_ago.className = "time-ago";
        time_ago.innerHTML = this.time_ago;

        var status_meta = document.createElement("div");
        status_meta.className = "status-meta";
        status_meta.appendChild(name);
        status_meta.appendChild(time_ago);

        var status = document.createElement("div");
        status.className = "status";
        status.innerHTML = this.status;

        var status_info = document.createElement("div");
        status_info.className = "status-info";
        status_info.appendChild(status_meta);
        status_info.appendChild(status);

        var item = document.createElement("div");
        item.className = "stream-item";
        item.appendChild(mugshot);
        item.appendChild(status_info);

        return item;
    }

    // initialize stream widget
    var stream = new Stream($("#stream"));
    
});
