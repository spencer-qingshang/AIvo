# 项目4_4_OSPFv3动态路由实战 (独立完整版)

> **实验目标**：从零开始，配置企业级 OSPFv3 协议，实现全网互通。
> **适用场景**：全新的拓扑环境。

---

## 一、 物理连线与基础环境 (从零开始)

### 1. 摆放与连线
同前：**3台 AR2220** (`R1-R2-R3`)，**2台 PC**。
连线：PC1-R1-R2-R3-PC2。

---

## 二、 基础 IP 地址配置 (必做铺垫)

### 1. R1 基础配置
```shell
<Huawei> system-view
[Huawei] sysname R1
[R1] ipv6
[R1] interface GigabitEthernet 0/0/1         # 接 PC1
[R1-GigabitEthernet0/0/1] ipv6 enable
[R1-GigabitEthernet0/0/1] ipv6 address 2001:1::254 64
[R1-GigabitEthernet0/0/1] quit
[R1] interface GigabitEthernet 0/0/0         # 接 R2
[R1-GigabitEthernet0/0/0] ipv6 enable
[R1-GigabitEthernet0/0/0] ipv6 address 2001:12::1 64
[R1-GigabitEthernet0/0/0] quit
```

### 2. R2 基础配置
```shell
<Huawei> system-view
[Huawei] sysname R2
[R2] ipv6
[R2] interface GigabitEthernet 0/0/0         # 接 R1
[R2-GigabitEthernet0/0/0] ipv6 enable
[R2-GigabitEthernet0/0/0] ipv6 address 2001:12::2 64
[R2-GigabitEthernet0/0/0] quit
[R2] interface GigabitEthernet 0/0/1         # 接 R3
[R2-GigabitEthernet0/0/1] ipv6 enable
[R2-GigabitEthernet0/0/1] ipv6 address 2001:23::2 64
[R2-GigabitEthernet0/0/1] quit
```

### 3. R3 基础配置
```shell
<Huawei> system-view
[Huawei] sysname R3
[R3] ipv6
[R3] interface GigabitEthernet 0/0/0         # 接 R2
[R3-GigabitEthernet0/0/0] ipv6 enable
[R3-GigabitEthernet0/0/0] ipv6 address 2001:23::3 64
[R3-GigabitEthernet0/0/0] quit
[R3] interface GigabitEthernet 0/0/1         # 接 PC2
[R3-GigabitEthernet0/0/1] ipv6 enable
[R3-GigabitEthernet0/0/1] ipv6 address 2001:2::254 64
[R3-GigabitEthernet0/0/1] quit
```

### 4. PC 配置
*   **PC1**: `2001:1::1` / 64, GW `2001:1::254`
*   **PC2**: `2001:2::1` / 64, GW `2001:2::254`

---

## 三、 核心：配置 OSPFv3 动态路由

> **配置口诀**：先开进程 `ospfv3 1` -> **必须配 Router-ID** -> 进接口绑区域 `ospfv3 1 area 0`。

### 1. 配置 R1 (Router-ID: 1.1.1.1)
```shell
[R1] ospfv3 1                                # 启动进程
[R1-ospfv3-1] router-id 1.1.1.1              # 【必配】配置身份证号
[R1-ospfv3-1] quit

# 接口绑定区域
[R1] interface GigabitEthernet 0/0/0
[R1-GigabitEthernet0/0/0] ospfv3 1 area 0    # 加入骨干区域 0
[R1-GigabitEthernet0/0/0] quit
[R1] interface GigabitEthernet 0/0/1         # 业务口也必须加入
[R1-GigabitEthernet0/0/1] ospfv3 1 area 0
[R1-GigabitEthernet0/0/1] quit
```

### 2. 配置 R2 (Router-ID: 2.2.2.2)
```shell
[R2] ospfv3 1
[R2-ospfv3-1] router-id 2.2.2.2
[R2-ospfv3-1] quit

[R2] interface GigabitEthernet 0/0/0
[R2-GigabitEthernet0/0/0] ospfv3 1 area 0
[R2-GigabitEthernet0/0/0] quit
[R2] interface GigabitEthernet 0/0/1
[R2-GigabitEthernet0/0/1] ospfv3 1 area 0
[R2-GigabitEthernet0/0/1] quit
```

### 3. 配置 R3 (Router-ID: 3.3.3.3)
```shell
[R3] ospfv3 1
[R3-ospfv3-1] router-id 3.3.3.3
[R3-ospfv3-1] quit

[R3] interface GigabitEthernet 0/0/0
[R3-GigabitEthernet0/0/0] ospfv3 1 area 0
[R3-GigabitEthernet0/0/0] quit
[R3] interface GigabitEthernet 0/0/1
[R3-GigabitEthernet0/0/1] ospfv3 1 area 0
[R3-GigabitEthernet0/0/1] quit
```

---

## 四、 验证结果

1.  **检查邻居状态** (关键)：
    在 R1 上：`display ospfv3 peer`
    *   **State**: 必须显示 **Full**。如果是 Init 或 2-Way 都不对。
2.  **Ping 测试**：
    PC1 Ping PC2：`ping 2001:2::1`
    *   **结果**：Reply from... (成功)。

---

## 五、 避坑指南
1.  **邻居起不来**：最常见的原因是忘了配 Router-ID，或者两台路由器的 ID 配重了（比如都配了 1.1.1.1）。
2.  **区域不一致**：R1 用了 area 0，R2 用了 area 1，这样是建不起来邻居的。初学者统一用 area 0 即可。