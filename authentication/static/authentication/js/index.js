function togglePasswordVisibility(inputId){
    var passwordField = document.getElementById(inputId);
    var toggleIcon = document.querySelector(`.show-password-toggle-${inputId}`);

    if (passwordField.type === "password") {
      passwordField.type = "text";
      toggleIcon.classList.add("active");
      passwordField.style.backgroundColor = "white";
      passwordField.style.color = "";
      toggleIcon.style.color = "";
    } else {
      passwordField.type = "password";
      toggleIcon.classList.remove("active");
      passwordField.style.backgroundColor = "white";
      passwordField.style.color = "";
      toggleIcon.style.color = "";
    }
  }
