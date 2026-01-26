# 项目3实战：OSPF动态路由 (真正从零开始·详解版)

> **实验目标**：从一张白纸开始，搭建三路由器网络，让北京PC和广州PC自动互通。
> **适用人群**：零基础新手。

---

## 第一阶段：物理连接 (地基)

**1. 摆放设备**
*   **3台路由器** (AR2220)：拖出来，分别改名为 `R1`, `R2`, `R3`。
*   **2台电脑** (PC)：拖出来，分别改名为 `PC1`, `PC2`。

**2. 连线 (手动 Copper 线)**
*   **PC1** (Eth 0/0/1)  --> **R1** (GE 0/0/1)
*   **R1**  (GE 0/0/0)     --> **R2** (GE 0/0/0)
*   **R2**  (GE 0/0/1)     --> **R3** (GE 0/0/0)
*   **R3**  (GE 0/0/1)     --> **PC2** (Eth 0/0/1)

**3. 开机**
*   框选所有设备，右键 -> **启动**。

---

## 第二阶段：配置基础IP (缺失的关键步骤)

> **为什么要这一步？**
> 路由器就像快递站，如果它自己的各个大门（接口）都没有门牌号（IP），它是没法工作的。OSPF 必须建立在接口有 IP 的基础上。

### 1. 配置 PC
*   **PC1**: IP `192.168.10.1`, 掩码 `255.255.255.0`, 网关 `192.168.10.254`。
*   **PC2**: IP `192.168.20.1`, 掩码 `255.255.255.0`, 网关 `192.168.20.254`。
*   *记得点“应用”。*

### 2. 配置 R1 (北京) 的接口
```shell
<Huawei> system-view             # 进入管理员模式
[Huawei] sysname R1              # 改名

# 配置连接 PC1 的口
[R1] interface GigabitEthernet 0/0/1
[R1-GigabitEthernet0/0/1] ip address 192.168.10.254 24
[R1-GigabitEthernet0/0/1] undo shutdown   # 激活接口
[R1-GigabitEthernet0/0/1] quit

# 配置连接 R2 的口
[R1] interface GigabitEthernet 0/0/0
[R1-GigabitEthernet0/0/0] ip address 12.1.1.1 24
[R1-GigabitEthernet0/0/0] undo shutdown
[R1-GigabitEthernet0/0/0] quit
```

### 3. 配置 R2 (上海) 的接口
```shell
<Huawei> system-view
[Huawei] sysname R2

# 左手接 R1
[R2] interface GigabitEthernet 0/0/0
[R2-GigabitEthernet0/0/0] ip address 12.1.1.2 24
[R2-GigabitEthernet0/0/0] undo shutdown
[R2-GigabitEthernet0/0/0] quit

# 右手接 R3
[R2] interface GigabitEthernet 0/0/1
[R2-GigabitEthernet0/0/1] ip address 23.1.1.2 24
[R2-GigabitEthernet0/0/1] undo shutdown
[R2-GigabitEthernet0/0/1] quit
```

### 4. 配置 R3 (广州) 的接口
```shell
<Huawei> system-view
[Huawei] sysname R3

# 左手接 R2
[R3] interface GigabitEthernet 0/0/0
[R3-GigabitEthernet0/0/0] ip address 23.1.1.3 24
[R3-GigabitEthernet0/0/0] undo shutdown
[R3-GigabitEthernet0/0/0] quit

# 右手接 PC2
[R3] interface GigabitEthernet 0/0/1
[R3-GigabitEthernet0/0/1] ip address 192.168.20.254 24
[R3-GigabitEthernet0/0/1] undo shutdown
[R3-GigabitEthernet0/0/1] quit
```

> **阶段自测**：此时，在 PC1 命令行输入 `ping 192.168.10.254` 必须通。如果不通，不要往下做，先检查连线。

---

## 第三阶段：配置 OSPF (开启自动导航)

> **OSPF 原理解析**：
> *   **router-id**：给路由器起个唯一的身份证号，防止重名。
> *   **area 0**：OSPF把网络分区管理，**0区**是骨干区（老大哥），所有路由器建议先连入0区。
> *   **network**：意思是“我要把我的哪个网段拿出来共享”。
> *   **0.0.0.255**：这叫“反掩码”。
>     *   掩码 `255.255.255.0` 意思是：前3段必须一样，最后1段随意。
>     *   反掩码 `0.0.0.255` 意思是：前3段必须精确匹配（0），最后1段随意（255）。

### 1. 配置 R1 的 OSPF
R1 需要告诉大家：“我有 192.168.10.0 和 12.1.1.0 这两个网段”。

```shell
[R1] ospf 1 router-id 1.1.1.1            # 启动OSPF进程1，身份证号1.1.1.1
[R1-ospf-1] area 0                       # 进入骨干区域 0
[R1-ospf-1-area-0.0.0.0] network 192.168.10.0 0.0.0.255   # 宣告PC1网段
[R1-ospf-1-area-0.0.0.0] network 12.1.1.0 0.0.0.255       # 宣告R1-R2网段
```

### 2. 配置 R2 的 OSPF
R2 同样告诉大家：“我有 12.1.1.0 和 23.1.1.0 这两个网段”。

```shell
[R2] ospf 1 router-id 2.2.2.2
[R2-ospf-1] area 0
[R2-ospf-1-area-0.0.0.0] network 12.1.1.0 0.0.0.255
[R2-ospf-1-area-0.0.0.0] network 23.1.1.0 0.0.0.255
```
*   *提示：敲完这一步，稍微等几秒，系统会提示 `Adjacency State Change ... Full`，说明 R2 已经和 R1 连上了！*

### 3. 配置 R3 的 OSPF
R3 告诉大家：“我有 23.1.1.0 和 192.168.20.0 这两个网段”。

```shell
[R3] ospf 1 router-id 3.3.3.3
[R3-ospf-1] area 0
[R3-ospf-1-area-0.0.0.0] network 23.1.1.0 0.0.0.255
[R3-ospf-1-area-0.0.0.0] network 192.168.20.0 0.0.0.255
```

---

## 第四阶段：验证 (见证奇迹)

### 1. 验证路由表 (看看有没有自动学到路)
回到 **R1**，输入：
`display ip routing-table`

*   **看什么？**
    *   看 `Protocol` (协议) 那一列。
    *   找有没有 `OSPF`。
    *   最重要的是：找有没有去往 `192.168.20.0/24` 的路。
    *   *解释*：R1 本来只连着 10.0，如果它表里有了 20.0，说明它通过 OSPF 听到了 R3 的呼喊。

### 2. 验证连通性
打开 **PC1** 命令行：
`ping 192.168.20.1`

*   **预期结果**：
    *   前一两个包可能会 `Request timeout` (正在问路)。
    *   后面应该全是 `Reply from 192.168.20.1 ...`。

如果到这一步通了，您就成功完成了一个企业级的基础网络配置！