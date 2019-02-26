# 字体解析器font_parser
    爬虫字体反扒处理器，包含（不限于）快手PC、头条PC端字体反扒处理
# 程序结构
    font_parser/
        config/
            setting.py配置文件
        parser/
            font_parser.py字体解析器父类
            kuaishou_font_parser.py快手字体解析器实现类
            maoyan_font_parser.py猫眼PC端字体解析器实现类
        web/
            processer.py 启动类，flask web处理器
        Dockerfile Docker
    
# 使用说明Usage
  **URL:** http://ip:port/process
  
  **Http Method:** POST
  
  **Headers:** 
  
        Content-Type: application/json
  **params:**
``` json        
        {  
          "channel" : "maoyan",
          "font_url" : "https://vfile.meituan.net/colorstone/2a9eb2852b2dee19c7720dae4a35c85f2076.woff",
          "data":"&#xe0b7;&#xe0b7;&#xf6ca;&#xe032;&#xe032;&#xf6ca;"
        }
``` 

``` json        
        {
          "channel" : "kuaishou",
          "font_url" : "https://static.yximgs.com/udata/pkg/kuaishou-front-end-live/fontscn_h57yip2q.ttf",
          "data":"붪.곭w"
        }
```          
