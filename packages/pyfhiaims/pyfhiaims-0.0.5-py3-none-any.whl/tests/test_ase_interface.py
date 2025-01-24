"""Tests for the ASE interface."""

import pytest


def test_ase_interface_outputs(data_dir):

    try:
        from pyfhiaims.external_interfaces.ase.io import read_aims_results
    except ImportError:
        pytest.skip("No ASE installed.")

    output_file = data_dir / "stdout" / "relax.out.gz"
    ase_results = read_aims_results(output_file, verbosity="all")
    from pprint import pprint
    pprint(ase_results)


def test_docs_control_in(data_dir):
    from pyfhiaims import AimsStdout
    from pprint import pprint
    output_file = data_dir / "stdout" / "single_point.out.gz"
    out_file = AimsStdout(output_file)
    pprint(out_file.warnings)

