#encoding:utf-8
#!/user/bin/python

import os
import MySQLdb
import sys
from PyQt5 import QtWidgets,QtCore,QtGui


class Main_View(QtWidgets.QMainWindow):
    def __init__(self,uid,username):
        super().__init__()
        self.uid = uid 
        self.username = username
        recode = self.check_information()  
        if recode == 0:
            print(recode)  
            exit()
        else:
            self.show_Main_view()  
    
    def check_information(self):
        '''检测 通过接口传来的数据'''
        try:
            int(self.uid)
        except:
            return 0

        conn = MySQLdb.connect(host="localhost",user="root",passwd="root",db="financialmanage",charset="utf8")
        cursor = conn.cursor()
        

        a = cursor.execute('select uid from userinformation where username="{}"'.format(self.username))   
        # 判断有无 username 无则 a为0
        if a == 0:
            print('a'+a)  
            conn.close()  
            return 0
        else:
            # 判断Uid 是否对应
            GetUid = cursor.fetchone()[0]
            if GetUid != self.uid:
                conn.close()  
                print(GetUid,self.uid)  
                return 0
            else:
                conn.close()
                return 1

    def show_Main_view(self):  
        self.setGeometry(115, 135, 800, 500)
        self.setWindowTitle("财务管理系统 - Mannage System  || {} 欢迎您的使用。".format(self.username))
        #设置 图标
        self.setWindowIcon(QtGui.QIcon('./img/appIco.ico'))  
        self.set_background_img()  

        #菜单栏
        MenuBar = self.menuBar()
        startMenu = MenuBar.addMenu('开始')
        moneyMenu = MenuBar.addMenu('财务管理')
        setMenu  = MenuBar.addMenu('设置')
        about_us = MenuBar.addMenu('关于')

        about_Action = QtWidgets.QAction('关于我们',self)
        about_Action.triggered.connect(self.about_Us)  
        about_us.addAction(about_Action)  

        APPQUIT_Act = QtWidgets.QAction('退出',self)
        startMenu.triggered.connect(self.Main_Quit)  
        startMenu.addAction(APPQUIT_Act)       


        #self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)  
        #禁止 拉伸窗口 窗口最大化
        self.setFixedSize(self.width(), self.height())
        self.show() 

    def Main_Quit(self):
        self.close()          

    def set_background_img(self):
        '''设置背景图片'''
        #判断用户有无预先设定 背景图片
        pic_path = './img/{}.jpg'.format(self.uid)
        #print()  
        recode = os.path.exists(pic_path)
        if recode == True:
            pal = QtGui.QPalette()
            pal.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(pic_path)))
            self.setPalette(pal)
            self.setAutoFillBackground(True)  
        else:
            #背景图片  图片大小默认为 800(长) * 500(宽)
            pal = QtGui.QPalette()
            #默认填充图片为 ./img/default.jpg
            pal.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap('./img/default.jpg')))  
            self.setPalette(pal)
            self.setAutoFillBackground(True)  

    def contextMenuEvent(self,event):
        '''右键菜单栏'''
        cmenu = QtWidgets.QMenu(self)
        quitAct = cmenu.addAction('退出')   
        action = cmenu.exec_(self.mapToGlobal(event.pos()))  
        if action == quitAct:
            self.close()  

    def closeEvent(self, event):
        '''关闭窗口警告'''
        reply = QtWidgets.QMessageBox.question(self,
            'Message',"确认退出吗？",
            QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No
            ,QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:  
            event.accept()
        else:
            event.ignore()

    def about_Us(self):
        '''这段代码有点丑 放到最后吧0.0'''
        QtWidgets.QMessageBox.question(self,'关于',"程序作者刚刚学习QT不久 \n这个程序是练手的 \
一个程序\n希望大神们轻喷\n有一起交流的童鞋们 也可\
以一起交流\n联系方式：2564845837@qq.com\nGithub:https://github.com/MoseChan",
QtWidgets.QMessageBox.Ok)  
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    try:    
        userID = sys.argv[1]
        userName = sys.argv[2]
    except:
        exit()  
    #print(userID,userName)

    main = Main_View(userID,userName)  
    sys.exit(app.exec_()) 
