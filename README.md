# Intro
Memory Sharing Multiprocessing Tool for Parallelizing Function Apply on Large Python Objects (i.e., np.array / pd.DataFrame)


# TODO:
- [X] Allow sharing of numpy array between processes forked by os.fork
- [X] Allow sharing of numpy array between processes created by billiard
- [X] Allow sharing of Pandas DataFrame between processes created by billiard
  - [X] SharedDataFrame class implemented (pd_share.py)
  - [X] Use SharedDataFrame with billiard
- [ ] Explain the code of this repo in README. (installation / run) 
- [ ] Build multi-thread version parallelism code using `rust` language
- [ ] Shared Memory for AutoML (parallel computation)
  - [X] Make sure sharedmem work with sklearn models (in grid_search)
  - [X] Make sure sharedmem work with all models (sklearn + xgboost + lightgbm) (see ml_models.py)
  - [ ] Make sure SharedDataFrame work with xgboost!
  - [ ] Build my own version of parallel grid search!
- [ ] Try experimenting with Ray tune
  - [ ] Run tutorial 
  - [ ] Study the usage 
  - [ ] Fix compatibility