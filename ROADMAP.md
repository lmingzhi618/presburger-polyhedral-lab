# 🧭 Project Roadmap — Presburger Polyhedral Lab

This document tracks the implementation progress of concepts and examples
from _Presburger Formulas and Polyhedral Compilation_ (S. Verdoolaege).

Each major section below corresponds to a chapter or concept in the book,
mapped to a Python module under `src/`.

---

## 1. Introduction and Tools
| Section | Description | Status |
|----------|--------------|--------|
| 1.1 | Polyhedral Compilation overview | ✅ Documented in README |
| 1.2.1 | `pet` (Polyhedral Extraction Tool) | ⚙️ Planned interface notes in `docs/tools.md` |
| 1.2.2 | `iscc` | ⏳ Future integration |
| 1.2.3 | Python interface | ✅ Project base uses pure Python (`islpy`, `sympy`) |

---

## 2. Sets of Named Integer Tuples
| Section | Description | Status |
|----------|--------------|--------|
| 2.1 | Named Integer Tuples | ⚙️ In progress — `polyhedral/sets.py` |
| 2.2 | Basic Set Operations | ⏳ Planned for later stage |
| 2.3 | Binary Relations | ⏳ To implement in `polyhedral/relations.py` |
| 2.4 | Wrapped Relations | ⏳ Optional extension (`wrapped_relations.py`) |

---

## 3. Presburger Sets and Relations
| Section | Description | Status |
|----------|--------------|--------|
| 3.1 | Intensional Descriptions | ✅ Implemented in `presburger/constraint.py` |
| 3.2 | Presburger Formulas | ⚙️ To implement in `presburger/formula.py` |
| 3.3 | Presburger Sets and Relations | ⏳ Planned (integration of formulas + sets) |
| 3.4 | Syntactic Sugar | ⏳ Utility layer for readability |
| 3.5 | Lexicographic Order | ⏳ Future: ordering constraints |
| 3.6 | Space-Local Operations | ⏳ Later optimization |
| 3.7 | Simplification and Quantifier Elimination | ⏳ To implement in `presburger/simplifier.py` |
| 3.8 | Sampling and Scanning | ⏳ Optional visualization utilities |
| 3.9 | Beyond Presburger Formulas | ⏳ Long-term exploration topic |

---

## 4. Piecewise Quasi-Affine Expressions
| Section | Description | Status |
|----------|--------------|--------|
| 4.1 | Quasi-Affine Expressions | ⏳ Planned `polyhedral/expressions.py` |
| 4.2 | Creation | ⏳ Planned |
| 4.3 | Operations (sum, union, product, pullback) | ⏳ Future implementation |
| 4.4 | Conversions | ⏳ Low priority |

---

## 5. Polyhedral Model
| Section | Description | Status |
|----------|--------------|--------|
| 5.1 | Main Concepts | ⚙️ Ongoing (`polyhedral/model.py`) |
| 5.2 | Instance Sets | ⏳ Planned |
| 5.3 | Access Relations | ⏳ Planned (`polyhedral/access.py`) |
| 5.4 | Dependence Relations | ⚙️ Handled in `dependence/analysis.py` |
| 5.5 | Data Layout Transformations | ⏳ Planned |
| 5.6 | Schedule Definition & Representation | ⏳ To implement (`scheduler/schedule.py`) |
| 5.7 | Context | ⏳ Future |
| 5.8 | Polyhedral Statements | ⏳ Long-term goal |
| 5.9 | Operations | ⏳ Post-scheduler phase |

---

## 6. Dependence Analysis
| Section | Description | Status |
|----------|--------------|--------|
| 6.1 | Dependence Analysis | ⚙️ Planned in `dependence/analysis.py` |
| 6.2 | Dataflow Analysis | ⏳ Planned |
| 6.3 | Approximate Dataflow Analysis | ⏳ Planned (`dependence/approximate.py`) |
| 6.4 | Applications of Approximate Dataflow Analysis | ⏳ Future extension |
| 6.5 | Kills | ⏳ Planned |
| 6.6 | Live-Out Accesses | ⏳ Planned (`dependence/live_out.py`) |

---

## Supporting Materials
| Area | Description | Status |
|-------|-------------|--------|
| Documentation | Background and examples | ⚙️ In progress under `docs/` |
| Papers | References and notes | ✅ `papers/` directory ready |
| Examples | Code for common kernels | ⚙️ Matrix multiply, stencil, reduction |
| Tests | Pytest-based unit testing | ✅ Working (`pytest.ini`, `tests/`) |

---

## Legend
✅ Complete ⚙️ In Progress ⏳ Planned / Not Yet Started

---
