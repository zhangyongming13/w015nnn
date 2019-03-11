# w015nnn
Get_something

2019.03.05.23.18在middlewares和pipelines添加了利用redis存储已经爬取过的url，避免下次爬取时重复爬取的功能，做到增量爬取。

2019.03.10.10.53将位于middlewares和pipeline的利用redis进行增量爬取的功能移到Spider中，直接跳过已经爬取的资源，避免重复爬取。
