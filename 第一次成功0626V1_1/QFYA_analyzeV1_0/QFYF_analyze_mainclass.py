# 2019-06-25 面向对象设计

import numpy as np
import matplotlib.pyplot as plt
import os
from PyQt5.QtWidgets import *
import multiprocessing           # 多进程处理模块


class ProcessData(object):
    def __init__(self):
        self.cwd = os.getcwd()  # 获取当前程序文件位置
        self.root = self.cwd
        self.root_to_xls = self.cwd
        self.x = []
        self.list_GPS_TimeUS = []
        self.list_GPS_NSats = []
        self.list_IMU_GyrZ_diff = []
        self.list_IMU_AccZ_diff = []
        self.list_MAG_MagZ_diff = []
        self.list_IMU2_GyrZ_diff= []
        self.list_IMU2_AccZ_diff = []
        self.list_IMU3_GyrZ_diff = []
        self.list_IMU3_AccZ_diff = []
        self.list_MAG2_MagZ_diff = []
        self.list_MAG3_MagZ_diff = []
        self.list_CTUN_A = []
        self.list_CTUN_DA = []
        self.list_CTUN_THO = []
        self.ACI_T4 = []
        self.ACI_T5 = []
        self.list_MKF1_ARD = []
        self.list_MKF1_TIMEUS = []
        self.list_RTK_SATS = []
        self.list_IMU_AccZ = []
        self.list_MAG_LENGTH = []
        self.dict_process_log = {}

    def load_log(self, filename):  # 载入日志文件,返回读取在内存的temp
        with open(filename, 'r') as file:  # with open 可以不用再close（） file
            temp_line = file.readlines()  # 采用readline()方式按行读进来，每行一个元素

        return temp_line
    def get_data_variable(self, temp_line):
        list_IMU_GyrZ = []
        list_IMU_AccZ = []
        list_IMU2_GyrZ = []
        list_IMU2_AccZ = []
        list_IMU3_GyrZ = []
        list_IMU3_AccZ = []
        list_MAG_MagZ = []
        list_MAG2_MagZ = []
        list_MAG3_MagZ = []
        list_GPS_NSats = []
        list_GPS_TimeUS = []
        list_CTUN_A = []
        list_CTUN_DA = []
        list_CTUN_THO = []
        list_ACI_T4 = []
        list_ACI_T5 = []
        list_MKF1_ARD = []
        list_MKF1_TIMEUS = []
        list_RTK_SATS = []
        list_MAG_MagX = []
        list_MAG_MagY = []
        for x in temp_line:
            if x[0:4] == 'GPS,':  # 查找gps
                list_temp_GPS = x[6:-1].split(',')  # 采用split函数分割该行字符串
                list_GPS_TimeUS.append(float(list_temp_GPS[0]))  # timeus为该行第1个元素
                list_GPS_NSats.append(float(list_temp_GPS[4]))  # nsats为该行第5个元素
            elif x[0:4] == 'IMU,':  # 查找imu
                list_temp_IMU = x[6:-1].split(',')  # 采用split函数分割该行字符串
                list_IMU_GyrZ.append(float(list_temp_IMU[3]))  # GYRZ为该行第4个元素
                list_IMU_AccZ.append(float(list_temp_IMU[6]))  # ACCZ为该行第7个元素
            elif x[0:4] == 'MAG,':  # 查找MAG
                list_temp_MAG = x[4:-1].split(',')  # 采用split函数分割该行字符串
                list_MAG_MagX.append(float(list_temp_MAG[1]))  # 第2个
                list_MAG_MagY.append(float(list_temp_MAG[2]))  # 第3个
                list_MAG_MagZ.append(float(list_temp_MAG[3]))  # 第四个
            elif x[0:4] == 'IMU2':  # 查找imu2
                list_temp_IMU2 = x[6:-1].split(',')  # 采用split函数分割该行字符串
                list_IMU2_GyrZ.append(float(list_temp_IMU2[3]))  # GYRZ为该行第4个元素
                list_IMU2_AccZ.append(float(list_temp_IMU2[6]))  # ACCZ为该行第7个元素
            elif x[0:4] == 'IMU3':  # 查找imu3
                list_temp_IMU3 = x[6:-1].split(',')  # 采用split函数分割该行字符串
                list_IMU3_GyrZ.append(float(list_temp_IMU3[3]))  # GYRZ为该行第4个元素
                list_IMU3_AccZ.append(float(list_temp_IMU3[6]))  # ACCZ为该行第7个元素
            elif x[0:4] == 'MAG2':  # 查找MAG2
                list_temp_MAG2 = x[4:-1].split(',')  # 采用split函数分割该行字符串
                list_MAG2_MagZ.append(float(list_temp_MAG2[3]))  # 第四个
            elif x[0:4] == 'MAG3':  # 查找MAG3
                list_temp_MAG3 = x[4:-1].split(',')  # 采用split函数分割该行字符串
                list_MAG3_MagZ.append(float(list_temp_MAG3[3]))  # 第四个
            elif x[0:4] == 'CTUN':  # 查找CTUN包中
                list_temp_CTUN = x[6:-1].split(',')  # 采用split函数分割该行字符串
                list_CTUN_A.append(float(list_temp_CTUN[6]))  # A为该行第7个元素
                list_CTUN_DA.append(float(list_temp_CTUN[5]))  # DA为该行第6个元素
                list_CTUN_THO.append(float(list_temp_CTUN[3]))  # THO为该行第4个元素
            elif x[0:4] == 'ACI,':  # 查找ACI包中
                list_temp_ACI = x[6:-1].split(',')  # 采用split函数分割该行字符串
                list_ACI_T4.append(float(list_temp_ACI[4]))  # T4为飞机编号
                list_ACI_T5.append(float(list_temp_ACI[5]))  # T5为飞控编号
            elif x[0:4] == 'MKF1':  # 查找MKF1包中
                list_temp_MKF1 = x[6:-1].split(',')  # 采用split函数分割该行字符串
                list_MKF1_ARD.append(float(list_temp_MKF1[9]))  # ARD为第十个
                list_MKF1_TIMEUS.append(float(list_temp_MKF1[0]))  # 时间戳
            elif x[0:4] == 'RTK,':  # 查找ACI包中
                list_temp_RTK = x[6:-1].split(',')  # 采用split函数分割该行字符串
                list_RTK_SATS.append(float(list_temp_RTK[4]))  # SATS为第5个
            else:
                continue
        return (list_GPS_TimeUS, list_GPS_NSats, list_IMU_GyrZ, \
        list_IMU_AccZ, list_MAG_MagX, list_MAG_MagY, list_MAG_MagZ, list_IMU2_GyrZ, \
        list_IMU2_AccZ, list_IMU3_GyrZ, list_IMU3_AccZ, list_MAG2_MagZ, list_MAG3_MagZ, list_CTUN_A, list_CTUN_DA, \
        list_CTUN_THO, list_ACI_T4, list_ACI_T5, \
        list_MKF1_ARD, list_MKF1_TIMEUS, list_RTK_SATS)
    def handle_one_log(self,root, x):
        file_name = root + '/' + x
        temp_line = self.load_log(file_name)  # 读取日志
        # 读取需要的变量的列表（调用get_data_variable函数）
        list_GPS_TimeUS, list_GPS_NSats, list_IMU_GyrZ, list_IMU_AccZ, list_MAG_MagX, list_MAG_MagY, list_MAG_MagZ, list_IMU2_GyrZ, list_IMU2_AccZ, list_IMU3_GyrZ, list_IMU3_AccZ, list_MAG2_MagZ, list_MAG3_MagZ, list_CTUN_A, list_CTUN_DA, list_CTUN_THO, list_ACI_T4, list_ACI_T5, list_MKF1_ARD, list_MKF1_TIMEUS, list_RTK_SATS = self.get_data_variable(temp_line)
        self.list_IMU_AccZ = np.array(list_IMU_AccZ)
        self.list_GPS_TimeUS = np.array(list_GPS_TimeUS)  # 创建数组
        self.list_GPS_NSats = np.array(list_GPS_NSats)
        self.list_IMU_GyrZ_diff = np.diff(np.array(list_IMU_GyrZ))  # diff是每行后面一个数减前面一个数
        self.list_IMU_AccZ_diff = np.diff(np.array(list_IMU_AccZ))
        self.list_MAG_MagZ_diff = np.diff(np.array(list_MAG_MagZ))
        self.list_IMU2_GyrZ_diff = np.diff(np.array(list_IMU2_GyrZ))
        self.list_IMU2_AccZ_diff = np.diff(np.array(list_IMU2_AccZ))
        self.list_IMU3_GyrZ_diff = np.diff(np.array(list_IMU3_GyrZ))
        self.list_IMU3_AccZ_diff = np.diff(np.array(list_IMU3_AccZ))
        self.list_MAG2_MagZ_diff = np.diff(np.array(list_MAG2_MagZ))
        self.list_MAG3_MagZ_diff = np.diff(np.array(list_MAG3_MagZ))
        self.list_MAG_LENGTH = np.sqrt(np.square(np.array(list_MAG_MagZ)) + np.square(np.array(list_MAG_MagX)) + np.square(
            np.array(list_MAG_MagY)))  # 地磁模长

        self.list_CTUN_A = np.array(list_CTUN_A)
        self.list_CTUN_DA = np.array(list_CTUN_DA)
        self.list_CTUN_THO = np.array(list_CTUN_THO)

        if len(list_ACI_T4) == 0:
            self.ACI_T4 = '未记录'
        else:
            self.ACI_T4 = list_ACI_T4[-1]  # 只需要一个字符就行

        if len(list_ACI_T5) == 0:
            self.ACI_T5 = '未记录'
        else:
            self.ACI_T5 = list_ACI_T5[-1]  # 只需要一个字符就行

        self.list_MKF1_ARD = np.array(list_MKF1_ARD)
        self.list_MKF1_TIMEUS = np.array(list_MKF1_TIMEUS)
        self.list_RTK_SATS = np.array(list_RTK_SATS)

        return (self.list_GPS_TimeUS, self.list_GPS_NSats, self.list_IMU_GyrZ_diff, self.list_IMU_AccZ_diff, self.list_MAG_MagZ_diff,
                self.list_IMU2_GyrZ_diff, self.list_IMU2_AccZ_diff, self.list_IMU3_GyrZ_diff, self.list_IMU3_AccZ_diff, self.list_MAG2_MagZ_diff,
                self.list_MAG3_MagZ_diff, self.list_CTUN_A, self.list_CTUN_DA, self.list_CTUN_THO, self.ACI_T4, self.ACI_T5, self.list_MKF1_ARD,
                self.list_MKF1_TIMEUS, self.list_RTK_SATS, self.list_IMU_AccZ, self.list_MAG_LENGTH)

    def updateAllData(self,root,file_names_all):
        # 运行一次便更新一次待处理的数据 处理次数根据files_name_all的大小 ,同时更新x的值 ，ACT4/5
        # multiprocessing.freeze_support()

        max_process = 8  # 最大进程数 因为是四核
        num_process = len(file_names_all)  # log文件个数
        if num_process > max_process: num_process = max_process  # pool里log文件个数不得超过最大进程数，如果超过了最大进程数，就按照最大进程数跑，多余进程的等待
        pool = multiprocessing.Pool(processes=num_process)  # 因为是四核，所以最大开了4*N个进程
        for x in file_names_all:  # 根据log的数量开进程数，
            # self.dict_process_log.setdefault('00000009.log', "123test")
            list_temp_process = pool.apply_async(self.handle_one_log, (root, x))
            self.dict_process_log.setdefault(x, list_temp_process.get())  # 将提取的数据和log文件名按照dict的形式存储 setdefalut方法见书p63
            self.dict_process_log.setdefault(x, "123test")
            list_temp_process = []  # 清空临时存储的列表

        pool.close()
        pool.join()

    def updateRoot(self,root,root_to_xls):
        self.root = root
        self.root_to_xls = root_to_xls

    def updateAttrData(self,x):
        (self.list_GPS_TimeUS, self.list_GPS_NSats, self.list_IMU_GyrZ_diff, self.list_IMU_AccZ_diff, self.list_MAG_MagZ_diff,
         self.list_IMU2_GyrZ_diff, self.list_IMU2_AccZ_diff, self.list_IMU3_GyrZ_diff, self.list_IMU3_AccZ_diff, self.list_MAG2_MagZ_diff,
         self.list_MAG3_MagZ_diff, self.list_CTUN_A, self.list_CTUN_DA, self.list_CTUN_THO, self.ACI_T4, self.ACI_T5, self.list_MKF1_ARD, self.list_MKF1_TIMEUS,
         self.list_RTK_SATS, self.list_IMU_AccZ, self.list_MAG_LENGTH) = self.dict_process_log[x]

    def judge_Continuous_zero(self,list1, num_zero):  # 判断list是否连续存在超过num_zero个0,布尔型 返回是否

        length = len(list1)

        flag = 'OK'
        count = 0
        for i in range(length):
            if abs(list1[i]) <= 0.000001:
                count = count + 1
            elif count > 0 and abs(list1[i]) > 0.000001:
                count = 0
            else:
                continue

            if count >= num_zero:  # 超过若干个数为0则代表连续为0
                flag = u'异常'  # 代表异常
                break

        if length == 0:
            flag = u'异常(无数据读入)'

        return flag
    def judge_gps_state(self,time_list1, nsats_list, num):  # 判断gps搜星是否正常  GPS包中 times变量>0的前提下， NSTATE变量>13 为正常，否则为不正常

        print('len(time_list1)', len(time_list1))
        time_list1 = time_list1[50:]  # 抛弃前50组数据，可能刚开机不稳定,5hz数据频率 即前10秒数据抛弃
        nsats_list = nsats_list[50:]
        print(len(time_list1))
        length = len(time_list1)
        flag = 'OK'
        for i in range(length):
            if nsats_list[i] < num:
                flag = u'异常(搜星数少)'

        if length == 0:
            flag = u'异常(无数据读入)'
        return flag
    def judge_height_error(self,DA_list, A_list, list_CTUN_THO):  # 判断在DA保持41帧不变的情况下，如果之后的da与a的误差大于0.2则异常
        length = len(DA_list)
        count = 0
        flag = 'OK'
        for i in range(length - 1):
            if DA_list[i] != 0 and abs(DA_list[i + 1] - DA_list[i]) < 0.00001:  # 不为零并保持不变，为了对不变帧数计数count
                count = count + 1
            elif abs(DA_list[i + 1] - DA_list[i]) > 0.00001:
                count = 0
            else:
                continue

            if count > 41:
                if DA_list[i] != 0 and list_CTUN_THO[i] > 0.1 and abs(DA_list[i] - A_list[i]) > 0.2:
                    flag = u'异常'
                else:
                    continue

        if length == 0:
            flag = u'异常(无数据读入)'
        return flag
    def cal_total_time(self,list1, list_time):
        time_second = 0.0
        flag = 0  # 状态标志  1代表正在记录时间  或者称为上一次状态  延迟状态
        length = len(list1)
        for i in range(length):
            if list1[i] == 1 and flag == 0:  # 代表从未解锁到解锁态  上升沿     当前值1 前一时刻0
                time_begin = list_time[i]
                flag = 1
            elif list1[i] == 0 and flag == 1:  # 代表从解锁到未解锁态  下降沿   当前值0  上一时刻1
                time_end = list_time[i - 1]
                time_second = time_second + time_end - time_begin
                flag = 0

        time_second = time_second / 1000000
        return time_second
    def cal_frequency(self,list1):
        length = len(list1)
        flag = 0  # 延后状态记录
        count = 0
        for i in range(length):
            if list1[i] == 4 and flag == 0:  # 从低电平到4
                flag = 1

            elif list1[i] != 4 and flag == 1:  # 从4到非4态
                count = count + 1
                flag = 0

        return count

    def judgeSensor_and_print(self,pd_statistical, x):
        # 判断imu异常
        flag_imu_gyro = self.judge_Continuous_zero(self.list_IMU_GyrZ_diff, 30)
        flag_imu_acc = self.judge_Continuous_zero(self.list_IMU_AccZ_diff, 30)
        flag_imu2_gyro = self.judge_Continuous_zero(self.list_IMU2_GyrZ_diff, 30)
        flag_imu2_acc = self.judge_Continuous_zero(self.list_IMU2_AccZ_diff, 30)
        flag_imu3_gyro = self.judge_Continuous_zero(self.list_IMU3_GyrZ_diff, 30)
        flag_imu3_acc = self.judge_Continuous_zero(self.list_IMU3_AccZ_diff, 30)
        # 判断磁传感器
        flag_mag1 = self.judge_Continuous_zero(self.list_MAG_MagZ_diff, 30)
        flag_mag2 = self.judge_Continuous_zero(self.list_MAG2_MagZ_diff, 30)
        flag_mag3 = self.judge_Continuous_zero(self.list_MAG3_MagZ_diff, 30)
        # 判断gps
        flag_gps = self.judge_gps_state(self.list_GPS_TimeUS, self.list_GPS_NSats, 13)
        # 判断减震 |DA-A|
        flag_da_a = self.judge_height_error(self.list_CTUN_DA, self.list_CTUN_A, self.list_CTUN_THO)
        # 计算ARD==1的时间

        # return (flag_imu_gyro, flag_imu_acc, flag_imu2_gyro, flag_imu2_acc, flag_imu3_gyro, flag_imu3_acc, flag_mag1, flag_mag2, flag_mag3, flag_gps, flag_da_a)
        time_second = self.cal_total_time(self.list_MKF1_ARD, self.list_MKF1_TIMEUS)  # 计算总的ADR高电平时间
        freq = self.cal_frequency(self.list_RTK_SATS)  # 统计RTK中SATS跳变次数
        # 根据行名和列名进行赋值
        pd_statistical.loc[x, '飞机ID'] = self.ACI_T4
        pd_statistical.loc[x, '飞控ID'] = self.ACI_T5
        pd_statistical.loc[x, '飞行时间(秒)'] = time_second
        pd_statistical.loc[x, 'RTK锁定后跳变次数'] = freq
        pd_statistical.loc[x, 'IMU1_陀螺'] = flag_imu_gyro
        pd_statistical.loc[x, 'IMU2_陀螺'] = flag_imu2_gyro
        pd_statistical.loc[x, 'IMU3_陀螺'] = flag_imu3_gyro
        pd_statistical.loc[x, 'IMU1_加表'] = flag_imu_acc
        pd_statistical.loc[x, 'IMU2_加表'] = flag_imu2_acc
        pd_statistical.loc[x, 'IMU3_加表'] = flag_imu3_acc
        pd_statistical.loc[x, '磁罗盘1'] = flag_mag1
        pd_statistical.loc[x, '磁罗盘2'] = flag_mag2
        pd_statistical.loc[x, '磁罗盘3'] = flag_mag3
        pd_statistical.loc[x, 'GPS搜星'] = flag_gps
        pd_statistical.loc[x, '高度误差|DA-A|<0.2'] = flag_da_a

        pd_statistical.to_excel(self.root_to_xls + '/' + 'log_analyze.xls')

    def plt(self,x):
        plt.figure(figsize=(20, 10))
        plt.subplot(221)
        plt.plot(self.list_CTUN_DA, label='CTUN_DA')
        plt.plot(self.list_CTUN_A, label='CTUN_A')
        plt.title(x)
        plt.xlabel(u'采样点数', fontproperties='SimHei', fontsize=14)
        plt.ylabel(u'米', fontproperties='SimHei', fontsize=14)
        plt.legend()
        plt.grid()

        plt.subplot(222)
        plt.plot(self.list_IMU_AccZ, label='IMU_ACCZ')
        # print(self.list_IMU_AccZ)
        plt.title(x)
        plt.xlabel(u'采样点数', fontproperties='SimHei', fontsize=14)
        plt.ylabel(u'ACCZ', fontproperties='SimHei', fontsize=14)
        plt.legend()
        plt.grid()

        plt.subplot(212)
        plt.plot(self.list_MAG_LENGTH, label='MAG_LENGTH')
        plt.title(x)
        plt.xlabel(u'采样点数', fontproperties='SimHei', fontsize=14)
        plt.ylabel(u'MAG', fontproperties='SimHei', fontsize=14)
        plt.legend()
        plt.grid()
        plt.savefig(self.root_to_xls + '/' + x + '.png', dpi=100)  # 将图片保存在输出目录下

