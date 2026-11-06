# A Semi-Supervised Few-Shot Framework for Detecting Stealth Malicious Network Traffic

[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![PyTorch: 2.7+](https://img.shields.io/badge/PyTorch-2.7%2B-red.svg)](https://pytorch.org/)

Official research repository containing the implementation and experimental material associated with the paper:

> **"A Semi-Supervised Few-Shot Framework for Detecting Stealth Malicious Network Traffic"**

---

## Authors & Affiliation

- **Luca Caviglione**<sup>1</sup> [<img src="https://cdn.simpleicons.org/orcid/A6CE39" width="12" alt="ORCID">](https://orcid.org/0000-0001-6466-3354) &bull; `luca.caviglione@ge.imati.cnr.it`
- **Massimo Guarascio**<sup>2</sup> [<img src="https://cdn.simpleicons.org/orcid/A6CE39" width="12" alt="ORCID">](https://orcid.org/0000-0001-7711-9833) &bull; `massimo.guarascio@icar.cnr.it`
- **Angelica Liguori**<sup>2</sup> [<img src="https://cdn.simpleicons.org/orcid/A6CE39" width="12" alt="ORCID">](https://orcid.org/0000-0001-9402-7375) &bull; `angelica.liguori@icar.cnr.it`
- **Francesco Scala**<sup>2</sup>[<img src="https://cdn.simpleicons.org/orcid/A6CE39" width="12" alt="ORCID">](https://orcid.org/0009-0007-5224-0910) &bull; `francesco.scala@icar.cnr.it`
- **Bernardo Valente**<sup>2,3</sup>[<img src="https://cdn.simpleicons.org/orcid/A6CE39" width="12" alt="ORCID">](https://orcid.org/0009-0009-2506-803X) &bull; `bernardo.valente@imtlucca.it`

<sup>1</sup> **National Research Council of Italy, Institute for Applied Mathematics and Information Technologies (CNR-IMATI)**
Via de Marini 6, Genova, 16149, Italy

<sup>2</sup> **National Research Council of Italy, Institute for High Performance Computing and Networking (CNR-ICAR)**  
Via P. Bucci 8/9C, 87036 Rende (CS), Italy  

<sup>3</sup> **IMT School for Advanced Studies** Piazza S. Ponziano 6, Lucca, 55100, Italy

---

## Overview

Modern malware increasingly disguises its network activity by mimicking legitimate traffic, making stealthy threats difficult to identify through signature-based mechanisms and conventional intrusion detection systems. Machine learning approaches can help detect these behaviors, but their effectiveness is often limited by the scarcity of labeled malicious samples and the substantial differences between benign and malicious traffic.

This work introduces **Data Driven Monitor (DDM)**, 
a dual-layer framework that combines semi-supervised representation learning with few-shot adaptation. 
In the upper layer, a neural architecture is trained only against normal traffic data
to extract general-purpose features. In the lower layer, a supervised module learns 
task-specific patterns from the limited labeled samples available.
The proposed design combines complementary attack-agnostic and anomaly-sensitive
representations, adopts an asymmetric freeze/unfreeze policy during few-shot adaptation, 
preserves input-level traffic indicators through a skip connection, and mitigates
attack-sample scarcity through batch-level resampling and selective augmentation.

The framework is evaluated against three stealth network threats:
- **Covert Data Exfiltration:** Hidden communication through the manipulation of IPv4 Time To Live (TTL) values.
- **Cobalt Strike DNS Beaconing:** Command & Control (C&C) communications embedded in DNS traffic.
- **Slow DoS:** Low-rate HTTP attacks designed to exhaust server resources while resembling legitimate traffic.

Experimental results show that DDM provides competitive detection performance across all three scenarios while maintaining a False Alarm Rate (FAR) close to zero.

---

## Repository Structure
```text
PERUN-DDM/
├── dataset/                        # Dataset folder
├── src/
│   ├── arn/
│   │   ├── loss.py                 # Loss functions for ARN
│   │   ├── model.py                # ARN model architecture
│   │   ├── plotter.py              # Methods for visualization
│   │   ├── trainer.py              # ARN training procedures
│   │   └── utils.py                # ARN utility functions
│   │
│   ├── dataset/
│   │   ├── _cobalt_loader.py       # Cobalt Strike dataset loader
│   │   ├── _covert_loader.py       # Covert dataset loader
│   │   ├── _slowdos_loader.py      # Slow DoS dataset loader
│   │   ├── dataset_loader.py       # Dataset loading
│   │   └── utils.py                # Preprocessing utilies
│   │
│   ├── model/
│   │   └── predictive_model.py     # DDM architecture and training/testing utilities
│   │
│   ├── support/
│   │   ├── arguments.py            # Command-line argument parsing
│   │   └── utils.py                # Utilities
│   │
│   ├── pre_train_arn.py            # ARN pre-training pipeline
│   ├── testing.py                  # Model testing
│   └── training.py                 # Model training
│
├── LICENSE
├── README.md
└── requirements.txt               # Dependencies
```

---
## Datasets

The experimental evaluation considers three datasets, each representing a different stealth attack scenario.


### 1. Covert Channel
<img src="images/case1_covert_channel.png" width="600">

- **Reference Dataset:** Network traces derived from the dataset presented in Cassavia et al. (2024), originally based on the IoT traffic benchmark by Sivanathan et al. (2018).
- **Scenario:** An infected IoT device exfiltrates information through a covert channel by manipulating the TTL field of IPv4 packets.
- **Traffic Generation:** The covert communication traces are generated using `pcapStego`.

### 2. Cobalt Strike
<img src="images/case2_cobalt_strike.png" width="600">

- **Reference Dataset:** DNS Exfiltration Dataset, based on real-world DNS traffic traces.
- **Scenario:** Cobalt Strike Command & Control communications are embedded in DNS conversations to conceal signaling and payload information.
- **Traffic Representation:** Pre-computed numerical features extracted from DNS conversations.

### 3. Slow DoS
<img src="images/case3_slow_dos.png" width="600">

- **Reference Dataset:** [CIC-IDS2017](https://www.unb.ca/cic/datasets/ids-2017.html).
- **Scenario:** Low-rate HTTP attacks target Web endpoints by maintaining long-lived connections and sending incomplete requests.
- **Attack Types:** Slowloris and slowHTTPtest.
- **Traffic Representation:** Labeled network-flow records.

### Dataset Statistics
In the following table are reported the main statistics of the datasets in terms of total tuples and distribution of samples.

| Dataset | Total Tuples | Benign Samples | Attack Samples |
|---|---:|---:|---:|
| Covert Channel | 120,950 | 103,385 | 17,565 |
| Cobalt Strike | 938,833 | 797,626 | 141,207 |
| Slow DoS | 549,044 | 537,749 | 11,295 |

**Data Availability:** The datasets are publicly available on their respective websites or upon request.

---
## Methodological Pipeline
<img src="images/architecture_final_2.png" width="600">

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Recommended: Dedicated virtual environment (`venv` or `conda`)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/massimo-guarascio/PERUN-DDM.git
   cd PERUN-DDM
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate
   # On Windows: myenv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Execution Workflow
The overall workflow consists of two main training stages: ARN pre-training and DDM training. 
The dataset to be used must be specified for each execution as well as the hyperparameters (otherwise default parameters are used).
They are selected through command-line arguments.

1. **ARN Pre-training**

Run the following command to pre-train the ARN architecture:
```bash
   PYTHONPATH=$(pwd) python3 src/pre_train_arn.py --attack-type slowdos --apply-normalization True --n_runs 1
   ```

2. **DDM training**

Once ARN pre-training is completed, run the main training script:
```bash
   PYTHONPATH=$(pwd) python3 src/training.py --attack-type slowdos --apply-normalization True
   ```

3. **DDM testing**
After the training phase, test the approach:
```bash
   PYTHONPATH=$(pwd) python3 src/testing.py --attack-type slowdos --apply-normalization True
   ```
#### Dataset Configuration

The --attack-type argument specifies the dataset to be used.

| Dataset       | Argument |
|---------------|----------|
| Covert Channel | `covert` |
| Cobalt Strike  | `cobalt` |
| Slow DoS       | `slowdos` |

For Cobalt Strike and Slow DoS datasets, normalization must be explicitly enabled using `--apply-normalization True`.

### Examples

#### Slow DoS:
```bash
PYTHONPATH=$(pwd) python3 src/pre_train_arn.py --attack-type slowdos --apply-normalization True --n_runs 1
PYTHONPATH=$(pwd) python3 src/training.py --attack-type slowdos --apply-normalization True
PYTHONPATH=$(pwd) python3 src/testing.py --attack-type slowdos --apply-normalization True
```
#### Cobalt Strike:

```bash
PYTHONPATH=$(pwd) python3 src/pre_train_arn.py --attack-type cobalt --apply-normalization True --n_runs 1
PYTHONPATH=$(pwd) python3 src/training.py --attack-type cobalt --apply-normalization True
PYTHONPATH=$(pwd) python3 src/testing.py --attack-type cobalt --apply-normalization True
```

#### Covert:

```bash
PYTHONPATH=$(pwd) python3 src/pre_train_arn.py --attack-type covert --n_runs 1
PYTHONPATH=$(pwd) python3 src/training.py --attack-type covert
PYTHONPATH=$(pwd) python3 src/testing.py --attack-type covert
```

### Configuration Parameters

Additional experimental settings can be specified through command-line arguments.

| Argument | Default | Description |
|---|---|---|
| `--device` | Automatically selected | Computation device (`cuda` or `cpu`) |
| `--seed` | `42` | Random seed for reproducibility |
| `--train-normal-ratio` | `0.5` | Fraction of normal data used for training |
| `--b-max` | `80` | Maximum attack budget |
| `--n-train-attacks` | `5` | Number of attack samples in the few-shot training set |
| `--apply-normalization` | `False` | Enables data normalization |
| `--batch-size` | `32` | DataLoader batch size |
| `--z-dim` | `8` | Latent code dimension for ARN Generator |
| `--nf-out` | `8` | Number of neurons for ARN Generator |
| `--n_runs` | `0` | Number of experimental runs |
| `--n_exps` | `our_model` | Name of the experimental run |
| `--num_epochs` | `50` | Number of ARN training epochs |
| `--lr_D` | `0.0001` | Learning rate for ARN Discriminator |
| `--lr_G` | `0.001` | Learning rate for ARN Generator |
| `--SAVE_FOLDER` | `./saved` | Directory for saving models |
| `--nout` | `16` | Number of neurons in ARN Discriminator feature extractor |
| `--nc_out` | `4` | Number of neurons in ARN Discriminator classifier |
| `--n_epochs_cpvae` | `16` | Number of DDM training epochs |

## Citation

If you use this codebase, framework, or dataset in your research, please cite our paper:

### APA Format
> Caviglione, L., Guarascio, M., Liguori, A., Scala, F., & Valente, B. (2026)
> *A Semi-Supervised Few-Shot Framework for Detecting Stealth Malicious Network Traffic*.
> Machine Learning Journal. Springer. 10.1007/s10994-026-07190-z

### BibTeX

```bibtex
@article{10.1007/s10994-026-07190-z,
  title   = {A Semi-Supervised Few-Shot Framework for Detecting
             Stealth Malicious Network Traffic},
  author  = {Caviglione, Luca and Guarascio, Massimo and
             Liguori, Angelica and Scala, Francesco and
             Valente, Bernardo},
  journal    = {Machine Learning},
  year = {2026},
  doi = {10.1007/s10994-026-07190-z}
}
```

---

## License

This project and associated materials are licensed under the **Creative Commons CC0 1.0 Universal** (CC0 1.0) Public Domain Dedication. See the [LICENSE](LICENSE) file for full details.

---

## Contact & Acknowledgements

For questions, collaborations, or issues regarding the framework, please contact:

- **Massimo Guarascio** &bull; `massimo.guarascio@icar.cnr.it`
- **CNR-ICAR** &bull; [www.icar.cnr.it](https://www.icar.cnr.it/)

### Funding

The work was partially supported by:

- **PERUN (101225653)** — Protecting Sensitive Cyber Ecosystems from Upcoming Next Generation and AI-generated Malware Threats, funded by the European Union under the Horizon Europe Programme.
- **FAIR (PE00000013)** — Future Artificial Intelligence Research, funded by the European Union under NextGeneration EU.
- **SERICS (PE00000014)** — Security and Rights in the Cyberspace, funded by the European Union under NextGeneration EU.
