from pathlib import Path
import argparse
import shutil
import pandas as pd

import inspect_results as ir

DEFAULT_OUT_ROOT = "/Users/mq20185996/Dropbox/teaching/2026/cogs2020/private/final_project_data/cat_learn_auto"


def _clean_frame(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [c.strip() for c in out.columns]
    if out.columns.duplicated().any():
        cols = list(out.columns)
        unique_cols = []
        merged = {}
        for c in cols:
            if c not in unique_cols:
                unique_cols.append(c)
        for c in unique_cols:
            idx = [i for i, cc in enumerate(cols) if cc == c]
            if len(idx) == 1:
                merged[c] = out.iloc[:, idx[0]]
            else:
                # Prefer right-most duplicate (typically corrected value), but
                # fall back to earlier columns if missing.
                merged[c] = out.iloc[:, idx[::-1]].bfill(axis=1).iloc[:, 0]
        out = pd.DataFrame(merged)
    out = out.loc[:, ~out.columns.str.contains(r"^Unnamed:")]
    return out


def build_clean_home_dataframe() -> pd.DataFrame:
    ir.block_size = 25
    df_train_rec, df_dt_rec, df_bs_rec = ir.load_data_home()
    df_lab_rec = ir.load_data_lab()
    d, d_dt, d_bs, d_lab = ir.prep_dfs(df_train_rec, df_dt_rec, df_bs_rec, df_lab_rec)
    d_all = ir.exclude_subject(d, d_dt, d_bs, d_lab)
    d_all = ir.renumber_days(d_all)

    d_home = d_all[d_all["session_type"].isin([
        "Training at home",
        "Dual-Task at home",
        "Button-Switch at home",
    ])].copy()

    d_home = _clean_frame(d_home)
    d_home["subject"] = pd.to_numeric(d_home["subject"], errors="raise").astype(int)
    d_home["day"] = pd.to_numeric(d_home["day"], errors="raise").astype(int)
    d_home["trial"] = pd.to_numeric(d_home["trial"], errors="coerce")
    return d_home


def export_home_data(d_home: pd.DataFrame, out_root: Path, overwrite: bool = True) -> None:
    out_data = out_root / "data_home_behave"
    if overwrite and out_data.exists():
        shutil.rmtree(out_data)
    out_data.mkdir(parents=True, exist_ok=True)

    d_home = d_home.sort_values(["subject", "day", "trial"], kind="mergesort").copy()

    n_files = 0
    for (sub, day), dd in d_home.groupby(["subject", "day"], sort=True):
        subj_dir = out_data / f"subj_{sub:03d}"
        subj_dir.mkdir(parents=True, exist_ok=True)
        fout = subj_dir / f"sub_{sub:03d}_day_{day:02d}_data.csv"
        dd.to_csv(fout, index=False)
        n_files += 1

    print(f"Wrote {n_files} files to: {out_data}")
    print(f"Subjects: {d_home['subject'].nunique()}")
    print(f"Rows: {len(d_home)}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export cleaned at-home teaching data in subject/day folder structure."
    )
    parser.add_argument(
        "--out-root",
        default=DEFAULT_OUT_ROOT,
        help="Output root directory (a data_home_behave folder will be created inside).",
    )
    parser.add_argument(
        "--no-overwrite",
        action="store_true",
        help="Do not remove existing output directory before exporting.",
    )
    args = parser.parse_args()

    d_home = build_clean_home_dataframe()
    export_home_data(d_home, Path(args.out_root), overwrite=not args.no_overwrite)


if __name__ == "__main__":
    main()
