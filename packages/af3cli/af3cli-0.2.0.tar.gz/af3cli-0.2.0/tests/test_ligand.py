import pytest

from af3cli.ligand import Ligand, LigandType


@pytest.mark.parametrize("lig_type,lig_type_value",[
    (LigandType.CCD, "ccdCodes"),
    (LigandType.SMILES, "smiles")
])
def test_ligand_type(lig_type: LigandType, lig_type_value: str) -> None:
    assert LigandType(lig_type).value == lig_type_value


@pytest.mark.parametrize("lig_type,lig_str,num,seq_id,actual_num",[
    (LigandType.CCD, "NAC", None, None, 1),
    (LigandType.CCD, "ATP", 2, ["A", "B"], 2),
    (LigandType.SMILES, "CCC", None, None, 1),
    (LigandType.SMILES, "CCC", 1, None, 1),
    (LigandType.SMILES, "CCC", 2, None, 2),
    (LigandType.SMILES, "CCC", 2, ["A", "B"], 2),
    (LigandType.SMILES, "CCC", None, ["A", "B"], 2)
])
def test_ligand_init(
        lig_type: LigandType,
        lig_str: str,
        num: int,
        seq_id: list[str] | str | None,
        actual_num: int
) -> None:
    ligand = Ligand(lig_type, lig_str, num, seq_id)
    assert ligand.ligand_type == lig_type
    assert ligand.ligand_str == lig_str
    assert ligand.num == actual_num
    assert ligand.get_id() == seq_id


@pytest.mark.parametrize("lig_type,lig_str,seq_id",[
    (LigandType.CCD, "ATP", ["A", "B"]),
    (LigandType.SMILES, "CCC", ["A", "B"]),
    (LigandType.SMILES, "CCC", ["A", "B"])
])
def test_ligand_to_dict(
        lig_type: LigandType,
        lig_str: str,
        seq_id: list[str] | str | None
) -> None:
    ligand = Ligand(lig_type, lig_str, seq_id=seq_id)
    lig_dict = ligand.to_dict()
    key, values = next(iter(lig_dict.items()))
    assert key == "ligand"
    assert values[lig_type.value] == lig_str
    assert values["id"] == seq_id
