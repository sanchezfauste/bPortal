function saveListLayout() {
  var selectedFields = $("#selected-fields li")
    .map(function() {
      return $(this).attr("id");
    })
    .get();

  var data = {
    selectedFields
  };

  $.ajax({
    type: "POST",
    data: JSON.stringify(data),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    error(response) {
      alert(response.responseJSON.error);
    },
    success(response) {
      alert(response.msg);
    }
  });
}

function save_layout_layout() {
  var selectedFields = [];
  $("#selected-fields div.row").map(function() {
    selectedFields.push(
      $(this)
      .children("div.col.card.sortable-ul")
      .map(function() {
        var children = $(this).children();
        if (children.length > 0) {
          return children.attr("id");
        } else {
          return "";
        }
      })
      .get()
    );
  });

  var data = {
    selectedFields
  };

  $.ajax({
    type: "POST",
    data: JSON.stringify(data),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    error(response) {
      alert(response.responseJSON.error);
    },
    success(response) {
      alert(response.msg);
    }
  });
}

function addLayoutRow() {
  $("#selected_fields_list_group").append(
    '\
        <div class="list-group-item justify-content-between">\
            <div class="row">\
                <div class="col card sortable-ul selected-field ml-2"></div>\
                <div class="col col-2 text-center align-self-center">\
                    <a class="btn btn-danger" href="#" role="button" onclick="remove_layout_row($(this));">\
                        <span class="oi oi-x"></span>\
                    </a>\
                </div>\
            </div>\
        </div>\
    '
  );
  $(".selected-field, #available-fields")
    .sortable({
      connectWith: ".sortable-ul"
    })
    .disableSelection();
  $(".selected-field").each(function() {
    $(this).on("sortreceive", function(event, ui) {
      if ($(this).children().length > 1) {
        $(ui.sender).sortable("cancel");
        var el1 = $(this).children()[0];
        var el2 = $(ui.item)[0];
        $(this).append(el2);
        $(ui.sender).append(el1);
      }
    });
  });
}

function addLayoutRow2() {
  $("#selected_fields_list_group").append(
    '\
        <div class="list-group-item justify-content-between">\
            <div class="row">\
                <div class="col card sortable-ul selected-field ml-2"></div>\
                <div class="col card sortable-ul selected-field ml-2"></div>\
                <div class="col col-2 text-center align-self-center">\
                    <a class="btn btn-danger" href="#" role="button" onclick="remove_layout_row($(this));">\
                        <span class="oi oi-x"></span>\
                    </a>\
                </div>\
            </div>\
        </div>\
    '
  );
  $(".selected-field, #available-fields")
    .sortable({
      connectWith: ".sortable-ul"
    })
    .disableSelection();
  $(".selected-field").each(function() {
    $(this).on("sortreceive", function(event, ui) {
      if ($(this).children().length > 1) {
        $(ui.sender).sortable("cancel");
        var el1 = $(this).children()[0];
        var el2 = $(ui.item)[0];
        $(this).append(el2);
        $(ui.sender).append(el1);
      }
    });
  });
}

function remove_layout_row(object) {
  var row = object.parent().parent();
  row.children("div.col.card.sortable-ul").map(function() {
    var children = $(this).children();
    if (children.length > 0) {
      $("#available-fields").append(children);
    }
  });
  row.parent().remove();
}