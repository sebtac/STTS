# STTS Model Search

# Thompson Sampling Based Best Model Search with Multiprocessing Implementation

# Objective
create TS based algorithm for best model search with multiprocessing implementation

# characteristics:
- for normally distributed objective (update STTS_sampler() otherwise)
- implementation for maximization objective (update # cond_index = np.argmin() otherwise)
- implemented with simple test case (update target = () to adjust to your use case)

# usage:

1.) Initialize trial_control table, one row per condition, count, each distribution parameter (example: norm(mu,sd))

2.) Initialize trial_table to collect the measure of interest across all runs

3.) Set max_count -- how many times each candidate model should be tested -- we do not want to run best model definitively but rather test "thoroughly" couple best models

4.) Set top_count -- how many candidate models should be fully tested (with max_count runs)

5.) List Conditions (the model parameters) (COND1, COND2)

6.) Adjust target variable to your use case -- this is the target objective.

# EXAMPLE REVIEW

- The expected values of the target variable are as seen in the top table

- The Bottom Table shows (in Green) the expected models to undergo the complete testing (with Max_Count Runs!)

- The expected BEST MOODEL: Model(128,15)

![github-small](https://github.com/sebtac/STTS/blob/main/STTS%20Example%20Settings.jpg)

### Results:

- Most of the models expected to be fully tested have been tested; when max_count is increased to 30 all expected conditions are fully tested
- The best performing model is the Model(128,15) but this depends on the variability of the results between models !!!
  - if you change the line target = (np.random.random())*(cond1_select * cond2_select) to target = (np.random.random())*(cond1_select + cond2_select) the TRUE-Best model will not be chosen every time, but it will be a good one with cond1 of 64 or 128!


COND1
[8.000 8.000 8.000 8.000 8.000 8.000 8.000 8.000 8.000 16.000 16.000
  16.000 16.000 16.000 16.000 16.000 16.000 16.000 32.000 32.000 32.000
  32.000 32.000 32.000 32.000 32.000 32.000 64.000 64.000 64.000 64.000
  64.000 64.000 64.000 64.000 64.000 128.000 128.000 128.000 128.000
  128.000 128.000 128.000 128.000 128.000]
 
 COND2
 [3.000 4.000 5.000 6.000 7.000 8.000 9.000 10.000 15.000 3.000 4.000
  5.000 6.000 7.000 8.000 9.000 10.000 15.000 3.000 4.000 5.000 6.000
  7.000 8.000 9.000 10.000 15.000 3.000 4.000 5.000 6.000 7.000 8.000
  9.000 10.000 15.000 3.000 4.000 5.000 6.000 7.000 8.000 9.000 10.000
  15.000]
 
 COUNT - N
 [2.000 2.000 2.000 2.000 2.000 2.000 2.000 2.000 2.000 2.000 2.000 2.000
  2.000 2.000 2.000 2.000 2.000 2.000 2.000 2.000 2.000 4.000 2.000 2.000
  2.000 13.000 16.000 2.000 2.000 9.000 2.000 2.000 2.000 2.000 16.000
  16.000 10.000 16.000 16.000 16.000 16.000 16.000 16.000 2.000 16.000]
 
 MU
 [11.475 7.790 16.627 3.718 16.624 8.605 6.218 9.453 41.747 21.803 31.304
  38.101 39.082 18.287 55.765 30.609 31.238 27.780 32.843 36.125 5.740
  107.476 49.661 31.581 38.650 156.857 202.294 57.241 25.156 109.791
  27.150 76.820 39.357 6.832 333.264 506.021 153.850 245.329 343.251
  352.302 396.703 565.535 574.046 13.766 952.117]
 
 SD
 [11.475 7.790 16.627 3.718 16.624 8.605 6.218 9.453 41.747 21.803 31.304
  38.101 39.082 18.287 55.765 30.609 31.238 27.780 32.843 36.125 5.740
  66.133 49.661 31.581 38.650 117.404 138.243 57.241 25.156 102.705
  27.150 76.820 39.357 6.832 196.719 293.040 108.933 165.622 180.710
  222.276 265.264 348.215 354.853 13.766 551.786]
