# cat_learn_auto_2025_s2

## Directory structure

- **code/**
  - `inspect_results.py` — main behavioral analysis script (figures + DBM fits)
  - `util_func_dbm.py` — decision-bound model likelihoods and DBM fitting routine
  - `run_exp.py` — experiment runtime code
  - `inspect_results_eeg.py` — EEG-related analysis (currently limited / in progress)

- **data_home_behave/**
  At-home training logs, organized by participant folder:

- **data_lab_behave/**
  Lab behavioral logs as flat CSV files:
  `data_lab_behave/sub_<ID>_day_<NNN>_data.csv`

- **data_lab_eeg/**
  Raw EEG files (e.g., `.bdf`) for lab sessions.

- **dbm_fits/**
  DBM fitting results

- **figures/**
  Output figures created by `inspect_results.py` et al.

---

## Session types & day coding

The analysis script organizes data into four session types:

* **Training at home**
  Days excluding [22, 23, 24] (after subject-wise day re-indexing)

* **Dual-Task at home**
  Day 22

* **Button-Switch at home**
  Days 23 and 24

---

## Data files: trial-level CSV structure

At-home training (and related at-home probe sessions) are
stored as trial-level CSV files.  Each row corresponds to
**one trial**.

### Columns

| Column   | Type | Description |
|---------|------|-------------|
| `subject` | int | Participant ID (numeric). |
| `day`     | int | Training day index within participant (starts at 1 for at-home training; special probe days may be coded as 22–24 depending on the session). |
| `trial`   | int | Trial index within day (0-based in the raw files). |
| `cat`     | str | Ground-truth category label for the stimulus (e.g., `"A"` or `"B"`). |
| `x`       | float | Stimulus value on dimension X in the **original stimulus space** (typically 0–100). |
| `y`       | float | Stimulus value on dimension Y in the **original stimulus space** (typically 0–100). |
| `xt`      | float | Transformed/scaled version of `x` used for modeling/decision-bound fits (task-specific transform). |
| `yt`      | float | Transformed/scaled version of `y` used for modeling/decision-bound fits (task-specific transform). |
| `resp`    | str | Participant response label (e.g., `"A"` or `"B"`). |
| `rt`      | float | Reaction time in milliseconds (ms). |
| `fb`      | str | Feedback text shown to the participant (e.g., `"Correct"` / `"Incorrect"`). |

# cat_learn_auto_2025_s2
