from numba import jit,njit
import time

def get_data_variable(temp_line):
    dic = {'list_IMU_GyrZ':[],'list_IMU_AccZ':[],'list_IMU2_GyrZ':[],'list_IMU2_AccZ':[], \
           'list_IMU3_GyrZ': [],'list_IMU3_AccZ':[],'list_MAG_MagZ':[],'list_MAG2_MagZ':[],\
           'list_MAG3_MagZ':[], 'list_GPS_NSats':[],'list_GPS_TimeUS':[],'list_CTUN_A':[],\
           'list_CTUN_DA':[],'list_CTUN_THO':[],'list_ACI_T4':[], 'list_ACI_T5':[],\
           'list_MKF1_ARD':[],'list_MKF1_TIMEUS':[],'list_RTK_SATS':[],'list_MAG_MagX':[],\
           'list_MAG_MagY':[]}

    timetp1 =time.time()
    def fun1(x):
        list_temp_GPS = x[6:-1].split(',')  # 采用split函数分割该行字符串
        dic['list_GPS_TimeUS'].append(float(list_temp_GPS[0]))  # timeus为该行第1个元素
        dic['list_GPS_NSats'].append(float(list_temp_GPS[4]))  # nsats为该行第5个元素

    def fun2(x):
        list_temp_IMU = x[6:-1].split(',')  # 采用split函数分割该行字符串
        dic['list_IMU_GyrZ'].append(float(list_temp_IMU[3]))  # GYRZ为该行第4个元素
        dic['list_IMU_AccZ'].append(float(list_temp_IMU[6]))  # ACCZ为该行第7个元素

    def fun3(x):
        list_temp_MAG = x[4:-1].split(',')  # 采用split函数分割该行字符串
        dic['list_MAG_MagX'].append(float(list_temp_MAG[1]))  # 第2个
        dic['list_MAG_MagY'].append(float(list_temp_MAG[2]))  # 第3个
        dic['list_MAG_MagZ'].append(float(list_temp_MAG[3]))  # 第四个

    def fun4(x):
        list_temp_IMU2 = x[6:-1].split(',')  # 采用split函数分割该行字符串
        dic['list_IMU2_GyrZ'].append(float(list_temp_IMU2[3]))  # GYRZ为该行第4个元素
        dic['list_IMU2_AccZ'].append(float(list_temp_IMU2[6]))  # ACCZ为该行第7个元素

    def fun5(x):
        list_temp_IMU3 = x[6:-1].split(',')  # 采用split函数分割该行字符串
        dic['list_IMU3_GyrZ'].append(float(list_temp_IMU3[3]))  # GYRZ为该行第4个元素
        dic['list_IMU3_AccZ'].append(float(list_temp_IMU3[6]))  # ACCZ为该行第7个元素

    def fun6(x):
        list_temp_MAG2 = x[4:-1].split(',')  # 采用split函数分割该行字符串
        dic['list_MAG2_MagZ'].append(float(list_temp_MAG2[3]))  # 第四个

    def fun7(x):
        list_temp_MAG3 = x[4:-1].split(',')  # 采用split函数分割该行字符串
        dic['list_MAG3_MagZ'].append(float(list_temp_MAG3[3]))  # 第四个

    def fun8(x):
        list_temp_CTUN = x[6:-1].split(',')  # 采用split函数分割该行字符串
        dic['list_CTUN_A'].append(float(list_temp_CTUN[6]))  # A为该行第7个元素
        dic['list_CTUN_DA'].append(float(list_temp_CTUN[5]))  # DA为该行第6个元素
        dic['list_CTUN_THO'].append(float(list_temp_CTUN[3]))  # THO为该行第4个元素

    def fun9(x):
        list_temp_ACI = x[6:-1].split(',')  # 采用split函数分割该行字符串
        dic['list_ACI_T4'].append(float(list_temp_ACI[4]))  # T4为飞机编号
        dic['list_ACI_T5'].append(float(list_temp_ACI[5]))  # T5为飞控编号

    def fun10(x):
        list_temp_MKF1 = x[6:-1].split(',')  # 采用split函数分割该行字符串
        dic['list_MKF1_ARD'].append(float(list_temp_MKF1[9]))  # ARD为第十个
        dic['list_MKF1_TIMEUS'].append(float(list_temp_MKF1[0]))  # 时间戳

    def fun11(x):
        list_temp_RTK = x[6:-1].split(',')  # 采用split函数分割该行字符串
        dic['list_RTK_SATS'].append(float(list_temp_RTK[4]))  # SATS为第5个

    t_temp = time.time()
    for x in temp_line:

        tmpx = x[0:4]
        dic1 = {'GPS,': fun1, 'IMU,':fun2, 'MAG,':fun3, 'IMU2':fun4, 'IMU3': fun5, 'MAG2':fun6, 'MAG3':fun7, 'CTUN':fun8, 'ACI,':fun9, 'MKF1':fun10, 'RTK,':fun11}
        if dic1.get(tmpx):
            dic1.get(tmpx)(x)
    tmpx = (time.time()-t_temp)
    tmpl = len(temp_line)
    print(tmpx/tmpl)
    print("长度为：%.8s "%(len(temp_line)))
    print("单次时间为：%.8s s"% (tmpx/float(tmpl)))
    timetp2 = time.time()
    print("中间判断时间为：%.8s s" %(timetp2-timetp1))
    return dic
    # return (list_GPS_TimeUS, list_GPS_NSats, list_IMU_GyrZ, \
    #         list_IMU_AccZ, list_MAG_MagX, list_MAG_MagY, list_MAG_MagZ, list_IMU2_GyrZ, \
    #         list_IMU2_AccZ, list_IMU3_GyrZ, list_IMU3_AccZ, list_MAG2_MagZ, list_MAG3_MagZ, list_CTUN_A, list_CTUN_DA, \
    #         list_CTUN_THO, list_ACI_T4, list_ACI_T5, \
    #         list_MKF1_ARD, list_MKF1_TIMEUS, list_RTK_SATS)


def load_log( filename):  # 载入日志文件,返回读取在内存的temp
    with open(filename, 'r') as file:  # with open 可以不用再close（） file
        temp_line = file.readlines()  # 采用readline()方式按行读进来，每行一个元素
    return temp_line
root = "D:/test"
x = "00000008.log"
file_name = root + '/' + x
temp_line = load_log(file_name)

time1 = time.time()
get_data_variable(temp_line)
time2 =time.time()
print("chengxushijian  %.8s s" % (time2 - time1))

