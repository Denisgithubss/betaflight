# Update Matek SEC1 OSD Position Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update `osd_sec1_tag_pos` to `2528` in `matekf405te_sd_restore_clean_v2.txt` and add a comment.

**Architecture:** 
1. Modify `matekf405te_sd_restore_clean_v2.txt`.
2. Replace `set osd_sec1_tag_pos = 2048` with a comment and the new value.
3. Verify and commit.

**Tech Stack:** Shell, Git.

---

### Task 1: Update Configuration File

**Files:**
- Modify: `matekf405te_sd_restore_clean_v2.txt`

- [ ] **Step 1: Replace value and add comment**

Old string:
```text
set osd_sec1_tag_pos = 2048
```

New string:
```text
# Position: lower-left corner, x=0,y=15
set osd_sec1_tag_pos = 2528
```

- [ ] **Step 2: Run verification**

Run: `grep -C 2 "osd_sec1_tag_pos" matekf405te_sd_restore_clean_v2.txt`
Expected:
```text
set osd_dropper_pos = 2082
# Position: lower-left corner, x=0,y=15
set osd_sec1_tag_pos = 2528
# removed unsupported: set dropper_pos = 34
```

### Task 2: Commit Changes

- [ ] **Step 1: Check status**

Run: `git status`

- [ ] **Step 2: Add and commit**

Run: `git add matekf405te_sd_restore_clean_v2.txt && git commit -m "Update Matek SEC1 OSD position to lower-left"`
