# 项目1：认识eNSP及VRP的基础操作 (深度备考版)

## 一、 eNSP 基础与环境搭建 (必考识记)

### 1.1 eNSP 模拟器组件
*   **eNSP (Enterprise Network Simulation Platform)**：华为提供的免费、可扩展、图形化网络仿真平台。
*   **三大核心底层依赖**（安装顺序建议）：
    1.  **WinPcap**：底层数据包捕获驱动。
    2.  **Wireshark**：网络协议分析器（抓包工具）。
    3.  **VirtualBox**：**核心虚拟机引擎**（设备运行的真实载体，通常建议使用 5.2.x 版本以保证兼容性）。

### 1.2 网络连接线缆
*   **Ethernet (以太网线/双绞线)**：连接 PC、交换机、路由器，最常用。
*   **Serial (串口线)**：连接广域网接口（如 S1/0/0），通常呈现为红色。
*   **Auto (自动选择)**：模拟器自动识别并连接最优线缆。

---

## 二、 VRP 操作系统与视图模式 (核心领会)

### 2.1 VRP 简介
*   **VRP (Versatile Routing Platform)**：华为通用路由平台，是华为数通设备的操作系统。
*   **版本演进**：目前实验和现网主流为 **VRP5**；最新一代为 **VRP8**（支持云化和分布式）。

### 2.2 命令行视图 (View) 切换逻辑（**必背**）

| 视图名称 | 提示符 | 进入命令 | 退出/回退命令 |
| :--- | :--- | :--- | :--- |
| **用户视图** | `<Huawei>` | 登录即进入 | `quit` (断开连接) |
| **系统视图** | `[Huawei]` | `system-view` | `quit` (回退到用户视图) |
| **接口视图** | `[Huawei-G0/0/0]` | `interface G0/0/0` | `quit` (回退到系统视图) |
| **协议视图** | `[Huawei-ospf-1]` | `ospf 1` | `quit` (回退到系统视图) |

*   **快捷回跳**：按 `Ctrl + Z` 或输入 `return` 可从任意视图直接回退到**用户视图**。

---

## 三、 VRP 基本操作与快捷键 (核心应用)

### 3.1 命令行求助与补全
*   **Tab 键**：部分输入后自动补全命令（如输入 `sys` 按 Tab 补全为 `system-view`）。
*   **? (问号)**：
    *   `sys?`：列出所有以 `sys` 开头的命令。
    *   `system-view ?`：列出该命令后可接的参数。

### 3.2 基础配置五步走
```shell
# 1. 进入系统视图
<Huawei> system-view

# 2. 修改设备名称 (方便标识)
[Huawei] sysname R1

# 3. 进入接口并配置 IP
[R1] interface GigabitEthernet 0/0/0
[R1-G0/0/0] ip address 192.168.1.1 24

# 4. 查看当前接口状态
[R1-G0/0/0] display this

# 5. 保存配置 (必须回到用户视图)
[R1-G0/0/0] return
<R1> save
```

---

## 四、 常用管理与维护命令 (考前速记)

### 1. 查看类命令 (Display)
*   `display version`：查看系统版本、运行时间、硬件信息。
*   `display current-configuration`：查看**当前生效**的配置（在 RAM 中，重启消失）。
*   `display saved-configuration`：查看**已保存**的配置（在 Flash/SD 卡中）。
*   `display ip interface brief`：**排障神句**。查看所有接口的 IP、物理状态 (Physical) 和协议状态 (Protocol)。

### 2. 删除与撤销命令 (Undo)
*   **原则**：在原命令前加 `undo`。
*   **示例**：
    *   删 IP：`undo ip address`
    *   改回默认名：`undo sysname`
    *   关闭接口：`shutdown` (反向：`undo shutdown`)

### 3. 系统维护
*   `reboot`：重启设备。
*   `reset saved-configuration`：清除已保存的配置（恢复出厂设置，需重启生效）。

---

## 五、 考纲重点提炼：哪些必须背？

### 1. 必背逻辑
*   **配置生效逻辑**：VRP 命令是“敲完即生效”，但属于“当前配置”，必须执行 `save` 才能持久化。
*   **视图层级关系**：配置接口 IP 必须先进入系统视图，再进入接口视图。

### 2. 必背关键字
*   `system-view` (进入管理模式)。
*   `interface` (进入端口)。
*   `display` (所有查看操作的开头)。
*   `undo` (所有删除/撤销操作的开头)。
*   `quit` / `return` (退出的两种方式)。

### 3. 常见报错信息辨析
*   **Error: Unrecognized command**：命令拼写错误或视图不对。
*   **Error: Incomplete command**：参数没输全（如 IP 后面漏了掩码）。
*   **Error: Ambiguous command**：输入的简写不唯一（有多个命令匹配）。

---

## 六、 常见模拟器故障排查 (eNSP 专用)

*   **设备启动报“错误代码 40”**：
    1.  检查 VirtualBox 里的 `Host-Only` 网络适配器是否被禁用。
    2.  在 eNSP 菜单 -> 工具 -> 注册设备，重新注册所有组件。
*   **命令行一直显示 “####”**：
    1.  通常是防火墙拦截了数据，关闭 Windows 防火墙或允许 eNSP 通过。
    2.  VirtualBox 版本过高（建议退回到 5.2.x 系列）。
