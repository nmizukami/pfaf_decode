# pfaf_decode
python script/utilities to decode pfafstetter code to identify river network relationships

e.g., 
1. upstream/downstream relationship
2. immediate downstream reach
3. subset upstream basins from larger basin
4. Find outlet reaches


To use pfafstetter modules:

Install the pfafstetter by

```bash
cd pfaf_decode 
conda activate $ENVIRONMENT_NAME
pip install -e .
```
or

Append to the system environment variable PYTHONPATH the pfafstetter directory 

```bash
PYTHONPATH=$PYTHONPATH:<path_to_pfafstetter directory>
export $PYTHONPATH
```
