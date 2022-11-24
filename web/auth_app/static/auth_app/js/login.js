$(function () {
  $('#loginForm').submit(login);
  $('#forgot-password-button').click(forgotPasswordModal);
  $('#forgotPasswordForm').submit(forgotPasswordSubmit);
  checkIfRedirect();
});


function checkIfRedirect() {
  const params = new URLSearchParams(window.location.search)
  const ifVerified = params.get("verified")
  const ifReset = params.get("reset")

  let alertBox = document.getElementById("alert-box")
  let handleAlerts = (type, text) => {
    alertBox.innerHTML = `<div class="alert alert-${type}" role="alert">${text}</div>`
  }

  if (ifVerified) {
    handleAlerts("success", "Now, you can successfully login!")
  }
  else if (ifReset) {
    handleAlerts("success", "Success, check your email for further instructions.")
  }
}

function forgotPasswordModal() {
  $("#pwdModal").modal() // При нахождении modal элемента нужно указать что он именно modal.
  // т.е. является модальным. И это же активирует весь необходимый функционал.
}

function forgotPasswordSubmit(e) { // предотвращаем дефолтное поведение, а точнее отдачу Response в виде json.
  e.preventDefault()
  let form = new FormData();
  form.append("email", $("#inner-email").val())

  let modalAlertBox = document.getElementById("alert-box-inner")
  let handleModalAlerts = (type, text) => {
    modalAlertBox.innerHTML = `<div style="color: red; margin-bottom: 10px;">${text}</div>`
  }

  $.ajax({
    url: "http://localhost:8008/api/v1/auth/password/reset/",
    type: "POST",
    data: form,
    processData: false,
    contentType: false,
    success: function (data) {
      window.location.replace('http://localhost:8008/login/?reset=True') // Перезагружаем страницу.
    },
    error: function (data) {
      console.log(data)
      handleModalAlerts("error", data.responseJSON["key"])
    }
  })
}


function login(e) {
  const form = $(this);
  e.preventDefault();
  $.ajax({
    url: form.attr("action"),
    type: "POST",
    dataType: 'json',
    data: form.serialize(),
    success: function (data) {
      location.reload();
    },
    error: function (data) {
      $("#emailGroup").addClass("has-error");
      $("#passwordGroup").addClass("has-error");
      $(".help-block").remove()
      $("#passwordGroup").append(
        '<div class="help-block">' + data.responseJSON.email + "</div>"
      );
    }
  })
}

