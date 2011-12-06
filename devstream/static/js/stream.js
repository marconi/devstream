(function($) {

    /**
     * Models and Collections
     */

    window.StreamItem = Backbone.Model.extend({
        is_last: false
    });
    window.StreamItemList = Backbone.Collection.extend({
        model: StreamItem,
        url: '/stream',
        comparator: function(streamItem) {
            // sort in descending so the last added is at the top
            return -streamItem.get("cid");
        }
    });

    /**
     * Views
     */

    window.StreamItemView = Backbone.View.extend({
        className: 'row',
        initialize: function() {
            _.bindAll(this, 'render');

            // listen for change event
            this.model.bind('change', this.render);

            this.template = _.template($('#stream-item-template').html());
        },
        render: function() {
            var renderedContent = this.template(this.model.toJSON());
            $(this.el).html(renderedContent);
            return this;
        }
    });
    window.StreamView = Backbone.View.extend({
        className: 'row stream',
        initialize: function() {
            _.bindAll(this, 'render');
            this.template = _.template($('#stream-template').html());

            // listen for reset event
            this.collection.bind('reset', this.render);
            this.collection.bind('add', this.add, this);
            this.collection.bind('remove', this.remove, this);
        },
        render: function() {
            // render the stream initially
            $(this.el).html(this.template({}));

            // get a hold of inner div
            var $streamItems = this.$(".stream-items");
            var streamView = this;

            this.collection.each(function(streamItem, index) {
                // if this is the last item,
                // add a last class.
                if ((index + 1) === streamView.collection.size()) {
                    streamItem.set({is_last: true});
                }
                else {
                    streamItem.set({is_last: false});
                }

                var streamItemView = new StreamItemView({model: streamItem});
                $streamItems.append(streamItemView.render().el);
            });
            return this;
        },
        add: function() {
            // re-render the widget after adding item
            this.render();
        },
        remove: function() {
            // re-render the widget after removing item
            this.render();
        }
    });

    /**
     * Router
     */
    window.Stream = Backbone.Router.extend({
        routes: {
            '': 'home',
            'stream/:more': 'stream'
        },
        initialize: function(container) {
            this.container = container;
            this.streamView = new StreamView({
                collection: new StreamItemList()
            });
        },
        home: function() {
            // render the widget by default
            $(this.container).append(this.streamView.render().el);
        },
        stream: function(action) {
            var stream = this;
            $.ajax({
                type: "GET",
                url: "/stream/" + action,
                dataType: "json",
                success: function(data, textStatus, jqXHR) {
                    var collection = stream.streamView.collection;
                    collection.add(data, {at: collection.size()});
                },
                statusCode: {
                    201: function (data, textStatus, jqXHR) {
                    },
                    400: function (data, textStatus, jqXHR) {
                        console.log("Error: " + data);
                    },
                    403: function (data, textStatus, jqXHR) {
                    },
                    405: function (data, textStatus, jqXHR) {
                    }
                }
            });
        },
    });

    $(document).ready(function() {
        window.streamApp = new Stream('#main-stream');
        Backbone.history.start();
    });

})(jQuery);