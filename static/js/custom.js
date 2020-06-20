var message = document.getElementById("message-container");

setTimeout(function(){
   message.style.display = "none";
}, 5000);


$(".custom-file-input").on("change", function() {
  var fileName = $(this).val().split("\\").pop();
  $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
});




