let params = new URLSearchParams(window.location.search)
let alert = document.getElementById("alert-box")

const handleAlerts = (type, text) => {
    alert.innerHTML = `<div class="alert alert-${type}" role="alert" style="margin: 10px 0 50px 0">${text}</div>`
  }


$.ajax({
  url: "/api/v1/auth/sign-up/verify/",
  type: "POST",
  data: {"key": params.get("key")},
  success: function (data) {
    console.log(data)
    handleAlerts("success", "Your account has been successfully activated! In 5 seconds, you will be automatically redirected to the login page.")
    setTimeout(() => {
      window.location.replace('http://localhost:8008/login/?verified=True')
    }, 5000)},
  error: function (data) {
    console.log(data)
    handleAlerts("warning", data.responseJSON["key"])
  }
})
