$(function () {
  $('#pwdModal').submit(forgotPassword);
});

function forgotPassword (e) {
  let email = $("#email")
  e.preventDefault()
  $.ajax({
    url: "/password-reset/",
    type: "POST",
    data: email,
  })
}
