

"""
body is from text box. (fxn replaces \n with %A0 and ' ' with %20)
subject is from a list from checkboxes. (printed comma separated)
"""
def make_link(body,to,subject):
    #Link: https://mail.google.com/mail/u/0/?view=cm&fs=1&to=someone@example.com&su=SUBJECT&body=BODY&bcc=someone.else@example.com&tf=1
    body = body.replace('\n', "%A0")
    body = body.replace(' ', "%20")
    subject = subject.replace('\n', "%A0")
    subject = subject.replace(' ', "%20")
    bcc = to[0]
    to_2 = to[1:]
    to_str = ''
    for x in xrange(len(to_2)):
        to_str += to_2[x] + ','
    to_str = to_str[:-1] #gets rid of comma at end
    #return bcc + '\n' + to_str
    return "https://mail.google.com/mail/u/0/?view=cm&fs=1&to=" + to_str + "&su=" + subject + "&body=" + body + "&bcc=" + bcc + "&tf=1"

#print make_link("The quick brown fox jumps over the lazy dog \n ahasdf asss",["jlei2@stuy.edu","rzheng2@stuy.edu","michael@gmail.com","amazon@gmail.com"])