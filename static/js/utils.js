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
function showPastEmails(to_email){
  var email_str = "https://mail.google.com/mail/u/0/#search/to:" + to_email
  var winning = window.open(email_str,"","width=500,height=500");
}
function popupEmailMultiple(){
  var form = document.getElementById("name_checks");
  var to_str;
  for (var c1 = 0; c1 < form.elements['checks'].length; c1++) {
    to_str += (form.elements['letters'][c1].value) + ',';
  }
  var body = document.getElementByName("body_name");
  var subject = document.getElementByName("subject_name")
  var email_str = "https://mail.google.com/mail/u/0/?view=cm&fs=1&bcc=" + to_str + "&su=" + subject + "&body=" + body;
  console.log(email_str);
  var winning = window.open(email_str, "", "width=500,height=500");
}
