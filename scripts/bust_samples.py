import glob, json, subprocess, sys
from rdkit import Chem
from rdkit.Chem import AllChem

smi = sys.argv[1]
pred_dir = sys.argv[2]
files = sorted(glob.glob(f'{pred_dir}/*_model_*.pdb'))
for i, f in enumerate(files):
    recs = [l for l in open(f) if l.startswith(('ATOM', 'HETATM'))]
    open(f'/tmp/s{i}_lig.pdb', 'w').writelines(l for l in recs if l[17:20].strip() == 'LIG')
    open(f'/tmp/s{i}_prot.pdb', 'w').writelines(l for l in recs if l[17:20].strip() != 'LIG')
    m = AllChem.AssignBondOrdersFromTemplate(Chem.MolFromSmiles(smi), Chem.MolFromPDBFile(f'/tmp/s{i}_lig.pdb'))
    w = Chem.SDWriter(f'/tmp/s{i}_lig.sdf'); w.write(m); w.close()
    r = subprocess.run(['bust', f'/tmp/s{i}_lig.sdf', '-p', f'/tmp/s{i}_prot.pdb'], capture_output=True, text=True)
    name = f.split('/')[-1]
    conf = json.load(open(f.replace(name, 'confidence_' + name.replace('.pdb', '.json'))))
    print(name, '->', r.stdout.strip().split('\n')[-1], '| confidence', round(conf['confidence_score'], 3))
