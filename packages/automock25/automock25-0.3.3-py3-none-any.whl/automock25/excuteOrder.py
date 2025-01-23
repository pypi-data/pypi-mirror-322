import json
from collections.abc import Sized

from DrissionPage._configs.chromium_options import ChromiumOptions
from DrissionPage import WebPage
import time
from datetime import datetime
import logset
import record
import threading
# 获取日志记录器
logger = logset.setup_logging()

htmlurl='file:///C:/Users/yf668/Desktop/11/11/%E7%BD%91%E5%8F%B0%E5%90%88%E4%B8%80%E8%90%A5%E4%B8%9A%E5%8E%85_jsp%23nogo.htm'
#htmlurl='http://nn.crm.gx.cmcc/index.jsp#nogo'
#WebPage的 d 模式，行为与ChromiumPage一致，s 模式行为与SessionPage一致。
def judgeLogin():
    #先判断  有没有登陆
    page = WebPage()
    page.get(htmlurl)
    #page.get('file:///C:/Users/yf668/Desktop/11/11/%E7%BD%91%E5%8F%B0%E5%90%88%E4%B8%80%E8%90%A5%E4%B8%9A%E5%8E%85_jsp%23nogo.htm')
    # 先判断有没有登录
    gonghaoUls = page.eles('tag=ul@class=ui-header-yg')

    if gonghaoUls :
        # 获取第一个 li 元素
        first_li = gonghaoUls[0]
        # 获取第一个 li 元素下的 a 标签
        a_tag = first_li('tag=a')
        if a_tag and a_tag.text.strip():
            print("已登录，第一个 li 元素的 a 标签文本为:", a_tag.text.strip())
            # 可以在这里添加其他操作
            return True
        else:
            print("未登录或第一个 li 元素的 a 标签文本为空")
            return False
    else:
        print("未登录或未找到 gonghaoUls 元素")
        return False

def chargeWithRetry(order_data):
    trycount =2
    for i in range(trycount):
        try:
            result = charge(order_data)
            if result['code'] == '1':
               notifySuccsess(order_data)
               break
            elif result['code'] == '0':

                if i == (trycount-1):  # 如果是第三次尝试且 code 为 0
                    logger.info(f" 重试三次没成功，推送失败吧: {order_data}")
                    order_data['msg']='重试两次失败'+result['msg']
                    notifyFail(order_data)

            else:
                logger.info(f"Retrying charge with order_data: {order_data}")
                time.sleep(3)  # 等待3秒后再次尝试
        except Exception as e:
            logger.error(f"Error in chargeWithRetry: {e}", exc_info=True)
            time.sleep(3)  #等待3秒后再次尝试

