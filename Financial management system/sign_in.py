#encoding:UTF-8
#!/user/bin/python

import MySQLdb

class sign_in():
    def __init__(self,username,password):
        self.username = username
        self.password = password

        self.login()
    def login(self):
        conn = MySQLdb.connect(host="localhost",user="root",passwd="root",db="financialmanage",charset="utf8")
        cursor = conn.cursor()

        cursor.execute('select password from userinformation where username ="{}"'.format(self.username))
        real_password = cursor.fetchone()
        if real_password == None:
            conn.close()  
            return 0,'登录失败，没有该用户名'
        else:
            real_password = real_password[0]
            if self.password == real_password:
                cursor.execute('select uid from userinformation where username = "{}"'.format(self.username))  
                uid = cursor.fetchone()[0]
                conn.close()
                #这里 return 1 表示 成功登录 而且 返回的第二个返回值 是 uid 不是提示信息  
                return 1,uid
            else:
                conn.close()  
                return 0,'登陆失败,密码错误'
