# 项目1：认识eNSP及VRP的基础操作

## 一、 学习目标

### 1. 识记
*   了解eNSP模拟器的作用
*   了解VRP操作系统的来源和发展
*   认识eNSP主界面和网络连接的线缆

### 2. 领会
*   熟悉VRP的命令和基本操作

### 3. 应用
*   能正确安装eNSP模拟器
*   能使用eNSP搭建和配置网络
*   能掌握VRP平台的应用
*   能熟悉VRP基本操作

---

## 二、 项目大纲与任务分解

### 任务1：认识与安装eNSP模拟器
1.  **eNSP简介**
    *   华为企业网络模拟平台 (Enterprise Network Simulation Platform) 的功能与特点。
    *   支持的设备类型：路由器、交换机、防火墙、WLAN、PC等。
2.  **软件安装环境**
    *   依赖软件安装：Wireshark (抓包), VirtualBox (虚拟化核心), WinPcap (数据包捕获)。
    *   eNSP主程序安装步骤与注意事项。
    *   常见启动报错与排查（如防火墙设置、虚拟网卡问题）。
3.  **熟悉软件界面**
    *   菜单栏与工具栏功能。
    *   设备区：分类与型号选择。
    *   工作区：拓扑绘制区域。
    *   常用工具：抓包、CLI控制台、文本注释、调色板。

### 任务2：构建基础网络拓扑
1.  **添加设备**
    *   拖拽路由器 (如AR2220)、交换机 (如S5700)、PC终端至工作区。
2.  **连接线缆 (Connections)**
    *   **Auto (自动)**：自动选择线缆类型。
    *   **Copper (铜轴电缆)**：连接以太网接口 (GE/Ethernet)。
    *   **Serial (串口线)**：连接广域网串口。
    *   **Fiber (光纤)**：连接光口。
3.  **设备操作**
    *   启动/停止单台设备与所有设备。
    *   进入设备命令行界面 (CLI)。

### 任务3：VRP基础操作与命令行视图
1.  **VRP体系介绍**
    *   华为通用路由平台 (Versatile Routing Platform) 的架构。
2.  **命令行视图 (CLI Views)**
    *   **用户视图** (`<Huawei>`)：仅能查看运行状态和统计信息，权限有限。
    *   **系统视图** (`[Huawei]`)：`system-view` 进入，可配置全局参数。
    *   **接口视图** (`[Huawei-GigabitEthernet0/0/1]`)：配置具体接口参数。
    *   **协议视图**：如OSPF、RIP等协议配置。
3.  **视图切换与常用快捷键**
    *   `quit`：退回上一级视图。
    *   `return` (或 Ctrl+Z)：直接退回用户视图。
    *   `Tab` 键：命令自动补全。
    *   `?`：获取命令帮助信息。
    *   命令缩写支持 (如 `sys` = `system-view`)。

### 任务4：设备基础配置实战
1.  **基本环境配置**
    *   修改设备主机名：`sysname R1`
    *   配置系统时钟：`clock datetime ...`
    *   配置登录标题消息 (Header)：`header login` / `header shell`
2.  **接口配置**
    *   进入接口：`interface GigabitEthernet 0/0/0`
    *   配置IP地址：`ip address 192.168.1.1 24`
    *   激活/关闭接口：`undo shutdown` / `shutdown`
    *   查看接口状态：`display interface brief`
3.  **配置文件管理**
    *   查看当前运行配置：`display current-configuration`
    *   保存配置到启动文件：`save`
    *   查看下次启动配置：`display saved-configuration`
    *   清除配置：`reset saved-configuration`

## 三、 实验总结
*   总结eNSP中不同线缆的使用场景。
*   熟练掌握从用户视图进入接口视图的命令流程。
*   理解“运行配置”与“保存配置”的区别。
