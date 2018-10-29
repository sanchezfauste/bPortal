$(document).ready(function() {
  $("#update-case-form").submit(function(event) {
    // Stop the browser from submitting the form.
    event.preventDefault();

    var formData = new FormData();
    formData.append("case-id", $("#case-id").val());
    formData.append("update-case-text", $("#update-case-text").val());

    var files = $("#update-case-attachment").prop("files");
    for (var i = 0, file; (file = files[i]); i++) {
      formData.append("update-case-attachment", file, file.name);
    }

    $("#loading_modal").modal("show");
    $.ajax({
      url: "/add_case_update/",
      type: "POST",
      data: formData,
      processData: false,
      contentType: false
    })
      .done(function(response) {
        $("#update_case_modal").each(function() {
          $("#update-case-text").val("");
          $("#update-case-attachment").val(null);
          tinyMCE.get("update-case-text").load();
          $("#case-updates").append(response.case_update);
          $(this)
            .find(".modal-body")
            .html(
              '<div class="alert alert-success" role="alert">' +
                response.msg +
                "</div>"
            );
          $(this).modal("show");
        });
      })
      .fail(function(response) {
        $("#update_case_modal").each(function() {
          $(this)
            .find(".modal-body")
            .html(
              '<div class="alert alert-danger" role="alert">' +
                response.responseJSON.error +
                "</div>"
            );
          $(this).modal("show");
        });
      })
      .always(function() {
        setTimeout(function() {
          $("#loading_modal").modal("hide");
        }, 500);
      });
  });
});

function collapseCaseUpdates() {
  $(".case-update-text").each(function() {
    $(this).collapse("hide");
  });
}

function expandCaseUpdates() {
  $(".case-update-text").each(function() {
    $(this).collapse("show");
  });
}
