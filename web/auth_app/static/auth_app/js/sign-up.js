console.log('sing-up')
$(function () {
  $('#signUpForm').submit(singUp);
});

let alert = document.getElementById("alert-box")

const handleAlerts = (type, text) => {
    let html = `<div class="alert alert-${type}" role="alert">${text}</div>`
    alert.insertAdjacentHTML("afterend", html)
  }

function singUp(e) {
  e.preventDefault()
  let form = $(this);
  $.ajax(
    {
      url: "/api/v1/auth/sign-up/",
      type: "POST",
      dataType: "json",
      data: form.serialize(),
      success: function (data) {
        document.getElementById("signUpForm").reset()
        $(".alert").remove()
        handleAlerts("success", "Registration success. Check your email for further instructions.")
      },
      error: function (data) {
        document.getElementById("signUpForm").reset()
        $(".alert").remove()
        for (current_error in data.responseJSON) {
          handleAlerts("danger", current_error + ": " + data.responseJSON[current_error])
        }
      }
    }
  )
}
