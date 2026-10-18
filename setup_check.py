import subprocess

CHECKS = [
    ("zika", "chem stack", '''python -c "import rdkit, meeko, Bio, pandas, sklearn, papermill"'''),
    ("zika", "numpy 1.26", '''python -c "import numpy; assert numpy.__version__.startswith('1.26')"'''),
    ("zika", "torch cuda", '''python -c "import torch; assert torch.cuda.is_available()"'''),
    ("zika", "boltz cli", "boltz --help"),
    ("zika", "posebusters", "bust --help"),
    ("zika", "vina", "vina --version"),
    ("zika", "fpocket", "which fpocket"),
    ("zika", "gnina", "$HOME/gnina --version"),
    ("zika-eval", "openstructure", '''python -c "from ost.mol.alg.ligand_scoring_scrmsd import SCRMSDScorer; from ost.mol.alg.ligand_scoring_lddtpli import LDDTPLIScorer"'''),
    ("zika-md", "openmm cpu", '''python -c "import openmm, pdbfixer; from openmm import Platform; Platform.getPlatformByName('CPU')"'''),
]

failed = 0
print(f"{'env':<10} {'check':<14} result")
for env, name, cmd in CHECKS:
    r = subprocess.run(["conda", "run", "-n", env, "bash", "-c", cmd], capture_output=True, text=True)
    ok = r.returncode == 0
    failed += not ok
    print(f"{env:<10} {name:<14} {'PASS' if ok else 'FAIL'}")
print(f"\n{len(CHECKS) - failed}/{len(CHECKS)} passed")
