$( document ).ready(function() {
    
    $('textarea').each(function () {
        this.setAttribute('style', 'height:' + (this.scrollHeight) + 'px;overflow-y:hidden;resize:none;');
    }).on('input', function () {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
        console.log(this);
        if (this.value.length > 0) {
            $('#update-case-form-submit-button').prop('disabled', false);
        } else {
            $('#update-case-form-submit-button').prop('disabled', true);
        }
    });

    $('#update-case-form').submit(function(event) {
        // Stop the browser from submitting the form.
        event.preventDefault();

        var data = {
            "case-id" : $('#case-id').val(),
            "update-case-text" : $('#update-case-text').val(),
        };

        $.ajax({
            url: "/add_case_update/",
            type: "POST",
            data: JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            error: function(response) {
                $('#update_case_modal').each(function () {
                    $(this).find('.modal-body').html(
                        '<div class="alert alert-danger" role="alert">'
                            + response.responseJSON.error + '</div>'
                    );
                    $(this).modal('show');
                });
            },
            success: function(response) {
                $('#update_case_modal').each(function () {
                    $('#update-case-text').val('');
                    $('#update-case-form-submit-button').prop('disabled', true);
                    $(this).find('.modal-body').html(
                        '<div class="alert alert-success" role="alert">'
                            + response.msg + '</div>'
                    );
                    $(this).modal('show');
                });
            }
        });
    });

});
