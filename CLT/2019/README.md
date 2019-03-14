The benchmarking code consists of two parts:

1. A driver (driver.py) is in charge of gathering the operations per second and writing them to a pickled Numpy object file. In 
addition, a *.p file is created with the shape (in Numpy terms) of the benchmarks values. This driver assumes a working memtier_benchmark
and a Redis server running on localhost on port 6379. 
2. A 3D bar chart plotter takes these two files and creates a 3D bar chart of these values and exports this chart to an SVG file.
This plotter expects three file pairs: s390, gcp (for Google cloud pllattform) and intel. These pairs are produced on the corresponding
plattform by running the driver with the architecture as the first command line parameter.

Requirements: 

- Numpy
- Matplotlib

Enjoy!
