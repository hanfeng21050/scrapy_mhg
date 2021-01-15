# scrapy_mhg
漫画柜漫画下载



### 前言

这是半年前学习pyton时所写的一个爬虫，纯属个人爱好。



### 使用方法

1. 修改setting.py中的图片保存地址和redis地址

   ```python
   REDIS_HOST = '4192.168.0.1'
   # 指定数据库的端口号
   REDIS_PORT = 6379
   # 没有密码则注释
   REDIS_PARAMS = {
       'password': '123',
   }
   
   # 自定义图片保存路径
   IMAGES_STORE = "E:\Python学习\image"
   ```

   

2. 打开项目路径，输入命令

   ```python
   scrapy crawl spider_pic_mhg
   ```

3. 连接redis， 输入命令

   ```
    ## url为漫画地址， 如  https://www.manhuagui.com/comic/7580/
    lpush mhg:start_urls <url>
   ```

4. 国内无法访问该网站或者访问很慢，请使用代理解决

5. 运行结果

   ![运行接口](https://coolmall-oss.oss-cn-hangzhou.aliyuncs.com/common/Snipaste_2021-01-15_17-42-17.png)

   