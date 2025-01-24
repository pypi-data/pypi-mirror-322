# pyfhiaims – an FHI-aims Python suite 

## Installation

You can install `pyfhiaims` from PyPI via `pip`:
```bash
pip install pyfhiaims
```

Or, alternatively, you can install it from the main branch of this Git repository:
```bash
git clone https://gitlab.com/FHI-aims-club/pyfhiaims.git
cd pyfhiaims
pip install .
```

## Usage
The FHI-aims output file can be parsed in the following way:

```python
from pyfhiaims import AimsStdout

stdout = AimsStdout("aims.out")
```

Then you can access all the parsed results (`stdout.results`),
run metadata (runtime choices and some geometry statistics — 
`stdout.metadata`), warnings (`stdout.warnings`), and errors.
Also, `stdout.is_finished_ok` tells if FHI-aims run has been finished 
without any errors.

There are several properties defined that make access to different 
widely used values easier, like `energy` and `forces`. 
Also, the top level keys of `stdout.results` dictionary can be accessed 
using dot notation (so run times can be accessed with 
`stdout.final["time"]`). 

There are many values that are parsed from the `aims.out` file; you are 
welcome to explore `stdout.results` dictionary. 

## Support
Just write us an issue in the issue tracker!

## Roadmap
To be written...

## Contributing
Contributions are extremely welcome!

## Authors and acknowledgment
The package was written by:
 * Tom Purcell
 * Andrei Sobolev

## License
The project is licensed under MIT license.
