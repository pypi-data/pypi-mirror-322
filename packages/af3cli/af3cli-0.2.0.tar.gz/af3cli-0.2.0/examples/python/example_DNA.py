"""
Example:
simple dsDNA

This script provides a Python implementation as an alternative to the af3cli input bash script.
"""

import pprint
from af3cli import InputBuilder, Sequence, SequenceType, Ligand, LigandType

# Define constants
FILENAME = "example_DNA_python.json"
JOB_NAME = "example_DNA_py_job"
INPUT_SEQUENCE_TYPE = SequenceType.DNA
INPUT_SEQUENCE_STR = "GCGAATTCG"
INPUT_SEQUENCE_NUM = 2

# Create DNA sequence object
sequence = Sequence(
    seq_type=INPUT_SEQUENCE_TYPE,
    seq_str=INPUT_SEQUENCE_STR,
    num=INPUT_SEQUENCE_NUM
)


# Build input configuration for the job
input_builder = InputBuilder()
input_builder.set_name(JOB_NAME)
input_builder.add_sequence(sequence)
internal_input = input_builder.build()

# Uncomment following line to generate output as JSON file
#internal_input.write(FILENAME)

print_json_via_debug = pprint.PrettyPrinter(indent=4)
print_json_via_debug.pprint(internal_input.to_dict())
