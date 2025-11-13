import argparse
import json
import os
import datetime
from pathlib import Path


def semver_key(v: str):
    # very small semver key: only numbers, ignore prerelease/build for ordering
    parts = v.split("-", 1)[0].split("+")[0].split(".")
    nums = []
    for p in parts[:3]:
        try:
            nums.append(int(p))
        except ValueError:
            nums.append(-1)
    while len(nums) < 3:
        nums.append(0)
    return tuple(nums)


def parse_date(d: str):
    try:
        return datetime.datetime.strptime(d, "%Y-%m-%d")
    except Exception as e:
        print(f"Failed to parse date {d}: {e}")
        return None


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def collect_models(models_dir: Path):
    out = []
    if not models_dir.exists():
        return out
    for p in sorted(models_dir.glob("*.json")):
        slug = p.stem
        try:
            m = load_json(p)
        except Exception as e:
            raise RuntimeError(f"Failed to parse model {p}: {e}")

        versions = m.get("versions", [])
        latest_ver = None
        latest_date = None
        if versions:
            latest_ver = sorted(
                [v.get("version", "0.0.0") for v in versions if isinstance(v, dict) and v.get("version")],
                key=semver_key,
                reverse=True,
            )[0]
            # pick most recent date
            dates = [parse_date(v.get("date")) for v in versions if isinstance(v, dict) and v.get("date")]
            dates = [d for d in dates if d is not None]
            latest_date = max(dates).strftime("%Y-%m-%d") if dates else None

        author_obj = m.get("author")
        author = None
        if isinstance(author_obj, dict):
            author = author_obj.get("name") or json.dumps(author_obj, ensure_ascii=False)
        elif isinstance(author_obj, str):
            author = author_obj

        out.append(
            {
                "name": slug,
                "description": m.get("description", ""),
                "author": author or "",
                "latest_version": latest_ver,
                "last_updated": latest_date,
                "labels": m.get("labels", []),
            }
        )
    return out


def collect_packages(packages_dir: Path, model_index: dict):
    out = []
    if not packages_dir.exists():
        return out
    for p in sorted(packages_dir.glob("*.json")):
        slug = p.stem
        try:
            pkg = load_json(p)
        except Exception as e:
            raise RuntimeError(f"Failed to parse package {p}: {e}")

        models = pkg.get("models", [])
        # derive latest version/date from referenced models if possible
        latest_date = pkg.get("date")
        author_obj = pkg.get("author")
        author = None
        if isinstance(author_obj, dict):
            author = author_obj.get("name") or json.dumps(author_obj, ensure_ascii=False)
        elif isinstance(author_obj, str):
            author = author_obj

        out.append(
            {
                "name": slug,
                "description": pkg.get("description", ""),
                "author": author or "",
                "last_updated": latest_date,
                "labels": pkg.get("labels", []),
            }
        )
    return out


def main():
    parser = argparse.ArgumentParser(description="Generate index.json from models/ and packages/")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]), help="Repo root directory")
    parser.add_argument("--output", default="index.json", help="Output index file path (relative to root)")
    args = parser.parse_args()

    root = Path(args.root)
    models_dir = root / "models"
    packages_dir = root / "packages"

    models = collect_models(models_dir)
    # create quick lookup for packages derivation
    model_index = {m["name"]: m for m in models}
    packages = collect_packages(packages_dir, model_index)

    index = {
        "version": "1",
        "generated_at": datetime.datetime.now(datetime.UTC).isoformat() + "Z",
        "models": models,
        "packages": packages,
    }

    out_path = root / args.output
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()

