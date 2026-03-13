from imports import *
from util_func_dbm import *


def load_data_home():

    dir_data_home = "../data_home_behave"

    df_train_rec = []  # training days
    df_bs_rec = []  # button switch days
    df_dt_rec = []  # dual task days

    for fd in os.listdir(dir_data_home):
        dir_data_fd = os.path.join(dir_data_home, fd)
        if os.path.isdir(dir_data_fd):
            for fs in os.listdir(dir_data_fd):
                f_full_path = os.path.join(dir_data_fd, fs)
                if os.path.isfile(f_full_path):

                    # The first session is an EEG session. Some people counted this session and
                    # began at-home sessions with day_02 and other omitted this and started with
                    # day_01.
                    #
                    # subj_002 has a day 22 that is mislabeled / ambiguous as
                    # sub_001_day_22_data.csv.
                    #
                    # sub 002 has an at home day labelled day 23 that was also the 17th at home
                    # day (i.e., an extra day)
                    #
                    # sub 008 did four extra days they didn't understand EEG days counted
                    #
                    # sub 015 missed 2 at home days, therefore, excluding days 22, 23, 24
                    #
                    # sub 019 did 2 extra days. Day 13 froze their computer during the task (84
                    # trials completed).  They continued with the next day instead of re-doing day
                    # 13. So, D13 is unusable and will be excluded here. Will also exclude day 18,
                    # because it is an extra at home day.
                    #
                    # Day Exclusion List
                    if os.path.join(fd, fs) not in [
                            'subj_002/sub_001_day_22_data.csv',  # mislabeled / ambiguous sub number
                            'subj_002/sub_002_day_23_data.csv',  # extra at home day
                            'subj_008/sub_008_day_18_data.csv',  # extra at home day
                            'subj_008/sub_008_day_19_data.csv',  # extra at home day
                            'subj_008/sub_008_day_20_data.csv',  # extra at home day
                            'subj_008/sub_008_day_21_data.csv',  # extra at home day
                            'subj_008/sub_008_day_22_data.csv',  # exclude DT
                            'subj_008/sub_008_day_23_data.csv',  # exclude BS
                            'subj_008/sub_008_day_24_data.csv',  # exclue BS
                            'subj_015/sub_015_day_22_data.csv',  # exclude DT
                            'subj_015/sub_015_day_23_data.csv',  # exclude BS
                            'subj_015/sub_015_day_24_data.csv',  # exclude BS
                            'subj_019/sub_019_day_13_data.csv',  # computer froze
                            'subj_019/sub_019_day_18_data.csv',  # exclude DT
                            'subj_019/sub_019_day_22_data.csv',  # exclude BS
                            'subj_019/sub_019_day_23_data.csv',  # exclude BS
                            'subj_019/sub_019_day_24_data.csv'
                    ]:  # extra at home day

                        df = pd.read_csv(f_full_path)
                        df['f_name'] = fs

                        # sub_003 somehow replicated day 18
                        # fix that here
                        if fs == 'sub_003_day_19_data.csv':
                            df['day'] = 19
                        elif fs == 'sub_003_day_20_data.csv':
                            df['day'] = 20

                        # sub_006 mislabeled days 22, 23, and 24 as sub_001
                        # manually change file name to: sub_006_day_22_data.csv,
                        # sub_006_day_23_data.csv, sub_006_day_24_data.csv
                        # fix that here
                        if fs == 'sub_006_day_22_data.csv':
                            df['subject'] = 6
                        elif fs == 'sub_006_day_23_data.csv':
                            df['subject'] = 6
                        elif fs == 'sub_006_day_24_data.csv':
                            df['subject'] = 6

                        # fix sub_015 mislabeling in raw data
                        # also fix extra 1 in day 7 (trial 60 or 61) manually
                        if fs == 'sub_015_day_01_data.csv':
                            df['subject'] = 15

                        # sub_016 mislabeled day 22 as sub_001 and had already
                        # changed file name to: sub_016_day_22_data.csv
                        # changing from subject 1 to subject 16
                        # fix that here
                        if fs == 'sub_016_day_22_data.csv':
                            df['subject'] = 16

                        # sub_017 day 17 mislabeled to sub_007_day_17_data.csv
                        # manually change file name to: sub_017_day_17_data.csv
                        # fix subject column here
                        if fs == 'sub_017_day_17_data.csv':
                            df['subject'] = 17

                        # sub_019
                        # mislabeled day 1 as sub_001
                        # no need to manually change file name
                        # fix that here
                        if fs == 'sub_019_day_01_data.csv':
                            df['subject'] = 19

                        # from trial 276 on day 24, 'day' changes to day 25
                        # (until the end of the expt)
                        # also, in this file there are 4 lines of ,,,,,,,,,,,
                        # after the end of the experiment
                        # manually removed those lines
                        # fix that here
                        if fs == 'sub_019_day_24_data.csv':
                            df['day'] = 24

                        day = df['day'].unique()

                        # training days
                        if ~np.isin(day, [22, 23, 24]):
                            df_train_rec.append(df)

                        # dual-task days
                        if day == 22:
                            df_dt_rec.append(df)

                        # button-switch days
                        if day in [23, 24]:
                            df_bs_rec.append(df)

    return df_train_rec, df_dt_rec, df_bs_rec


