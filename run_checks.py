import glob
import itertools
import time
import plotly.express as px
from analyses import *


ignore = [".md", ".py"]


analyses = {
    "500kreads.fa.gz": [count_gs_in_fastq],
    "big.fq.gz": [scan_file, count_gs_in_fastq],
    "big.bed.gz": [scan_file],
    "big.vcf.gz": [scan_file]
}


def get_suitable_analyses(file_name):
    return itertools.chain(*[functions for file_ending, functions in analyses.items()
                             if file_name.endswith(file_ending)])


def run_analysis(function, file_name):
    t_start = time.perf_counter()
    function(file_name)
    time_spent = time.perf_counter()-t_start

    results_file = "results/" + function.__name__ + "-" + file_name + ".csv"
    with open(results_file, "a") as f:
        f.write(str(int(time.time())) + "," + str(time_spent) + "\n")

    # update plot
    fig_file = results_file.replace(".csv", ".png")
    fig_title = function.__name__ + " on file " + file_name
    with open(results_file) as f:
        lines = [l.split(",") for l in f.readlines()]
        timestamps = np.array([int(l[0]) for l in lines], dtype='datetime64[s]')
        values = [float(line[1]) for line in lines]
        fig = px.line(x=timestamps, y=values, title=fig_title)
        fig.write_image(fig_file)

    return fig_file


result_files = []
for file in glob.glob("*"):
    if file.split(".")[-1] in ignore or file.startswith("."):
        continue

    for analysis in get_suitable_analyses(file):
        result_files.append(run_analysis(analysis, file))


# make readme
with open("Readme.md", "w") as f:
    for result in result_files:
        f.write("![](" + result + ")\n\n")



