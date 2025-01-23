from DataRecorder import Recorder
from datetime import datetime

def addData(data):
    recorder = Recorder('order.csv')
    orderno = data['resdata']['orderno']
    mobile =data['resdata']['mobile']
    province = data['resdata']['province']
    amount = data['resdata']['amount']
    orderTime = data['resdata']['orderTime']
    #status=1  #  充值中
    #statusname='充值中'
    status = data['status']
    statusname = data['statusname']
    pushstatus = data['pushstatus']
    pushtime = data['pushtime']
    # 获取当前时间
    chargetime = data['chargetime']

    finishtime = data['finishtime']


    #订单号,手机号,省份,金额,状态,状态,是否推送,订单时间,充值时间,完成时间,推送时间
    recorder.add_data((orderno,mobile,province,amount,status,statusname,pushstatus,orderTime,chargetime,finishtime,pushtime))
    recorder.record()




