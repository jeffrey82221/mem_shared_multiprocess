# Intro
Memory Sharing Multiprocessing Tool for Parallelizing Function Apply on Large Python Objects (i.e., np.array / pd.DataFrame)


# TODO:
- [X] Allow sharing of numpy array between processes forked by os.fork
- [X] Allow sharing of numpy array between processes created by billiard
- [X] Allow sharing of Pandas DataFrame between processes created by billiard
  - [X] SharedDataFrame class implemented (pd_share.py)
  - [X] Use SharedDataFrame with billiard
- [ ] Make sure SharedDataFrame work with sklearn models (duck type) for hyperparameter tuning 