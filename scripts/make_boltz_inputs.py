import sys
from pathlib import Path
import pandas as pd

root = Path.home() / 'OpenBindZika'
run = sys.argv[1]
limit = int(sys.argv[2]) if len(sys.argv) > 2 else None

fa = open(root / 'tutorial/inputs/NS2B-NS3_protein_sequence.fasta').read().split('>')[1:]
seqs = {r.split('\n')[0].split('|')[1]: ''.join(r.split('\n')[1:]) for r in fa}
ns2b, ns3 = seqs['Chain A'], seqs['Chain B']
assert len(ns2b) == 46 and len(ns3) == 168

df = pd.read_csv(root / 'data/challenge/openbind-blind-challenge-1-TEST-BLINDED.csv')
if limit:
    df = df.head(limit)

out = root / 'runs' / run / 'inputs'
out.mkdir(parents=True, exist_ok=True)
for name, smi in zip(df['Molecule_Name'], df['SMILES']):
    (out / f'{name}.yaml').write_text(f"""version: 1
sequences:
  - protein:
      id: A
      sequence: {ns2b}
      msa: {root}/data/msa/zika_ns2b.csv
  - protein:
      id: B
      sequence: {ns3}
      msa: {root}/data/msa/zika_ns3.csv
  - ligand:
      id: C
      smiles: {smi}
""")
print(len(df), 'inputs written to', out)
