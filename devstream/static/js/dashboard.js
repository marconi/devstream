(function($) {

    /**
     * Models and Collections
     */

    window.GroupItem = Backbone.Model.extend({
        urlRoot: '/group/',
    });

    window.GroupItemList = Backbone.Collection.extend({
        model: GroupItem,
        url: '/groups/',
        comparator: function(groupItem) {
            // sort in descending so the last added is at the top
            return -groupItem.get("id");
        }
    });

    /**
     * Views
     */

    window.GroupItemView = Backbone.View.extend({
        tagName: 'li',
        initialize: function() {
            _.bindAll(this, 'render');

            // listen for change event
            this.model.bind('change', this.render, this);
            this.model.bind('destroy', this.remove, this);

            this.template = _.template($('#group-item-template').html());
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

    window.GroupsView = Backbone.View.extend({
        tagName: 'div',
        id: 'group-list',
        initialize: function() {
            _.bindAll(this, 'render');
            this.template = _.template($('#group-template').html());

            // listen for reset event
            this.collection.bind('reset', this.reset, this);
            this.collection.bind('add', this.addItem, this);

            // render initially so adding items below
            // triggers the render.
            $(this.el).html(this.template({}));
        },
        events: {

        },
        addItem: function(item) {
            var groupItemView = new GroupItemView({model: item});
            this.$("ul").append(groupItemView.render().el);
        },
        reset: function() {
            // clear out existing rows, after all this is a reset
            this.$("li").remove();

            // then add each new item in the collection
            this.collection.each(this.addItem);
        }
    });

    $(document).ready(function() {
        window.GroupsView = new GroupsView({
            el: $("#group-list"),
            collection: new GroupItemList()
        });
    });

})(jQuery);