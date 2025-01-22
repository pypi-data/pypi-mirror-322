## Reason
Downloading from official repository is slow. Downloading from google drive repetitively often fails.

## Usage
Install package by `pip3 install -e . ` and then 
```
from ycb_utils import load
mesh = load("011_banana")  # mesh is trimesh.Trimesh object
```

##  License of stl files
The files in `ycb_utils/stl_files/` are download by https://www.ycbbenchmarks.com/
License for the data set is : Creative Commons Attribution 4.0 International (CC BY 4.0)
See http://ycb-benchmarks.s3-website-us-east-1.amazonaws.com/ for the detail

