(function($) {

    /**
     * Models and Collections
     */

    window.GroupItem = Backbone.Model.extend({
        urlRoot: '/group/',
        defaults: function() {
            return {
                name: null,
                members: 0,
                last_activity: null,
                selected: false
            }
        },
        toggleSelected: function() {
            this.set({selected: !this.get('selected')});
        }
    });

    window.GroupItemList = Backbone.Collection.extend({
        model: GroupItem,
        url: '/groups/',
        comparator: function(groupItem) {
            // sort in descending so the last added is at the top
            return groupItem.get("id");
        },
        // filter down selected groups
        selected: function() {
            return this.filter(function(group){
                return group.get('selected');
            });
        }
    });

    /**
     * Views
     */

    window.GroupItemView = Backbone.View.extend({
        tagName: 'li',
        initialize: function() {
            _.bindAll(this, 'render');

            // listen for events
            this.model.bind('change', this.render, this);
            this.model.bind('destroy', this.remove, this);

            this.template = _.template($('#group-item-template').html());
        },
        events: {
            'click .group-selection input': 'toggleSelection'
        },
        toggleSelection: function(e) {
            this.model.toggleSelected();
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
            this.action_template = _.template($('#group-action-template').html());

            // listen for reset event
            this.collection.bind('change', this.render, this);
            this.collection.bind('reset', this.reset, this);
            this.collection.bind('add', this.addItem, this);
            this.collection.bind('remove', this.reset, this);
            this.collection.bind('remove', this.render, this);

            // render initially so adding items below
            // triggers the render.
            $(this.el).html(this.template({}));

            // also render group action
            this.$("#group-action-wrapper").html(this.action_template({
                selected: 0
            }));
            this.collection.fetch();
        },
        events: {
            'click .modal-wrapper a.close': 'closeOverlay',
            'click #create-group': 'createGroup',
            'click .modal-footer a': 'createGroupSubmit',
            'keypress input[name=groupName]': 'createGroupSubmit',
            'submit #create-group-modal form': 'interceptFormSubmit',
            'click #leave-group': 'leaveGroup',
            'click #cancel': 'closeOverlay',
            'click #leaving-ok': 'leaveGroupSubmit',
            'keyup input[name=group_filter]': 'filterGroup'
        },
        filterGroup: function() {
            var filter = this.$("input[name=group_filter]").val();
            this.$("#group-list li").each(function () {
                var groupName = $(this).find(".group-name").text();
                if (groupName.search(new RegExp(filter, "i")) < 0) {
                    $(this).hide();
                } else {
                    $(this).show();
                }
            });
        },
        closeOverlay: function(e) {
            this.$("#create-group-modal").hide();
            this.$("#leaving-group-modal").hide();
            this.$(".modal-wrapper").hide();
            this.$(".modal-overlay").hide();
            this.$(".modal-body").removeClass("success");
            this.$(".modal-body").removeClass("error");
            this.$(".modal-body .message").html("").hide();

            // this check is needed since calling closeOverlay
            // directly makes e = undefined.
            if (e !== undefined) {
                e.preventDefault();
            }
        },
        createGroup: function(e) {
            this.$(".modal-overlay").show();
            this.$(".modal-wrapper").show();
            this.$("#create-group-modal").show();
            this.$("input[name=groupName]").focus();
            e.preventDefault();
        },
        interceptFormSubmit: function(e) {
            return false;
        },
        createGroupSubmit: function(e) {
            if (e.keyCode !== 13) {
                return;
            }

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
        leaveGroup: function(e) {
            this.$(".modal-overlay").show();
            this.$(".modal-wrapper").show();
            this.$("#leaving-group-modal").show();
            e.preventDefault();
        },
        leaveGroupSubmit: function(e) {
            var groupsView = this;
            var collection = this.collection;
            var ids = [];
            _.each(collection.selected(), function(group) {
                ids.push(group.id);
            });
            var idsStr = ids.join("&");
            $.ajax({
                type: "POST",
                data: {ids: idsStr},
                url: "/groups/leave",
                dataType: "json",
                success: function(data, textStatus, jqXHR) {
                    collection.remove(collection.selected());
                },
                complete: function(jqXHR, textStatus) {
                    groupsView.closeOverlay();
                },
                statusCode: {
                    400: function (data, textStatus, jqXHR) {
                        console.log("Error: " + data);
                    }
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
        },
        render: function() {
            // when main view is called,
            // only render the group action buttons.
            this.$("#group-action-wrapper").html(this.action_template({
                selected: this.collection.selected().length
            }));
        }
    });

    $(document).ready(function() {
        window.groupsView = new GroupsView({
            el: $("#dashboard-widget"),
            collection: new GroupItemList()
        });
    });

})(jQuery);