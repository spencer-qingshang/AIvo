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
... (此处省略已有内容)

### 3. Record Key Vocabulary
**Goal:** Automatically archive a key word into the lesson's vocabulary table.
**Trigger:** "Add [word] to my vocabulary list", "Note down [word] with meaning [meaning]".
**Actions:**
1.  Identifies the current episode code (e.g., S01E01).
2.  Calls `scripts/add_vocab.py` with word, phonetic, and meaning.
3.  Ensures the row is correctly inserted into the Markdown table.

## Scripts
...
### `add_vocab.py`
- **Path:** `scripts/add_vocab.py`
- **Purpose:** Adds a row to the vocabulary table in the lesson note.
- **Parameters:** `--se`, `--word`, `--phonetic`, `--meaning`, `--context`

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

## 🧠 Teaching Strategy (User Preferences)
- **NO Meaning/Context/Tone:** Do NOT ask about what a sentence "means", the "emotion" of a character, or "subtext".
- **PURE Grammar Focus:** Only ask about syntactic structures, part of speech (词性), tense rules (时态规则), sentence patterns (句式), and morphological rules (构词/变形).
- **Flow:** One sentence at a time.
- **Feedback:** Log technical grammatical errors to `练习反馈日志.md`.

## Error Handling
- Checks if files already exist (prevents overwrite).
- Validates season/episode format.
