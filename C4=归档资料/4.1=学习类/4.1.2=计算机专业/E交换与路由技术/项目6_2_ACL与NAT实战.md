# 项目6-2：路由器流量控制与NAT实战手册

> **核心目标**：用 ACL 禁止某个部门上网，用 NAT 让全公司通过一个公网 IP 上网。
> **场景**：AR1 是公司出口路由器，连接内网和互联网（ISP）。

---

## 一、 环境准备 (手把手搭拓扑)

### 1. 拖动设备
*   **路由器 (Router)**：选择 **AR2220**，拖入 2 台。
    *   第一台重命名为 `AR1` (公司出口)。
    *   第二台重命名为 `ISP` (模拟互联网)。
*   **交换机 (Switch)**：选择 **S3700**，拖入 1 台，作为内网接入（不需配置，仅作傻瓜交换机用）。
*   **终端 (PC)**：拖入 2 台，重命名为 `PC1` 和 `PC2`。

### 2. 物理连线
使用 **Copper (铜轴线)**：
*   **PC1** 连 **S3700** 的 `Eth 0/0/1`。
*   **PC2** 连 **S3700** 的 `Eth 0/0/2`。
*   **S3700** 的 `Eth 0/0/3` 连 **AR1** 的 `GE 0/0/0` (内网口)。
*   **AR1** 的 `GE 0/0/1` (外网口) 连 **ISP** 的 `GE 0/0/0`。

### 3. 开机与IP配置
*   **PC1**: IP `192.168.1.10`, 网关 `192.168.1.254`。
*   **PC2**: IP `192.168.1.20`, 网关 `192.168.1.254`。
*   **ISP**: 
    ```shell
    [ISP] interface g0/0/0
    [ISP-g0/0/0] ip address 202.100.1.2 24
    ```

### 4. 规划表
| 设备 | 接口 | IP地址 | 说明 |
| :--- | :--- | :--- | :--- |
| **AR1** | GE 0/0/0 | 192.168.1.254/24 | 内网网关 |
| **AR1** | GE 0/0/1 | 202.100.1.1/24 | 公网接口 |
| **ISP** | GE 0/0/0 | 202.100.1.2/24 | 运营商对端 |

---

## 二、 ACL 实战 (门禁卡升级版)

### 1. 基础 ACL 2000 (一刀切：禁止某人上网)
```shell
[AR1] acl 2000
[AR1-acl-basic-2000] rule deny source 192.168.1.20 0
# 大白话：PC2 (192.168.1.20) 被拉黑了，啥也干不了。
[AR1-acl-basic-2000] rule permit source any
[AR1-acl-basic-2000] quit
```

### 2. 高级 ACL 3000 (精细化：只禁 Ping，允许别的)
> **进阶挑战**：如果我们只想禁止 PC1 Ping 通外网，但允许它正常上网浏览网页，该怎么办？
```shell
[AR1] acl 3000
[AR1-acl-adv-3000] rule deny icmp source 192.168.1.10 0 destination any
# 大白话：禁止 PC1 发出的 ICMP (Ping) 包去往任何地方。
[AR1-acl-adv-3000] rule permit ip source any destination any
# 大白话：放行其他所有 IP 流量（包括 TCP/UDP 等）。
[AR1-acl-adv-3000] quit
```

### 3. 应用 ACL (二选一)
**注意**：一个接口的一个方向只能应用一个 ACL。如果你想试 ACL 3000，需要先删掉 ACL 2000 的配置。
```shell
# 先清除之前的配置（如果有）
[AR1] interface g0/0/0
[AR1-GigabitEthernet0/0/0] undo traffic-filter inbound

# 应用高级 ACL 3000
[AR1-GigabitEthernet0/0/0] traffic-filter inbound acl 3000
```

---

## 三、 NAT 实战 (Easy-IP 伪装术)

### 1. 定义允许 NAT 的流量 (ACL)
```shell
[AR1] acl 2001
[AR1-acl-basic-2001] rule permit source 192.168.1.0 0.0.0.255
# 大白话：定义一张白名单，允许 192.168.1.X 网段的所有人做 NAT 转换。
[AR1-acl-basic-2001] quit
```

### 2. 配置 Easy-IP (出海口)
```shell
[AR1] interface g0/0/1
[AR1-GigabitEthernet0/0/1] nat outbound 2001
# 大白话：在这个公网接口上开启 NAT。只要是 ACL 2001 里的人想出去，统统把源 IP 换成这个接口的公网 IP (202.100.1.1)。
```

### 3. 配置默认路由 (指路牌)
```shell
[AR1] ip route-static 0.0.0.0 0 202.100.1.2
# 大白话：所有要去互联网的数据包，都扔给 ISP (202.100.1.2)。
```

---

## 四、 验证 (拿出证据)

### 1. ACL 验证 (以 ACL 3000 为例)
*   **PC1 ping 202.100.1.2** -> **不通** (Request timeout)。
    *   *原因*：命中 rule deny icmp。
*   **PC1 访问 HTTP 服务** (如果 ISP 开启了 HTTP Server) -> **能通**。
    *   *说明*：只禁了 Ping，没禁别的。

### 2. NAT 验证 (抓包实锤)
这是最关键的一步，证明 NAT 真的生效了：
1.  **开启抓包**：右键点击 ISP 的 `GE 0/0/0` 接口，选择 **Start Capture (开始抓包)**。
2.  **产生流量**：让 PC2 (或未被禁 Ping 的 PC) 去 `ping 202.100.1.2`。
3.  **观察 Wireshark**：
    *   在 Wireshark 过滤器栏输入 `icmp`。
    *   查看 **Source (源地址)** 列。
    *   **成功标志**：你应该看到源 IP 是 **202.100.1.1** (AR1 的外网口地址)，**绝对不能**是 192.168.1.20。
    *   *原理*：NAT 把私网 IP 偷梁换柱成了公网 IP。

### 3. 专业命令查看
```shell
[AR1] display nat session all
# 结果示例：
# NAT Session Table Information:
# Protocol          : ICMP(1)
# SrcAddr   Port    : 192.168.1.20   256   <--- 内网真实 IP
# DestAddr  Port    : 202.100.1.2    256
# NAT-Info
#   New SrcAddr     : 202.100.1.1    <--- 转换后的公网 IP
```

---

## 五、 保存配置 (必做!)

**AR1 和 ISP 都要保存**：
```shell
<AR1> save
<ISP> save
```