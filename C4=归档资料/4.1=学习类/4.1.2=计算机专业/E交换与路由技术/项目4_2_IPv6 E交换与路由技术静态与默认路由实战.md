# 项目4_2_IPv6静态与默认路由实战 (独立完整版)

> **实验目标**：在全新的拓扑中，通过配置 IPv6 静态路由，打通全网。
> **适用场景**：从零开始的新实验，不依赖任何之前的配置。

---

## 一、 物理连线与基础环境 (从零开始)

### 1. 摆放与连线
1.  新建拓扑，拖出 **3台 AR2220** (`R1`, `R2`, `R3`) 和 **2台 PC** (`PC1`, `PC2`)。
2.  **手动连线** (使用黑色实线 Copper)：
    *   `PC1 (E0/0/1)` <---> `R1 (G0/0/1)`
    *   `R1 (G0/0/0)` <---> `R2 (G0/0/0)`
    *   `R2 (G0/0/1)` <---> `R3 (G0/0/0)`
    *   `R3 (G0/0/1)` <---> `PC2 (E0/0/1)`
3.  **开启设备**：框选所有设备，点击启动，等待接口变绿。

---

## 二、 基础 IP 地址配置 (必做铺垫)

> **说明**：在配路由之前，必须先配好接口 IP。以下是完整的初始化命令。

### 1. 配置 R1 基础 IP
```shell
<Huawei> system-view
[Huawei] sysname R1
[R1] ipv6                                    # 全局开启 IPv6
[R1] interface GigabitEthernet 0/0/1         # 连接 PC1
[R1-GigabitEthernet0/0/1] ipv6 enable
[R1-GigabitEthernet0/0/1] ipv6 address 2001:1::254 64
[R1-GigabitEthernet0/0/1] quit
[R1] interface GigabitEthernet 0/0/0         # 连接 R2
[R1-GigabitEthernet0/0/0] ipv6 enable
[R1-GigabitEthernet0/0/0] ipv6 address 2001:12::1 64
[R1-GigabitEthernet0/0/0] quit
```

### 2. 配置 R2 基础 IP
```shell
<Huawei> system-view
[Huawei] sysname R2
[R2] ipv6
[R2] interface GigabitEthernet 0/0/0         # 连接 R1
[R2-GigabitEthernet0/0/0] ipv6 enable
[R2-GigabitEthernet0/0/0] ipv6 address 2001:12::2 64
[R2-GigabitEthernet0/0/0] quit
[R2] interface GigabitEthernet 0/0/1         # 连接 R3
[R2-GigabitEthernet0/0/1] ipv6 enable
[R2-GigabitEthernet0/0/1] ipv6 address 2001:23::2 64
[R2-GigabitEthernet0/0/1] quit
```

### 3. 配置 R3 基础 IP
```shell
<Huawei> system-view
[Huawei] sysname R3
[R3] ipv6
[R3] interface GigabitEthernet 0/0/0         # 连接 R2
[R3-GigabitEthernet0/0/0] ipv6 enable
[R3-GigabitEthernet0/0/0] ipv6 address 2001:23::3 64
[R3-GigabitEthernet0/0/0] quit
[R3] interface GigabitEthernet 0/0/1         # 连接 PC2
[R3-GigabitEthernet0/0/1] ipv6 enable
[R3-GigabitEthernet0/0/1] ipv6 address 2001:2::254 64
[R3-GigabitEthernet0/0/1] quit
```

### 4. 配置 PC IP
*   **PC1**：IP `2001:1::1` / 64，网关 `2001:1::254`。点应用。
*   **PC2**：IP `2001:2::1` / 64，网关 `2001:2::254`。点应用。

---

## 三、 核心：配置静态路由 (本实验重点)

### 1. 配置 R1 (指明去往 2.0 网段的路)
```shell
# 去往 2001:2::/64 (广州)，下一跳找 R2 (2001:12::2)
[R1] ipv6 route-static 2001:2:: 64 2001:12::2
```

### 2. 配置 R2 (指明双向路)
```shell
# 去往 2001:1::/64 (北京)，下一跳找 R1
[R2] ipv6 route-static 2001:1:: 64 2001:12::1

# 去往 2001:2::/64 (广州)，下一跳找 R3
[R2] ipv6 route-static 2001:2:: 64 2001:23::3
```

### 3. 配置 R3 (指明回程路)
```shell
# 去往 2001:1::/64 (北京)，下一跳找 R2
[R3] ipv6 route-static 2001:1:: 64 2001:23::2
```

---

## 四、 验证结果

1.  **Ping 测试**：
    在 PC1 上：`ping 2001:2::1`
    *   结果：`Reply from...` (通了)。

2.  **断开实验** (可选)：
    如果你想试一下**默认路由**，可以在 R1 上执行：
    ```shell
    [R1] undo ipv6 route-static 2001:2:: 64 2001:12::2  # 删掉明细路由
    [R1] ipv6 route-static :: 0 2001:12::2             # 加上默认路由
    ```
    再次 Ping，依然通。

---

## 五、 排错自查
1.  如果 Ping 不通，先检查 IP 配没配对：在 R1 ping 2001:12::2 (R2)，看直连通不通。
2.  检查 R3 上有没有回程路由，这是最容易漏的。