# 项目4_4_OSPFv3 动态路由实战 (零基础保姆级)

> **实验目标**：配置企业级主流的 OSPFv3 协议，实现中大型 IPv6 网络的高速自动寻路。
> **适用场景**：绝大多数企业内部网络。

---

## 一、 知识点大白话解析

> **1. 什么是 OSPFv3？**
> 它是 IPv4 版 OSPF (v2) 的升级版。之所以叫 v3，就是因为它专门服务于 IPv6。
>
> **2. 为什么还要配“Router ID”？它长得怎么像 IPv4？**
> 这是一个新手最容易困惑的点。虽然 OSPFv3 跑在 IPv6 上，但它依然需要一个 32 位的数字作为自己的“身份证”。
> **规则**：这个 ID 必须写成类似 `1.1.1.1` 的格式。它只是个代号，跟你的实际 IP 无关，但每台路由器的 ID 必须唯一。
>
> **3. 配置核心：接口使能**
> 跟 RIPng 类似，OSPFv3 不再在全局通过 `network` 命令宣告。你只需要进接口说一句：“这个接口归 OSPFv3 进程 1 管，它属于 Area 0 区域”。

---

## 二、 环境准备

### 1. 清理环境 (重要！)
如果你刚才做了 **项目 4_3 (RIPng)**，请务必删除配置。

**在 R1, R2, R3 上分别操作：**
```shell
<R1> system-view
[R1] undo ripng 1
# 如果你不确定接口下有没有残留，放心，全局删了 ripng 1，接口下的使能也就自动失效了。
```

---

## 三、 核心配置步骤 (开启高速自动导航)

### 1. R1 配置
```shell
<R1> system-view
[R1] ospfv3 1                 # 启动 OSPFv3 进程 1
[R1-ospfv3-1] router-id 1.1.1.1  # 【关键】手动配置身份证号
[R1-ospfv3-1] quit

# 进入连接 R2 的口，使能 OSPFv3 
[R1] interface GigabitEthernet 0/0/0
[R1-GigabitEthernet0/0/0] ospfv3 1 area 0   # 归进程1管，属于区域0

# 进入连接 PC1 的口，使能 OSPFv3 
[R1] interface GigabitEthernet 0/0/1
[R1-GigabitEthernet0/0/1] ospfv3 1 area 0
```

### 2. R2 配置
```shell
<R2> system-view
[R2] ospfv3 1
[R2-ospfv3-1] router-id 2.2.2.2
[R2-ospfv3-1] quit

[R2] interface GigabitEthernet 0/0/0
[R2-GigabitEthernet0/0/0] ospfv3 1 area 0

[R2] interface GigabitEthernet 0/0/1
[R2-GigabitEthernet0/0/1] ospfv3 1 area 0
```

### 3. R3 配置
```shell
<R3> system-view
[R3] ospfv3 1
[R3-ospfv3-1] router-id 3.3.3.3
[R3-ospfv3-1] quit

[R3] interface GigabitEthernet 0/0/0
[R3-GigabitEthernet0/0/0] ospfv3 1 area 0

[R3] interface GigabitEthernet 0/0/1
[R3-GigabitEthernet0/0/1] ospfv3 1 area 0
```

---

## 四、 验证与检查 (见证奇迹)

### 1. 检查邻居关系 (看有没有牵手成功)
在 R1 上输入：
`display ospfv3 peer`

*   **看什么？**：看 `State` (状态) 这一列。
*   **满分结果**：必须看到 **Full**。如果是 Init 或 2-Way，说明配置有问题或对方还没反应过来。

### 2. 查看 IPv6 路由表
在 R1 上输入：
`display ipv6 routing-table protocol ospfv3`

*   **期待结果**：你应该能看到通过 OSPFv3 学到的 `2001:2::/64` 网段。

### 3. 最终连通性大考
打开 **PC1** 命令行：
`ping 2001:2::1`

*   **期待结果**：Reply from ...

---

## 五、 新手避坑指南 (常见报错)

1.  **邻居起不来 (State 不是 Full)？**
    *   **检查 ID**：是不是两台路由器配了同一个 Router-ID？(比如都配了 1.1.1.1)。
    *   **检查区域**：是不是一边配了 area 0，另一边配了 area 1？同一根线两端的区域必须一致。
2.  **路由表学不到？**
    *   **检查接口使能**：看看是不是忘了在接 PC 的那个口（G0/0/1）下敲 `ospfv3 1 area 0`。如果你不敲，路由器就不会把这个网段告诉别人。
3.  **万能排错命令**：
    *   `display ospfv3 interface`：查看哪些接口正在运行 OSPFv3。