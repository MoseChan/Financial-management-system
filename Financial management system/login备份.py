#encoding:utf-8
#!/user/bin/python

import sys , os
from PyQt5 import QtWidgets,QtGui,QtCore
import ctypes

from sign_up import sign_up
from sign_in import sign_in

class Index(QtWidgets.QMainWindow):
    '''
    Show index view
    '''  
    def __init__(self,userId,Uname):
        super().__init__()
        #self.set_Ui()
        #self.hide_Cmd()
        self.userId = userId 
        self.Uname = Uname
    def set_Ui(self):
        self.setGeometry(115, 135, 800, 500)
        self.setWindowTitle("财务管理系统 - Mannage System  || {} 欢迎您的使用。".format(self.Uname))
        self.setWindowIcon(QtGui.QIcon('./img/appIco.ico'))  

        #self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)  
        #禁止 拉伸窗口 窗口最大化
        self.setFixedSize(self.width(), self.height())
        self.show() 
        #a = login()  

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self,
            'Message',"确认退出吗？",
            QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No
            ,QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:  
            event.accept()
        else:
            event.ignore()



    def hide_Cmd(self):
        '''隐藏CMD'''
        self.whnd = ctypes.windll.kernel32.GetConsoleWindow()  
        if self.whnd != 0:  
            ctypes.windll.user32.ShowWindow(self.whnd, 0)  
            ctypes.windll.kernel32.CloseHandle(self.whnd)
              


class login_view(QtWidgets.QMainWindow):
    '''登录界面'''
    def __init__(self):
        super().__init__()
        self.show_login_view()
    def show_login_view(self):
        self.setGeometry(200, 250, 350, 200)
        self.setWindowTitle("Login System")
        self.setWindowIcon(QtGui.QIcon('./img/appIco.ico'))  

        self.login_btn = QtWidgets.QPushButton('Login',self)
        self.login_btn.move(125,150)
        self.sign_up_btn = QtWidgets.QPushButton('sign up',self)
        self.sign_up_btn.move(230,150)

        self.username_Label = QtWidgets.QLabel('请输入用户名：',self)
        self.username_Label.move(30,40)
        self.username_Edit = QtWidgets.QTextEdit(self)
        self.username_Edit.move(120,40)
        self.password_Label = QtWidgets.QLabel('请输入密码：',self)
        self.password_Edit = QtWidgets.QTextEdit(self)
        self.password_Edit.move(120,85)
        self.password_Label.move(30,85)
        #self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)  
        #禁止 拉伸窗口 窗口最大化
        self.setFixedSize(self.width(), self.height())


        #self.login_btn.clicked.connect()     
        self.show()
        # return 1

    def loginButton_clicked(self):
        '''点击登录按钮'''
        u = self.username_Edit.toPlainText()  
        p = self.password_Edit.toPlainText()

        recode,Re_tips=sign_in(u,p).login()
        #成功登录时 Re_tips 返回的是 uid 详细参见 sign_in.login()   
        if recode == 1:
            QtWidgets.QMessageBox.question(self,'Message',"成功登录！",
                QtWidgets.QMessageBox.Ok)

            self.close()
            #main = Index(userId = Re_tips,Uname = u).set_Ui()  
        elif recode == 0:
            #登陆失败
            QtWidgets.QMessageBox.question(self,'Message',Re_tips,
                QtWidgets.QMessageBox.Ok)  


class sign_Up_view(QtWidgets.QMainWindow):
    '''注册界面'''
    def __init__(self):
        super().__init__()

    def show_sign_up_view(self):
        self.setGeometry(200, 250, 350, 200)
        self.setWindowTitle("sign Up")

        ok_btn = QtWidgets.QPushButton('OK',self)
        self.username_Edit = QtWidgets.QTextEdit(self)
        self.password_Edit = QtWidgets.QTextEdit(self)
        self.repassword_Edit = QtWidgets.QTextEdit(self)
        self.Email_Edit = QtWidgets.QTextEdit(self)
        username_Label = QtWidgets.QLabel("用户名：",self)
        password_Label = QtWidgets.QLabel("密码：",self)
        rePassword_Label = QtWidgets.QLabel("重新输入密码：",self)
        Email_Label = QtWidgets.QLabel("邮箱：",self)

        ok_btn.move(200,155)

        username_Label.move(10,20)
        password_Label.move(10,60)
        rePassword_Label.move(10,100)
        Email_Label.move(10,140)

        self.username_Edit.move(100,20)
        self.password_Edit.move(100,60)
        self.repassword_Edit.move(100,100)
        self.Email_Edit.move(100,140)

        ok_btn.clicked.connect(self.ok_clicked)
        self.show()


    def ok_clicked(self):
        '''注册页面 按钮点击事件'''
        u = self.username_Edit.toPlainText()
        p = self.password_Edit.toPlainText()
        e = self.Email_Edit.toPlainText()
        re_p = self.repassword_Edit.toPlainText()
        recode,return_Tips = sign_up(username=u, password=p, Email=e,reinput_passwd=re_p).add_user_info()
        if recode == 0:
            QtWidgets.QMessageBox.question(self,'Message',return_Tips,
                QtWidgets.QMessageBox.Ok)
            #self.close()  
        elif recode == 1:
            QtWidgets.QMessageBox.question(self,'Message',return_Tips,
                QtWidgets.QMessageBox.Ok)
            self.close()  


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    #index_Form = Index()
    sign_up_view = sign_Up_view()

    login_system = login_view()
    login_system.sign_up_btn.clicked.connect(sign_up_view.show_sign_up_view)
    login_system.login_btn.clicked.connect(login_system.loginButton_clicked)  
    #a.sign_up_btn.clicked.connect(a.show_signUp_view)
    
    sys.exit(app.exec_())  