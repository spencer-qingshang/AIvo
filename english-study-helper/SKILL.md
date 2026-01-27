---
name: english-study-helper
description: Automates English learning workflows for Modern Family and PETS-3: initializes lesson files, generates vocabulary quizzes, and logs learning errors.
---

# English Study Helper

## Description
This skill acts as your personal English learning assistant for the **AIvo** project. It automates the repetitive file management tasks defined in the Conductor workflow, allowing you to focus on listening and speaking.

## When to Use
- **Start a new lesson:** "Prepare files for Modern Family S01E02", "Init lesson S01E03".
- **Log a mistake:** "Log error: misspelled 'coach'", "Record grammar mistake: forgot 'are'".
- **Review:** "Show me today's learning progress", "Check study status".

## Workflows

### 1. Initialize New Lesson (Modern Family)
**Goal:** Create standard note files for a new episode.
**Trigger:** "Init lesson [Season][Episode]" (e.g., S01E02)
**Actions:**
1.  Calculates the correct path: `C4=归档资料/4.1=学习类/4.1.1=英语学习/美剧/摩登家庭/`.
2.  Creates 3 files if they don't exist:
    - `摩登家庭[SxxExx]_重点词汇与答疑笔记.md`
    - `摩登家庭[SxxExx]_回译练习清单.md`
    - Updates `每日学习进度表.md` with new rows.

### 2. Log Learning Error
**Goal:** Quickly record a blind spot during practice without switching contexts.
**Trigger:** "Log error [content]"
**Actions:**
1.  Appends the error to the current day's section in `练习反馈日志.md`.
2.  Formats it as a checklist item `[ ]` so it can be reviewed later.

## Scripts

### `init_lesson.py`
- **Path:** `scripts/init_lesson.py`
- **Purpose:** Scaffolds the markdown files for a specific episode.
- **Parameters:** `--season`, `--episode`

### `log_error.py`
- **Path:** `scripts/log_error.py`
- **Purpose:** Appends formatted error entries to the daily log.
- **Parameters:** `--content`, `--type` (optional)

## Usage Examples
- `python scripts/init_lesson.py --season 01 --episode 02`
- `python scripts/log_error.py --content "Misspelled 'definitely' as 'definatly'"`

## Error Handling
- Checks if files already exist (prevents overwrite).
- Validates season/episode format.
