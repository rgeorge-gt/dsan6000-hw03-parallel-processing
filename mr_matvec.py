import os
import sys
from datetime import datetime, timedelta
import joblib
from mrjob.job import MRJob

class MatVecProduct(MRJob):
    def mapper(self, _, line):
        if os.path.isfile("b_small.pkl"):
            b = joblib.load("b_small.pkl")
        else:
            b = joblib.load("b_large.pkl")

        line_elts = line.split()

        row_index = int(line_elts[0])
        col_index = int(line_elts[1])
        A_val = float(line_elts[2])

        # Emit row index and contribution to that row
        yield row_index, A_val * b[col_index]

    def reducer(self, key, values):
        # Sum all contributions belonging to the same row
        yield key, sum(values)


if __name__ == '__main__':
    start_time = datetime.now()
    MatVecProduct.run()
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    sys.stderr.write(str(elapsed_time / timedelta(seconds=1)))
