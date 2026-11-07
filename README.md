# OpenBindZika

Pose prediction for the OpenBind Blind Challenge 1, the Zika virus NS2B-NS3 protease.

This is a work in progress. I am building it in the open while the challenge runs.

## The challenge

The task is to predict the protein-ligand complex for 400 compounds. A prediction counts only if the ligand BiSyRMSD is below 1.5 A, the lDDT-PLI is above 0.8, and all PoseBusters checks pass. Submissions close on 16 December 2026.

Challenge page: https://huggingface.co/spaces/openadmet/openbind-blind-challenge-1

## What is in this repo

- `notebooks/zika_pipeline.ipynb` holds the whole pipeline in one notebook.
- `scripts/` has two early helper scripts that the notebook now replaces.
- `setup_check.py` tests the three environments.
- The `.yml` and `.txt` files are snapshots of the environments.

## Approach

1. Run Boltz-2 on every compound and keep five samples each.
2. Check every sample with PoseBusters.
3. Pick one pose per compound, using the highest confidence among the samples that pass.
4. Planned next, relax the pocket around poses that still clash, using OpenMM.
5. Planned next, add template-based placement from public NS2B-NS3 structures.

Done so far are the environments, a three-compound Boltz pilot, the PoseBusters check, and a test of the official scorer. The full 400 compound run has not been done yet.

## Environments

| Env | Holds | Used for |
|---|---|---|
| `zika` | Boltz, PoseBusters, Vina, RDKit, PyTorch | generating and checking poses |
| `zika-eval` | OpenStructure | the official scorer |
| `zika-md` | OpenMM, PDBFixer | pocket relaxation |

## Setup

I have not yet tested a rebuild from these files.

    conda env create -f zika_env_after_boltz.yml
    conda env create -f zika_eval_env.yml
    conda env create -f zika_md_env.yml
    conda activate zika
    pip install posebusters "click==8.1.7"
    conda install -c conda-forge fpocket

## Data

The challenge data is not in this repo. I download it from Hugging Face and clone the organizers' tutorial repo into `tutorial/`.

    hf download openadmet/openbind-blind-challenge-1 --repo-type dataset --local-dir data/challenge
    git clone https://github.com/OpenADMET/OpenBind-Challenge-1-Tutorial.git tutorial

## Licenses and disclosures

The code is under the MIT license. I use public data only and no proprietary data. The tools I call keep their own licenses.
