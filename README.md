
### How To Run Application ###

Greetings Control :),
My system is Ubuntu 18.04.
To run application it's necessary to clone repository or download zip file in previously
created virtual enviroment on local machine or maybe Docker container.
Useful link to download and install [virtualenv](https://help.dreamhost.com/hc/en-us/articles/115000695551-Installing-and-using-virtualenv-with-Python-3).
In application is used Python==3.6.9(Ubuntu system one).

Command for installing all dependencies is `$ pip install -r requirements.txt`.
Off course if you don't like pip and virtualenv, [pipenv](https://pipenv-fork.readthedocs.io/en/latest/) 
is similar and easy to use package manager (pip and virtualenv is combined in pipenv).

After creating virtual enviroment and installing all dependencies, just type `flask run` in terminal, 
where run.py file is located, and application will be started on http://127.0.0.1:6767/ or http://localhost:6767/.


### About Application ###

**Database**

Database used in application is PostgreSQL==10.0.
If you need to install and setup PostgreSQL on your machine, useful [link](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04).
.env file is created to handle all enviroment variables, in this file you will 
find instructions where to put you path to database, api keys, email users etc. For testing database
changes and to see what happening, usefull application is PgAdmin, but i am not expert with PgAdmin, 
i like to use terminal, and after installing and setu if you want to quickly open created database for this application.
Usefull command is 
`$ psql -d <nameofdatabase> -U <nameofdatabaseuser> -h localhost`

**Application**

Framework used in application is Flask, and i tried to use as less as i can packages in application.
So for REST server you will find there is no present Flask-RESTful extension.
Every route is pretty self explanatory, i tried to comments as much i can to describe each method in application.
Maybe coding is little inconsistent, but i try to use few different approach to handling logic.


**Test RESTful**

For testing REST API-s I used Postman, if you need to download it, useful [link](https://www.postman.com/downloads/).
Endpoints for testing API-s is http://127.0.0.1:6767/api/api_routes/.

-To create user endpoint is /create_user
It's neccessary to setup method to POST and you need to setup body to row, and where is TEXT
on the same navigation bar to change to JSON, and to send:
```
{
	"fullname": "Firstname Lastname",
	"email": "emailemail@mail.com",
	"password": "password1",
	"confirm_password": "password1"
}
```
I added validation to correspond to form which is used in application. Password will be hashed.

-To login in application endpoint is /login
In this endpoint I used Basic Authentication, and it's neccessary to set Postman, in Autorization card 
set type to Basic Auth, and in fields where is 
USERNAME to type EMAIL used for registration and in field where is PASSWORD, 
PASSWORD which is used to for registration application. After login token will be presented to user 
(JWT) and with token wich is needed to be placed in headers in /all_users route, user will
 be able to see all registered users in application, token will last 90 minutes, of course 
 it can be set for another amount of time, after 90 minutes user must be logged again.


-To see all registered users endpoint is /all_users
Set method to GET and as I mentioned before in headers it's is neccessary to 
uncheck generic keys and to add folowing:
| Key            | Value                   |
| -------------- | ----------------------- |
| Content-Type   | application/json        |
| Authorization  | Basic                   | 
| x-access-token | *here goes token value* | 

After sending request user will be able to see credentials of all other registered users, 
of course password will not be disaplayed.

-To ask for reset password endpoint is /request_reset
On this endpoint, method is GET and it's neccessary to send email in JSON format.
```
{
    "email": "emailusedfor@registration.app"
}
```
After email is checked for validation and if it is present in database, email with instruction will
be sent to user. Email which is send to user is slightly different depends from which side off application
is asked for password reset, but in both cases token(in this case I used itsdangerous.TimedJSONWebSignatureSerializer class) will be send in email, token for password reset will last 30 minutes.
To test endpoint it's needed to copy url present in email, and it will look something like this
http://localhost:6767/api/api_routes/reset_password/<token_value_here>,
and to send, method is POST.
```
{
	"password": "newpassword",
	"confirm_password": "newpassword"
}
```
After validation is checked, user is successfully changed password and now is able to login with new password.


**Email Provider**
I tried to use Sendgrid as suggessted in Home assigment document, you will find enviroment variables 
which are lead to Sendgrid setup, but unfortunately
after implementation of Sengrid and no errors in code, output of Flask Shell is in the code block, 
and after sending lot off emails, neither one is delivered on recepient address, 
as you can see that email is received by server 
in line where `data: (250, b'Ok: queued as wZPZNS6URw2kc0jvahTQPA'` is present.
But email is never delivered. So as alternative I used Gmail smtp with app password, 
as you will find in .env file.

**Output from flask shell**

```
from app import mail
from flask_mail import Message
msg = Message('test mail', recipients=['vladimirmijatovic@yandex.com'])
msg.body = 'test body'
msg.html = '<p>test html</p>'
mail.send(msg)
send: 'ehlo [127.0.1.1]\r\n'
reply: b'250-smtp.sendgrid.net\r\n'
reply: b'250-8BITMIME\r\n'
reply: b'250-PIPELINING\r\n'
reply: b'250-SIZE 31457280\r\n'
reply: b'250-STARTTLS\r\n'
reply: b'250-AUTH PLAIN LOGIN\r\n'
reply: b'250 AUTH=PLAIN LOGIN\r\n'
reply: retcode (250); Msg: b'smtp.sendgrid.net\n8BITMIME\nPIPELINING\nSIZE 31457280\nSTARTTLS\nAUTH PLAIN LOGIN\nAUTH=PLAIN LOGIN'
send: 'STARTTLS\r\n'
reply: b'220 Begin TLS negotiation now\r\n'
reply: retcode (220); Msg: b'Begin TLS negotiation now'
send: 'ehlo [127.0.1.1]\r\n'
reply: b'250-smtp.sendgrid.net\r\n'
reply: b'250-8BITMIME\r\n'
reply: b'250-PIPELINING\r\n'
reply: b'250-SIZE 31457280\r\n'
reply: b'250-STARTTLS\r\n'
reply: b'250-AUTH PLAIN LOGIN\r\n'
reply: b'250 AUTH=PLAIN LOGIN\r\n'
reply: retcode (250); Msg: b'smtp.sendgrid.net\n8BITMIME\nPIPELINING\nSIZE 31457280\nSTARTTLS\nAUTH PLAIN LOGIN\nAUTH=PLAIN LOGIN'
send: 'AUTH PLAIN AGFwaWtleQBTRy5SN19scWY3NlFuV3BuaVBnR3JnckNBLl8xbmxPZXQ1V1RRWk9TZ2ZtQU1XUWhjMXM0YlV0eGROaWsybFptTjltWG8=\r\n'
reply: b'235 Authentication successful\r\n'
reply: retcode (235); Msg: b'Authentication successful'
send: 'mail FROM:<mijatovski@gmail.com> size=820\r\n'
reply: b'250 Sender address accepted\r\n'
reply: retcode (250); Msg: b'Sender address accepted'
send: 'rcpt TO:<vladimirmijatovic@yandex.com>\r\n'
reply: b'250 Recipient address accepted\r\n'
reply: retcode (250); Msg: b'Recipient address accepted'
send: 'data\r\n'
reply: b'354 Continue\r\n'
reply: retcode (354); Msg: b'Continue'
data: (354, b'Continue')
send: b'Content-Type: multipart/mixed; boundary="===============1762790784697053485=="\r\nMIME-Version: 1.0\r\nSubject: test mail\r\nFrom: mijatovski@gmail.com\r\nTo: vladimirmijatovic@yandex.com\r\nDate: Tue, 05 May 2020 11:31:14 +0200\r\nMessage-ID: <158867104195.4326.17079206942877741620@mijato>\r\n\r\n--===============1762790784697053485==\r\nContent-Type: multipart/alternative;\r\n boundary="===============8402721611717171372=="\r\nMIME-Version: 1.0\r\n\r\n--===============8402721611717171372==\r\nContent-Type: text/plain; charset="utf-8"\r\nMIME-Version: 1.0\r\nContent-Transfer-Encoding: 7bit\r\n\r\ntest body\r\n--===============8402721611717171372==\r\nContent-Type: text/html; charset="utf-8"\r\nMIME-Version: 1.0\r\nContent-Transfer-Encoding: 7bit\r\n\r\n<p>test html</p>\r\n--===============8402721611717171372==--\r\n\r\n--===============1762790784697053485==--\r\n.\r\n'
reply: b'250 Ok: queued as wZPZNS6URw2kc0jvahTQPA\r\n'
reply: retcode (250); Msg: b'Ok: queued as wZPZNS6URw2kc0jvahTQPA'
data: (250, b'Ok: queued as wZPZNS6URw2kc0jvahTQPA')
send: 'quit\r\n'
reply: b'221 See you later\r\n'
reply: retcode (221); Msg: b'See you later'
```
-So that will be instructions for "HOW TO" use application, so thanks for oportunity and hope you will successfully 
setup and run this app, offcourse if you run on some problems and errors you can write me at any time.
All the best, 
Vladimir.
