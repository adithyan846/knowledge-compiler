# GitHub Development Workflow

This project follows an issue-driven development workflow.

## 1. Create an Issue

Every new feature, bug fix, or improvement starts with a GitHub Issue.

The issue should contain:

* A clear title
* Description
* Goals
* Acceptance criteria

Example:

```
#12 LLM Interpreter
```

---

## 2. Create a Branch

Create a feature branch linked to the issue.

```bash
git checkout -b feature/12-llm-interpreter
```

Branch naming:

```
feature/<issue-number>-<short-name>
```

Examples:

```
feature/12-llm-interpreter
feature/13-json-output
bugfix/21-title-parser
```

---

## 3. Implement the Feature

Develop the feature on the branch.

Make small, meaningful commits.

Example:

```bash
git commit -m "Implement prompt builder"
git commit -m "Add JSON validation"
git commit -m "Improve retry logic"
```

---

## 4. Push the Branch

```bash
git push origin feature/12-llm-interpreter
```

---

## 5. Open a Pull Request

Create a Pull Request from the feature branch into `main`.

Reference the related issue.

Example:

```
Closes #12
```

GitHub will automatically close the issue after merging.

---

## 6. Merge

Merge the Pull Request after review or testing.

Delete the feature branch if it is no longer needed.

---

## 7. Close the Issue

If it was not automatically closed, close it manually.

Each completed issue should represent one finished engineering task.

---

## 8. Complete the Milestone

When every issue belonging to a milestone is closed:

* Close the milestone.
* Verify the project is in a stable state.

Example:

```
v0.1.0
```

Completed issues:

* Parser
* Extractor
* Fragmenter
* Analyzer
* Rule Interpreter
* Schema Loader
* Schema Resolver
* Validator
* Writer
* Indexer
* Orchestrator

---

## 9. Create a Release

After closing the milestone, create a GitHub Release.

Example:

```
v0.1.0
```

Include:

* Summary
* Implemented features
* Known limitations
* Future work

---

## 10. Start the Next Milestone

Create the next milestone.

Example:

```
v0.2.0
```

Create new issues for the next set of features.

Example:

* LLM Interpreter
* Prompt Builder
* JSON KnowledgeUnit
* Retry Strategy
* Evaluation Dataset
* CLI
* Knowledge Graph

---

# Overall Workflow

```
Create Issue
        ↓
Create Branch
        ↓
Implement Feature
        ↓
Commit Changes
        ↓
Push Branch
        ↓
Open Pull Request
        ↓
Merge into Main
        ↓
Close Issue
        ↓
Complete Milestone
        ↓
Create Release
        ↓
Start Next Milestone
```

---

# Versioning

```
v0.1.0  Initial deterministic compiler
v0.1.1  Bug fixes
v0.2.0  LLM interpreter
v0.3.0  Retrieval improvements
v1.0.0  Stable release
```

---

# Guiding Principle

* One issue = one engineering task.
* One branch = one issue.
* One milestone = one release.
* One release = one stable version.

