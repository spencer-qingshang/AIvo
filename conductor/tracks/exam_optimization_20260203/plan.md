# 实施计划 - 2026 考期优化 (免考提速)

## 第一阶段：环境准备与旧文档分析
- [x] Task: 备份当前的 `自考专本连读极速毕业计划_专科优先版.md` 到 `conductor/archive/`。
- [x] Task: 提取所有受影响科目的考试代码与档期映射表，确保逻辑无误。

## 第二阶段：核心计划重构 (v2.0)
- [x] Task: 创建新文档 `C2=等待处理/2.4=日程/自考专本连读极速毕业计划_免考提速版.md`。
- [x] Task: 实现 2026 年考期逻辑重组：
    - 将 13793 标记为【免考】。
    - 移动 00022 (高数专) 至 2026.10 Sat PM。
- [x] Task: 实现 2027-2028 年本科联动插队：
    - 00023 (高数本) -> 2027.04 Sat PM。
    - 13003 (数据结构) -> 2027.10 Sat PM。
    - 13013 (高级语言) -> 2028.04 Sat PM。
- [x] Task: 更新里程碑预测日期（专科 2026.10 通关，本科 2028.04 通关）。

## 第三阶段：一致性校验与交付
- [ ] Task: 编写 Python 脚本 `verify_exam_schedule.py` 自动化检测新计划中的档期冲突。
- [ ] Task: 运行校验脚本并确保 0 冲突。
- [ ] Task: 更新 `GEMINI.md` 或相关仪表盘，反射最新的毕业预测时间。
- [ ] Task: Conductor - User Manual Verification '计划重构' (Protocol in workflow.md)

## 第四阶段：收尾
- [ ] Task: 提交所有文档变更并记录 Git Notes。
- [ ] Task: Conductor - User Manual Verification '最终交付' (Protocol in workflow.md)
