"""
Example:
Pseudomonas aeruginosa PvdQ covalently acylated with myristic acid
    - Protein Data Bank (PDB) Entry: 3SRA
    - Reference: https://www.rcsb.org/structure/3SRA

This script provides a Python implementation as an alternative to the af3cli input bash script.
"""

import pprint
from af3cli import InputBuilder, Sequence, SequenceType, Ligand, LigandType, Bond

# Define filename and job name
FILENAME = "example_bonds_python.json"
JOB_NAME = "example_bonds_py_job"


# Protein sequence for PvdQ subunit alpha
PROTEIN_SEQUENCE_A = (
    "TGLAADIRWTAYGVPHIRAKDERGLGYGIGYAYARDNACLLAEEIVTARGERARYFGSEGKSSAELDNLPSDI"
    "FYAWLNQPEALQAFWQAQTPAVRQLLEGYAAGFNRFLREADGKTTSCLGQPWLRAIATDDLLRLTRRLLVEGG"
    "VGQFADALVAAAPPGAE"
)
PROTEIN_ID_A = "E"

# Protein sequence for PvdQ subunit beta
PROTEIN_SEQUENCE_B = (
    "SNAIAVGSERSADGKGMLLANPHFPWNGAMRFYQMHLTIPGRLDVMGASLPGLPVVNIGFSRHLAWTHTVDTS"
    "SHFTLYRLALDPKDPRRYLVDGRSLPLEEKSVAIEVRGADGKLSRVEHKVYQSIYGPLVVWPGKLDWNRSEAY"
    "ALRDANLENTRVLQQWYSINQASDVADLRRRVEALQGIPWVNTLAADEQGNALYMNQSVVPYLKPELIPACAI"
    "PQLVAEGLPALQGQDSRCAWSRDPAAAQAGITPAAQLPVLLRRDFVQNSNDSAWLTNPASPLQGFSPLVSQEK"
    "PIGPRARYALSRLQGKQPLEAKTLEEMVTANHVFSADQVLPDLLRLCRDNQGEKSLARACAALAQWDRGANLD"
    "SGSGFVYFQRFMQRFAELDGAWKEPFDAQRPLDTPQGIALDRPQVATQVRQALADAAAEVEKSGIPDGARWGD"
    "LQVSTRGQERIAIPGGDGHFGVYNAIQSVRKGDHLEVVGGTSYIQLVTFPEEGPKARGLLAFSQSSDPRSPHY"
    "RDQTELFSRQQWQTLPFSDRQIDADPQLQRLSIRE"
)
PROTEIN_ID_B = "G"

# Sequence type definition
INPUT_SEQUENCE_TYPE = SequenceType.PROTEIN

# Myristic acid, CCD format
LIGAND_TYPE = LigandType.CCD
LIGAND_CCD = "MYR"
LIGAND_ID = "M"

# Bond expression
BOND_EXPRESSION = f"{PROTEIN_ID_B}:1:OG-{LIGAND_ID}:1:C1"

# Create protein sequence object
sequence_a = Sequence(
    seq_type=INPUT_SEQUENCE_TYPE,
    seq_str=PROTEIN_SEQUENCE_A,
    seq_id=PROTEIN_ID_A
)
sequence_b = Sequence(
    seq_type=INPUT_SEQUENCE_TYPE,
    seq_str=PROTEIN_SEQUENCE_B,
    seq_id=PROTEIN_ID_B
)

# Create ligand object
ligand = Ligand(
    ligand_type=LIGAND_TYPE,
    ligand_str=LIGAND_CCD,
    seq_id=LIGAND_ID
)

# Create bond object
bond = Bond.from_string(BOND_EXPRESSION)

# Build input configuration for the job
input_builder = InputBuilder()
input_builder.set_name(JOB_NAME)
input_builder.add_sequence(sequence_a)
input_builder.add_sequence(sequence_b)
input_builder.add_ligand(ligand)
input_builder.add_bonded_atom_pair(bond)
internal_input = input_builder.build()

# Uncomment following line to generate output as JSON file
#internal_input.write(FILENAME)

print_json_via_debug = pprint.PrettyPrinter(indent=4)
print_json_via_debug.pprint(internal_input.to_dict())
