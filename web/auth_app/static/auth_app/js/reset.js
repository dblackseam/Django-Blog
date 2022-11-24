$(function () {
  $('#resetPasswordForm').submit(passwordReset);
});

const handleAlerts = (type, text) => {
    alert.innerHTML = `<div class="alert alert-${type}" role="alert" style="margin: 10px 0 50px 0">${text}</div>`
  }

const params = new URLSearchParams(window.location.search)

function passwordReset (e) {
  e.preventDefault()
  let data = new FormData();
  data.append("password_1", $("#password_1").val())
  data.append("password_2", $("#password_2").val())
  data.append("uid", params.get("key"))
  data.append("key", params.get("uid"))

  $.ajax({
    type: "POST",
    url: "/api/v1/auth/password/reset/confirm/",
    data: data,
    processData: false,
    contentType: false,
    success: function (data) {
      console.log(data)
      window.location.replace('http://localhost:8008/login/?verified=True')
    },
    error: function (data) {
      console.log("error", data)
      handleAlerts("alert", data.responseJSON)
    }
  })
}
