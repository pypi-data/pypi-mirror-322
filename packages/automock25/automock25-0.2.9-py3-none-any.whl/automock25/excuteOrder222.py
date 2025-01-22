
from DrissionPage._configs.chromium_options import ChromiumOptions
from DrissionPage import WebPage
import time
from datetime import datetime
import logset
import record
# 获取日志记录器
logger = logset.setup_logging()

#WebPage的 d 模式，行为与ChromiumPage一致，s 模式行为与SessionPage一致。

def charge(order_data):
    # 这里可以添加处理订单的逻辑
    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    order_data['chargetime'] =  formatted_time
    logger.info(f"Charging order: {order_data}")
    page = WebPage()
    page.get('https://shop.10086.cn/mall_210_210.html')

    elephone = page.ele('@name=phonenum')
    #print(elephone.text())
    if elephone:
        elephone.input(order_data['resdata']['mobile'])  # 原写法
        # elephone.set.attr('value', order_data['resdata']['mobile'])
    else:
        logger.info("手机号码框没找到.")
        return


    # 等待元素加载
    time.sleep(1)  # 等待2秒
    # 点击 元
    page.ele('tag:span@class=yuan_show toggle').click()
    # 等待页面加载
    #page.wait.load_start()


    #classamount ='home_firstscreen_'+str(order_data['resdata']['amount'])
    stramount = str(order_data['resdata']['amount'])+' 元'
    logger.info(stramount)

    elesa=page('tag:dd@class=yuan')
    elesa_arr=elesa.eles('tag:a')
    amountFlag = 0
    for c in elesa_arr:
        if c.text == stramount:
            c.click()  # 点击元素
            print(c.text + " --面值 clicked successfully.")
            amountFlag=1
            break
        else:
            logger.info("面值 not found."+c.text)
    #    print(c.text)
    if amountFlag==1:
        btnCharge=page('tag:a@url=https://shop.10086.cn/i/?f=rechargecredit')
        if btnCharge:
            btnCharge.click()
        else:
            logger.info("立即交费的按钮没找到.")
            return


    #amounttaga=elesa_c.ele('text:{stramount}')
    #print(amounttaga.text())
    order_data['status'] = '2'
    order_data['statusname'] = '充值成功'
    f_current_time = datetime.now()
    finishtime = current_time.strftime('%Y-%m-%d %H:%M:%S')
    order_data['finishtime'] = finishtime
    record.push_order(order_data)

    # 示例：假设需要根据订单数据进行某些操作
    # 例如：扣款、记录日志等
    # 这里暂时只打印订单数据
    # 实际应用中可以添加具体的业务逻辑
    return {"status": "success", "message": "Order charged successfully"}




