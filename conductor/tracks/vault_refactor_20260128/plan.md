# Implementation Plan - English Learning Vault Refactor

## Phase 1: Preparation & Setup [checkpoint: 194e378]
- [x] Task: Create new directory structure (00=仪表盘, 10=学习素材, 20=知识库, 30=复盘, 40=考试, 99=归档, 模板). [9da8b2c]
- [x] Task: Create `模板` folder and draft standard templates. [9da8b2c]
    - [x] Sub-task: Create `素材模板` template (metadata: source, status, tags).
    - [x] Sub-task: Create `单词模板` template (metadata: vocab, definition, examples).
    - [x] Sub-task: Create `语法模板` template (metadata: grammar, difficulty).
    - [x] Sub-task: Create `错题模板` template (metadata: error, reason, related_source).
    - [x] Sub-task: Create `复盘模板` template (metadata: review, date, score).
- [x] Task: Install/Enable Dataview plugin (User verification required). [User Verified]
- [x] Task: Conductor - User Manual Verification 'Phase 1: Preparation & Setup' (Protocol in workflow.md). [194e378]

## Phase 2: Automation & Dashboard Implementation [checkpoint: 754be95]
- [x] Task: Implement `English_Home.md` (Dashboard). [020da51]
    - [x] Sub-task: Add "Active Tasks" query (Dataview).
    - [x] Sub-task: Add "Review Queue" query (Dataview).
    - [x] Sub-task: Add "Statistics" view (DataviewJS).
- [x] Task: Implement dynamic views. [1c30b1f]
    - [x] Sub-task: Create `Mistake_Bank.md` with auto-aggregated errors.
    - [x] Sub-task: Create `Vocab_Book.md` with auto-aggregated vocabulary.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Automation & Dashboard Implementation' (Protocol in workflow.md). [754be95]

## Phase 3: Migration Script Development (Python) [checkpoint: abefd45]
- [x] Task: Analyze source file structure (`重点词汇与答疑笔记.md`, `每日学习进度表.md`). [Analysis Complete]
- [x] Task: Develop `scripts/migrate_notes.py`. [63a504b]
    - [x] Sub-task: Implement file reader to parse Markdown tables and lists from old notes.
    - [x] Sub-task: Implement content extractor for Vocab and Errors.
    - [x] Sub-task: Implement note generator to create new files based on templates.
    - [x] Sub-task: Dry run script and verify output.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Migration Script Development' (Protocol in workflow.md). [abefd45]

## Phase 4: Execution & Verification
- [x] Task: Run migration script for "Modern Family S01E01". [ba93c1d]
- [x] Task: Run migration script for "PETS-3 2015-Sep". [ba93c1d]
- [ ] Task: Manually verify migrated content in Obsidian Dashboard.
- [ ] Task: Archive remaining legacy files to `99_Archive`.
- [ ] Task: Update project `README.md` or `index.md` with new structure usage guide.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Execution & Verification' (Protocol in workflow.md).
