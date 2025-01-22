# ARTOF
The ARTOF package is a tool to read, process and analyze data collected from angle resolved time of flight (ARTOF) sensors.

## Getting started
To use this package python version >=3.10 is needed. The installation can be done using the command:
```
pip install ARTOF
```

## Example
Import the ARTOFLoader class
```py
from ARTOF.Loader import ARTOFLoader
```
Load run and transformed to desired format with desired x0, y0 and t0. The path should lead to a directory with all datafiles and metadata files (f.e. `aquisition.cfg`)
```py
artofLoader.load_run('./Run_018/', 'raw_SI', x0=0, y0=0)
```
Bin data (this step can rerun indepently of load_run)
```py
artofLoader.bin_data(bin_confs = [[-0.027, 0.027, 101], [-0.027, 0.027, 101],[0.3e-6, .4e-6, 201]])
```

Plot data as projection onto one or two axes and custom ranges for each axis
```py
artofLoader.plot([2])
artofLoader.plot([0,1], ranges=[None, None, [80, 120]])
```
Export data to a file in the same manner as plotting it
```py
artofLoader.export_to_csv('./export/Run_18_t.csv', [2])
artofLoader.export_to_csv('./export/Run_18_t.csv', [0,1], ranges=[None, None, [80, 120]])
```


## Documentation
The documenation can be found [here](https://codebase.helmholtz.cloud/carl.meier/artof/-/blob/main/Documentation.md). It is automatically generated from the docstrings in all python classes.

## Workflow
The implementation of a new feature should be conducted as follows:
1. Create a new branch with a sensible name as a fork from `dev`.
2. Implement features.
3. Check if all excisting tests are still working (cmd: `pytest`) and write new test functions using.
4. If there were changes to `dev` since the initial fork, merge it into your branch and resolve conflicts.
5. Increase version number in `setup.cfg` file.
6. Update documentation using the command `pydoc-markdown`.
6. Push all changes to the remote repository and create a merge request to `dev`.
7. Make sure all tests succeed in the pipeline and merge.
8. Create a merge request to `main` once enough features accumulated to roll out a new version. Make again sure all test pipelines succeed.
9. After merging to `main` a new version of the package is released to PyPi upon a successful pipeline run.

## Issues and new features
Issues and new features can be added [here](https://codebase.helmholtz.cloud/carl.meier/artof/-/issues).