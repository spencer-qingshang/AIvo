# 项目3实战：单臂路由 (Router-on-a-Stick)

> **实验目标**：让属于 VLAN 10 的 PC1 和属于 VLAN 20 的 PC2，通过路由器 R1 的一个物理接口实现互通。
> **前提**：请清空 eNSP 画布，新建拓扑。

---

## 一、 拓扑搭建与 IP 规划

### 1. 设备与连线
*   **1台路由器** (AR2220): 命名 `R1`
*   **1台交换机** (S3700): 命名 `SW1`
*   **2台电脑**: `PC1` (VLAN 10), `PC2` (VLAN 20)

**连线图 (手动 Copper)**：
*   **PC1** (Eth 0/0/1)  --> **SW1** (Eth 0/0/1)
*   **PC2** (Eth 0/0/1)  --> **SW1** (Eth 0/0/2)
*   **SW1** (GE 0/0/1)   --> **R1**  (GE 0/0/0)

### 2. IP 地址配置 (PC端)
*   **PC1**: `192.168.10.1`, Mask `255.255.255.0`, GW `192.168.10.254`
*   **PC2**: `192.168.20.1`, Mask `255.255.255.0`, GW `192.168.20.254`
*   *点应用！*

---

## 二、 交换机配置 (SW1)

我们需要把 PC 分别划入不同 VLAN，并把连接路由器的口设为“干道”(Trunk)，允许所有 VLAN 通过。

```shell
<Huawei> system-view
[Huawei] sysname SW1

# 1. 创建 VLAN
[SW1] vlan batch 10 20

# 2. 将 PC1 划入 VLAN 10
[SW1] interface Ethernet 0/0/1
[SW1-Ethernet0/0/1] port link-type access
[SW1-Ethernet0/0/1] port default vlan 10
[SW1-Ethernet0/0/1] quit

# 3. 将 PC2 划入 VLAN 20
[SW1] interface Ethernet 0/0/2
[SW1-Ethernet0/0/2] port link-type access
[SW1-Ethernet0/0/2] port default vlan 20
[SW1-Ethernet0/0/2] quit

# 4. 配置连接路由器的口为 Trunk (关键步骤)
[SW1] interface GigabitEthernet 0/0/1
[SW1-GigabitEthernet0/0/1] port link-type trunk
[SW1-GigabitEthernet0/0/1] port trunk allow-pass vlan 10 20
[SW1-GigabitEthernet0/0/1] quit
```

---

## 三、 路由器配置 (R1) - 核心手术

路由器的一个物理口 `GE0/0/0` 本身无法配置两个网关 IP。我们需要创建**子接口**。

### 1. 配置 VLAN 10 的网关 (子接口 .10)
```shell
<Huawei> system-view
[Huawei] sysname R1

[R1] interface GigabitEthernet 0/0/0.10     # 创建子接口 .10
[R1-GigabitEthernet0/0/0.10] dot1q termination vid 10  # 绑定 VLAN 10 标签
[R1-GigabitEthernet0/0/0.10] ip address 192.168.10.254 24
[R1-GigabitEthernet0/0/0.10] arp broadcast enable      # 【必杀技】开启ARP广播
[R1-GigabitEthernet0/0/0.10] quit
```

### 2. 配置 VLAN 20 的网关 (子接口 .20)
```shell
[R1] interface GigabitEthernet 0/0/0.20     # 创建子接口 .20
[R1-GigabitEthernet0/0/0.20] dot1q termination vid 20  # 绑定 VLAN 20 标签
[R1-GigabitEthernet0/0/0.20] ip address 192.168.20.254 24
[R1-GigabitEthernet0/0/0.20] arp broadcast enable      # 别忘了这个！
[R1-GigabitEthernet0/0/0.20] quit
```

---

## 四、 验证与排错

### 1. 验证 PC1 -> 网关
在 PC1 命令行：`ping 192.168.10.254`
*   **通**：说明 PC1 到路由器的 .10 子接口是通的。
*   **不通**：检查 SW1 的 trunk 配置，或者 R1 的 `arp broadcast enable` 有没有敲。

### 2. 验证 PC1 -> PC2
在 PC1 命令行：`ping 192.168.20.1`
*   **通**：恭喜！PC1 的包发给网关 .10，路由器发现要去 20.0 网段，就自动转发给 .20 接口，再发给 PC2。这就是单臂路由的魅力。

---

## 五、 知识点补丁 (为什么这么配？)

*   **`dot1q termination vid 10`**：
    *   路由器默认不懂 VLAN 标签。这条命令是告诉它：“如果你收到带着 VLAN 10 标签的数据包，就把它剥开；如果你要发包给 VLAN 10，记得贴上 10 号标签。”
*   **`arp broadcast enable`**：
    *   **这是新手最大的坑**。华为路由器的子接口默认不处理 ARP 广播。如果不敲这行，PC1 喊“网关你在哪”，路由器听到了但装聋作哑，导致无法通信。
