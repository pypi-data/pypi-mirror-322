# Case studies for the DeepMol publication

## Installation

1. Clone the repository and move into the directory:

```bash
git clone https://github.com/BioSystemsUM/deepmol_case_studies.git
cd deepmol_case_studies
```

2. Create a conda environment and activate it:

```bash
conda create -n deepmol_case_studies python=3.10
conda activate deepmol_case_studies
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
pip install --no-deps deepmol[all]==1.1.7
```

4. Install the package:

```bash
pip install .
```

## AutoML experiments - TDC Commons

AutoML experiments can be found in **[here](scripts/tdc/)**.

We used podman/docker for the experiments, the **[Dockerfile](Dockerfile)** can be found in this repository.

The "run" file can be found in **[here](run.sh)**.

## Comparison of DeepMol and QSARTuna

AutoML experiments for comparison between DeepMol and QSARTuna can be found in **[here](scripts/benchmark_automl/data_for_benchmark)**.

We used podman/docker for the experiments, the **[Dockerfile](Dockerfile)** can be found in this repository.

The "run_automl_benchmark" file can be found in **[here](run_automl_benchmark.sh)**.

## Benchmark computational resources and runtimes of DeepMol

The scripts to evaluate computational resources and runtimes of each method in DeepMol are **[here](scripts/benchmark_automl/benchmark_resources.py)**.

All the dataframes with this information are available **[here](scripts/benchmark_automl/runtimes/)**.

## Evaluate TDC commons benchmark datasets

To train and evaluate DeepMol models:

```python
from dcs.evaluation import get_results

results = get_results(tdc_dataset_name="Bioavailability_Ma", pipeline="bioavailability_optimal")
```

The **tdc_dataset_name** parameter is used to download the TDC commons benchmark datasets. Available datasets:
- "AMES"
- "BBB_Martins"
- "Bioavailability_Ma"
- "Caco2_Wang"
- "Clearance_Hepatocyte_AZ"
- "Clearance_Microsome_AZ"
- "HIA_Hou"
- "Pgp_Broccatelli"
- "Solubility_AqSolDB"
- "Lipophilicity_AstraZeneca"
- "VDss_Lombardo"
- "CYP2C9_Veith"
- "CYP2D6_Veith"
- "CYP3A4_Veith"
- "CYP2C9_Substrate_CarbonMangels"
- "CYP2D6_Substrate_CarbonMangels"
- "CYP3A4_Substrate_CarbonMangels"
- "DILI"
- "Half_Life_Obach"
- "hERG"
- "LD50_Zhu"
- "PPBR_AZ"

While the **pipeline** parameter is for internal pipeline loading. The pipelines are listed according to the paper, where there are the pipelines created based on the first AutoML experiment and the ones that were further optimized (optimal). Available pipelines:

- "ames"
- "bbb"
- "bioavailability" 
- "bioavailability_optimal"
- "caco"
- "clearance_hepatocyte"
- "clearance_microsome"
- "hia"
- "pgp"
- "solubility"
- "lipophilicity"
- "lipophilicity_optimal"
- "vdss"
- "cyp2c9"
- "cyp2d6"
- "cyp3a4" 
- "cyp2c9_substrate"
- "cyp2d6_substrate"
- "cyp3a4_substrate"
- "dili"
- "half_life"
- "herg"
- "hia"
- "ld50"
- "ppbr"

If intended, the default pipelines (all but the optimal) for each dataset can be called as follows:

```python
from dcs.evaluation import get_results

results = get_results(tdc_dataset_name="Bioavailability_Ma")
```

# Using DeepMol models

Models available so far: 

| Model Name                                   | How to Call                     | Prediction Type                                                |
|---------------------------------------------|---------------------------------|----------------------------------------------------------------|
| BBB (Blood-Brain Barrier)                   | `BBB`                  | Penetrates BBB (1) or does not penetrate BBB (0)              |
| AMES Mutagenicity                           | `AMES`                         | Mutagenic (1) or not mutagenic (0)                            |
| Human plasma protein binding rate (PPBR)    | `PPBR`                      | Rate of PPBR expressed in percentage                          |
| Volume of Distribution (VD) at steady state | `VDss`                | Volume of Distribution expressed in liters per kilogram (L/kg)|
| Caco-2 (Cell Effective Permeability)        | `Caco2`                   | Cell Effective Permeability (cm/s)                            |
| HIA (Human Intestinal Absorption)           | `HIA`                      | Absorbed (1) or not absorbed (0)                              |
| Bioavailability                             | `Bioavailability`           | Bioavailable (1) or not bioavailable (0)                      |
| Lipophilicity                               | `Lipophilicity`    | Lipophilicity log-ratio                                       |
| Solubility                                  | `Solubility`           | Solubility (log mol/L)                                        |
| CYP P450 2C9 Inhibition                     | `CYP2C9Inhibition`                 | Inhibit (1) or does not inhibit (0)                           |
| CYP P450 3A4 Inhibition                     | `CYP3A4Inhibition`                 | Inhibit (1) or does not inhibit (0)                           |
| CYP2C9 Substrate                            | `CYP2C9Substrate`| Metabolized (1) or does not metabolize (0)                    |
| CYP2D6 Substrate                            | `CYP2D6Substrate`| Metabolized (1) or does not metabolize (0)                    |
| CYP3A4 Substrate                            | `CYP3A4Substrate`| Metabolized (1) or does not metabolize (0)                    |
| Hepatocyte Clearance                        | `HepatocyteClearance`      | Drug hepatocyte clearance (uL.min-1.(10^6 cells)-1)           |
| NPClassifier                        | `NPClassifier`      | Pathway, Superclass, Class           |
| Plants secondary metabolite precursors predictor                        | `PlantsSMPrecursorPredictor`      | Precursor 1; Precursor 2           |
| Microsome Clearance                 | `MicrosomeClearance`       | Drug microsome clearance (mL.min-1.g-1)          |
| LD50                                | `LD50`        | LD50 (log(1/(mol/kg)))                      |
| hERG Blockers                       | `hERGBlockers`           | hERG blocker (1) or not blocker (0)               |

## How to use:

You can use them either individually or mixed together. 

You can call one model individually and get the results in one dataframe:




