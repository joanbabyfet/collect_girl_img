from bs4 import BeautifulSoup
import requests
import sys
import time
import os

class collect:
    '处理采集业务'
    def __init__(self, config, header, img_header):
        self.config     = config
        self.header     = header
        self.img_header = img_header

    # 采集妹子图片
    def mzitu(self, number):
        if number == '': number = 1

        total_count     = 1
        for id, name in self.config['category'].items():
            for page in range(1, int(number) + 1): # 深度爬取几页
                url = '%s%s/page/%s/' % (self.config['base_url'], id, str(page))
                resp = requests.get(url, headers = self.header)
                resp.encoding = 'utf-8' # 使用与网页相对应的编码格式, 避免乱码
                soup = BeautifulSoup(resp.text, 'html.parser') # 通过html dom解析器采集数据
                list_range = self.config['list'][id]['range']
                list_rules = self.config['list'][id]['rules']['thumb']
                imgs = soup.select(list_range)

                sn = 1
                for img in imgs:
                    self.get_remote_image(img[list_rules], id, str(page), str(sn)) # 获取大图
                    print("【正在下载】 {%s}第%d页第%d张图片, 共下载了%d张图片" % (name, page, sn, total_count))
                    sn += 1
                    total_count += 1

    # 获取图片名称
    def get_image_name(self, page, sn):
        filename = page + '_' + sn + '.jpg' # 页码_序号.jpg
        return filename

    # 将远程图片下载至本地
    def get_remote_image(self, img_url, dir = '', page = '', sn = ''):
        filename = self.get_image_name(page, sn)

        if dir == '':
            upload_dir = sys.path[0] + '\\src\\' # 本地绝对路径
        else:
            upload_dir = sys.path[0] + '\\src\\' + dir + '\\'
        
        if os.path.exists(upload_dir) == False: # 不存在则创建
            os.mkdir(upload_dir)

        resp = requests.get(img_url, headers = self.img_header)
        with open(upload_dir + filename, 'wb') as f:
            f.write(resp.content) # 获取图片二进制格式(数据流)

def main():
    header = { # 访问主页请求头
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'Hm_lvt_35913bd1337af2e18096896fa8d667a9=' + str(int(time.time())) + '; Hm_lpvt_35913bd1337af2e18096896fa8d667a9=' + str(int(time.time())),
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
    img_header = { # 访问图片请求头
        'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'referer': 'https://mmzztt.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
    config = { # 配置
        'base_url': 'https://mmzztt.com/',
        'category': {
            'photo': '写真馆',
        },
        'list': {
            'photo': {
                'range': '.u-thumb-v img',
                'rules': {
                    'thumb': 'data-srcset'
                },
                'page_size': '24' # 每页展示几条
            }
        }
    }
    # 运行采集
    number = input('请输入采集页数:')
    collect(config, header, img_header).mzitu(number)

if __name__ == '__main__': # 主入口
    main()