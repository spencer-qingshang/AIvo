# 项目5-2：组建旁挂式三层WLAN实战手册 (进阶版)

> **核心目标**：在 eNSP 模拟器中，实现 AC 旁挂在核心交换机旁，AP 跨网段通过三层组网上线，STA 获取业务网段 IP。
> **场景特点**：三层组网（AC与AP不在同网段）、旁挂模式、隧道转发、Option 43 引导。

---

## 一、 环境准备 (拓扑搭建)

### 1. eNSP 拓扑图
*   **AC6005**: 旁挂在 CoreSW 上。
*   **CoreSW (S5700)**: 核心交换机，充当全网“大管家”和网关。
*   **AccSW (S3700)**: 接入交换机，透传 VLAN。
*   **AP6050**: 瘦 AP。
*   **STA**: 无线终端。

### 2. 规划表 (脑子清醒的关键)
| 区域 | VLAN | IP网段 | 说明 |
| :--- | :--- | :--- | :--- |
| **管理 VLAN (AP)** | VLAN 100 | 192.168.100.0/24 | AP 们住的房间 |
| **业务 VLAN (STA)** | VLAN 200 | 192.168.200.0/24 | 手机上网的房间 |
| **AC 互联 VLAN** | VLAN 10 | 192.168.10.0/24 | AC 与 核心互联的房间 |
| **AC 管理 IP** | - | 192.168.10.1 | AC 的身份证号 |
| **Option 43** | - | 192.168.10.1 | 核心告诉 AP 去哪找 AC |

---

## 二、 核心交换机配置 (总管家)

### 1. 基础 VLAN 与 接口
```shell
[CoreSW] vlan batch 10 100 200
[CoreSW] interface g0/0/1  # 连 AC
[CoreSW-GigabitEthernet0/0/1] port link-type trunk
[CoreSW-GigabitEthernet0/0/1] port trunk allow-pass vlan 10
[CoreSW] interface g0/0/2  # 连 接入交换机
[CoreSW-GigabitEthernet0/0/2] port link-type trunk
[CoreSW-GigabitEthernet0/0/2] port trunk allow-pass vlan 100 200
```

### 2. 配置网关与 DHCP (派发任务)
```shell
[CoreSW] dhcp enable
# 管理网段（发给AP）
[CoreSW] interface vlanif 100
[CoreSW-Vlanif100] ip address 192.168.100.1 24
[CoreSW-Vlanif100] dhcp select interface
[CoreSW-Vlanif100] dhcp server option 43 sub-option 3 ascii 192.168.10.1
# 大白话：配置 Option 43。AP 领 IP 时，顺便告诉它：“AC 在 192.168.10.1 哪，快去报到！”

# 业务网段（发给STA）
[CoreSW] interface vlanif 200
[CoreSW-Vlanif200] ip address 192.168.200.1 24
[CoreSW-Vlanif200] dhcp select interface

# 与 AC 互联的 IP
[CoreSW] interface vlanif 10
[CoreSW-Vlanif10] ip address 192.168.10.2 24
```

---

## 三、 接入交换机配置 (透传)
```shell
[AccSW] vlan batch 100 200
[AccSW] interface g0/0/1 # 连核心
[AccSW-GigabitEthernet0/0/1] port link-type trunk
[AccSW-GigabitEthernet0/0/1] port trunk allow-pass vlan 100 200
[AccSW] interface g0/0/2 # 连 AP
[AccSW-GigabitEthernet0/0/2] port link-type trunk
[AccSW-GigabitEthernet0/0/2] port trunk pvid vlan 100 # AP 发出的报文默认进 VLAN 100
[AccSW-GigabitEthernet0/0/2] port trunk allow-pass vlan 100 200
```

---

## 四、 AC 核心配置 (大脑)

### 1. 互联与路由 (确保能通)
```shell
[AC] vlan 10
[AC] interface vlanif 10
[AC-Vlanif10] ip address 192.168.10.1 24
[AC] ip route-static 0.0.0.0 0 192.168.10.2
# 大白话：加一条默认路由，让 AC 知道怎么去 100 和 200 网段。
```

### 2. 隧道源接口 (报到地址)
```shell
[AC] capwap source interface vlanif 10
```

### 3. WLAN 业务 (隧道转发)
```shell
[AC] wlan
[AC-wlan-view] security-profile name sec-p2
[AC-wlan-sec-prof-sec-p2] security wpa2 psk pass-phrase huawei@123 aes
[AC-wlan-view] ssid-profile name ssid-p2
[AC-wlan-ssid-prof-ssid-p2] ssid Huawei-Layer3
[AC-wlan-view] vap-profile name vap-p2
[AC-wlan-vap-prof-vap-p2] forward-mode tunnel
# 大白话：配置为“隧道转发”！所有流量都回传给 AC 统一管理。
[AC-wlan-vap-prof-vap-p2] service-vlan vlan-id 200
# 大白话：手机上网流量打上 VLAN 200 的标签。
[AC-wlan-vap-prof-vap-p2] security-profile sec-p2
[AC-wlan-vap-prof-vap-p2] ssid-profile ssid-p2
```

---

## 五、 结果验证

1.  **AP 上线**：`display ap all`。State 应为 `nor`。
    *   *排错提示*：如果不在线，检查 `ping 192.168.100.X` (AP的IP) 是否通畅。
2.  **STA 测试**：连上 `Huawei-Layer3`，看 IP 是否是 `192.168.200.X`。
3.  **流量观察**：在 AC 接口抓包，看 STA 上网时是否有 CAPWAP 封装的数据。
