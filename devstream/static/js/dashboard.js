(function($) {

    /**
     * Models and Collections
     */

    window.GroupItem = Backbone.Model.extend({
        urlRoot: '/group/',
        defaults: {
            'name': '--',
            'members': 0,
            'last_activity': '--'
        }
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
            'click #create-group-modal a.close': 'closeCreateGroupOverlay',
            'click #create-group': 'createGroup',
            'click .modal-footer a': 'createGroupSubmit',
            'keypress input[name=groupName]': 'createGroupSubmit',
            'submit #create-group-modal form': 'interceptFormSubmit'
        },
        closeCreateGroupOverlay: function(e) {
            this.$(".modal-wrapper").hide();
            this.$(".modal-overlay").hide();
            this.$(".modal-body").removeClass("success");
            this.$(".modal-body").removeClass("error");
            this.$(".modal-body .message").html("").hide();
            e.preventDefault();
        },
        createGroup: function(e) {
            this.$(".modal-overlay").show();
            this.$(".modal-wrapper").show();
            this.$("input[name=groupName]").focus();
            e.preventDefault();
        },
        interceptFormSubmit: function(e) {
            return false;
        },
        createGroupSubmit: function(e) {
            var groupsView = this;
            var groupName = this.$("input[name=groupName]").val();

            // clear message indicators
            this.$(".modal-body").removeClass("success");
            this.$(".modal-body").removeClass("error");

            // if the group name is empty,
            // show error message.
            if (groupName.trim() === "") {
                this.$(".modal-body").addClass("error");
                this.$(".modal-body .message").html("Group name is required");
                this.$(".modal-body .message").show();
                return;
            }

            var group = new GroupItem({name: groupName});
            group.save({}, {
                success: function(model, response) {
                    groupsView.collection.add(model);
                    groupsView.collection.sort();

                    // show success message
                    var msg = "Group has been added successfully.";
                    groupsView.$(".modal-body").addClass("success");
                    groupsView.$(".modal-body .message").html(msg);
                    groupsView.$(".modal-body .message").show();

                    groupsView.$("input[name=groupName]").val('').focus();
                },
                error: function(model, response) {
                    var msg = "Unable to save your group, please try again.";
                    groupsView.$(".modal-body").addClass("error");
                    groupsView.$(".modal-body .message").html(msg);
                    groupsView.$(".modal-body .message").show();
                }
            });
            e.preventDefault();
        },
        addItem: function(item) {
            var groupItemView = new GroupItemView({model: item});
            this.$("#group-list ul").append(groupItemView.render().el);
        },
        reset: function() {
            // clear out existing rows, after all this is a reset
            this.$("li").remove();

            // then add each new item in the collection
            this.collection.each(this.addItem);
        }
    });

    $(document).ready(function() {
        window.groupsView = new GroupsView({
            el: $("#dashboard-widget"),
            collection: new GroupItemList()
        });
        window.groupsView.collection.fetch();  // load default items
    });

})(jQuery);