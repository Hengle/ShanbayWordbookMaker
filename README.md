# ShanbayWordbookMaker

## extract

extract.py 可以用来提取单词，将所有文章保存为 txt 文件，运行脚本就可以将内容去重整理到 Total.log 中。

## submit

submit.py 用来上传单词，会正确地根据单元中 200 个单词的上限进行分隔单元。

## 自定义

脚本中有很多地方需要改，首先需要获得自己的 Cookie，使用浏览器登录后打开开发者工具即可查找到。
其次需要先手动创建单词本，记录下对应的 ID 并修改 submit.py 中对应代码。