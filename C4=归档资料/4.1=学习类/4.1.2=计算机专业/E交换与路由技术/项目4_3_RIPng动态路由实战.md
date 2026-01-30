# 项目4_3_RIPng动态路由实战 (独立完整版)

> **实验目标**：从零开始，使用 RIPng 协议实现全网自动互通。
> **适用场景**：全新的拓扑环境。

---

## 一、 物理连线与基础环境 (从零开始)

### 1. 摆放与连线
同项目 4_2：
*   **3台 AR2220** (`R1`, `R2`, `R3`)，**2台 PC**。
*   连线：PC1-R1-R2-R3-PC2。
*   **开启设备**。

---

## 二、 基础 IP 地址配置 (必做铺垫)

> **注意**：如果你已经熟悉了 IP 配置，可以快速刷入。

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

## 三、 核心：配置 RIPng 动态路由

> **配置口诀**：先开进程 `ripng 1`，再进接口 `ripng 1 enable`。每个有 IP 的口都要配！

### 1. 配置 R1 (开启 RIPng)
```shell
[R1] ripng 1                                 # 启动进程
[R1-ripng-1] quit
[R1] interface GigabitEthernet 0/0/0         # 互联口
[R1-GigabitEthernet0/0/0] ripng 1 enable
[R1-GigabitEthernet0/0/0] quit
[R1] interface GigabitEthernet 0/0/1         # 业务口 (必配!)
[R1-GigabitEthernet0/0/1] ripng 1 enable
[R1-GigabitEthernet0/0/1] quit
```

### 2. 配置 R2 (开启 RIPng)
```shell
[R2] ripng 1
[R2-ripng-1] quit
[R2] interface GigabitEthernet 0/0/0
[R2-GigabitEthernet0/0/0] ripng 1 enable
[R2-GigabitEthernet0/0/0] quit
[R2] interface GigabitEthernet 0/0/1
[R2-GigabitEthernet0/0/1] ripng 1 enable
[R2-GigabitEthernet0/0/1] quit
```

### 3. 配置 R3 (开启 RIPng)
```shell
[R3] ripng 1
[R3-ripng-1] quit
[R3] interface GigabitEthernet 0/0/0
[R3-GigabitEthernet0/0/0] ripng 1 enable
[R3-GigabitEthernet0/0/0] quit
[R3] interface GigabitEthernet 0/0/1
[R3-GigabitEthernet0/0/1] ripng 1 enable
[R3-GigabitEthernet0/0/1] quit
```

---

## 四、 验证结果

1.  **查看路由表**：
    在 R1 上：`display ripng 1 route`
    *   你应该能看到 `2001:2::/64` 的路由信息。
2.  **Ping 测试**：
    PC1 Ping PC2：`ping 2001:2::1`
    *   **结果**：Reply from... (成功)。

---

## 五、 避坑指南
1.  **忘记宣告 PC 所在的接口**：这是新手最容易犯的错。如果你不在 R1 的 G0/0/1 接口下敲 `ripng 1 enable`，R1 就不会把 "我家有 1.0 网段" 这件事告诉 R2 和 R3，导致回包回不来。