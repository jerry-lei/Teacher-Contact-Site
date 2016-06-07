/**
 * Checks if the div is style is block or none. Switches to the other one.
 *
 * divName: The id of the div that is to be switched.
 *
 */
function showHideDiv(divName){
  if (document.getElementById(divName).style.display === "none"){document.getElementById(divName).style.display = "block";}
  else{document.getElementById(divName).style.display = "none";}
}

/**
 * These two functions show/hide the confirm.
 * Used in: 'class.html'
 *
 */
function showConfirm(){
  showHideDiv('hideOriginal');
  showHideDiv('confirmDelete');
}
function returnOriginal(){
  showHideDiv('hideOriginal');
  showHideDiv('confirmDelete');
}

/**
 * Brings up a popup window with compose email with 'to' field and 'subject' field filled out
 * Used in: 'class.html'
 *
 */
function popupEmail(to_email, from_name, class_name, class_period){
  var email_str = "https://mail.google.com/mail/u/0/?view=cm&fs=1&to=" + to_email + "&su=" + from_name + "%20-%20" + class_name + "%20-%20Period%20" + class_period;
  console.log(email_str);
  var winning = window.open(email_str,"","width=500,height=500");
}

/**
 * Popup window with compose email. BCC to checked students. Subject and body from form.
 * Used in: 'sendMail.html'
 *
 */
function popupEmailMultiple(){
  //var form = document.getElementById("name_checks");
  var form = document.getElementsByName("checks");
  var to_str = "";
  for (var c1 = 0; c1 < form.length; c1++){
    if(form[c1].checked){
      console.log(form[c1]);
      to_str += form[c1].value + ",";
    }
  }

  console.log(to_str);
  var body = document.getElementById("body_name").value;
  body = body.replace(/\r?\n/g, '%0A');
  var subject = document.getElementById("subject_name").value;
  var email_str = "https://mail.google.com/mail/u/0/?view=cm&fs=1&bcc=" + to_str + "&su=" + subject + "&body=" + body;
  var winning = window.open(email_str, "", "width=500,height=500");
}

/**
 * Popup window with a search for the emails sent to param: 'to_email'
 *
 */
function showPastEmails(to_email){
  var email_str = "https://mail.google.com/mail/u/0/#search/to:" + to_email
  var winning = window.open(email_str,"","width=500,height=500");
}
