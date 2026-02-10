# 项目1：认识 eNSP 与 VRP 基础操作 - 知识汇总

## 一、 核心背诵知识点

### 1. eNSP 模拟器
- **定义**：华为提供的图形化网络仿真平台。
- **关键组件**：VirtualBox（底层虚拟机）、Wireshark（抓包工具）。
- **主要功能**：模拟路由器、交换机、WLAN、防火墙等设备及其互连。

### 2. VRP 通用路由平台
- **全称**：Versatile Routing Platform。
- **定义**：华为公司数据通信产品的通用操作系统。
- **发展趋势**：VRP5 (目前主流) -> VRP8 (面向云和新业务)。

### 3. VRP 命令行视图（核心考点！）
- **用户视图**：<Huawei>。登录后的初始视图，仅能查询。
- **系统视图**：[Huawei]。通过 system-view 进入，可进行全局配置。
- **接口视图**：[Huawei-GigabitEthernet0/0/0]。进入特定接口配置参数。
- **协议视图**：[Huawei-ospf-1]。配置动态路由等协议。

### 4. 命令行交互与帮助（隐藏重点）
- **上下文帮助 `?`**：在任何位置输入 `?` 可查看可用命令或参数。
- **自动补全 `Tab`**：输入命令前缀后按 `Tab` 补全。
- **快捷键**：
  - `Ctrl+Z`：直接退回用户视图。
  - `Ctrl+C`：停止当前执行的操作。
  - `Ctrl+A` / `Ctrl+E`：光标移动到行首/行尾。
- **历史记录**：使用上下方向键调回命令，`display history-command` 查看记录。

### 5. 线缆与接口识记
- **常用线缆**：
  - **Copper (铜缆/网线)**：连接 GE/Ethernet 接口。
  - **Serial (串口线)**：连接 Serial 接口（常用于广域网 PPP/HDLC 实验）。
- **接口命名**：`接口类型 槽位/子卡/接口序号`，例如 `GigabitEthernet 0/0/0`。

---

## 二、 核心命令速查表

| 功能 | 命令 | 备注 |
| :--- | :--- | :--- |
| 进入系统视图 | `system-view` | 简写 `sys` |
| 退出当前视图 | `quit` | 简写 `q` |
| 直接退回用户视图 | `return` | 快捷键 `Ctrl+Z` |
| 修改设备名称 | `sysname [名称]` | 仅系统视图可用 |
| 查看当前运行配置 | `display current-configuration` | 简写 `dis cu` |
| 查看接口状态 | `display ip interface brief` | 简写 `dis ip int br` |
| 查看视图下配置 | `display this` | 视图敏感命令 |
| 查看历史命令 | `display history-command` | 默认记录10条 |
| 保存配置 | `save` | 用户视图下操作 |
| 重启设备 | `reboot` | 用户视图下操作 |

---

## 三、 模拟预测题型

### 1. 选择题 (预测)
- **题目**：VRP 操作系统的系统视图提示符是？
  - A. <Huawei>
  - B. [Huawei]
  - C. (Huawei)
  - D. {Huawei}
  - **答案**：B

### 2. 填空题 (预测)
- **题目**：从接口视图直接退回到用户视图的快捷键是 ________。
  - **答案**：Ctrl+Z (或输入 return)

### 3. 简答题 (预测)
- **题目**：简述查看当前配置命令 `display current-configuration` 与查看保存配置命令 `display saved-configuration` 的区别。
  - **答案**：前者查看的是内存中正在运行的配置（掉电丢失），后者查看的是保存在闪存中、设备重启后将加载的配置。

### 4. 应用题 (预测)
- **场景**：在 eNSP 中建立两台路由器的连接。
- **要求**：
  1. 修改路由器名为 R1。
  2. 为接口 G0/0/0 配置地址 192.168.1.1/24。
  3. 查看该接口的摘要状态。
- **命令参考**：
  `<Huawei> system-view` 
  `[Huawei] sysname R1` 
  `[R1] interface GigabitEthernet 0/0/0` 
  `[R1-GigabitEthernet0/0/0] ip address 192.168.1.1 24` 
  `[R1-GigabitEthernet0/0/0] display ip interface brief` 

