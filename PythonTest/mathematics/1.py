import scipy as sp
import os
data_path = "./data"

matrix = sp.io.mmread(os.path.join(data_path,"add20.mtx"))
matrix = matrix.toarray()

print(matrix)