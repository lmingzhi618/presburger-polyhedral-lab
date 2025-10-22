# presburger-polyhedral-lab
A minimal research framework exploring Presburger arithmetic and polyhedral compilation.

## 🌍 Overview

This project is inspired by the book **“Presburger Formula and Polyhedral Compilation”**, aiming to bridge theory and implementation.  
It serves as a **hands-on laboratory** for learning and experimenting with:

- Presburger arithmetic and affine constraints
- Polyhedral representation of loop nests
- Dependence analysis and scheduling
- Affine transformations and code generation
- Visualization of polyhedra and scheduling results

The goal is to **translate theory into working prototypes** and to document every step for educational and research use.

---

## 🧩 Project Structure  

```
presburger-polyhedral-lab/
│
├── docs/ # Reading notes and algorithm explanations
│ ├── ch1_presburger.md
│ ├── ch2_polyhedral_model.md
│ ├── ch3_dependence_analysis.md
│ ├── ch4_scheduling.md
│ └── ch5_codegen.md
│
├── src/ # Core implementation
│ ├── presburger/ # Integer sets, constraints, union, intersection
│ ├── polyhedral/ # Iteration domains, access relations
│ ├── dependence/ # Dependence graph and polyhedron
│ ├── scheduler/ # Feautrier / Pluto-style scheduling
│ └── codegen/ # Loop reconstruction and affine codegen
│
├── examples/ # Experiments and demos
│ ├── matrix_multiply/
│ ├── stencil_loop/
│ └── reduction/
│
├── tests/ # Unit and regression tests
│
├── papers/ # Reference papers, BibTeX, summary notes
│ └── references.bib
│
└── README.md
```

## 🔧 Dependencies

- Python ≥ 3.10  
- `sympy` for symbolic math  
- `z3-solver` or `pulp` for constraint solving  
- `matplotlib` / `plotly` for visualization  
- (Optional) `islpy` for interoperability with ISL

---

## 🚀 Getting Started

```bash
git clone https://github.com/<yourname>/presburger-polyhedral-lab.git
cd presburger-polyhedral-lab
pip install -r requirements.txt

Example usage (coming soon):
-- python examples/matrix_multiply/demo.py

📚 Learning Roadmap
Stage	Topic	Goal
1️⃣	Presburger arithmetic	Implement set and constraint manipulation
2️⃣	Polyhedral representation	Define iteration domains and access functions
3️⃣	Dependence analysis	Build dependence polyhedra
4️⃣	Scheduling	Apply affine scheduling algorithms
5️⃣	Code generation	Produce transformed loop nests
6️⃣	Visualization	Plot iteration spaces and transformations
📖 Reference Materials

Presburger Formula and Polyhedral Compilation

Feautrier, P. “Dataflow analysis of array and scalar references.” (1991)

Bondhugula, U. et al. “Pluto: Automatic parallelization using affine transformations.” (2008)

⚖️ License

MIT License.
This project is for personal learning and research only and is not affiliated with MathWorks.

🙌 Acknowledgment

This repository is part of my self-learning journey bridging compiler theory, high-performance computing, and affine transformations.
Contributions and discussions are welcome.
