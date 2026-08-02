# Siesta Knowledge Schema

## Purpose

The schema defines how knowledge is represented inside the Siesta knowledge base.

Its goals are:

* Keep knowledge consistent.
* Make retrieval predictable.
* Make files understandable by both humans and AI.
* Separate content from metadata.
* Prevent duplicated or conflicting knowledge.

The schema is designed to be independent of any specific AI model, embedding system, database, or retrieval engine.

---

# Design Principles

## 1. One Knowledge Unit Per File

Each file should represent exactly one:

* concept
* question
* workflow
* troubleshooting guide
* decision
* reference

Do not combine unrelated knowledge into a single file.

---

## 2. Organize by Topic

Folders represent subjects.

Example:

```text
knowledge/
└── drone/
    └── esc/
```

Files represent individual knowledge units.

Example:

```text
how_to_flash_esc_through_flight_controller.yaml
```

Knowledge type is stored inside the file.

Example:

```yaml
types:
  - workflow
  - troubleshooting
```

---

## 3. Facts Have One Owner

Every fact should have exactly one canonical source.

Good:

```text
why_am32_flashing_requires_telemetry.yaml
```

Other files reference it.

Bad:

The same fact copied into multiple workflows.

Duplicated facts eventually become inconsistent.

---

## 4. Workflows Reference Facts

Workflows describe actions.

Facts explain why those actions exist.

Example:

Workflow:

```text
Verify telemetry connection.
```

Reference:

```text
why_am32_flashing_requires_telemetry.yaml
```

---

## 5. Metadata Describes Knowledge

Folders answer:

> What subject is this?

File names answer:

> What specific knowledge is this?

Metadata answers:

> What type of knowledge is this?

Keep these responsibilities separate.

---

## 6. Human Readability Comes First

Knowledge files are expected to be read directly.

Someone opening a file in a text editor should understand it without needing special tooling.

Machine-readable structure should never significantly reduce human readability.

---

# Schema Structure

Every knowledge file follows the Core Schema.

Additional schemas extend the Core Schema depending on the knowledge type.

```text
Core
│
├── Workflow
├── Fact
├── Troubleshooting
├── Decision
└── Reference
```

---

# Core Schema

Every knowledge file must satisfy `core.yaml`.

Required fields:

* schema_version
* id
* title
* tags
* types
* summary

Optional fields:

* related
* metadata

---

# Extension Schemas

## Workflow

Use for procedures or sequences of actions.

Typical fields:

* safety_rules
* prerequisites
* workflow
* verification
* troubleshooting
* engineering_notes

---

## Fact

Use for verified engineering knowledge.

Typical fields:

* fact
* explanation
* consequences
* evidence

---

## Troubleshooting

Use for diagnosing failures.

Diagnostics should be ordered according to engineering value:

Expected Value = Likelihood × Ease of Verification

Start with:

* most likely
* cheapest to verify
* least destructive

Do not begin with expensive or unlikely solutions.

---

## Decision

Use for engineering decisions.

Document:

* decision
* rationale
* alternatives
* consequences

---

## Reference

Use for information that primarily links or points to other knowledge.

Examples:

* documentation
* manuals
* specifications
* related resources

---

# Choosing Types

Knowledge can belong to multiple types.

Example:

```yaml
types:
  - workflow
  - troubleshooting
```

Avoid creating separate copies simply because information belongs to multiple categories.

---

# Relationships

Use `related` to connect knowledge units.

Prefer references instead of duplicated information.

Example:

```yaml
related:
  - esc.am32.telemetry_required
  - esc.motor.kv.configuration
```

---

# Naming Guidelines

Use descriptive filenames.

Prefer:

```text
how_to_flash_esc_through_flight_controller.yaml
```

instead of:

```text
flash.yaml
```

Prefer:

```text
why_motor_kv_must_be_configured.yaml
```

instead of:

```text
motor.yaml
```

A filename should clearly answer the question:

> What knowledge does this file contain?

---

# Schema Evolution

The schema is expected to evolve.

Every knowledge file contains:

```yaml
schema_version: 1
```

Future versions should remain backward compatible whenever practical.

Schema changes should be intentional and documented.

---

# Philosophy

The knowledge base is not built to store information.

It is built to retrieve the correct information at the correct time.

Every design decision should improve:

* consistency
* maintainability
* discoverability
* retrieval quality
* long-term reliability

The architecture should remain useful regardless of future AI models or retrieval technologies.

