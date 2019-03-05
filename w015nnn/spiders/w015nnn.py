import scrapy, time, random, threading, requests
from w015nnn.items import W015NnnItem
from w015nnn.settings import DEFAULT_REQUEST_HEADERS


url = ['http://www.75aeae.com/artlist/23.html']


class MyThread(threading.Thread):  # 类继承多线程的方法threading.Thread，并加入返回数据的方法
    def __init__(self, func, args):
        threading.Thread.__init__(self)
        # self.name = name
        self.func = func
        self.args = args
        self.result = self.func(*self.args)  # 接收函数返回的数据

    def get_result(self):
        try:
            return self.result  # 返回结果
        except Exception:
            return None


class W015nnn(scrapy.Spider):
    name = '75aeae'
    start_urls = ['http://www.75aeae.com/artlist/23.html']
    url_init = 'http://www.75aeae.com'
    next = '下一页'

    def parse(self, response):
        data = response.xpath("//div[@class='atrlist']/ul")
        for each in data:  # 得到链接内所有帖子的链接和名字
            item = W015NnnItem()
            item['tiezi_name'] = each.xpath("./li[@class='name']/a/text()").extract()[0]
            item['tiezi_date'] = each.xpath("./li[@class='time']/font/text() | ./li[@class='time']/text()").extract()[0]
            item['tiezi_link'] = self.url_init + each.xpath("./li[@class='name']/a/@href").extract()[0]
            time.sleep(8 + random.randint(2, 5))
            tiezi_data = scrapy.Request(item['tiezi_link'], meta={'item': item}, callback=self.get_tupian_link)
            yield tiezi_data  # 提交数据到具体函数
        # 判断下一页
        flag = response.xpath("//div[@class='vodbox']/div[@class='page']/a/text()").extract()[-2]
        if flag == self.next:
            next_page = response.xpath("//div[@class='vodbox']/div[@class='page']/a/@href").extract()[-2]
            url = self.url_init + next_page
            time.sleep(10 + random.randint(12, 82) / 10)
            yield scrapy.Request(url, callback=self.parse)
        else:
            print('爬取完毕！')

    def get_tupian_link(self, tiezi_data):
        item = tiezi_data.meta['item']
        tupian_link = []
        all_tupian_link = tiezi_data.xpath("//div[@class='artbody']/div[@class='cont']/center/div[@id='postmessage']/img")
        for each in all_tupian_link:
            link = each.xpath("./@src").extract()[0]
            tupian_link.append(link)
        item['tupian_link'] = tupian_link
        tupian_data = []
        start_time = time.time()
        self.threding_for_get_tupiandata(item['tiezi_name'], item['tiezi_link'], item['tupian_link'], tupian_data)
        # self.get_tupian_data(item['tiezi_name'], item['tiezi_link'], item['tupian_link'], tupian_data)
        print(time.time() - start_time)
        item['tupian_data'] = tupian_data
        yield item

    def get_tupian_data(self, tiezi_name, tiezi_link, tupian_link, tupian_data):
        print('正在爬取帖子： %s 的图片!!!' % tiezi_name)
        num = 0
        for each in tupian_link:
            num = num + 1
            header = DEFAULT_REQUEST_HEADERS
            header['Referer'] = tiezi_link
            # proxy = random.choice(ip_list)
            try:
                req = requests.get(each, headers=header, timeout=30)
                # print(req.text)
                if req.content:
                    tupian_data.append(req.content)
                print('第%d张图片爬取成功' % num)
            except:
                print('第%d张图片爬取不成功' % num)

    def threding_for_get_tupiandata(self, tiezi_name, tiezi_link, tupian_link, tupian_data):  # 多线程爬取图片
        print('正在爬取帖子： %s 的图片!!!' % tiezi_name)
        tupian_link_range = range(len(tupian_link))
        # 第一种多线程，为list里面的每一个dict元素创建一个进程，这样的做法导致了创建太多的进程
        # 导致验证IP地址所耗费的时间比单线程的还低 大概在17秒，如果减少for循环，这样可以降低到10秒左右
        threads = []
        for i in tupian_link_range:
            # zhang = tupian_link[i]
            t = MyThread(self.get_tupian_data_requests, (tupian_link[i], tiezi_link))
            threads.append(t)
            t.start()
        [t.join() for t in threads]
        number = 1
        for t in threads:
            result = t.get_result()
            if result != None:
                print('第%s张图片爬取完毕' % number)
                number = number + 1
                tupian_data.append(result)
                # print(result)
                # with open('1.jpg', 'wb') as f:
                #     f.write(result)
            else:
                pass

    def get_tupian_data_requests(self, tupian_link, tiezi_link):
        header = DEFAULT_REQUEST_HEADERS
        header['Referer'] = tiezi_link
        # proxy = random.choice(ip_list)
        try:
            req = requests.get(tupian_link, headers=header, timeout=30)
            # print(req.text)
            if req.content:
                return req.content
            else:
                pass
        except Exception as e:
            print(e)
