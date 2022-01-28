# Intro
Memory Sharing Multiprocessing Tool for Parallelizing Function Apply on Large Python Objects (i.e., np.array / pd.DataFrame)


# TODO:
- [X] Allow sharing of numpy array between processes forked by os.fork
- [X] Allow sharing of numpy array between processes created by billiard
- [ ] Allow sharing of Pandas DataFrame between processes created by billiard
  - [X] SharedDataFrame class implemented
  - [ ] Use SharedDataFrame with billiard