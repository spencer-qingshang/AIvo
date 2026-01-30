1. IPv6地址的基本配置

**识记：IPv6地址的优势；IPv6地址的报头结构。**
...
3. 全局开启：`ipv6`
4. 进入接口：`ipv6 enable`
5. 配置地址：`ipv6 address 2001::1 64`


2. 使用IPv6静态路由及默认路由实现网络连通

**识记：IPv6地址结构；IPv6地址类型；IPv6路由。**
...
*   **地址表达方式**：首选格式（全写）、压缩格式（省0）、内嵌IPv4格式。


3. 使用动态路由RIPng协议实现网络连通

**识记：RIPng；RIPng工作机制；RIPng报文格式。**
...
*   **命令区别**：
    *   RIPng配置：先全局进程 `ripng 1`，再进接口 `ripng 1 enable`。

4. 使用动态路由OSPFv3协议实现网络连通

**识记：OSPFv3基本概念；OSPFv3的报文；OSPFv3的LSA类型；OSPFv3的定时器。**
...
1. 配置 Router ID.
2. 全局开启 OSPFv3 进程.
3. **进接口绑定区域**：`ospfv3 1 area 0`.