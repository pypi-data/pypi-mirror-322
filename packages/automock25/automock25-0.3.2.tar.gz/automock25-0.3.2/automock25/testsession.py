

from DrissionPage import SessionPage





def main():
    # 创建页面对象
    page = SessionPage()

    page.get('https://shop.10086.cn/mall_210_210.html')

    print(page.title)
    print(page.html)


if __name__ == '__main__':
    main()