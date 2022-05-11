from matplotlib import pyplot as plt

beam_times = [
    0.825,  # lusiadas
    11.972,  # yahoo_answers
    18.269  # amazon_review
]

spark_times = [
    4.317,  # lusiadas
    10.953,  # yahoo_answers
    13.258  # amazon_review

]
sequential_times = [
    0.042,  # lusiadas
    3.640,  # yahoo_answers
    6.414  # amazon_review
]

files_lines = [
    10000,  # lusiadas
    60000,  # yahoo_answers
    100000  # amazon_review
]

plt.style.use('seaborn')
plt.title('')
plt.xlabel('Dataset size (numbe of lines)')
plt.ylabel('Elapsed time (in seconds)')
plt.plot(files_lines, sequential_times, linestyle='--',
         marker='o', color='b', label='Sequential')
plt.plot(files_lines, beam_times, linestyle='--',
         marker='o', color='g', label='Beam')
plt.plot(files_lines, spark_times, linestyle='--',
         marker='o', color='r', label='PySpark')
plt.tight_layout()
plt.xticks(files_lines)
plt.legend()
plt.show()
