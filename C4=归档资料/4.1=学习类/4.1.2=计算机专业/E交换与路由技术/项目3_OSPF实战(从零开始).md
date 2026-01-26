# 项目3实战：OSPF动态路由 (从零开始纯净版)

> **实验目标**：在不配置任何静态路由的情况下，直接配置 OSPF 协议，实现全网自动寻址。

---

## 一、 拓扑搭建与 IP 配置

### 1. 物理连接
*   使用 `Copper` 线手动连接：
    *   PC1 <-> R1 (GE 0/0/1)
    *   R1 (GE 0/0/0) <-> R2 (GE 0/0/0)
    *   R2 (GE 0/0/1) <-> R3 (GE 0/0/0)
    *   R3 (GE 0/0/1) <-> PC2

### 2. IP 与网关 (必须先配好)
*   **PC1**: `192.168.10.1`, GW `192.168.10.254`
*   **PC2**: `192.168.20.1`, GW `192.168.20.254`

---

## 二、 OSPF 核心配置步骤

### 1. R1 配置 (北京)
```shell
<R1> system-view
[R1] ospf 1 router-id 1.1.1.1
[R1-ospf-1] area 0
[R1-ospf-1-area-0.0.0.0] network 192.168.10.0 0.0.0.255
[R1-ospf-1-area-0.0.0.0] network 12.1.1.0 0.0.0.255
```

### 2. R2 配置 (上海)
```shell
<R2> system-view
[R2] ospf 1 router-id 2.2.2.2
[R2-ospf-1] area 0
[R2-ospf-1-area-0.0.0.0] network 12.1.1.0 0.0.0.255
[R2-ospf-1-area-0.0.0.0] network 23.1.1.0 0.0.0.255
```

### 3. R3 配置 (广州)
```shell
<R3> system-view
[R3] ospf 1 router-id 3.3.3.3
[R3-ospf-1] area 0
[R3-ospf-1-area-0.0.0.0] network 23.1.1.0 0.0.0.255
[R3-ospf-1-area-0.0.0.0] network 192.168.20.0 0.0.0.255
```

---

## 三、 验证与检查
1.  **检查邻居关系**：在 R2 上输入 `display ospf peer brief`。如果 State 显示为 `Full`，说明路由器之间已经建立了信任关系。
2.  **查看路由表**：输入 `display ip routing-table protocol ospf`。查看是否学到了对端电脑的网段。
3.  **Ping测试**：PC1 Ping PC2。
