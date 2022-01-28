"""
class storing pandas DataFrame in shared memory to be accesses by multiple processes
"""
import pandas as pd
import sharedmem
class SharedDataFrame:
    def __init__(self, dataframe):
        self.__cols = SharedDataFrame.__to_shared(dataframe.columns)
        self.__values = dict()
        for col in dataframe.columns:
            self.__values[col] = SharedDataFrame.__to_shared(dataframe[col])

    @staticmethod
    def __to_shared(array):
        fp = sharedmem.empty(array.shape, dtype=array.dtype)
        fp[:] = array[:]
        return fp

    def __getitem__(self, col):
        return self.__values[col]

    @property
    def columns(self):
        return self.__cols

    def to_pandas(self):
        table = pd.DataFrame()
        for col in self.__cols.tolist():
            table[col] = self.__values[col].tolist()
        return table

if __name__ == '__main__':
    data = [['Y', 'N', 'N', 'N', 'N', 'N', 'N', 1],
             ['N', 'Y', 'N', 'N', 'N', 'N', 'N', 1],
             ['N', 'N', 'Y', 'N', 'N', 'N', 'N', 1],
             ['N', 'N', 'N', 'Y', 'N', 'N', 'N', 1],
             ['N', 'N', 'N', 'N', 'Y', 'N', 'N', 1],
             ['N', 'N', 'N', 'N', 'N', 'Y', 'N', 2],
             ['N', 'N', 'N', 'N', 'N', 'N', 'Y', 2],
             ['N', 'N', 'N', 'N', 'N', 'N', 'N', 3],
             ['Y', 'N', 'N', 'N', 'N', 'Y', 'Y', 1],
             ['N', 'N', 'N', 'N', 'Y', 'N', 'Y', 1]]
    df = pd.DataFrame(data=data, columns=['travel_card',
                                            'five_profession_card',
                                            'world_card',
                                            'wm_cust',
                                            'gov_employee',
                                            'military_police_firefighters',
                                            'salary_ind',
                                            'output'])
    print('Before Sharing')
    print(df)
    shared_df = SharedDataFrame(df)
    print('After Sharing')
    print(shared_df.to_pandas())
    from pandas.testing import assert_frame_equal
    assert_frame_equal(df, shared_df.to_pandas(), check_dtype=True)
    print('Identical!')