def charge(order_data):
    # 这里可以添加处理订单的逻辑

    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    order_data['chargetime'] =  formatted_time
    logger.info(f"Charging order: {order_data}")
    page = WebPage()
    page.get(htmlurl)
    #page.get( 'file:///C:/Users/yf668/Desktop/11/11/%E7%BD%91%E5%8F%B0%E5%90%88%E4%B8%80%E8%90%A5%E4%B8%9A%E5%8E%85_jsp%23nogo.htm')
    page.set.auto_handle_alert()  # 这之后出现的弹窗都会自动确认
    # 先判断有没有登录
    gonghaoUls = page.eles('tag=ul@class=ui-header-yg')

    if gonghaoUls :
        # 获取第一个 li 元素
        first_li = gonghaoUls[0]
        # 获取第一个 li 元素下的 a 标签
        a_tag = first_li('tag=a')
        if a_tag and a_tag.text.strip():
            logger.info("已登录，第一个 li 元素的 a 标签文本为:"+ a_tag.text.strip())
            # 可以在这里添加其他操作
        else:
            logger.info("未登录或第一个 li 元素的 a 标签文本为空")
            return  {'code':'0' ,'msg':'未登录或第一个 li 元素的 a 标签文本为空'}
    else:
        logger.info("未登录或未找到 gonghaoUls 元素")
        return {'code':'0', 'msg':'未登录或未找到 gonghaoUls 元素'}



    elephone = page.ele('#phoneNum')  #.kscz .kscz_dl  @name=phone_id
    #print(elephone.text())
    if elephone:
        elephone.input(order_data['resdata']['mobile'])  # 原写法
        # elephone.set.attr('value', order_data['resdata']['mobile'])
    else:
        logger.info("手机号码框没找到.")
        return {'code': '0', 'msg': '手机号码框没找到'}



    #classamount ='home_firstscreen_'+str(order_data['resdata']['amount'])
    stramount = str(order_data['resdata']['amount'])
    logger.info("要充值的金额："+stramount +"元")


    # 等待元素加载
    time.sleep(2)  # 等待2秒
    # 点击 元

    elesa = page('#PayFeeSelect')
    elesa_arr = elesa.eles('tag:a')
    amountFlag = 0
    for c in elesa_arr:
        if c.attr('data') == stramount:
            c.click()  # 点击元素
            print(c.text + " --面值 clicked successfully.")
            amountFlag = 1
            break
        else:
            logger.info("面值 not found." + c.text)


    # 等待页面加载
    #page.wait.load_start()
    eleamount=page('#pay_amount')
    logger.info("检验面值. 页面输入框中金额：" + eleamount.value)


    if amountFlag==1:
        btnCharge=page('#check_kscz1')
        if btnCharge:
            logger.info("点击 充值 按钮 ")
            btnCharge.click()
        else:
            logger.info("充值按钮没找到.")
            return {'code': '0', 'msg': '充值按钮没找到'}

   # 这里会有一个弹窗 点确定

    #/public/OperKsczAction/quickReChargeCheck.action 金额 的判断 。是否欠费
    #   //判断号码是否是4G用户
    #var url2 = _cp + '/public/OperKsczAction/queryBlackInfo.action';
    #// 判断是否为大流量副卡 - -start
    #url = _cp + '/public/OperKsczAction/getUserFamilyNetBxl.action';
    #/ public / OperKsczAction / chackLateMoney.action  违约金判断
    # '/public/OperKsczAction/paperlessPrint.action';    //当前欠费

    #public / OperKsczAction / quickReCharge.action   最终充值
    # 启动监听线程
    listen_start_time = time.time()
    max_duration = 5  # 监听最大时长为5秒
    msg=''

    def listen_for_charge_result():
        nonlocal chargeResult
        try:
            logger.info("开始监听.")
            page.listen.start('http://nn.crm.gx.cmcc/public/OperKsczAction/quickReCharge.action')  # 开始监听，指定获取包含该文本的数据包

            for packet in page.listen.steps():
                if time.time() - listen_start_time > max_duration:
                    break  # 超过最大时长，停止监听

                logger.info("监听中...")
                print(packet.url)  # 打印数据包url
                print(packet.response.body)  # 打印数据包url
                # 将body 解析成Json  判断 json中的code 是否为0
                try:
                    response_body = packet.response.body.decode('utf-8')  # 假设响应体是UTF-8编码的
                    json_data = json.loads(response_body)  # 解析为JSON
                    if json_data.get('code') == 0:
                        logger.info("拿 到监听结果 了 。推送结果 并停止监听 ")
                        print("拿 到监听结果 了 。推送结果 并停止监听 ")
                        chargeResult = True
                        break  # 退出循环
                    else:
                        logger.info(f"Code is {json_data.get('code')}, not successful.")
                        msg= '充值失败'+json_data.get('code')
                        print(f"Code is {json_data.get('code')}, not successful.")
                except json.JSONDecodeError:
                    logger.error("Failed to decode JSON from response body.")
                    print("Failed to decode JSON from response body.")
                except Exception as e:
                    logger.error(f"An error occurred: {e}")
                    print(f"An error occurred: {e}")

            page.listen.stop()  # 监听到想要的结果，立即停止监听
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            print(f"An error occurred: {e}")

        # 启动监听线程

    listen_thread = threading.Thread(target=listen_for_charge_result)
    listen_thread.start()

    # 等待监听线程结束或超时
    listen_thread.join(timeout=max_duration)

    if not listen_thread.is_alive():
        logger.info("监听线程已结束.")
    else:
        logger.info("监听线程超时，设置 chargeResult 为 False.")
        chargeResult = False


    if chargeResult:

        return {'code': '1', 'msg': '充值成功'}
    else:
        return {'code': '0', 'msg': msg if msg else '无监听数据'}

    # 示例：假设需要根据订单数据进行某些操作
    # 例如：扣款、记录日志等
    # 这里暂时只打印订单数据
    # 实际应用中可以添加具体的业务逻辑


def notifySuccsess(order_data):
    order_data['status'] = '2'
    order_data['statusname'] = '充值成功'
    f_current_time = datetime.now()
    f_current_time = datetime.now()
    finishtime = f_current_time.strftime('%Y-%m-%d %H:%M:%S')
    order_data['finishtime'] = finishtime
    record.push_order(order_data)

def notifyFail(order_data):
    order_data['status'] = '0'
    order_data['statusname'] = '充值失败'
    f_current_time = datetime.now()
    f_current_time = datetime.now()
    finishtime = f_current_time.strftime('%Y-%m-%d %H:%M:%S')
    order_data['finishtime'] = finishtime
    record.push_order(order_data)




