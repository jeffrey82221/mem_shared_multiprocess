# Intro
Memory Sharing Multiprocessing Tool for Parallelizing Function Apply on Large Python Objects (i.e., np.array / pd.DataFrame)


# TODO:
- [X] Allow sharing of numpy array between processes forked by os.fork
- [X] Allow sharing of numpy array between processes created by billiard
- [X] Allow sharing of Pandas DataFrame between processes created by billiard
  - [X] SharedDataFrame class implemented (pd_share.py)
  - [X] Use SharedDataFrame with billiard
- [ ] Shared Memory for AutoML (parallel computation)
  - [X] Make sure sharedmem work with sklearn models (in grid_search)
  - [ ] Make sure SharedDataFrame work with xgboost
  - [ ] Build my own version of parallel grid search!