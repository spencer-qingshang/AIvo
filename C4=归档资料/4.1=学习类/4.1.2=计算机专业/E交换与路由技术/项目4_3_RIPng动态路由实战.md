# 项目4_3_RIPng 动态路由实战 (零基础保姆级)

> **实验目标**：利用 RIPng 协议（RIP 的下一代，支持 IPv6），让路由器自动通过“聊天”来交换路由信息，无需手动指路。
> **适用场景**：小型 IPv6 网络，作为动态路由协议入门。

---

## 一、 知识点大白话解析

> **1. 什么是 RIPng？**
> RIPng (Next Generation) 是专门为 IPv6 设计的动态路由协议。
> **比喻**：就像在一个小区群里，每个邻居都大喊：“我负责 1 号楼！”。过一会儿，整栋楼的人都知道怎么去 1 号楼了。
>
> **2. 它的规则是什么？**
> *   **按“跳”数算路**：经过一个路由器就算一跳。最多支持 15 跳，16 跳就认为路断了。
> *   **组播喊话**：它不再满大街（广播）喊话，而是定向给加入 RIPng 群组的人喊（组播地址 `FF02::9`）。
>
> **3. 配置上与 IPv4 有什么区别？**
> *   **IPv4 RIP**：在全局视图下敲 `network 192.168.1.0`。
> *   **IPv6 RIPng**：**不在全局宣告网段**。你必须进入每一个接口（比如 G0/0/0），直接说：“这个接口加入 RIPng 进程 1 ！”。

---

## 二、 环境准备

### 1. 清理环境 (重要！)
如果你刚才做了 **项目 4_2 (静态路由)**，请务必先删除那些手动指的路，否则你看不到动态路由生效的效果。

**在 R1, R2, R3 上分别操作：**
```shell
<R1> system-view
[R1] undo ipv6 route-static :: 0
[R1] undo ipv6 route-static 2001:2:: 64 2001:12::2
# 提示：如果不确定有没有删干净，输入 display current-configuration | include ipv6 route-static
```
*清理完后，PC1 应该 **无法** Ping 通 PC2。*

---

## 三、 核心配置步骤 (开启自动寻路)

### 1. R1 配置
```shell
<R1> system-view
[R1] ripng 1                  # 启动 RIPng 进程，编号为 1
[R1-ripng-1] quit

# 进入连接 R2 的口，使能 RIPng
[R1] interface GigabitEthernet 0/0/0
[R1-GigabitEthernet0/0/0] ripng 1 enable

# 进入连接 PC1 的口，使能 RIPng (这样大家才知道 1.0 网段在哪)
[R1] interface GigabitEthernet 0/0/1
[R1-GigabitEthernet0/0/1] ripng 1 enable
```

### 2. R2 配置
```shell
<R2> system-view
[R2] ripng 1
[R2-ripng-1] quit

[R2] interface GigabitEthernet 0/0/0
[R2-GigabitEthernet0/0/0] ripng 1 enable

[R2] interface GigabitEthernet 0/0/1
[R2-GigabitEthernet0/0/1] ripng 1 enable
```

### 3. R3 配置
```shell
<R3> system-view
[R3] ripng 1
[R3-ripng-1] quit

[R3] interface GigabitEthernet 0/0/0
[R3-GigabitEthernet0/0/0] ripng 1 enable

[R3] interface GigabitEthernet 0/0/1
[R3-GigabitEthernet0/0/1] ripng 1 enable
```

---

## 四、 验证与检查 (见证奇迹)

### 1. 查看 RIPng 路由表
在 R1 上输入：
`display ripng 1 route`

*   **看什么？**：检查列表中是否有 `2001:2::/64` (广州 PC 网段) 和 `2001:23::/64` (骨干网段)。
*   **状态**：如果能看到这些网段，说明 OSPF 已经通过邻居“学到”了这些知识。

### 2. 最终 Ping 测试
打开 **PC1** 的命令行：
`ping 2001:2::1`

*   **期待结果**：直接 Ping 通！

---

## 五、 新手避坑指南 (常见报错)

1.  **路由表是空的？**
    *   **原因 1**：检查每个路由器的接口下是否都敲了 `ripng 1 enable`。如果只在全局启动进程而不进接口使能，是没有用的。
    *   **原因 2**：检查路由器之间是否能 Ping 通对方的接口 IP。
2.  **配置了没反应？**
    *   RIPng 反应比较慢（通常每 30 秒才更新一次），敲完命令后请耐心等一会儿，或者多按几次回车。