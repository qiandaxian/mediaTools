
## 中航讯多媒体小工具 
@author qiandaxian
--


资源文件夹助手
--
该功能依赖于离线资源包cictecMedia,主要实现了以下功能

- 媒体资源下载
- apk拷贝
- 离线包校验


485协议模拟助手
--
该功能通过读取线路.xml，解析xml生成对应的485信号的文本文件。目前支持的协议有

- 网智协议
- 西安协议

技术说明
--
- ui：pyqt5
- xml解析：xml.sax
- 其他：os，urllib3等

未完成
--
- 媒体文件校验码校验
- author文件校验
- lines.xml校验
- source.xml校验
- control.xml媒体id对应文件是否存在校验
- 线路文件校验