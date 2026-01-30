# 项目4_4_OSPFv3动态路由实战 (超详细保姆级)

> **实验目标**：配置 OSPFv3 协议，实现企业级的高效路由。
> **前置条件**：完成项目 4_1 的 IP 配置。

---

## 一、 清理 RIPng 配置 (必做)

> **说明**：为了避免 RIPng 干扰，我们需要先关闭它。

### 1. 删除所有路由器的 RIPng 进程
```shell
# R1
<R1> system-view
[R1] undo ripng 1   # 只要删了全局进程，接口下的配置会自动消失

# R2
<R2> system-view
[R2] undo ripng 1

# R3
<R3> system-view
[R3] undo ripng 1
```
*操作完后，建议输入 `display this` 确认配置已干净。*

---

## 二、 配置 OSPFv3 协议 (核心部分)

> **核心逻辑**：三步走。1.开进程 -> 2.配 Router-ID (必配!) -> 3.进接口绑定区域。

### 1. 配置路由器 R1
```shell
<R1> system-view
# 第一步：启动 OSPFv3 进程
[R1] ospfv3 1

# 第二步：配置 Router-ID (这是OSPFv3启动的必要条件)
# 注意：格式必须是 x.x.x.x，虽然是 IPv6 环境，但 ID 依然长得像 IPv4
[R1-ospfv3-1] router-id 1.1.1.1
[R1-ospfv3-1] quit

# 第三步：接口绑定区域 (所有接口都划入骨干区域 Area 0)
[R1] interface GigabitEthernet 0/0/0
[R1-GigabitEthernet0/0/0] ospfv3 1 area 0  # 【关键】绑定到区域0
[R1-GigabitEthernet0/0/0] quit

[R1] interface GigabitEthernet 0/0/1
[R1-GigabitEthernet0/0/1] ospfv3 1 area 0  # 【必做】PC口也要宣告
[R1-GigabitEthernet0/0/1] quit
```

### 2. 配置路由器 R2
```shell
<R2> system-view
[R2] ospfv3 1
[R2-ospfv3-1] router-id 2.2.2.2  # ID 不能和 R1 相同
[R2-ospfv3-1] quit

# 两个接口都配
[R2] interface GigabitEthernet 0/0/0
[R2-GigabitEthernet0/0/0] ospfv3 1 area 0
[R2-GigabitEthernet0/0/0] quit

[R2] interface GigabitEthernet 0/0/1
[R2-GigabitEthernet0/0/1] ospfv3 1 area 0
[R2-GigabitEthernet0/0/1] quit
```

### 3. 配置路由器 R3
```shell
<R3> system-view
[R3] ospfv3 1
[R3-ospfv3-1] router-id 3.3.3.3  # ID 唯一
[R3-ospfv3-1] quit

# 两个接口都配
[R3] interface GigabitEthernet 0/0/0
[R3-GigabitEthernet0/0/0] ospfv3 1 area 0
[R3-GigabitEthernet0/0/0] quit

[R3] interface GigabitEthernet 0/0/1
[R3-GigabitEthernet0/0/1] ospfv3 1 area 0
[R3-GigabitEthernet0/0/1] quit
```

---

## 三、 验证与深度排错

### 1. 检查邻居状态 (最关键的一步)
在 R1 上输入：
`display ospfv3 peer`

*   **观察**：找到 `State` 这一列。
*   **满分**：显示 **Full** (表示完全同步)。
*   **不及格**：
    *   **Init**：我发了 Hello 包，但还没收到对方的回复。
    *   **2-Way**：建立了双向通信，但还没开始交换路由信息。
    *   **Down**：完全不通。

### 2. 检查路由表
在 R1 上输入：
`display ipv6 routing-table protocol ospfv3`

*   应该能看到 `2001:2::/64`。

### 3. Ping 测试
PC1 Ping PC2：`ping 2001:2::1` -> 通！

### 4. 常见坑点 CheckList
*   **坑1：Router-ID 没配或配重了**
    *   如果不配 Router-ID，OSPFv3 进程根本起不来。
    *   如果 R1 和 R2 都配了 1.1.1.1，它俩会打架，邻居建不起来。
*   **坑2：区域 ID 不一致**
    *   R1 的接口配了 area 0，R2 的接口配了 area 1，它俩就“语言不通”，无法建立邻居。
*   **坑3：PC 口没宣告**
    *   如果 R1 的 G0/0/1 (接 PC1 的口) 没敲 `ospfv3 1 area 0`，虽然 R1 和 R2 邻居正常，但 PC2 永远 ping 不通 PC1，因为 R2 根本不知道 PC1 在哪。
