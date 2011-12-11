$(document).ready(function() {

    // action for alert messages close button
    $("a.close").click(function(e) {
        var msg = $(this).parent(".alert-message");
        $(msg).fadeOut("fast", function() {
            $(msg).remove();
        });
        e.preventDefault();
    });

});