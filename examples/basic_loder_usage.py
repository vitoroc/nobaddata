import pandas as pd

import nobaddata.checks  # required to register built-in checks
from nobaddata.core.engine import Engine

df = pd.DataFrame({"email": ["a", None, "b"], "age": [10, 200, 30]})

engine = Engine.from_yaml("examples/config.yaml")

results = engine.run(df)

for r in results:
    print(r)
