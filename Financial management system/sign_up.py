#encoding:utf-8
#!/user/bin/python
import MySQLdb
import re
import random
import os

class sign_up():
    def __init__(self,username,password,Email,reinput_passwd):
        '''初始化数据'''
        self.username = username
        self.password = password
        self.Email = Email
        self.reinput_passwd = reinput_passwd

    def add_user_info(self):
        '''
        返回值
        状态码 + 返回信息
        0 即为注册失败
        1 为成功
        '''
        #判断是否有空
        if self.username == '' or self.password == '' or self.Email == '' or self.reinput_passwd == '':
            return 0,'不可有任何一项留空'
        
        #判断E mail 格式
        Email_re = re.compile(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$')
        check_mail = re.search(Email_re,self.Email)
        if check_mail == None:
            return 0,'error ,邮箱格式错误！'

        if self.password != self.reinput_passwd:
            return 0,'error ,两次密码输入不一致'

        #连接数据库
        conn = MySQLdb.connect(host="localhost",user="root",passwd="root",db="financialmanage",charset="utf8")
        cursor = conn.cursor()
        #查找有无相同用户名
        cursor.execute('select username from userinformation where username = "{}"'.format(self.Email))  
        search_record = cursor.fetchone()
        if search_record == None:
            try:
                self.uid = self.generate_Uid()  
                record = cursor.execute('insert into userinformation(username,password,Email,uid) value("{}","{}","{}","{}")'.format(self.username,self.password,self.Email,self.uid))
                if record == 0:
                    conn.close()
                    return 0,'创建失败,请尝试输入其他值'
                else:
                    conn.close()
                    self.create_userDir()  
                    return 1,'成功创建账户'
            except Exception as e:
                print(e)  
                conn.close()
                return 0,'创建失败,数据库发生未知错误！'
        else:
            conn.close()  
            return 0,'注册失败,用户名已注册.如果忘记密码,请联系数据管理员。'

    def create_userDir(self):
        '''生成用户文件夹'''
        try:
            #用户文件夹名称即为uid
            os.mkdir('./data/{}'.format(str(self.uid)))  
        except Exception as e:
            print(e)              
          
    def generate_Uid(self):
        '''简单的生成一个 uid'''

        #生成 uid的长度
        loop_Number = random.randint(8,10)
        
        uid = ''
        #使用 random 模块 生成uid
        for i in range(0,loop_Number):
            uid = uid+str(random.randint(0,9))
        return uid
        