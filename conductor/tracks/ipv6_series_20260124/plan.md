# Implementation Plan - Project 4 IPv6 Practical Series

本计划旨在创建一套完整的 IPv6 实战手册系列（共4个文件）。每一步都将确保从零基础开始，涵盖从拓扑搭建到配置验证的全过程。

## Phase 1: 环境准备与模板统一
- [x] Task: 统一实战手册的文档模板，确保“大白话解释 + 详细步骤 + 常见报错”的风格一致。 [87da5d7]
- [ ] Task: Conductor - User Manual Verification 'Phase 1: 环境准备' (Protocol in workflow.md)

## Phase 2: 编写项目 4.1 - IPv6 地址基础配置实战
- [x] Task: 编写“拓扑搭建”章节：指导用户在 eNSP 中手动拖拽 3 台 AR2220 路由器和 2 台 PC，并指定手动连接的接口编号。 [de480c5]
- [x] Task: 编写“基础配置”章节：包含全局开启 IPv6 命令，以及在各接口配置全球单播地址和链路本地地址的详细命令。 [de480c5]
- [x] Task: 编写“PC 配置”章节：指导用户在 PC 界面填写 IPv6 地址、前缀长度和网关。 [de480c5]
- [x] Task: 编写“验证”章节：提供 `display ipv6 interface brief` 查看状态及 `ping ipv6` 测试直连通性的步骤。 [de480c5]
- [ ] Task: Conductor - User Manual Verification 'Phase 2: 编写项目 4.1 - IPv6 地址基础配置实战' (Protocol in workflow.md)

## Phase 3: 编写项目 4.2 - IPv6 静态与默认路由实战
- [x] Task: 编写“环境准备”章节：说明此实验基于 4.1 的基础配置。 [f2e263e]
- [x] Task: 编写“静态路由配置”章节：详细列出 R1、R2、R3 需要配置的 `ipv6 route-static` 命令。 [f2e263e]
- [x] Task: 编写“默认路由配置”章节：讲解 `:: 0` 的含义及在 R1 上配置默认路由的步骤。 [f2e263e]
- [x] Task: 编写“验证与原理”章节：指导用户查看 IPv6 路由表，并解释下一跳使用链路本地地址的优势。 [f2e263e]
- [ ] Task: Conductor - User Manual Verification 'Phase 3: 编写项目 4.2 - IPv6 静态与默认路由实战' (Protocol in workflow.md)

## Phase 4: 编写项目 4.3 - RIPng 动态路由实战
- [x] Task: 编写“清理配置”章节：指导用户使用 `undo` 命令删除上一阶段配置的静态路由，恢复纯净环境。 [0a90e09]
- [x] Task: 编写“RIPng 配置”章节：包含全局启动进程和接口下使能 RIPng 的详细步骤，强调与 IPv4 RIP 的区别。 [0a90e09]
- [x] Task: 编写“验证”章节：指导用户通过查看 RIPng 路由表和邻居状态来确认配置成功。 [0a90e09]
- [ ] Task: Conductor - User Manual Verification 'Phase 4: 编写项目 4.3 - RIPng 动态路由实战' (Protocol in workflow.md)

## Phase 5: 编写项目 4.4 - OSPFv3 动态路由实战
- [x] Task: 编写“清理配置”章节：删除 RIPng 配置。 [366d106]
- [x] Task: 编写“OSPFv3 核心配置”章节：详细讲解 Router-ID 的手动配置、OSPFv3 进程启动以及接口下绑定 Area 0 的步骤。 [366d106]
- [x] Task: 编写“验证与排错”章节：提供查看 OSPFv3 邻居状态 (Full) 的命令，并列出新手常见的漏掉“ipv6 enable”等报错情况。 [366d106]
- [ ] Task: Conductor - User Manual Verification 'Phase 5: 编写项目 4.4 - OSPFv3 动态路由实战' (Protocol in workflow.md)
