function showConfirm(){
  document.getElementById('hideOriginal').style.display = "none";
  document.getElementById('confirmDelete').style.display = "block";
}
function returnOriginal(){
  document.getElementById('hideOriginal').style.display = "block";
  document.getElementById('confirmDelete').style.display = "none";
}
function popupEmail(to_email, from_name, class_name, class_period){
  var email_str = "https://mail.google.com/mail/u/0/?view=cm&fs=1&to=" + to_email + "&su=" + from_name + "%20-%20" + class_name + "%20-%20Period%20" + class_period;
  console.log(email_str);
  var winning = window.open(email_str,"","width=500,height=500");
}
function showHideDiv(divName){
  if (document.getElementById(divName).style.display === "none"){document.getElementById(divName).style.display = "block";}
  else{document.getElementById(divName).style.display = "none";}
}
//function popupEmailMultiple(to_emails, from_name, )
