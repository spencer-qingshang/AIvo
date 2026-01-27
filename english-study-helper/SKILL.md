---
name: english-study-helper
description: Automates English learning workflows for Modern Family and PETS-3: initializes lesson files, logs learning errors, and archives vocabulary.
---

# English Study Helper

## Description
This skill acts as your personal English learning assistant for the **AIvo** project. It automates repetitive file management tasks defined in the Conductor workflow and enforces a strict "Pure Grammar" teaching strategy.

## When to Use
- **Start a new lesson:** "Prepare files for Modern Family S01E02", "Init lesson S01E03".
- **Log a mistake:** "Log error: misspelled 'coach'", "Record grammar mistake: forgot 'are'".
- **Add vocabulary:** "Add 'fawn over' to vocabulary", "Note down 'creed' with meaning".
- **Review:** "Check study status", "Show today's progress".

## 🧠 Teaching Strategy (CRITICAL)
**User Preference: Pure Grammar & Structure Analysis**

1.  **NO Translation Options:** Never use Chinese translations as multiple-choice options (User has subtitles).
2.  **NO Meaning/Context/Tone Questions:** Do NOT ask about what a sentence "means", the "emotion" of a character, or "subtext" unless it directly affects grammar (e.g., subjunctive mood).
3.  **FOCUS:**
    - **Syntactic Structures:** (e.g., Subject + Link Verb + Predicate)
    - **Parts of Speech:** (e.g., Verb acting as Noun)
    - **Tense Rules:** (e.g., Sequence of Tenses, Past Perfect vs. Past Simple)
    - **Sentence Patterns:** (e.g., Inversion, Ellipsis, Appositives)
    - **Morphology:** (e.g., Suffixes, prefixes, compound words)
4.  **Flow:** Analyze one sentence at a time.
5.  **Feedback:** Log technical grammatical errors to `练习反馈日志.md` immediately.

## Workflows

### 1. Initialize New Lesson
**Goal:** Create standard note files for a new Modern Family episode.
**Trigger:** "Init lesson [Season][Episode]" (e.g., S01E02)
**Actions:**
1.  Calculates path: `C4=归档资料/4.1=学习类/4.1.1=英语学习/美剧/摩登家庭/`.
2.  Creates files if missing:
    - `摩登家庭[SxxExx]_重点词汇与答疑笔记.md` (Standard Template)
    - `摩登家庭[SxxExx]_回译练习清单.md`
3.  Updates `每日学习进度表.md` with new study rows.

### 2. Log Learning Error
**Goal:** Quickly record a blind spot during practice without switching contexts.
**Trigger:** "Log error [content]"
**Actions:**
1.  Appends the error to the current day's section in `练习反馈日志.md`.
2.  Formats it as a checklist item `[ ]` for later review.

### 3. Record Key Vocabulary
**Goal:** Automatically archive a key word into the lesson's note file.
**Trigger:** "Add [word] to my vocabulary list", "Note down [word]".
**Actions:**
1.  Identifies current episode code.
2.  Calls `scripts/add_vocab.py` with word, meaning, and context.
3.  Inserts the row into the Markdown table or list in `重点词汇与答疑笔记.md`.

## Scripts

### `init_lesson.py`
- **Path:** `scripts/init_lesson.py`
- **Purpose:** Scaffolds note files and updates progress table.
- **Parameters:** `--season` (e.g., 01), `--episode` (e.g., 02)

### `log_error.py`
- **Path:** `scripts/log_error.py`
- **Purpose:** Appends formatted error entries to the daily log.
- **Parameters:** `--content` (Error description), `--type` (Optional category)

### `add_vocab.py`
- **Path:** `scripts/add_vocab.py`
- **Purpose:** Adds a vocabulary entry to the specific lesson note.
- **Parameters:** `--se` (S01E01), `--word`, `--phonetic` (optional), `--meaning`, `--context`

## Usage Examples
- `python scripts/init_lesson.py --season 01 --episode 02`
- `python scripts/log_error.py --content "Grammar: Negative Infinitive rule violated"`
- `python scripts/add_vocab.py --se S01E01 --word "fawn over" --meaning "奉承" --context "Everybody fawning over Lily"`

## Error Handling
- Checks if files already exist (prevents overwrite).
- Validates season/episode format.
- Handles missing table headers gracefully (appends to end).