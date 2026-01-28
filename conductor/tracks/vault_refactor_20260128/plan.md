# Implementation Plan - English Learning Vault Refactor

## Phase 1: Preparation & Setup
- [x] Task: Create new directory structure (00_Dashboard, 10_Inputs, 20_Knowledge, 30_Review, 40_Exam, 99_Archive, Templates). [f231320]
- [ ] Task: Create `Templates` folder and draft standard templates.
    - [ ] Sub-task: Create `Source Note` template (metadata: source, status, tags).
    - [ ] Sub-task: Create `Vocab Note` template (metadata: vocab, definition, examples).
    - [ ] Sub-task: Create `Grammar Note` template (metadata: grammar, difficulty).
    - [ ] Sub-task: Create `Error Log` template (metadata: error, reason, related_source).
    - [ ] Sub-task: Create `Daily Review` template (metadata: review, date, score).
- [ ] Task: Install/Enable Dataview plugin (User verification required).
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Preparation & Setup' (Protocol in workflow.md).

## Phase 2: Automation & Dashboard Implementation
- [ ] Task: Implement `English_Home.md` (Dashboard).
    - [ ] Sub-task: Add "Active Tasks" query (Dataview).
    - [ ] Sub-task: Add "Review Queue" query (Dataview).
    - [ ] Sub-task: Add "Statistics" view (DataviewJS).
- [ ] Task: Implement dynamic views.
    - [ ] Sub-task: Create `Mistake_Bank.md` with auto-aggregated errors.
    - [ ] Sub-task: Create `Vocab_Book.md` with auto-aggregated vocabulary.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Automation & Dashboard Implementation' (Protocol in workflow.md).

## Phase 3: Migration Script Development (Python)
- [ ] Task: Analyze source file structure (`重点词汇与答疑笔记.md`, `每日学习进度表.md`).
- [ ] Task: Develop `scripts/migrate_notes.py`.
    - [ ] Sub-task: Implement file reader to parse Markdown tables and lists from old notes.
    - [ ] Sub-task: Implement content extractor for Vocab and Errors.
    - [ ] Sub-task: Implement note generator to create new files based on templates.
    - [ ] Sub-task: Dry run script and verify output.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Migration Script Development' (Protocol in workflow.md).

## Phase 4: Execution & Verification
- [ ] Task: Run migration script for "Modern Family S01E01".
- [ ] Task: Run migration script for "PETS-3 2015-Sep".
- [ ] Task: Manually verify migrated content in Obsidian Dashboard.
- [ ] Task: Archive remaining legacy files to `99_Archive`.
- [ ] Task: Update project `README.md` or `index.md` with new structure usage guide.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Execution & Verification' (Protocol in workflow.md).
