from DrissionPage import ChromiumPage

page = ChromiumPage()

page.listen.start('https://shop.10086.cn/i/v1/cust/orderlistqry')  # 开始监听，指定获取包含该文本的数据包


page.get('https://shop.10086.cn/i/?f=rechargecredit')
#print(page.mode)
#page.change_mode()


page.ele("#rechargerecord").click()

for packet in page.listen.steps():
    print(packet.url)  # 打印数据包url
    print(packet.response.body)  # 打印数据包url
    #print(packet.response.body.data.outParam)  # 打印数据包url
    #page.run_js("")

    #page('@rel=next').click()  # 点击下一页

page.wait.load_start()  # 等待页面进入加载状态
print(page.html)  # 打印数据包url


#page.get('https://shop.10086.cn/i/apps/serviceapps/chargerecord/index.html')
# print(page.mode)
# print(page.html)


# for packet in page.listen.steps():
#     print(packet.url)  # 打印数据包url
#     page('@rel=next').click()  # 点击下一页
#     i += 1
#     if i == 5:
#         break

#
# page = ChromiumPage()
#
# page.get('https://gitee.com/explore/all')  # 访问网址
#
# i = 0
# for packet in page.listen.steps():
#     print(packet.url)  # 打印数据包url
#     page('@rel=next').click()  # 点击下一页
#     i += 1
#     if i == 5:
#         break

#https://shop.10086.cn/i/v1/cust/orderlistqry