# NoBadData

![python](https://img.shields.io/badge/python-3.10%2B-blue)
![license](https://img.shields.io/badge/license-MIT-green)

A lightweight and extensible Python framework for **data quality checks** on tabular datasets.

Built to define reusable validation rules and run them consistently across datasets.

---

## 🚀 Features

* Modular **check-based architecture**
* Standardized output via `CheckResult`
* Built-in **execution engine**
* Robust error handling (no pipeline breaking)
* Incrementally tested
* Easy to extend with custom checks

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/vitoroc/nobaddata.git
cd nobaddata
```

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

Install dependencies:

```bash
pip install -e .
pip install pytest pytest-cov
```

---

## 🧠 Quick Example

```python
import pandas as pd

from nobaddata.core.engine import Engine
from nobaddata.checks.nulls import NullCheck

df = pd.DataFrame({
    "email": ["a@example.com", None, "b@example.com"]
})

checks = [
    NullCheck(column="email", threshold=0.0)
]

engine = Engine(checks)
results = engine.run(df)

for r in results:
    print(r)
```

---

## 🧱 Project Structure

```bash
nobaddata/
├── nobaddata/
│   ├── core/
│   │   ├── check.py
│   │   └── engine.py
│   ├── models/
│   │   └── result.py
│   └── checks/
│       └── nulls.py
│
├── tests/
│   ├── core/
│   └── checks/
│
├── examples/
├── pyproject.toml
└── README.md
```

---

## 🔍 Core Concepts

### Check

Abstract base class that defines a validation rule.

```python
class Check:
    def run(self, df) -> CheckResult:
        ...
```

---

### CheckResult

Standardized output for all checks:

* `check_name`
* `status` → PASS / FAIL / ERROR
* `severity`
* `details`

---

### Engine

Executes multiple checks safely:

* runs all checks
* isolates failures
* returns structured results

---

## 🧪 Running Tests

Run:

```bash
pytest
```

Open HTML report:

```bash
htmlcov/index.html
```

---

## 📊 Example Output

```text
CheckResult(
  check_name='null_check_email',
  status='FAIL',
  severity='WARNING',
  details={
    'null_count': 1,
    'total_rows': 3,
    'null_ratio': 0.33
  }
)
```

---
## 📓 Note
```
import nobaddata.checks  # required to register built-in checks
```

---

## 📄 License

GNU GENERAL PUBLIC LICENSE
