"""
Example:
Human Kv7.2 (KCNQ2) with retigabine
    - Protein Data Bank (PDB) Entry: 7CR2
    - Reference: https://www.rcsb.org/structure/7CR2

This script provides a Python implementation as an alternative to the af3cli input bash script.
"""

import pprint
from af3cli import InputBuilder, Sequence, SequenceType, Ligand, LigandType

# Define constants
FILENAME = "example_SMILES_python.json"
JOB_NAME = "example_SMILES_py_job"
INPUT_SEQUENCE_TYPE = SequenceType.PROTEIN
INPUT_SEQUENCE_STR = (
    "MAGKPPKRNAFYRKLQNFLYNVLERPRGWAFIYHAYVFLLVFSCLVLSVFSTIKEYEKSSEGALYILEIVTIV"
    "VFGVEYFVRIWAAGCCCRYRGWRGRLKFARKPFCVIDIMVLIASIAVLAAGSQGNVFATSALRSLRFLQILRM"
    "IRMDRRGGTWKLLGSVVYAHSKELVTAWYIGFLCLILASFLVYLAEKGENDHFDTYADALWWGLITLTTIGYG"
    "DKYPQTWNGRLLAATFTLIGVSFFALPAGILGSGFALKVQEQHRQKHFEKRRNPAAGLIQSAWRFYATNLSRT"
    "DLHSTWQYYERTVTVPMYSSQTQTYGASRLIPPLNQLELLRNLKSKSGLAFRKDPPPEPSPSKGSPCRGPLCG"
    "CCPGRSSQKVSLKDRVFSSPRGVAAKGKGSPQAQTVRRSPSADQSLEDSPSKVPKSWSFGDRSRARQAFRIKG"
    "AASRQNSEEASLPGEDIVDDKSCPCEFVTEDLTPGLKVSIRAVCVMRFLVSKRKFKESLRPYDVMDVIEQYSA"
    "GHLDMLSRIKSLQSRVDQIVGRGPAITDKDRTKGPAEAELPEDPSMMGRLGKVEKQVLSMEKKLDFLVNIYMQ"
    "RMGIPPTETEAYFGAKEPEPAPPYHSPEDSREHVDRHGCIVKIVRSSSSTGQKNFSVEGGSSGGWSHPQFEK"
)
INPUT_SEQUENCE_NUM = 4  # homotetrameric channel protein

LIGAND_TYPE = LigandType.SMILES
LIGAND_SMILES = "CCOC(=O)NC1=C(C=C(C=C1)NCC2=CC=C(C=C2)F)N"
LIGAND_NUM = 4

# Create protein sequence object
sequence = Sequence(
    seq_type=INPUT_SEQUENCE_TYPE,
    seq_str=INPUT_SEQUENCE_STR,
    num=INPUT_SEQUENCE_NUM
)

# Create ligand object
ligand = Ligand(
    ligand_type=LIGAND_TYPE,
    ligand_str=LIGAND_SMILES,
    num=LIGAND_NUM
)

# Build input configuration for the job
input_builder = InputBuilder()
input_builder.set_name(JOB_NAME)
input_builder.add_sequence(sequence)
input_builder.add_ligand(ligand)
internal_input = input_builder.build()

# Uncomment following line to generate output as JSON file
#internal_input.write(FILENAME)

print_json_via_debug = pprint.PrettyPrinter(indent=4)
print_json_via_debug.pprint(internal_input.to_dict())
