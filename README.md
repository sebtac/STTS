# STTS

# Thompson Sampling Based Best Model Search with Multiprocessing Implementation

# Objective
create TS based algorithm for best model search with multiprocessing implementation

# characteristics:
- for normally distributed objective (update STTS_sampler() otherwise)
- implementation for maximization objective (update # cond_index = np.argmin() otherwise)
- implemented with simple test case (update target = () to adjust to your use case)

# usage:

1.) Initalize trial_control table, one row per condition, count, each distribution paramter (example: norm(mu,sd))

2.) Initalize tiral_table to collect the measure of interst accross all runs

3.) Set max_count -- how many times each candidate model should be tested -- we do nto want to run best model idefinatively but rather test "thoroughly" couple best models

4.) Set top_count -- how many candidate models should be fully tested (with max_count runs)

5.) List Conditions (the model parameters) (COND1, COND2)

6.) Adjust target variable to your use case -- this is the traget objective.

# EXAMPLE REVIEW

- The expected values of the target varible are as seen in the top table

- The expected models to undergo the complete testing (with Max_Count Runs!)

- The expected BEST MOODEL: Model(128,15)

![github-small](https://github.com/sebtac/STTS/blob/main/STTS%20Example%20Settings.jpg)

### Results:

- Most of the models expected to be fully tested have been tested; when max_count is increased to 30 all exepected conditions are fully tested
- The best performing model is the Model(128,15) but this depends on the variablilty of the resutls between models !!!
  - if you change the line target = (np.random.random())*(cond1_select * cond2_select) to target = (np.random.random())*(cond1_select + cond2_select) the TRUE-Best model will not be chosen every time but it will be a good one with cond1 of 64 or 128!

![github-small](https://github.com/sebtac/MLxE/blob/main/Sewak%20-%20Models%20Comparison%20-%208-Games%20MA.jpg)
