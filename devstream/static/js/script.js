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
});
