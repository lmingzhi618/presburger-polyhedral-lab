# Contributing

This is a **personal learning repository** inspired by the book *Presburger Formula and Polyhedral Compilation*.  
Issues and pull requests are welcome for discussion and collaboration, but please note the following scope and guidelines.

---

## 🎯 Scope

- This project is for **educational and experimental** purposes only.  
- The goal is to explore **Presburger arithmetic**, **polyhedral compilation**, and related compiler theory.  
- The repository does **not** represent any company or organization.  
- Please avoid using or referencing any proprietary or confidential materials.

---

## ⚙️ Development Setup

You can clone the repo and install dependencies as follows:

```bash
git clone https://github.com/lmingzhi618/presburger-polyhedral-lab.git
cd presburger-polyhedral-lab
pip install -r requirements.txt

You may use a virtual environment:
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

🧩 Code Style Guidelines
	•	Use Python 3.10+
	•	Follow PEP8 conventions
	•	Use type hints and mypy when practical
	•	Each module should have basic unit tests under tests/
	•	Use docstrings ("""...""") to document functions and classes clearly
	•	Keep modules minimal and composable (each directory is one conceptual layer)


🧪 Testing

Run all tests:
```bash
pytest -v
```

For a specific test module:
```bash
pytest tests/test_presburger.py
```

🧠 Suggested Contribution Areas

If you want to add or improve something:
	•	Implement missing algorithms from the book
	•	Add visualizations for iteration domains or schedules
	•	Add new examples (matrix multiplication, stencil, reduction)
	•	Write explanatory notes or mathematical derivations in docs/

📜 Commit & Branching

Follow a clean commit convention:
```bash
feat: add polyhedral representation structure
fix: correct constraint projection
docs: update scheduling notes
test: add dependence analysis tests
refactor: reorganize codegen module
```

For larger work, create a branch:
```bash
git checkout -b feature/scheduler
```

📖 Documentation

Keep explanatory notes in docs/:
	•	ch1_presburger.md — Presburger arithmetic foundations
	•	ch2_polyhedral_model.md — Polyhedral representation
	•	ch3_dependence_analysis.md — Dependence polyhedra
	•	ch4_scheduling.md — Affine scheduling algorithms
	•	ch5_codegen.md — Code generation from schedules

Each doc should include both math definitions and implementation notes.

⚖️ License

MIT License.
By contributing, you agree that your code will be released under the same license.

⸻

🙌 Acknowledgment

This project exists to bridge theory and practice in compiler research.
Contributions, discussions, and educational forks are welcome!
