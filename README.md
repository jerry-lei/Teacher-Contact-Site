# Teacher Contact Site
This Teacher Contact Site is a final project for a software development class. It is written to meet the needs of a Stuyvesant High School teacher, Mr. Wisotsky, for an easier way to contact students and their parents.

### Authors:
- [Ri Jiu Zheng](https://github.com/RJZheng1)
- [Jerry Lei](https://github.com/jerrylei98)
- [Winton Yee](https://github.com/blehw)
- [Masahero Masuda](https://github.com/masa13)

### Devlog:
- [x] May 17, 2016: First meeting with client
- [x] May 26, 2016: Second meeting with client

### Todo (Client requested):
- [x] &nbsp; Login through Google API (stuy.edu only)
- [x] &nbsp; Logout
- [x] &nbsp; Import contact info of students
- [x] &nbsp; Contact info overrides
- [x] &nbsp; Allow students to import contact info of parents
- [x] &nbsp; Class profile
- [x] &nbsp; Student profile
- [x] &nbsp; Teachers see students info
- [x] &nbsp; Teacher access to contactInfo.html
- [x] &nbsp; Send single email
- [x] &nbsp; Send mass emails (link to create email: https://mail.google.com/mail/?view=cm&fs=1&to=someone@example.com&su=SUBJECT&body=BODY&bcc=someone.else@example.com , www.w3schools.com/tags/ref_urlencode.asp)
- [x] &nbsp; Logs of letters/what kinds of letters/notes to a log
- [x] &nbsp; Show emails sent to a student (through window)
- [ ] &nbsp; Links to send previously generated letters (with ability to edit)
- [ ] &nbsp; (Stretch) Print address on double sided paper
- [ ] &nbsp; (Stretch) Voice call

### Sources:
- https://github.com/BlackrockDigital/startbootstrap-bare
- https://developers.google.com/gmail/api/quickstart/js

### DEPLOYMENT GUIDE:
1. Get API keys from https://console.developers.google.com
  - Select 'Create a project...' from dropdown on top right, 'Select a project'
  - Fill in project name with 'Stuyvesant Contact Site'
  - Click on 'Google+ API' under Social APIs
    - Click on the blue 'Enable' button
  - On the left navigation bar, go to the 'Credentials' page
    - Go to the 'OAuth consent screen' tab
      - Fill in 'Product name shown to users' with 'Stuyvesant Contact Site'
      - Click 'Save' (Will be directed to a credentials page)
        - Select Web Application under 'Application type'
        - Name: Stuyvesant Contact Site
        - Authorized Javascript origins: http://<site ip/name>
        - Click 'Create'
    - Go to 'Credentials' tab
      - Click on 'Stuyvesant Contact Site'
      - Click 'Download JSON' button
      - Save the json file as 'gmail.json'
2. Put the json file in the repo<br>
  ├───Teacher-Contact-Site<br>
  │&nbsp;&nbsp;&nbsp;└───gmail.json<br>
3. Enable Gmail and Google+ APIs
4. Necessary python imports:
  - flask
  - json
  - pymongo
  - MongoDB
5. Run app.py
