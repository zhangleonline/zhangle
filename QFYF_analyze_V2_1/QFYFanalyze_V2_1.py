import sys
from QFYF_analyze_mainclass import *

from PyQt5.QtWidgets import *
import pandas as pd
from PyQt5.QtCore import Qt
import time


class MainForm(QWidget):

    def __init__(self, name = 'MainForm'):
        super(MainForm,self).__init__()


        self.setWindowTitle(name)
        self.cwd = os.getcwd() # 获取当前程序文件位置

        self.dir_choose1 = self.cwd
        self.dir_choose2 = self.cwd

        self.resize(400, 500)   # 设置窗体大小

        # 显示1，显示输入文件夹的信息
        # self.display1 = QLineEdit()
        self.display1 = QLabel()
        self.display1.setObjectName("Empty")
        self.display1.setText("Empty(默认当前根目录)")

        # 显示2，显示输出位置信息
        # self.display2 = QLineEdit()
        self.display2 = QLabel()
        self.display2.setObjectName("Empty")
        self.display2.setText("Empty（默认当前根目录）")

        # btn 显示输入文件夹按钮
        self.btn_chooseDir1 = QPushButton(self)
        self.btn_chooseDir1.setObjectName("btn_chooseDir")
        self.btn_chooseDir1.setText("选择输入文件夹")

        # btn 显示输出位置按钮
        self.btn_chooseDir2 = QPushButton(self)
        self.btn_chooseDir2.setObjectName("btn_chooseDir2")
        self.btn_chooseDir2.setText("选择输出文件夹位置")

        # btn 4
        self.btn_startTask = QPushButton(self)
        self.btn_startTask.setObjectName("btn_startTask")
        self.btn_startTask.setText("开始")

        # self.display3 = QLineEdit()
        self.display3 = QLabel()
        self.display3.setObjectName("未开始")
        self.display3.setText("未开始")



        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.btn_chooseDir1, 0, Qt.AlignHCenter)
        self.btn_chooseDir1.setFixedSize(150, 30)
        layout.addWidget(self.display1, 0, Qt.AlignHCenter)
        self.display1.setFixedSize(200, 80)
        layout.addWidget(self.btn_chooseDir2, 0, Qt.AlignHCenter)
        self.btn_chooseDir2.setFixedSize(150, 30)
        layout.addWidget(self.display2, 0, Qt.AlignHCenter)
        self.display2.setFixedSize(200, 80)

        layout.addWidget(self.btn_startTask, 0, Qt.AlignHCenter)
        self.btn_startTask.setFixedSize(150, 30)
        layout.addWidget(self.display3, 0, Qt.AlignHCenter)
        self.display3.setFixedSize(250, 100)
        self.setLayout(layout)

        # 设置信号
        self.btn_chooseDir1.clicked.connect(self.slot_btn_chooseDir1)
        self.btn_chooseDir2.clicked.connect(self.slot_btn_chooseDir2)
        self.btn_startTask.clicked.connect(self.slot_btn_startTask)



    def slot_btn_chooseDir1(self):      #  按钮1回调函数
        self.dir_choose1 = QFileDialog.getExistingDirectory(self,
                                    "选取输入文件夹",
                                    self.cwd) # 起始路径

        if self.dir_choose1 == "":
            print("\n取消选择")
            self.display1.setText("\n取消选择")
            return

        print("\n你选择的输入文件夹为:")
        print(self.dir_choose1)
        self.display1.setText("\n你选择的输入文件夹为:"+self.dir_choose1)

    def slot_btn_chooseDir2(self):    #  按钮2回调函数
        self.dir_choose2 = QFileDialog.getExistingDirectory(self,
                                    "选取输出文件放置文件夹",
                                    self.cwd) # 起始路径

        if self.dir_choose2 == "":
            print("\n取消选择")
            self.display2.setText("\n取消选择")
            return

        print("\n文件输出位置为:")
        print(self.dir_choose2)
        self.display2.setText("\n文件输出为:"+self.dir_choose2)

    def slot_btn_startTask(self):     #按钮3保存回调函数
        starttime = time.time()

        self.display3.setText("load data...文件较大请稍等...")
        QApplication.processEvents()
        root = self.dir_choose1
        root_to_xls = self.dir_choose2
        file_names_all = get_all_file_name(root)  # 获取该目录下所有log文件名，返回的是一个列表
        if (len( file_names_all)) ==0:     # 判断文件夹下是否有待处理文件
            self.display3.setText("Error: Find no .log file!")
            QApplication.processEvents()
            return

        ProData = ProcessData()
        # 创建excel的数据输出结构（行名和列名），模块pandas
        list_statistical = [u'飞机ID', u'飞控ID', u'飞行时间(秒)', u'IMU1_陀螺', u'IMU2_陀螺', u'IMU3_陀螺', u'IMU1_加表', u'IMU2_加表',
                            u'IMU3_加表', u'磁罗盘1', u'磁罗盘2', u'磁罗盘3', u'GPS搜星', u'高度误差|DA-A|<0.2', u'RTK锁定后跳变次数']  # 统计生成表格
        pd_statistical = pd.DataFrame(columns=list_statistical, index=file_names_all)
        ProData.updateRoot(root, root_to_xls)
        tmptime1 = time.time()
        ProData.updateAllData(root,file_names_all)
        tmpdtime = time.time() - tmptime1
        print("文件读取时间：%.4s s" % tmpdtime)

        for x in file_names_all:
            ProData.updateAttrData(x)
            ProData.judgeSensor_and_print(pd_statistical, x)
            ProData.plt(x)
            self.display3.setText(x+",processed")
            QApplication.processEvents()
        dtime = time.time() - starttime
        print("运行时间为：%.4s s" % dtime)
        self.display3.setText("All Done! Success!运行时间：%.4s s" % dtime)

def get_all_file_name(root):  # 将目标文件夹下的所有待处理log文件名字取出
    file_names_all= []
    file_names_all_all = os.listdir(root)   #listdir是os的一个方法，列出当前目录下所有的文件列表。
    for x in file_names_all_all:     # x是取出log型文件
        if x[-3:] == 'log':
            file_names_all.append(x)
    return file_names_all          #log型文件列表

if __name__=="__main__":
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    mainForm = MainForm('QFYF_analyze V2.1')
    mainForm.show()
    sys.exit(app.exec_())
