$( document ).ready(function() {
    
    $('textarea').each(function () {
        this.setAttribute('style', 'height:' + (this.scrollHeight) + 'px;overflow-y:hidden;resize:none;');
    }).on('input', function () {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
        if (this.value.length > 0) {
            $('#update-case-form-submit-button').prop('disabled', false);
        } else {
            $('#update-case-form-submit-button').prop('disabled', true);
        }
    });

    $('#update-case-form').submit(function(event) {
        // Stop the browser from submitting the form.
        event.preventDefault();

        var formData = new FormData();
        formData.append("case-id", $('#case-id').val());
        formData.append("update-case-text", $('#update-case-text').val());

        var files = $('#update-case-attachment').prop('files');
        for(var i = 0, file; file = files[i]; i++) {
            formData.append('update-case-attachment', file, file.name);
        }

        $.ajax({
            url: "/add_case_update/",
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
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
                    $('#update-case-attachment').val(null);
                    $('#update-case-form-submit-button').prop('disabled', true);
                    $('#case-updates').append(response.case_update);
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

function collapse_case_updates() {
    $('.case-update-text').each(function () {
        $(this).collapse('hide')
    });
}

function expand_case_updates() {
    $('.case-update-text').each(function () {
        $(this).collapse('show')
    });
}
