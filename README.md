# Migration-Aware Genetic Optimization for MapReduce Scheduling and Replica Placement in Hadoop

This program has been implemented for the research presented in the article "Migration-Aware Genetic Optimization for MapReduce Scheduling and Replica Placement in Hadoop", accepted for publication in the "Journal of Grid Computing".


This a NSGA-II algorithm implementation in python 2.7, considering the GA settings explained in the article. For more details, please, read the article in https://doi.org/10.1007/s10723-018-9432-8

This program is released under the GPLv3 License.

**Please consider to cite this work as**:

```bash

@article{guerrero_migrationaware,
	title = {Migration-Aware Genetic Optimization for MapReduce Scheduling and Replica Placement in Hadoop},
	volume = {29},
	copyright = {All rights reserved},
	issn = {1558-2183},
	doi = {10.1109/TPDS.2018.2837743},
	abstract = {This work addresses the optimization of file locality, file availability, and replica migration cost in a Hadoop architecture. Our optimization algorithm is based on the Non-dominated Sorting Genetic Algorithm-II and it simultaneously determines file block placement, with a variable replication factor, and MapReduce job scheduling. Our proposal has been tested with experiments that considered three data center sizes (8, 16 and 32 nodes) with the same workload and number of files (150 files and 3519 file blocks). In general terms, the use of a placement policy with a variable replica factor obtains higher improvements for our three optimization objectives. On the contrary, the use of a job scheduling policy only improves these objectives when it is used along a variable replication factor. The results have also shown that the migration cost is a suitable optimization objective as significant improvements up to 34% have been observed between the experiments.},
	number = {16},
	journal = {Journal of Grid Computing},
	author = {Guerrero, Carlos and Lera, Isaac and Juiz, Carlos},
	month = feb,
	year = {2018},
	keywords = {Resource management, Genetic algorithm,Multi-objective optimization,Replica placement, MapReduce scheduling, Hadoop},
	pages = {265–-284}
}
```

**Execution of the program**:

```bash
    python mainGA.py
```

**Acknowledgment**:

This research was supported by the Spanish Government (Agencia Estatal de Investigación) and the European Commission (Fondo Europeo de Desarrollo Regional) through Grant Number TIN2017-88547-P (AEI/FEDER, UE).
