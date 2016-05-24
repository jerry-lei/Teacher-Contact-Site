# Teacher Contact Site
This Teacher Contact Site is a final project for a software development class. It is written to meet the needs of a Stuyvesant High School teacher, Mr. Wisotsky, for an easier way to contact students and their parents.

### Authors:
- [Ri Jiu Zheng](https://github.com/RJZheng1)
- [Jerry Lei](https://github.com/jerrylei98)
- [Winton Yee](https://github.com/blehw)
- [Masahero Masuda](https://github.com/masa13)

### Devlog:
- [x] May 17, 2016: First meeting with client
- [x] May 22, 2016: Oauth done
- [x] May 22, 2016: Limited to only stuy.edu emails
- [ ] May 26, 2016: Second meeting with client

### Todo (Client requested):
- [x] &nbsp; Login through Google API (stuy.edu only) -- SOMETIMES REQUIRES REFRESH
- [x] &nbsp; Logout (technically) -- LOGOUT PAGE WILL NOT AUTO CLOSE
- [x] &nbsp; Import contact info of students
- [x] &nbsp; Contact info overrides
- [x] &nbsp; Allow students to import contact info of parents
- [x] &nbsp; Class profile
- [ ] &nbsp; Student profile
- [ ] &nbsp; Teachers cannot see students info
- [ ] &nbsp; Teacher access to contactInfo.html
- [x] &nbsp; Send single email
- [ ] &nbsp; Send mass emails (link to create email: https://mail.google.com/mail/?view=cm&fs=1&to=someone@example.com&su=SUBJECT&body=BODY&bcc=someone.else@example.com , www.w3schools.com/tags/ref_urlencode.asp)
- [ ] &nbsp; Logs of letters/what kinds of letters/notes to a log
- [ ] &nbsp; Links to send previously generated letters (with ability to edit)
- [ ] &nbsp; (Stretch) Print address on double sided paper
- [ ] &nbsp; (Stretch) Voice call

### Sources:
- https://github.com/BlackrockDigital/startbootstrap-bare
- https://developers.google.com/gmail/api/quickstart/js

### How to use (server sided):
1. Get API keys from https://console.developers.google.com
2. Save the json file and rename it to gmail.json in the directory named 'secret_key' next to the github repo<br>
   ``` $ ~/Teacher-Contact-Site```<br>
   ``` $ ~/secret_key/gmail.json```<br>
3. Enable Gmail and Google+ APIs
4. Necessary python imports:
  - flask
  - json
  - pymongo
  - MongoDB
5. Run app.py
