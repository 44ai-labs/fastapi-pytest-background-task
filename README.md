## FastAPI Background Task Test with Pytest

This is a simple test of FastAPI background tasks with Pytest.

### Setup

Using conda.

```bash
conda create python=3.11 --prefix /scratch/janniss/conda/background
conda activate /scratch/janniss/conda/background
pip install uv
uv pip install -r requirements.txt
```

### Run tests

```bash
make test
```
