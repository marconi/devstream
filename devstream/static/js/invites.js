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
             'click #invite-members': 'inviteMembers',
             'click .modal-wrapper a.close': 'closeOverlay',
             'click #send-invites': 'inviteMembersSubmit'
         },
         closeOverlay: function(e) {
             this.$("#invite-members-modal").hide();
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
         inviteMembers: function(e) {
             this.$(".modal-overlay").show();
             this.$(".modal-wrapper").show();
             this.$("#invite-members-modal textarea").val("");
             this.$("#invite-members-modal").show();
             e.preventDefault();
         },
         inviteMembersSubmit: function(e) {
             var inviteView = this;
             var emails = this.$("#invite_emails").val().trim().split(",");
             var validEmails = [];

             // filter only valid emails
             var emailPattern = new RegExp(/^(("[\w-+\s]+")|([\w-+]+(?:\.[\w-+]+)*)|("[\w-+\s]+")([\w-+]+(?:\.[\w-+]+)*))(@((?:[\w-+]+\.)*\w[\w-+]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$)|(@\[?((25[0-5]\.|2[0-4][\d]\.|1[\d]{2}\.|[\d]{1,2}\.))((25[0-5]|2[0-4][\d]|1[\d]{2}|[\d]{1,2})\.){2}(25[0-5]|2[0-4][\d]|1[\d]{2}|[\d]{1,2})\]?$)/i);
             _.each(emails, function(email) {
                 if (emailPattern.test(email.trim())) {
                     validEmails.push(email.trim());
                 }
             });

             // clear message indicators
             this.$(".modal-body").removeClass("success");
             this.$(".modal-body").removeClass("error");

             if (validEmails.length == 0) {
                 this.$(".modal-body").addClass("error");
                 this.$(".modal-body .message").html("You need to enter at least one valid email.");
                 this.$(".modal-body .message").show();
                 return;
             }

             // send invites
             $.ajax({
                 type: "POST",
                 data: {invites: validEmails.join("&"), group_id: activeGroupId},
                 url: "/invite",
                 dataType: "json",
                 success: function(data, textStatus, jqXHR) {
                     // show success message
                     var msg = "Invites has been sent successfully.";
                     inviteView.$(".modal-body").addClass("success");
                     inviteView.$(".modal-body .message").html(msg);
                     inviteView.$(".modal-body .message").show();

                     inviteView.$("#invite_emails").val('').focus();
                 },
                 statusCode: {
                     400: function (data, textStatus, jqXHR) {
                         console.log("Error: " + data);
                         var msg = "Unable to send invites, please try again.";
                         inviteView.$(".modal-body").addClass("error");
                         inviteView.$(".modal-body .message").html(msg);
                         inviteView.$(".modal-body .message").show();
                     },
                     404: function (data, textStatus, jqXHR) {
                         // when the group_id passed doesn't exist
                         
                     }
                 }
             });
             e.preventDefault();
         }
     });

     $(document).ready(function() {
         window.inviteView = new InviteView({
             el: $("#invites"),
         });
     });

})(jQuery);