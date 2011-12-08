(function($) {

    /**
     * Models and Collections
     */

    window.StreamItem = Backbone.Model.extend({});

    window.StreamItemList = Backbone.Collection.extend({
        model: StreamItem,
        url: '/stream/',
        comparator: function(streamItem) {
            // sort in descending so the last added is at the top
            return -streamItem.get("id");
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
            this.model.bind('change', this.render, this);
            this.model.bind('destroy', this.remove, this);

            this.template = _.template($('#stream-item-template').html());
        },
        render: function() {
            var renderedContent = this.template(this.model.toJSON());
            $(this.el).html(renderedContent);
            return this;
        },
        remove: function() {
            $(this.el).remove();
        }
    });

    window.StreamView = Backbone.View.extend({
        className: 'row stream',
        initialize: function() {
            _.bindAll(this, 'render');
            this.template = _.template($('#stream-template').html());

            // listen for reset event
            this.collection.bind('reset', this.reset, this);
            this.collection.bind('add', this.addItem, this);

            // render initially so adding items below
            // triggers the render.
            $(this.el).html(this.template({}));

            // hide preloader by default
            this.$('.more-preloader').hide();

            // TODO: load initial stream content via collection fetch
        },
        events: {
            "click #post-box input": "updateStatus",
            "click .stream-more a": "moreStatus"
        },
        addItem: function(item) {
            var streamItemView = new StreamItemView({model: item});
            this.$(".stream-items").append(streamItemView.render().el);
        },
        reset: function() {
            this.collection.each(this.addItem);
        },
        updateStatus: function(e) {
            var newStatus = {
                author: '',
                created: '',
                status: this.$("textarea#status").val(),
                type: 'status'
            }
            
            e.preventDefault();
        },
        moreStatus: function(e) {
            var streamView = this;
            var collection = streamView.collection;

            // hide show more link and show preloader
            streamView.$('.stream-more a').hide();
            streamView.$('.more-preloader').show();

            $.ajax({
                type: "GET",
                data: {last_id: collection.last().get("id"), num: 5},
                url: "/stream/more",
                dataType: "json",
                success: function(data, textStatus, jqXHR) {
                    if (data === null) {
                        // if there's no more data,
                        // hide the show more link and preloader.
                        streamView.$('.more-preloader').hide();
                        streamView.$('.stream-more a').hide();
                    }
                    else {
                        collection.add(data);
                    }
                },
                statusCode: {
                    200: function (data, textStatus, jqXHR) {
                        // only toggle back show more link and
                        // preloader if there's still more data.
                        if (data !== null) {
                            // toggle show more and preloader
                            streamView.$('.more-preloader').hide();
                            streamView.$('.stream-more a').show();
                        }
                    },
                    400: function (data, textStatus, jqXHR) {
                        console.log("Error: " + data);
                    }
                }
            });
            e.preventDefault();
        }
    });

    /**
     * Router
     */
    window.Stream = Backbone.Router.extend({
        routes: {
            '': 'home'
        },
        initialize: function(container) {
            this.streamView = new StreamView({
                el: $(container),
                collection: new StreamItemList()
            });
        },
        home: function() {
        }
    });

    $(document).ready(function() {
        window.streamApp = new Stream('#main-stream');
        Backbone.history.start();
    });

})(jQuery);