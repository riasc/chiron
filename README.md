[![Downloads](https://img.shields.io/github/downloads/riasc/chiron/total.svg)](https://img.shields.io/github/downloads/riasc/chiron/total.svg)

# chiron
Predict hypercholesterolemia from the Personalized Environment and Genes Study

## DREAM Challenge

This has been part of the [PEGS DREAM Challenge](https://www.synapse.org/Synapse:syn52817032/wiki/624336).

### Team - The312

Official Synapse Team Project Page: [The312](https://www.synapse.org/Synapse:syn61682977/wiki/629098)

- [Richard A. Schäfer](https://www.synapse.org/Profile:3348050)
- [Fikrat Talibli](https://www.synapse.org/Profile:3509170)

### Usage

usage: main.py [-h] -i INPUT [-s] -o OUTPUT

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Survey files
  -s, --synthetic       Use of synthetic data
  -o OUTPUT, --output OUTPUT
                        Output file

In the challenge the data was mounted on `/input` and the output was supposed to be written to `/output` in an output file called `predictions.csv` with the following format:

| Column Name | Column type | Description |
| ----------- | ----------- | ----------- |
| `epr_number` | str | EPR number | Sample/Participant IDs must be unique and match with those in the input files; there must be one prediction per sample ID or participant ID for PEGS participants. |
| `disease_probability` | float | All probabilities must be a number between 0 (indicating no likelihood of the disease) and 1 (indicating 100% likelihood of having the disease); null/NaN values are not accepted |

For that reason, we used the following ENTRYPONT in the [Dockerfile](Dockerfile):

```
ENTRYPOINT [ "python3", "/chiron/main.py", "--input", "/input", "--output", "/output" ]
```

## Data

We used the `train_data[_synthetic]` and `test_data[_synthetic]` provided by the challenge for
training and validation, respectively.

## Features

We extracted the following features from the data

### Surveys

We only used the `health and exposure` data for the training. The main reason for that is that `exposomeA`
and `exposomeB` only contain about a third of the samples. At first, we looked at the number of missing (`.M`)
or skipped (`.S`) values. Consequently, we excluded that have more than 20% missing values and features that
are not relevant for high cholesterol.

### Genomic Data

#### SNVs (small indels)

We matched the provided SNVs (e.g., PEGS_genomic_data/SNVs_small_indels/) against the PGS catalog for
hypercholesterolemia ([ref/PGS.txt](https://github.com/riasc/chiron/blob/main/ref/PGS.txt)) and calculated
the PGS for each sample. For that, we used the following formula:

$$PGS = \sum_{i=1}^{n} w_i \cdot g_i$$

where $w_i$ is the weight for the $i$-th SNP and $g_i =\{0,1,2\}$ is
the genotype for the $i$-th SNP. The genotype corresponds to the number of reference alleles, 0 (AA),
1 (AB), and 2 (BB).

#### Telomere Content

We directly used the provided aggregated telomeric content estimates provided in the data
(e.g., telomere_content/PEGS_telomere_content_estimates_train_synthetic.xlsx)

#### Ancestry

We used the provided ancestry data and used the columns for AMR (Americas -- refers to
indigeneous ancestry), AFR (African), EAS (East Asian), EUR (European), and SAS (South Asian).

#### HLA Typing

We used the provided HLA typing data and encoded the genes into pair of features consisting of
the combined alleles and the genotype as follows:

Let $A_1$ and $A_2$ be the two alleles for a gene $i$, we define a function $f$ that maps each
allele $a \in \mathcal{A}$ to a unique integer $f(a)$ such that:

$$A_{1i-num} = f(A_{1i})$$

and

$$A_{2i-num} = f(A_{2i})$$

We then create the combined feature value $C_i$ as:

$$C_i = A_{1i-num} \cdot 100 + A_{2i-num}$$

And the genotype feature value $H_i$ as:

$$H_i = \begin{cases} 0 & \text{if } A_{1i} = A_{2i} \\ 1 & \text{if } A_{1i} \neq A_{2i} \end{cases}$$

#### Methylation

We used the
[Infinium MethylationEPIC v1.0 Product Files](https://support.illumina.com/downloads/infinium-methylationepic-v1-0-product-files.html)
and identified the CpG sites associated with genes that are relevant for hypercholesterolemia. These include:

- LDLR (Low-Density Lipoprotein Receptor): Mutations in the LDLR gene are the most common cause of familial
hypercholesterolemia. The LDLR gene encodes the LDL receptor, which is responsible for removing low-density
lipoprotein (LDL) cholesterol from the bloodstream.
- APOB (Apolipoprotein B): This gene encodes apolipoprotein B, a primary protein component of LDL particles.
Mutations in the APOB gene can lead to defective binding of LDL particles to their receptors, resulting in
increased blood levels of LDL cholesterol.
- PCSK9 (Proprotein Convertase Subtilisin/Kexin Type 9): The PCSK9 gene encodes a protein that regulates the
number of LDL receptors on the surface of liver cells. Gain-of-function mutations in PCSK9 lead to fewer LDL
receptors and higher cholesterol levels.
- LDLRAP1 (Low-Density Lipoprotein Receptor Adaptor Protein 1): Mutations in this gene can cause autosomal
recessive hypercholesterolemia, a condition similar to familial hypercholesterolemia but inherited differently.
- CETP (Cholesteryl Ester Transfer Protein): Variants in the CETP gene can influence HDL cholesterol levels,
indirectly affecting LDL levels and overall cholesterol metabolism.
- LIPA (Lysosomal Acid Lipase A): Mutations in LIPA can lead to cholesterol ester storage disease and contribute
to elevated cholesterol levels.
- ABCG5 and ABCG8 (ATP-Binding Cassette Subfamily G Members 5 and 8): These genes are involved in the regulation
of cholesterol absorption and excretion. Mutations can lead to conditions like sitosterolemia, which can influence
cholesterol levels.
- APOE (Apolipoprotein E): Variants in the APOE gene can affect cholesterol metabolism, particularly the clearance
of triglyceride-rich lipoproteins. Certain alleles, like APOE4, are associated with higher cholesterol levels and
an increased risk of cardiovascular disease.

The resulting CpG island are stored in [ref/CpG.txt](https://github.com/riasc/chiron/ref/CpG.txt)

#### Structural Variants

We used the provided structural variant data and calculated the number of deletions, duplications, and inversions
that occur within the genes associated with hypercholesterolemia. The genes are the same as for the methylation data.

# Output
