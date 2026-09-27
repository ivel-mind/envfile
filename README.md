# envfile

Read and write a small subset of `.env` files.

Handles comments, `export `, empty values, and quotes around values that contain spaces. Does not expand variables and does not look at the process environment.

```python
from envfile import parse_env, emit_env

data = parse_env("NAME=Ada\n")
print(emit_env(data))
```

```bash
python -m unittest test_envfile.py
```

MIT
