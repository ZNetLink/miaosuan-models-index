#!/usr/bin/env python3
import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("jsonschema is required. pip install jsonschema", file=sys.stderr)
    sys.exit(2)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schema"


def load_json(p: Path):
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_one(instance_path: Path, schema_path: Path):
    instance = load_json(instance_path)
    schema = load_json(schema_path)
    try:
        jsonschema.validate(instance=instance, schema=schema)
    except jsonschema.ValidationError as e:
        print(f"✗ {instance_path} invalid: {e.message}")
        return False
    except jsonschema.SchemaError as e:
        print(f"Schema error in {schema_path}: {e}")
        return False
    else:
        print(f"✓ {instance_path} valid against {schema_path.name}")
        return True


def main():
    ok = True
    # validate all models
    models_dir = ROOT / "models"
    if models_dir.exists():
        for p in sorted(models_dir.glob("*.json")):
            ok = validate_one(p, SCHEMA_DIR / "model.schema.json") and ok

    # validate all packages
    packages_dir = ROOT / "packages"
    if packages_dir.exists():
        for p in sorted(packages_dir.glob("*.json")):
            ok = validate_one(p, SCHEMA_DIR / "package.schema.json") and ok

    # validate index.json if present
    idx = ROOT / "index.json"
    if idx.exists():
        ok = validate_one(idx, SCHEMA_DIR / "index.schema.json") and ok

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