def get_all_file_name(root):  # 将目标文件夹下的所有待处理log文件名字取出
    file_names_all= []
    file_names_all_all = os.listdir(root)   #listdir是os的一个方法，列出当前目录下所有的文件列表。
    for x in file_names_all_all:     # x是取出log型文件
        if x[-3:] == 'log':
            file_names_all.append(x)
    return file_names_all          #log型文件列表

# if __name__=='__main__':   #主函数入口
#
#     # app = QApplication(sys.argv)
#     # mainForm = MainForm('QFYF_test V1.0')
#     # mainForm.show()
#     # sys.exit(app.exec_())
#     # root, root_to_xls = mainForm.Loc_value()
#
#     root = input("输入待处理文件夹地址，如 C:/Users/zhangwenqi/Desktop/python_log/11：")
#     root_to_xls = input("输入输出文件夹地址，如 C:/Users/zhangwenqi/Desktop/python_log/test：")
#
#     # print(root_to_xls)
#     file_names_all = get_all_file_name(root)  # 获取该目录下所有log文件名，返回的是一个列表
#
#     ProData = ProcessData()
#
#     # 创建excel的数据输出结构（行名和列名），模块pandas
#     list_statistical = [u'飞机ID', u'飞控ID', u'飞行时间(秒)', u'IMU1_陀螺', u'IMU2_陀螺', u'IMU3_陀螺', u'IMU1_加表', u'IMU2_加表',
#                         u'IMU3_加表', u'磁罗盘1', u'磁罗盘2', u'磁罗盘3', u'GPS搜星', u'高度误差|DA-A|<0.2', u'RTK锁定后跳变次数']  # 统计生成表格
#     pd_statistical = pd.DataFrame(columns=list_statistical, index=file_names_all)
#
#     ProData.updateRoot(root,root_to_xls)
#     ProData.updateAllData(root,file_names_all)
#     for x in file_names_all:
#         ProData.updateAttrData(x)
#         ProData.judgeSensor_and_print(pd_statistical, x)
#         ProData.plt(x)


