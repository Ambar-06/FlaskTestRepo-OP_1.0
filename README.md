# FlaskTestRepo-OP_2.0\

##Sample POSTMAN Requests --------- 1\
URL : http://127.0.0.1:5000/generateToken \
Method : POST\
Header : *BLANK*\
Body :  {\
    "Email": "ambar@onecorp.co.in",\
    "Key": "45c376aef58f268d7212652a87ad1d6de3647e63e9daf2e5d04b"\
}\

##Sample POSTMAN Requests --------- 2\
URL : http://127.0.0.1:5000/generate_long_lived_token \
Method : POST\
Header : *BLANK*\
Body :  {\
    "access_token": *"<OBTAINED FROM FIRST THE RESPONSE OF FIRST REQUEST>"*\
}\

##Sample POSTMAN Requests --------- 3\
URL : http://127.0.0.1:5000/AddUser \
Method : POST\
Header : Authorization : Bearer *<LONG-LIVE-TOKEN>*\
Body :  {\
    "FirstName" : "",\
    "LastName" : "",\
    "Password" : "",\
    "Email" : "",\
    "Mobile" : ""\
}\

##Sample POSTMAN Requests --------- 4\
URL : http://127.0.0.1:5000/GetUsers \
Method : POST\
Header : Authorization : Bearer *<LONG-LIVE-TOKEN>*\
Body :  *BLANK*\

##Sample POSTMAN Requests --------- 5\
URL : http://127.0.0.1:5000/me \
Method : POST\
Header : Authorization : Bearer *<LONG-LIVE-TOKEN>*\
Body :  {\
    "UserToken" : *"<USERTOKEN_OF_CURRENT_USER>"*\
}

##Sample POSTMAN Requests --------- 6\
URL : http://127.0.0.1:5000/UpdateUser \
Method : POST\
Header : Authorization : Bearer *<LONG-LIVE-TOKEN>*\
Body :  {\
    "UserToken" : "c7967144-3ec3-11ee-bbe7-0211585a676a",     -- REQUIRED, Restt other fields are Optional\
    "" : "",\
    "" : "", ...\
}\

