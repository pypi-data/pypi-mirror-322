智窝助手sdk，包括以下功能：

1. 调用数据助手

2. 发送消息

    2.1 发送websocket消息

    2.2 发送钉钉webhook消息


3. 细节说明

ZhiwoAssistant有两个参数，一个是jep传递给main_function的param，必传；

一个是local，默认为True。如果设置为True，就会调用localhost:8080的服务，说明是在dev、test、uat、prod的本地调用本地。

如果设置为False，就会根据token调用不同环境的远程服务。

有三种远程服务：test、uat、prod，由param.authorization决定。param.authorization由代码传递给jep，或者点击助手编辑页的"获取凭证"获取。
