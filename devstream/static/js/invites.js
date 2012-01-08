(function($) {

    /**
     * Views
     */
     
     window.InviteView = Backbone.View.extend({
         initialize: function() {
             _.bindAll(this, 'render');
             this.template = _.template($('#invite-template').html());

             // render initially
             $(this.el).html(this.template({}));
         },
         events: {
             'click #invite-members': 'inviteMembers'
         },
         inviteMembers: function() {
             console.log('here');
         }
     });

     $(document).ready(function() {
         window.inviteView = new InviteView({
             el: $("#invites"),
         });
     });

})(jQuery);