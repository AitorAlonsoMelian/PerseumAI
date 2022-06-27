import os
import pandas as pd
import sys
import matplotlib.pyplot as plt

"""This files implements an app to convert all patterns from a directory into images"""

def pattern_to_image(filename, dest_path, source_path):
    """Converts a pattern from a file to an image"""
    dataframe = pd.read_csv(source_path + filename, index_col=0)
    dataframe.plot(title=f"{filename}")
    plt.savefig(dest_path + filename + ".png")

file_list = os.listdir(sys.argv[1])
for file in file_list:
    pattern_to_image(file, sys.argv[2], sys.argv[1])