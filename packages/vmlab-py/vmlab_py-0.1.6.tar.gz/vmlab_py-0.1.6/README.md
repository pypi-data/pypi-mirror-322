# vmlab-py-package

pypi link : [vmlab_py](https://pypi.org/project/vmlab-py/)

## Requirements

```bash
pip install maturin
```

## Build the python package

```bash
maturin build --release
```

## Test in locally

```
pip install target/wheels/{GENERATED_WHEELS_NAME}.whl
```

## Publish to PyPI

```
maturin publish
```

