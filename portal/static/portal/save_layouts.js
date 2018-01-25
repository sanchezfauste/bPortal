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

function save_detail_layout() {

    var selected_fields = [];
    $('#selected-fields div.row').map(function() {
        selected_fields.push($(this).children('div.col.card.sortable-ul').map(function() {
            var children = $(this).children();
            if (children.length > 0) {
                return children.attr('id');
            } else {
                return '';
            }
        }).get());
    });

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

function add_detail_row() {
    $('#selected_fields_list_group').append('\
        <div class="row">\
            <div class="col card sortable-ul selected-field"></div>\
            <div class="col card sortable-ul selected-field"></div>\
            <div class="col col-2 text-center align-self-center">\
                <a class="btn btn-danger" href="#" role="button" onclick="remove_detail_row($(this));">\
                    <span class="oi oi-x"></span>\
                </a>\
            </div>\
        </div>\
    ');
    $( ".selected-field, #available-fields" ).sortable({
      connectWith: ".sortable-ul"
    }).disableSelection();
    $(".selected-field").each(function() {
      $(this).on("sortreceive", function(event, ui) {
        if ($(this).children().length > 1) {
          $(ui.sender).sortable('cancel');
        }
      })
    });
}

function remove_detail_row(object) {
    var row = object.parent().parent();
    row.children('div.col.card.sortable-ul').map(function() {
        var children = $(this).children();
        if (children.length > 0) {
            $('#available-fields').append(children);
        }
    })
    row.remove()
}
