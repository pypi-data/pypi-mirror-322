# NectaPy

A Python package for accessing NECTA (National Examinations Council of Tanzania) examination results.

## Installation

```bash
pip install NectaPy

```

## Usage

```python
from NectaPy import st_result
# Get student result
result = st_result('XXXX/0003/2023', 'ftna');
print(result)
```

## Supported Examinations

Primary Level:

> - SFNA (Standard 2): 2017-2024
> - PSLE (Standard 7): 2016-2024

Secondary Level:

> - FTNA (Form 2): 2022-2024
> - CSEE (Form 4): 2015-2024
> - ACSEE (Form 6): 2014-2024

College Level:

> - GATCE: 2019-2024
> - DSEE: 2019-2024
> - GATSCCE: 2019-2024

### Example Output

```json
{
"CNO": "XXXX/0003",
"PReM NO": "xxxxxxx"
"CANDIDATE NAME": "XXXXX XXXXX XXXXX",
"SEX": "F",
"AGGT": "18",
"DIV": "II",
"DETAILED SUBJECTS": "CIV-'D' HIST-'C' GEO-'B' KISW-'C' ENGL-'B' PHY-'D' CHEM-'B' BIO-'C' B/MATH-'C'"
}

```
