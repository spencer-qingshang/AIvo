# 项目3实战：单臂路由 (不同VLAN间互访)

> **实验目标**：让属于 VLAN 10 的 PC1 和属于 VLAN 20 的 PC2，通过路由器 R1 的一个物理接口实现互通。
> **适用场景**：公司为了省钱，买不起三层交换机，又想让不同部门互通时。

---

## 一、 核心原理大白话 (新手必读)

**1. 为什么要搞这个？**
交换机把 PC1 (10号楼) 和 PC2 (20号楼) 隔离了，平时老死不相往来。想通信，必须找个“中介”——路由器。

**2. 什么是“单臂”？**
路由器只有一只手（一根线）连着交换机。但这只手要同时处理 10号楼 和 20号楼 的快递。

**3. 我们敲的命令到底在干嘛？**
*   **交换机 Trunk** (`allow-pass vlan 10 20`)：
    *   告诉交换机保安：“这个路由器是自己人，以后凡是带 `10` 和 `20` 标签的信，别拦着，让他过！”
    *   *刚才你没通，就是因为保安把信扣下了。*
*   **路由器子接口** (`interface ... .10` + `dot1q ... 10`)：
    *   路由器把一只手变魔术成了两只手。左手(.10)专门收发贴了“10”标签的信，右手(.20)专门收发贴了“20”标签的信。
*   **ARP 广播开启** (`arp broadcast enable`)：
    *   告诉路由器：“别装高冷！如果电脑喊你名字（问网关在哪），你必须答应！”（华为路由器默认是不理人的）。

---

## 二、 拓扑搭建与 IP 规划
*   **R1** (GE0/0/0) <---> **SW1** (GE0/0/1)
*   **PC1** (Eth0/0/1) <---> **SW1** (Eth0/0/1)
*   **PC2** (Eth0/0/1) <---> **SW1** (Eth0/0/2)
*   **PC1 IP**: `192.168.10.1`, GW `192.168.10.254`
*   **PC2 IP**: `192.168.20.1`, GW `192.168.20.254`

---

## 三、 配置步骤 (保姆级)

### 1. 交换机配置 (SW1)
```shell
<Huawei> system-view
[Huawei] sysname SW1
[SW1] vlan batch 10 20                   # 建好10号和20号楼

# 把 PC1 关进 10号楼
[SW1] interface Ethernet 0/0/1
[SW1-Ethernet0/0/1] port link-type access
[SW1-Ethernet0/0/1] port default vlan 10
[SW1-Ethernet0/0/1] quit

# 把 PC2 关进 20号楼
[SW1] interface Ethernet 0/0/2
[SW1-Ethernet0/0/2] port link-type access
[SW1-Ethernet0/0/2] port default vlan 20
[SW1-Ethernet0/0/2] quit

# 【关键】给路由器开绿灯 (Trunk)
[SW1] interface GigabitEthernet 0/0/1
[SW1-GigabitEthernet0/0/1] port link-type trunk
[SW1-GigabitEthernet0/0/1] port trunk allow-pass vlan 10 20  # 没这行就Ping不通！
[SW1-GigabitEthernet0/0/1] quit
```

### 2. 路由器配置 (R1)
```shell
<Huawei> system-view
[Huawei] sysname R1

# 配置左手 (.10)
[R1] interface GigabitEthernet 0/0/0.10
[R1-GigabitEthernet0/0/0.10] dot1q termination vid 10  # 认领10号标签
[R1-GigabitEthernet0/0/0.10] ip address 192.168.10.254 24
[R1-GigabitEthernet0/0/0.10] arp broadcast enable      # 必须开！
[R1-GigabitEthernet0/0/0.10] quit

# 配置右手 (.20)
[R1] interface GigabitEthernet 0/0/0.20
[R1-GigabitEthernet0/0/0.20] dot1q termination vid 20  # 认领20号标签
[R1-GigabitEthernet0/0/0.20] ip address 192.168.20.254 24
[R1-GigabitEthernet0/0/0.20] arp broadcast enable      # 必须开！
[R1-GigabitEthernet0/0/0.20] quit
```

---

## 四、 验证与排错
1.  **Ping 网关**：PC1 Ping 192.168.10.254。如果不通，查 SW1 的 `allow-pass` 和 R1 的 `arp broadcast`。
2.  **Ping 对方**：PC1 Ping 192.168.20.1。如果通了，说明路由器成功当了中介。