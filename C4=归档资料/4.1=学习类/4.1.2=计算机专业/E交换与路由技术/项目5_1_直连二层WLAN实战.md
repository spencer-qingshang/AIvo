# 项目5-1：组建直连式二层WLAN实战手册 (小白版)

> **核心目标**：在 eNSP 模拟器中，通过 1 台 AC 控制器和 1 台 AP 建立无线网络，让手机（STA）能连上名为 "Huawei-Layer2" 的 WIFI。
> **场景特点**：二层组网（AC与AP在同网段）、直接转发、AC 兼职当 DHCP 老师发 IP。

---

## 一、 环境准备 (手把手搭拓扑)

### 1. 拖动设备
*   **AC (无线控制器)**：在左侧工具栏选择 **WLAN** -> **AC6005**，拖入 1 台。
*   **AP (无线接入点)**：在左侧工具栏选择 **WLAN** -> **AP6050**，拖入 1 台。
*   **STA (无线终端)**：在左侧工具栏选择 **终端** -> **STA** (看起来像个笔记本或手机)，拖入 1 台。

### 2. 物理连线 (Copper 铜线)
*   **AC** 的 `GE 0/0/1` 接口 <--> 连 **AP** 的 `GE 0/0/0` 接口。
*   *注意*：STA 是无线的，不需要连线。

### 3. 开机
全选设备，点击启动。

### 4. 规划表
| 设备 | 接口 | IP地址/网段 | 说明 |
| :--- | :--- | :--- | :--- |
| **AC 管理 IP** | Vlanif 1 | 192.168.10.1/24 | AC 自己的身份证号 |
| **AP/STA IP网段** | DHCP | 192.168.10.0/24 | AP 和手机都从这里领 IP |
| **WIFI 名字 (SSID)** | - | Huawei-Layer2 | 手机搜到的名字 |
| **WIFI 密码** | - | huawei@123 | 手机连网的暗号 |

---

## 二、 基础配置 (打地基)

### 1. 配置 AC 的管理 IP
```shell
<Huawei> system-view
[Huawei] sysname AC
[AC] vlan 10
[AC-vlan10] quit
# 虽然是二层组网，我们习惯给管理口配个 VLAN
[AC] interface vlanif 1
[AC-Vlanif1] ip address 192.168.10.1 24
# 大白话：给 AC 设置一个 192.168.10.1 的 IP 地址。
```

### 2. 接口开启 DHCP (AC 兼职派发员)
```shell
[AC] dhcp enable
[AC] interface vlanif 1
[AC-Vlanif1] dhcp select interface
[AC-Vlanif1] dhcp server option 43 sub-option 3 ascii 192.168.10.1
# 大白话：让 AC 在这个接口上开启“发 IP 地址”的服务。加上 Option 43 确保万无一失。
```

---

## 三、 AP 上线 (让 AC 找到 AP)

### 1. 指定 AC 的源接口
```shell
[AC] capwap source interface vlanif 1
# 大白话：AC 告诉 AP：“以后大家汇报工作，都发到 192.168.10.1 这个地址来”。
```

### 2. 发现 AP 并允许上线
```shell
[AC] wlan
[AC-wlan-view] ap-group name default
# 大白话：进入无线管理模式，准备用默认的小组来管 AP。
[AC-wlan-view] ap-id 0 mac-address <AP的MAC地址>
# 大白话：把 AP 的 MAC 地址登记一下，给它编个号叫 0 号。
# 注意：在 eNSP 中，右键 AP 查看“配置”可以复制 MAC 地址 (格式 xxxx-xxxx-xxxx)。
[AC-wlan-ap-0] ap-name Office-AP
[AC-wlan-ap-0] ap-group default
[AC-wlan-ap-0] quit
```

---

## 四、 WLAN 业务配置 (正式广播 WIFI)

### 1. 安全模板 (设密码)
```shell
[AC-wlan-view] security-profile name sec-p1
[AC-wlan-sec-prof-sec-p1] security wpa2 psk pass-phrase huawei@123 aes
# 大白话：创建一个保险柜名字叫 sec-p1，密码设为 huawei@123，加密方式选 AES。
[AC-wlan-sec-prof-sec-p1] quit
```

### 2. SSID 模板 (起名字)
```shell
[AC-wlan-view] ssid-profile name ssid-p1
[AC-wlan-ssid-prof-ssid-p1] ssid Huawei-Layer2
# 大白话：创建一个名字模板叫 ssid-p1，里面的 WIFI 名字叫 Huawei-Layer2。
[AC-wlan-ssid-prof-ssid-p1] quit
```

### 3. VAP 模板 (大锅炖：把名字和密码绑定到一起)
```shell
[AC-wlan-view] vap-profile name vap-p1
[AC-wlan-vap-prof-vap-p1] forward-mode direct-forward
# 大白话：设置转发模式为“直接转发”（抖音流量不走 AC）。
[AC-wlan-vap-prof-vap-p1] service-vlan vlan-id 1
# 大白话：让大家连上 WIFI 后，都在 VLAN 1 这个房间里。
[AC-wlan-vap-prof-vap-p1] security-profile sec-p1
[AC-wlan-vap-prof-vap-p1] ssid-profile ssid-p1
# 大白话：把刚才设的密码和名字都塞进这个业务包里。
[AC-wlan-vap-prof-vap-p1] quit
```

### 4. 把 VAP 应用到 AP 组
```shell
[AC-wlan-view] ap-group name default
[AC-wlan-view-ap-group-default] vap-profile vap-p1 wlan 1 radio all
# 大白话：让 default 组里的所有 AP，无论 2.4G 还是 5G 频率，都把刚才那个 WIFI 信号发出去。
```

---

## 五、 结果验证 (大功告成)

1.  **查看 AP 状态**：
    在 AC 上输入 `display ap all`。如果 `State` 是 `nor` (normal)，说明 AP 已经乖乖听话了。
2.  **STA 连网**：
    双击 eNSP 里的 STA 终端，点击“无线网络”，搜到 `Huawei-Layer2`，输入密码 `huawei@123`，点击连接。
3.  **检查 IP**：
    在 STA 上打开命令行输入 `ipconfig`，看是否拿到了 `192.168.10.X` 的地址。