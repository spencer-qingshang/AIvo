# 项目4_3_RIPng动态路由实战 (超详细保姆级)

> **实验目标**：配置 RIPng 协议，让三台路由器自动互相学习路由信息。
> **前置条件**：完成项目 4_1 的 IP 配置。

---

## 一、 清理环境 (必做步骤)

> **说明**：如果你刚刚做完了静态路由实验，必须把它们删掉，否则会影响动态路由的实验效果（静态路由优先级高，会覆盖动态路由）。

### 1. 删除 R1 的静态路由
```shell
<R1> system-view
# 删除默认路由 (如果配过)
[R1] undo ipv6 route-static :: 0 2001:12::2
# 删除明细路由 (如果配过)
[R1] undo ipv6 route-static 2001:2:: 64 2001:12::2
```

### 2. 删除 R2 的静态路由
```shell
<R2> system-view
[R2] undo ipv6 route-static 2001:1:: 64 2001:12::1
[R2] undo ipv6 route-static 2001:2:: 64 2001:23::3
```

### 3. 删除 R3 的静态路由
```shell
<R3> system-view
[R3] undo ipv6 route-static 2001:1:: 64 2001:23::2
```

---

## 二、 配置 RIPng 协议 (不省略任何设备)

> **核心逻辑**：两步走。第一步全局开进程，第二步进接口使能。每一个有 IP 的接口都要配！

### 1. 配置路由器 R1
```shell
<R1> system-view
# 第一步：启动 RIPng 进程，进程号设为 1
[R1] ripng 1
[R1-ripng-1] quit

# 第二步：进入连接 R2 的接口 (G0/0/0)
[R1] interface GigabitEthernet 0/0/0
[R1-GigabitEthernet0/0/0] ripng 1 enable   # 【关键】将此接口加入 RIPng 进程1
[R1-GigabitEthernet0/0/0] quit

# 第三步：进入连接 PC1 的接口 (G0/0/1)
[R1] interface GigabitEthernet 0/0/1
[R1-GigabitEthernet0/0/1] ripng 1 enable   # 【必做】别忘了这个口，否则别人不知道怎么去PC1
[R1-GigabitEthernet0/0/1] quit
```

### 2. 配置路由器 R2
```shell
<R2> system-view
[R2] ripng 1
[R2-ripng-1] quit

# 左右两个接口都要使能
[R2] interface GigabitEthernet 0/0/0
[R2-GigabitEthernet0/0/0] ripng 1 enable
[R2-GigabitEthernet0/0/0] quit

[R2] interface GigabitEthernet 0/0/1
[R2-GigabitEthernet0/0/1] ripng 1 enable
[R2-GigabitEthernet0/0/1] quit
```

### 3. 配置路由器 R3
```shell
<R3> system-view
[R3] ripng 1
[R3-ripng-1] quit

# 两个接口都要使能
[R3] interface GigabitEthernet 0/0/0
[R3-GigabitEthernet0/0/0] ripng 1 enable
[R3-GigabitEthernet0/0/0] quit

[R3] interface GigabitEthernet 0/0/1
[R3-GigabitEthernet0/0/1] ripng 1 enable
[R3-GigabitEthernet0/0/1] quit
```

---

## 三、 验证与排错

### 1. 查看 RIPng 路由表
在 R1 上输入：
`display ripng 1 route`

*   **观察**：能否看到 `2001:2::/64` (这是 PC2 的网段)？
*   **注意**：RIPng 更新比较慢（30秒一次），如果刚配完没看到，请等一分钟再查。

### 2. Ping 测试
在 PC1 上：
`ping 2001:2::1`

*   **结果**：Reply from ... 即为成功。

### 3. 排错指南
*   **现象**：路由表里只有直连路由，没有学到远端的。
*   **原因**：
    1.  **接口漏配**：最常见的是 R1 忘了在连接 PC1 的接口 (G0/0/1) 上敲 `ripng 1 enable`，导致 R1 不会把 1.0 网段告诉别人。
    2.  **进程号不一致**：建议所有设备都统一用 `ripng 1`，虽然协议允许多进程，但新手容易搞混。
    3.  **链路不通**：检查 R1 和 R2 之间物理连接是否正常。
