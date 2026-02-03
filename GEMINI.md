# Project Context: AIvo Personal Knowledge Base

## Overview
This directory (`G:\Desktop\学习\AIvo`) is a personal knowledge base managed with **Obsidian**. It functions as a comprehensive system for learning, personal management, and interest tracking. The vault is version-controlled using Git.

## Directory Structure
The vault follows a specific workflow-based organization method (C1-C5):

- **`C1=收集箱` (Inbox)**
  - Purpose: Temporary storage for unprocessed notes and raw materials.
  - Content examples: Notes on Marxism (`马克思*.md`), Xi Jinping Thought (`习近平*.md`), and raw text files.

- **`C2=等待处理` (Pending/Actionable)**
  - Purpose: Active tasks, daily logs, and schedules.
  - Subdirectories:
    - `2.1=备忘录`: Memos.
    - `2.4=日程`: Schedules, study plans (Self-taught exams/自考).
    - `2.5=日记本`: Daily diaries (e.g., May 2023 entries).

- **`C3=将来可能` (Someday/Maybe)**
  - Purpose: Future ideas, planning, and reviews.

- **`C4=归档资料` (Archives/Reference)**
  - Purpose: Permanent storage for reference materials, organized by domain.
  - Subdirectories:
    - `4.1=学习类`: Academic subjects (English, Computer Science, Math).
    - `4.2=工作类`: Work-related logs (Map making).
    - `4.3=生活类`: Life records and news.

- **`C5=专题研究` (Projects/Topics)**
  - Purpose: Active deep-dives into specific hobbies or subjects.
  - Topics:
    - `5.1=英雄联盟`: League of Legends (ADC/Kai'Sa).
    - `5.2=尤克里里`: Ukulele practice.
    - `5.4=PS学习`: Photoshop tutorials.
    - `5.5=模型学习`: 3D Modeling (Crab rigging).
    - `5.6=云顶之弈`: Teamfight Tactics (TFT) strategies.

## Key Files & Scripts

- **`extract_ch6.py`**
  - **Type:** Python Script.
  - **Purpose:** a utility script to extract specific chapters (specifically Chapter 6) from the file `C1=收集箱/习近平.md` and save it to `temp_ch6.md`. It uses regex matching for chapter headers.
  - **Usage:** Run via `python extract_ch6.py`.

- **`.gitignore`**
  - Configured to ignore Obsidian workspace state files (`workspace.json`).

## Obsidian Configuration
- **Plugins:**
  - `obsidian-git`: For syncing the vault with a git repository.
  - `obsidian-markmind`: For creating mind maps (found in `C4` and `C5` folders).
  - `obsidian-custom-attachment-location`: Manages attachment (image) paths.
  - `easy-typing-obsidian`: Enhances text input.

## 🎓 自考毕业里程碑 (2026 优化版)
- **专科笔试通关预测**：2026年10月 (因免考 13793 提前半年)
- **本科笔试通关预测**：2028年04月 (因计划整体前移提前半年)
- **核心策略**：免考《计算机程序设计基础 (13793)》，腾出周六下午黄金档期。

## Usage Guidelines
- **Language:** The primary language of notes is **Chinese**.
- **Note-Taking:** Notes are Markdown-formatted.
- **Workflow:** New information enters `C1`, gets processed into `C2` (tasks) or `C5` (projects), and eventually archived in `C4`.
