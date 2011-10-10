(function($){
    $.fn.stream = function() {

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
            return this;
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
                $(stream.widget).prepend(item);

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
            return this;
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

        return new Stream(this[0]);
    }
}(jQuery));