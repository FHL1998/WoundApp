import os
import sqlite3

from kivymd.toast import toast

from db.sqlite3_connect import select_data, insert_data, select


def insert_into_account(username, email, password, github_login_flag):
    conn = sqlite3.connect('patients_information.db')
    c = conn.cursor()
    userflag = False
    toast("User Already Exists! Please Log In !")
    user = "user already exists"
    # d = c.fetchone()
    #sql = "SELECT Username,Password from account WHERE Username = '{}'".format(username)
    #select_data(sql)
    c.execute("SELECT Username,Password from account WHERE Username = '{}'".format(username))
    d = c.fetchone()
    if d is None:
        userflag = True
        user = "created"
        sql = "INSERT INTO account(Username,Email,Password,Github) values('{}','{}','{}','{}')".format(username, email,
                                                                                                       password,
                                                                                                       github_login_flag)
        insert_data(sql)
        # c.execute("INSERT INTO account values('{}','{}','{}')".format(username, email, password))
    print(user)
    conn.commit()
    conn.close()
    return userflag, user


def insert_into_github_account(username, email, password, remember_me_flag, github_login_flag):

    #user = "Github Account Creating"
    sql = "INSERT INTO account(Username,Email,Password,Remember,Github) values('{}','{}','{}','{}','{}')" \
            .format(username, email, password, remember_me_flag, github_login_flag)
    insert_data(sql)
    # c.execute("INSERT INTO account values('{}','{}','{}')".format(username, email, password))
    #print(user)


def get_password(email):
    # sql = "SELECT Username,Password from account WHERE Username = '{}'".format(username)
    # sql = "SELECT Email,Password from account WHERE Email = '{}'".format(email)
    # select_data(sql)
    conn = sqlite3.connect('patients_information.db')
    c = conn.cursor()
    c.execute("SELECT Email,Password from account WHERE Email = '{}'".format(email))
    d = c.fetchone()
    if d is None:
        conn.commit()
        conn.close()
        return False, None
    if len(d) != 0:
        conn.commit()
        conn.close()
        return True, d[1]


def retrieve(email, password):
    conn = sqlite3.connect('patients_information.db')
    c = conn.cursor()
    userflag = False
    userinfo = "user Not exist"
    c.execute("SELECT Email from account WHERE Email = '{}'".format(email))
    # sql = "SELECT Email from account WHERE Email = '{}'".format(email)
    # select_data(sql)
    # c.execute("SELECT name from login WHERE name = '{}'".format(username))
    d = c.fetchone()
    if d is not None:
        userflag = True
        userinfo = "Password Changed"
        sql = "UPDATE account SET password = '{}' WHERE Email='{}' ".format(password, email)
        insert_data(sql)
        # c.execute("UPDATE account SET password = '{}' WHERE Username='{}' ".format(password, username))
    conn.commit()
    conn.close()
    return userflag, userinfo


def reset(username, password):
    conn = sqlite3.connect('patients_information.db')
    c = conn.cursor()
    userflag = False
    userinfo = "user Not exist"
    c.execute("SELECT Username from account WHERE Username = '{}'".format(username))
    # sql = "SELECT Email from account WHERE Email = '{}'".format(email)
    # select_data(sql)
    # c.execute("SELECT name from login WHERE name = '{}'".format(username))
    d = c.fetchone()
    if d is not None:
        userflag = True
        userinfo = "Password Reset"
        sql = "UPDATE account SET password = '{}' WHERE Username='{}' ".format(password, username)
        insert_data(sql)
        # c.execute("UPDATE account SET password = '{}' WHERE Username='{}' ".format(password, username))
    conn.commit()
    conn.close()
    return userflag, userinfo
