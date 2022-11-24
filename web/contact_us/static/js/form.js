$(function () {
  $('#contactUsForm').submit(SendEmails);
});

function SendEmails(e) { // e - event (действие, которое происходит по клику мыши)
  e.preventDefault() // предотвращаем отправку формы на сервер
  let data = new FormData(); // FormData метод используется для того что создать некую коллекцию, благодаря которой
  // отправка файлов станет возможна
  // let file = $(this)[0].files[0]; // эта строчка просто не работает!!!!!
  // Проверяем переданы ли следующие значения в форме, и если да, так же добавляем их в нашу FormData.
  let name = $("#name").val()
  let email = $("#email").val()
  let image = $("#image").get(0).files[0]  // get(0) - возвращает весь html элемент полностью. А files
  // возвращает файл. Файловый объект переданный в форме.
  data.append('content', $("#content").val())
  if (name && email) {
    data.append('name', name)
    data.append('email', email)
  }
  if (image) {
    data.append('image', image);
  }

  $.ajax({
      type: "POST",
      url: "/feedback/",
      data: data,
      processData: false,  // processData попытается преобразовать данные формы в строку. Но ставим False т.к. с
    // FormData сделать подобное не получится и мы получим ошибку.
      contentType: false, // отключаем дефолтный application/json.
      success: function (data) {
        document.getElementById("contactUsForm").reset()
        handleAlerts("success", "Thank you for your message! It is very important for us. Please, don't forget to check your email.")
      },
      error: function (data) {
        console.log("error", data)
      }
    })

  const alertBox = document.getElementById("alert-box")

  const handleAlerts = (type, text) => {
    alertBox.innerHTML = `<div class="alert alert-${type}" role="alert">${text}</div>`
  }
}



