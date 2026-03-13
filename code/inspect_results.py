"""
Main behavioral analysis script for the longitudinal category-learning automaticity study
(cat_learn_auto_pace_2025_s2).

Overview
--------
Participants practice a procedural categorization task longitudinally:
- At-home training across many days
- Interleaved special at-home sessions:
    * Dual-task day (day 22)
    * Button-switch days (days 23–24)
- Lab sessions approximately every ~5 days (behavior + EEG recorded; EEG analysis lives elsewhere)

This script:
1) Loads at-home CSVs from ../data/*/sub_*_day_*_data.csv with manual corrections/exclusions.
2) Loads lab behavioral CSVs from ../data_lab_behave/*.csv with a few filename/day fixes.
3) Builds unified long-format dataframe across session types:
      - Training at home
      - Dual-Task at home
      - Button-Switch at home
      - Training in the Lab
4) Applies inclusion criteria:
      - keep only subjects with data present in ALL session types
      - Stroop (ns_*) accuracy >= 0.80 (computed where ns_* columns exist)
      - RT filter for plotting (rt <= 3000 ms)
5) Fits decision-bound models (DBM) per subject × day (block_size=25 trials) if
   ../dbm_fits/dbm_results.csv does not already exist; selects best model by BIC and collapses to:
      - procedural (GLC)
      - rule-based (unidimensional)
6) Produces figures in ../figures/:
      - DBM BIC by day and best_model_class
      - Accuracy by day across session types
      - RT by day across session types
      - Dual-task: last training vs dual-task day (accuracy + RT)
      - Button-switch: last training vs button-switch days (accuracy + RT)
      - EEG predictions placeholder figure (synthetic)

Data organization assumptions
-----------------------------
At-home data are organized by participant folder, e.g.:
  ../data/subj_<hash>/sub_<ID>_day_<NN>_data.csv

Lab behavioral files live in:
  ../data_lab_behave/sub_<ID>_day_<NNN>_data.csv

The script contains a manual "day exclusion list" and several subject-specific fixes
(mislabeled subject IDs, mislabeled day numbers, extra days). These are documented inline.
"""

from imports import *
from util_func_dbm import *
from util_func_analysis import *

if __name__ == '__main__':

    # Init figure style
    sns.set_palette("rocket", n_colors=4)
    plt.rc('axes', labelsize=14)
    plt.rc('xtick', labelsize=12)
    plt.rc('ytick', labelsize=12)

    block_size = 25

    df_train_rec, df_dt_rec, df_bs_rec = load_data_home()
    df_lab_rec = load_data_lab()
    d, d_dt, d_bs, d_lab = prep_dfs(df_train_rec,
                                    df_dt_rec,
                                    df_bs_rec,
                                    df_lab_rec,
                                    block_size=block_size)
    d_all = exclude_subject(d, d_dt, d_bs, d_lab)
    d_all = renumber_days(d_all)

    inspect_dbm(d, block_size=block_size)

    dd_all = prep_figure_data(d_all)
    plot_all_session_figures(dd_all)

    d_dtf = prep_dual_task_data(dd_all)
    plot_dual_task_figure(d_dtf)
    res = run_dual_task_stats(d_dtf)

    d_bsf = prep_button_switch_data(dd_all)
    plot_button_switch_figure(d_bsf)
    res_bs1, res_bs2 = run_button_switch_stats(d_bsf)

    plot_eeg_predictions()
