import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv() 

mydb = mysql.connector.connect(
  host=os.environ.get('HOST'),
  user=os.environ.get('USER'),
  password=os.environ.get('PASSWORD'),
  database=os.environ.get('DB')
)


def dictfetchall(cursor=''):
    # "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def dictfetchone(cursor=''):
    # "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return dict(zip([col[0] for col in desc], cursor.fetchone()))


cursor = mydb.cursor()

def addUser_q(data):
    resp = cursor.execute(""" 
        INSERT INTO AISocialMediaDB.smUsers
        (
        UserId,
        UserToken,
        UserName,
        FirstName,
        LastName,
        Password,
        Email,
        Mobile,
        Source,
        Device,
        IsDeleted,
        CreatedAt,
        CreatedBy,
        UpdatedAt,
        UpdatedBy)
        VALUES
        (uuid(),UUID(),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", data)
    mydb.commit()
    return resp


def get_user_q(data):
    resp = cursor.execute('''SELECT 
    ID,
    ID KeyIndex,
    UserId,
    CompanyId,
    UserName,
    FirstName,
    LastName,
    ProfilePicture,
    Password,
    Country,
    State,
    City,
    Address,
    PinCode,
    Email,
    Mobile,
    IsMobileVerified,
    IsEmailVerified,
    IsDeleted,
    UserToken,
    JobTitle,
    OnepostCalendar,
    CreatedAt,
    CreatedBy,
    UpdatedAt,
    UpdatedBy ID
    FROM
    AISocialMediaDB.smUsers where UserToken='{}' and IsDeleted=0;'''.format(data))
    resp = dictfetchone(cursor)
    if resp:
        resp = resp
    else:
        resp = None
    return resp
    

def updateUser_q(data):
    resp = cursor.execute(""" 
        UPDATE AISocialMediaDB.smUsers
        SET
        UserName  = %s,
        FirstName  = %s,
        LastName  = %s,
        Email  = %s,
        Mobile  = %s,
        Source  = %s,
        Device  = %s,
        IsDeleted  = %s,
        CreatedAt  = %s,
        CreatedBy  = %s,
        UpdatedAt  = %s,
        UpdatedBy  = %s WHERE UserId=%s;""", data)
    mydb.commit()
    return resp
    

def getUsers_q():
    resp = cursor.execute("""SELECT * FROM AISocialMediaDB.smUsers WHERE IsDeleted = '0';""")
    resp = dictfetchall(cursor)
    print(resp)
    if resp and cursor.rowcount:
        resp = resp
    return resp

    