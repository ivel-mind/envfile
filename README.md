# envfile

Read and write a small subset of `.env` files.

Handles comments, `export `, empty values, and quotes around values that contain spaces. Does not expand variables and does not look at the process environment.

```python
from envfile import parse_env, emit_env, overlay_env, changed_keys

data = parse_env("NAME=Ada\n")
print(emit_env(overlay_env(data, {"NAME": "Grace"})))
changed_keys({"NAME": "Ada"}, {"NAME": "Grace"})  # ["NAME"]
```

```bash
python -m unittest test_envfile.py
```

MIT
