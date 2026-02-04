# 项目6-4：PPP 广域网认证实战手册

> **核心目标**：配置 PPP 链路的 PAP 和 CHAP 认证，确保广域网连接的安全。
> **场景**：公司（R1）通过串口（Serial）专线连接到分公司或运营商（R2），需要进行身份验证。

---

## 一、 环境准备 (手把手搭拓扑)

### 1. 添加模块 (AR2220 默认没有串口)
*   **拖入路由器**：拖入 2 台 **AR2220**，分别命名为 `R1` (认证方) 和 `R2` (被认证方)。
*   **加装接口卡**：
    1.  **右键**点击 R1，选择 **设置 (Settings)**。
    2.  在面板视图中，找到 **2SA** (2 Port Serial Interface Card)。
    3.  将其拖入路由器的空槽位（例如 slot 1 或 slot 2）。
    4.  对 R2 重复同样的操作。
*   **注意**：必须在**关机**状态下添加模块。如果已经开机，请先右键 Stop。

### 2. 物理连线 (Serial 串口线)
*   选择 **Serial** 线（红色闪电折线）。
*   连接 **R1** 的 `Serial 1/0/0` (或你加装的槽位端口) <--> **R2** 的 `Serial 1/0/0`。

### 3. 开机与基础配置 (打通物理层)
*   **配置 R1 (认证方/服务端)**：
    ```shell
    <Huawei> system-view
    [Huawei] sysname R1
    [R1] interface serial 1/0/0 (或者 serial 2/0/0，看你插在哪)
    [R1-Serial1/0/0] link-protocol ppp
    # 说明：华为串口默认就是 PPP 协议。
    [R1-Serial1/0/0] ip address 10.1.1.1 30
    [R1-Serial1/0/0] quit
    ```

*   **配置 R2 (被认证方/客户端)**：
    ```shell
    <Huawei> system-view
    [Huawei] sysname R2
    [R2] interface serial 1/0/0
    [R2-Serial1/0/0] link-protocol ppp
    [R2-Serial1/0/0] ip address 10.1.1.2 30
    [R2-Serial1/0/0] quit
    ```

*   **连通性测试**：
    *   此时还没配认证，直接 Ping 应该能通。
    *   在 **R1** 上输入：`ping 10.1.1.2`。
    *   **结果**：应该看到 `Reply from ...`。如果不通，检查线有没有插对接口。

---

## 二、 PAP 认证实战 (明文，两次握手)

> **场景**：R1 是服务端（主考官），R2 是客户端（考生）。R2 把账号密码明文发给 R1。

### 1. R1 配置 (主考官：存名单，开启认证)
```shell
# 第一步：在 AAA 里把 R2 的账号存进去
[R1] aaa
[R1-aaa] local-user user_r2 password cipher huawei123
[R1-aaa] local-user user_r2 service-type ppp
[R1-aaa] quit

# 第二步：在串口上开启 PAP 认证请求
[R1] interface serial 1/0/0
[R1-Serial1/0/0] ppp authentication-mode pap
# 大白话：R1 对 R2 说：“你要连我？请把你的 PAP 账号密码发过来。”
```

### 2. R2 配置 (考生：发账号)
```shell
[R2] interface serial 1/0/0
[R2-Serial1/0/0] ppp pap local-user user_r2 password simple huawei123
# 大白话：R2 乖乖地把账号 user_r2 和密码 huawei123 发给 R1。
```

### 3. 验证与重启接口
*   配置完认证后，协议状态可能不会立即变（因为 PPP 已经协商过了）。
*   **必须重启接口**触发重新协商：
    ```shell
    [R1-Serial1/0/0] shutdown
    [R1-Serial1/0/0] undo shutdown
    ```
*   **检查状态**：
    *   `display interface serial 1/0/0`
    *   如果 `Line protocol current state : UP`，说明认证通过。
    *   如果 `Line protocol` 是 `DOWN`，说明账号密码不对。

---

## 三、 CHAP 认证实战 (密文，三次握手)

> **场景**：更安全。R1 发起挑战，R2 计算哈希值回应。密码不在网线上跑。
> **准备**：为了测试效果，先**清除**之前的 PAP 配置。
> *   R1: `[R1-s1/0/0] undo ppp authentication-mode`
> *   R2: `[R2-s1/0/0] undo ppp pap local-user`

### 1. R1 配置 (主考官：存名单，开启认证)
```shell
# AAA 里已经有 user_r2 了，不用重复建，除非你想换密码。
# 在串口上开启 CHAP 认证
[R1] interface serial 1/0/0
[R1-Serial1/0/0] ppp authentication-mode chap
# 大白话：R1 对 R2 说：“我要考考你，我发个随机数，你把加密结果发回来。”
```

### 2. R2 配置 (考生：存密码，自动计算)
```shell
[R2] interface serial 1/0/0
[R2-Serial1/0/0] ppp chap user user_r2
[R2-Serial1/0/0] ppp chap password simple huawei123
# 大白话：R2 准备好自己的用户名和密码。收到随机数后，会自动用这个密码进行加密计算，然后回传。
```

### 3. 验证
*   同样，重启接口触发协商：
    ```shell
    [R1-Serial1/0/0] shutdown
    [R1-Serial1/0/0] undo shutdown
    ```
*   **抓包观察** (可选)：
    *   右键 R1 的 Serial 接口抓包。
    *   你会看到 `Challenge` (R1发)、`Response` (R2回)、`Success` (R1确认) 三个包。
    *   你看不到 `huawei123` 这个明文密码。

---

## 四、 保存配置 (别忘了!)

*   **R1**:
    ```shell
    <R1> save
    # 输入 y 确认
    ```
*   **R2**:
    ```shell
    <R2> save
    ```

---

## 五、 故障排查 (Troubleshooting)

### 1. 必杀技：打开 Debug 调试
如果你死活 Ping 不通，协议状态一直是 DOWN，不要猜，直接看设备怎么说：
```shell
<R1> debugging ppp all
<R1> terminal monitor
<R1> terminal debugging
# 然后重启接口 (shutdown -> undo shutdown)
```
*   **现象 A**：看到 `PAP/CHAP authentication failed`。
    *   *原因*：账号或密码错了。
*   **现象 B**：看到 `Timeout`。
    *   *原因*：链路不通，或者对面根本没配认证回应。
*   **用完记得关掉**：`<R1> undo debugging all`。

### 2. 常见问题
*   **Ping 不通？**
    *   检查 `display ip interface brief`，看 Serial 口是不是 UP。
    *   如果 Protocol 是 DOWN，大概率是认证没通过。
*   **eNSP 里没有 Serial 口？**
    *   请回顾“环境准备”，必须先关机，拖入 `2SA` 模块，再开机。
*   **Authentication-mode 选哪种？**
    *   两边必须一致？不对。是**服务端**决定用什么模式，**客户端**配合配置对应的参数。

### 3. 进阶挑战：双向认证
目前的配置是 R1 认证 R2（R1 是考官）。如果 R2 也不信任 R1，想反过来认证 R1 怎么办？
*   **思路**：两边都当“考官”，同时也都当“考生”。
*   **R1**：既配 `ppp authentication-mode`，也配 `ppp chap user/password`。
*   **R2**：同上。
*   只有双方都通过了对方的考试，链路才会 UP。这是最高安全级别的配置。
