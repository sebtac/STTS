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

3.) Initalize tiral_table to collect the measure of interst accross all runs

4.) Set max_count -- how many times each candidate model should be tested -- we do nto want to run best model idefinatively but rather test "thoroughly" couple best models

5.) Set top_count -- how many candidate models should be fully tested (with max_count runs)

6.) List Conditions (the model parameters) (COND1, COND2)

7.) Adjust target variable to your use case -- this is the traget objective.
