function save_list_layout() {

    var selected_fields = $('#selected-fields li').map(function() {
        return $(this).attr('id');
    }).get();

    var data = {"selected_fields" : selected_fields};

    $.ajax({
        type: "POST",
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        error: function(response) {
            alert(response.responseJSON.error);
        },
        success: function(response) {
            alert("Layout updated successfully");
        }
    });

}