def load_data_lab():

    dir_data_lab_beh = "../data_lab_behave"

    df_lab_rec = []

    for fd in os.listdir(dir_data_lab_beh):
        f_df = os.path.join(dir_data_lab_beh, fd)
        if os.path.isfile(f_df) and fd != '.DS_Store':
            df = pd.read_csv(f_df)

            # mislabelled sub_003_day_401_data.csv
            # manually changed file name to: sub_003_day_403_data.csv
            # fix here
            if fd == 'sub_003_day_401_data.csv':
                df['day'] = 403

            # mislabelled sub_015_day_15_data.csv
            # manually changed file name to: sub_015_day_215_data.csv
            # fix here
            if fd == 'sub_015_day_15_data.csv':
                df['day'] = 215

            df_lab_rec.append(df)

    return df_lab_rec


def prep_dfs(df_train_rec, df_dt_rec, df_bs_rec, df_lab_rec, block_size=25):

    d = pd.concat(df_train_rec, ignore_index=True)
    d.sort_values(by=['subject', 'day', 'trial'], inplace=True)
    d['acc'] = (d['cat'] == d['resp']).astype(int)
    d['day'] = d.groupby('subject')['day'].rank(method='dense').astype(int)
    d['trial'] = d.groupby(['subject']).cumcount()
    d['n_trials'] = d.groupby(['subject', 'day'])['trial'].transform('count')
    d['block'] = d.groupby(['subject', 'day'
                            ])['trial'].transform(lambda x: x // block_size)
    d['session_type'] = 'Training at home'

    d_dt = pd.concat(df_dt_rec, ignore_index=True)
    d_dt.sort_values(by=['subject', 'day', 'trial'], inplace=True)
    d_dt['acc'] = (d_dt['cat'] == d_dt['resp']).astype(int)
    d_dt['day'] = d_dt.groupby('subject')['day'].rank(
        method='dense').astype(int)
    d_dt['day'] = d_dt['day'].map({1: 22})
    d_dt['trial'] = d_dt.groupby(['subject']).cumcount()
    d_dt['n_trials'] = d_dt.groupby(['subject',
                                     'day'])['trial'].transform('count')
    d_dt['session_type'] = 'Dual-Task at home'

    d_bs = pd.concat(df_bs_rec, ignore_index=True)
    d_bs.sort_values(by=['subject', 'day', 'trial'], inplace=True)
    d_bs['acc'] = (d_bs['cat'] == d_bs['resp']).astype(int)
    d_bs['day'] = d_bs.groupby('subject')['day'].rank(
        method='dense').astype(int)
    d_bs['day'] = d_bs['day'].map({1: 23, 2: 24})
    d_bs['trial'] = d_bs.groupby(['subject']).cumcount()
    d_bs['n_trials'] = d_bs.groupby(['subject',
                                     'day'])['trial'].transform('count')
    d_bs['session_type'] = 'Button-Switch at home'

    d_lab = pd.concat(df_lab_rec, ignore_index=True)
    d_lab['acc'] = (d_lab['cat'] == d_lab['resp']).astype(int)
    d_lab['day'] = d_lab.groupby('subject')['day'].rank(
        method='dense').astype(int)
    d_lab['day'] = d_lab['day'].map({1: 0.5, 2: 4.5, 3: 8.5, 4: 12.5, 5: 21})
    d_lab['trial'] = d_lab.groupby(['subject']).cumcount()
    d_lab['n_trials'] = d_lab.groupby(['subject',
                                       'day'])['trial'].transform('count')
    d_lab['block'] = d_lab.groupby(
        ['subject', 'day'])['trial'].transform(lambda x: x // block_size)
    d_lab['session_type'] = 'Training in the Lab'

    # print days present in each dataframe for each subject
    # print("Days present in training data:")
    # print(d.groupby('subject')['day'].unique())
    # print(d.groupby('subject')['day'].nunique())

    # print("\nDays present in dual-task data:")
    # print(d_dt.groupby('subject')['day'].unique())
    # print(d_dt.groupby('subject')['day'].nunique())

    # print("\nDays present in button-switch data:")
    # print(d_bs.groupby('subject')['day'].unique())
    # print(d_bs.groupby('subject')['day'].nunique())

    # print("\nDays present in lab data:")
    # print(d_lab.groupby('subject')['day'].unique())
    # print(d_lab.groupby('subject')['day'].nunique())

    return d, d_dt, d_bs, d_lab


def exclude_subject(d, d_dt, d_bs, d_lab):
    # create a numpy array of the intersection of subjects across all dataframes
    all_subs = np.unique(
        np.concatenate([
            d.subject.unique(),
            d_dt.subject.unique(),
            d_bs.subject.unique(),
            d_lab.subject.unique()
        ]))

    # identify subjects in all three home data frames
    subs_to_keep = np.intersect1d(all_subs, d.subject.unique())
    subs_to_keep = np.intersect1d(subs_to_keep, d_dt.subject.unique())
    subs_to_keep = np.intersect1d(subs_to_keep, d_bs.subject.unique())
    subs_to_keep = np.intersect1d(subs_to_keep, d_lab.subject.unique())
    excluded_subs_missing_data = np.setdiff1d(all_subs, subs_to_keep)

    # compute Stroop accuracy and identify subjects with accuracy < 80%
    d_dt['acc_stroop'] = np.nan
    d_dt.loc[d_dt['ns_correct_side'].notna(), 'acc_stroop'] = (
        d_dt['ns_correct_side'] == d_dt['ns_resp']).astype(int)
    d_dt['acc_stroop_mean'] = d_dt.groupby('subject')['acc_stroop'].transform(
        lambda x: np.nanmean(x))
    excluded_subs_stroop = d_dt.groupby('subject')['acc_stroop_mean'].first()[
        d_dt.groupby('subject')['acc_stroop_mean'].first() < 0.80].index.values

    # identify subjects with more or less than 2 button switch days (should be empty)
    d_bs_counts = d_bs.groupby('subject')['day'].nunique()
    excluded_subs_bs = d_bs_counts[d_bs_counts != 2].index.values

    # merge all dataframes inserting np.nan into columns that don't exist in a particular dataframe
    d_all = pd.concat([d, d_dt, d_bs, d_lab], ignore_index=True, sort=False)

    # exclude excluded_subs_missing_data, excluded_subs_stroop, and excluded_subs_bs from d_all
    subs_to_exclude = np.unique(
        np.concatenate([
            excluded_subs_missing_data, excluded_subs_stroop, excluded_subs_bs
        ]))
    d_all = d_all[~d_all['subject'].isin(subs_to_exclude)].copy()

    return d_all


def renumber_days(d_all):

    # inspect day numbers present per subject after exclusions
    for sub in d_all['subject'].unique():
        sub_mask = d_all['subject'] == sub
        print(
            f"Subject {sub} days: {sorted(d_all.loc[sub_mask, 'day'].unique())}"
        )

    # re-assign day numbers to be dense ranks within each subject, so that we can more easily
    # compare across subjects with different day numbers.
    #
    # This can lead to misleading results if subjects differ in which raw day values are present:
    # dense ranking is computed per subject, so the same dense day index may correspond to different
    # original day codes across subjects. In that case, day-specific contrasts (e.g., raw day
    # 22/23/24) should be performed before this step, or by preserving raw day in a separate column.
    d_all['day'] = d_all.groupby('subject')['day'].rank(
        method='dense').astype(int)

    # inspect day numbers present per subject after dense ranks
    for sub in d_all['subject'].unique():
        sub_mask = d_all['subject'] == sub
        print(
            f"Subject {sub} days: {sorted(d_all.loc[sub_mask, 'day'].unique())}"
        )

    return d_all


def inspect_dbm(d, block_size=25):

    # Fit DBM here
    models = [
        nll_unix,
        nll_unix,
        nll_uniy,
        nll_uniy,
        nll_glc,
        nll_glc,
    ]
    side = [0, 1, 0, 1, 0, 1]
    k = [2, 2, 2, 2, 3, 3]
    n = block_size
    model_names = [
        "nll_unix_0",
        "nll_unix_1",
        "nll_uniy_0",
        "nll_uniy_1",
        "nll_glc_0",
        "nll_glc_1",
    ]

    if not os.path.exists("../dbm_fits/dbm_results.csv"):
        dbm = (d.groupby(["subject", "day"]).apply(fit_dbm, models, side, k, n,
                                                   model_names).reset_index())
        dbm.to_csv("../dbm_fits/dbm_results.csv")
    else:
        dbm = pd.read_csv("../dbm_fits/dbm_results.csv")
        dbm = dbm[["subject", "day", "model", "bic", "p"]]

    def assign_best_model(x):
        min_bic = x['bic'].min()
        winners = x.loc[x['bic'] == min_bic, 'model'].unique()
        x = x.copy()
        if len(winners) == 1:
            x['best_model'] = winners[0]
            x['is_tie'] = False
        else:
            x['best_model'] = np.nan
            x['is_tie'] = True
        return x

    dbm = dbm.groupby(["subject",
                       "day"]).apply(assign_best_model,
                                     include_groups=False).reset_index()
    dbm = dbm[dbm["model"] == dbm["best_model"]]
    dbm = dbm[["subject", "day", "bic", "best_model"]]
    dbm = dbm.drop_duplicates().reset_index(drop=True)
    dbm["best_model_class"] = dbm["best_model"].str.split("_").str[1]
    dbm.loc[dbm["best_model_class"] != "glc",
            "best_model_class"] = "rule-based"
    dbm.loc[dbm["best_model_class"] == "glc",
            "best_model_class"] = "procedural"
    dbm["best_model_class"] = dbm["best_model_class"].astype("category")
    dbm = dbm.reset_index(drop=True)

    # print proportion of best model classes across all subjects and days
    print(dbm.groupby('day')['best_model_class'].value_counts(normalize=True))

    # plot bic across days for each model class
    fig, ax = plt.subplots(1, 1, squeeze=False, figsize=(10, 7))
    sns.pointplot(data=dbm,
                  x='day',
                  y='bic',
                  hue='best_model_class',
                  errorbar=('se'),
                  ax=ax[0, 0])
    ax[0, 0].set_xlabel('Day')
    ax[0, 0].set_ylabel('BIC')
    plt.tight_layout()
    plt.savefig('../figures/dbm_bic_performance.png', dpi=300)


def prep_figure_data(d_all):

    # aggregate data for upcoming figures
    d_all = d_all[d_all['rt'] <= 3000]
    dd_all = d_all.groupby(['subject', 'day', 'session_type']).agg({
        'acc': 'mean',
        'rt': 'mean'
    }).reset_index()

    return dd_all


def plot_all_session_figures(dd_all):

    # Figure --- all session types
    fig, ax = plt.subplots(1, 1, squeeze=False, figsize=(8, 5))
    sns.pointplot(data=dd_all,
                  x='day',
                  y='acc',
                  hue='session_type',
                  errorbar=('se'),
                  ax=ax[0, 0])
    [
        x.set_xticks(np.arange(0, dd_all['day'].max() + 2, 1))
        for x in ax.flatten()
    ]
    ax[0, 0].set_xlabel('Day', fontsize=16)
    ax[0, 0].set_ylabel('Proportion correct', fontsize=16)
    ax[0, 0].legend(title='')
    plt.savefig('../figures/training_performance_days.png', dpi=300)
    plt.close()

    # Figure --- all session types RT
    fig, ax = plt.subplots(1, 1, squeeze=False, figsize=(8, 5))
    sns.pointplot(data=dd_all,
                  x='day',
                  y='rt',
                  hue='session_type',
                  errorbar=('se'),
                  ax=ax[0, 0])
    [
        x.set_xticks(np.arange(0, dd_all['day'].max() + 2, 1))
        for x in ax.flatten()
    ]
    ax[0, 0].set_xlabel('Day', fontsize=16)
    ax[0, 0].set_ylabel('Reaction Time', fontsize=16)
    ax[0, 0].legend(title='')
    plt.savefig('../figures/training_performance_days_rt.png', dpi=300)
    plt.close()


def prep_dual_task_data(dd_all):

    # prepare a data frame comparing last day of training to dual-task day
    d_dtf = dd_all[dd_all['day'].isin([20, 22])].copy()

    # change the day column to categorical for plotting with names
    # "Last Training Day" and "Dual-Task Day"
    d_dtf['day'] = d_dtf['day'].map({
        20: 'Last Training Day',
        22: 'Dual-Task Day'
    })

    return d_dtf


def plot_dual_task_figure(d_dtf):

    # plot point range plot comparing the last day of training to dual-task day
    fig, ax = plt.subplots(2, 1, squeeze=False, figsize=(5, 8))
    sns.pointplot(data=d_dtf, x='day', y='acc', errorbar=('se'), ax=ax[0, 0])
    sns.pointplot(data=d_dtf, x='day', y='rt', errorbar=('se'), ax=ax[1, 0])
    ax[0, 0].yaxis.set_major_formatter(
        plt.FuncFormatter(lambda y, _: '{:.2f}'.format(y)))
    ax[0, 0].set_xlabel('')
    ax[0, 0].set_ylabel('Accuracy (proportion correct)')
    ax[1, 0].set_xlabel('')
    ax[1, 0].set_ylabel('Reaction Time (ms)')
    plt.tight_layout()
    plt.savefig('../figures/dual_task_performance.png', dpi=300)
    plt.close()


def run_dual_task_stats(d_dtf):

    # dual-task stats
    res = pg.ttest(x=d_dtf[d_dtf['day'] == 'Last Training Day']['acc'],
                   y=d_dtf[d_dtf['day'] == 'Dual-Task Day']['acc'],
                   alternative='greater',
                   paired=True)

    return res


def prep_button_switch_data(dd_all):

    # prepare a data frame comparing last day of training to button-switch days
    d_bsf = dd_all[dd_all['day'].isin([20, 23, 24])].copy()

    # change the day column to categorical for plotting with names
    # "Last Training Day", "Button-Switch Day 1", "Button-Switch Day 2"
    d_bsf['day'] = d_bsf['day'].map({
        20: 'Last Training Day',
        23: 'Button-Switch Day 1',
        24: 'Button-Switch Day 2'
    })

    return d_bsf


def plot_button_switch_figure(d_bsf):

    # plot point range plot comparing the last day of training to button-switch days
    fig, ax = plt.subplots(2, 1, squeeze=False, figsize=(7, 8))
    sns.pointplot(data=d_bsf, x='day', y='acc', errorbar=('se'), ax=ax[0, 0])
    sns.pointplot(data=d_bsf, x='day', y='rt', errorbar=('se'), ax=ax[1, 0])
    ax[0, 0].set_xlabel('')
    ax[0, 0].set_ylabel('Accuracy (proportion correct)')
    ax[1, 0].set_xlabel('')
    ax[1, 0].set_ylabel('Reaction Time (ms)')
    plt.tight_layout()
    plt.savefig('../figures/button_switch_performance.png', dpi=300)
    plt.close()


def run_button_switch_stats(d_bsf):

    # button-switch stats
    res_bs1 = pg.ttest(x=d_bsf[d_bsf['day'] == 'Last Training Day']['acc'],
                       y=d_bsf[d_bsf['day'] == 'Button-Switch Day 1']['acc'],
                       alternative='greater',
                       paired=True)

    res_bs2 = pg.ttest(x=d_bsf[d_bsf['day'] == 'Last Training Day']['acc'],
                       y=d_bsf[d_bsf['day'] == 'Button-Switch Day 2']['acc'],
                       alternative='greater',
                       paired=True)

    return res_bs1, res_bs2


def plot_eeg_predictions():

    # Make EEG predictions figure
    # draw 5 sets of two gaussians one centered at 500 ms and another centered at 1000 ms
    # let the amplitude of these gaussian increase across the 5 sets, but at different rates for
    # each centre.
    fig, ax = plt.subplots(1, 1, squeeze=False, figsize=(8, 5))
    x = np.linspace(0, 1500, 1000)
    for i in range(5):
        y1 = (2 * i + 1) * np.exp(-0.5 * ((x - 500) / 100)**2)
        y2 = (i + 2) * np.exp(-0.5 * ((x - 1000) / 100)**2)
        ax[0, 0].plot(x, y1 + y2, label=f'Set {i+1}')
    ax[0, 0].set_xlabel('Time within trial (ms)', fontsize=16)
    ax[0, 0].set_ylabel('Functional Connectivity (a.u.)', fontsize=16)
    ax[0, 0].legend().remove()
    ax[0, 0].legend([f'Day {i+1}' for i in range(5)], title='')
    plt.savefig('../figures/eeg_predictions.png', dpi=300)
    plt.close()


def plot_rt_vs_dist_vs_days(d_all):

    d = d_all[d_all['session_type'] == 'Training in the Lab'].copy()
    d['session_type'] = d['session_type'].astype('category')
    d['day'] = d['day'].astype('category')

    # make dist_to_bound column that is the orthogonal distance 
    # from the category boundary (y=x) in the stimulus space (x,y)
    # values
    d['dist_to_bound'] = np.abs(d['y'] - d['x']) / 2

    # group dist-to-bound into quantile bins and keep numeric bin edges for labels
    d['dist_to_bound_bin'], bin_edges = pd.qcut(d['dist_to_bound'],
                                                q=5,
                                                labels=False,
                                                retbins=True,
                                                duplicates='drop')

    # summarize RT as mean +/- SEM for each day x distance bin
    d_sum = d.groupby(['day', 'dist_to_bound_bin'],
                      observed=True)['rt'].agg(rt_mean='mean',
                                               rt_sem='sem').reset_index()

    # plot reaction time as lines with points and SEM error bars
    fig, ax = plt.subplots(1, 1, squeeze=False, figsize=(7, 5))
    for day, day_df in d_sum.groupby('day', sort=True):
        day_df = day_df.sort_values('dist_to_bound_bin')
        ax[0, 0].errorbar(day_df['dist_to_bound_bin'],
                          day_df['rt_mean'],
                          yerr=day_df['rt_sem'],
                          marker='o',
                          linestyle='-',
                          capsize=0,
                          label=f'Day {day}')

    # label x-axis ticks only at bins present in data using bin means
    present_bins = sorted(d_sum['dist_to_bound_bin'].dropna().astype(int).unique())
    bin_mean_map = d.groupby('dist_to_bound_bin', observed=True)['dist_to_bound'].mean()
    tick_labels = [f"{bin_mean_map.loc[b]:.3f}" for b in present_bins]

    ax[0, 0].set_xticks(present_bins)
    ax[0, 0].set_xticklabels(tick_labels, ha='right')
    ax[0, 0].set_xlabel('Distance from category boundary (bin mean)', fontsize=16)
    ax[0, 0].set_ylabel('Reaction Time (ms)', fontsize=16)
    ax[0, 0].legend(title='')
    plt.tight_layout()
    plt.savefig('../figures/rt_vs_dist_vs_days.png', dpi=300)
    plt.close()
