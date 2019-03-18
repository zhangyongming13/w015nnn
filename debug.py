from scrapy import cmdline
import os


os.chdir('./images')  # 切换到images目录
cmdline.execute("scrapy crawl 75aeae -s LOG_FILE=all.log".split())
#  -s LOG_FILE=all.log
