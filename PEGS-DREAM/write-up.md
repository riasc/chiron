# chiron: Prediction of hypercholesterolemia from PEGS data (PEGS DREAM Challenge 2024)

Richard A. Schäfer (1) & Fikrat Talibli (2)

(1) Department of Urology, Northwestern University Feinberg School of Medicine, Chicago, IL 60611, United States
(2) Institute of Biomedical Genetics, University of Stuttgart, Stuttgart, BW 70569, Germany

## Summary

In this work, we present **chiron**, as part of our submission to the PEGS DREAM Challenge 2024 [1] for predicting hypercholesterolemia from PEGS data. We provide the source code and detailed documentation at https://github.com/riasc/chiron. It is distributed under MIT license. 

## Introduction

Hypercholesterolemia is characterized by elevated levels of low-density lipoprotein cholesterol (LDL-C). Cholesterol is an essential component of the cell membrane. However, excessive amounts can lead to the formation of plaques in the arteries, obstructing blood flow and leading to premature atherosclerotic cardiovascular diseases (ASCVD) [2][3]. Most commonly, high cholesterol is caused by hereditary factors, but also lifestyle choices such as poor diet, lack of physical activity, and smoking can contribute to it. In addition, health conditions such as chronic kidney disease and diabetes are responsible for the increase in cholesterol [4][5]. It is, therefore, of interest to estimate the individual risk of developing hypercholesterolemia. Studies that aim to predict hypercholesterolemia utilize various data, including socioeconomic features and clinical risk factors, but generally neglect genetic factors [6]. As different machine learning models (e.g., random forest, deep learning, gradient boosting) achieve a similar prediction accuracy, the data availability and feature extraction become crucial factors that can influence the effectiveness of the prediction [7]. However, when integrating multi-dimensional data, no single prediction algorithm performs optimally for all the utilized data [8]. The Personalized Genes and Environment Study (PEGS) is a comprehensive cohort of health and exposure data (https://www.niehs.nih.gov/research/clinical/studies/pegs/index.cfm). In the PEGS data freeze v3.1, various data are integrated, providing a unique resource of multi-dimensional data. In this work, we focus on the use of gradient boosting for the prediction of hypercholesterolemia with high-dimensional data. We make use of XGBoost [9] as it can handle missing data, which is prevalent in PEGS, depending on the data type. In addition, XGBoost does not require data scaling or normalization and has been 
shown to outperform other methods for the classification of tabular datasets [10]. We present Chiron, a comprehensive workflow that integrates multi-dimensional data to predict hypercholesterolemia. 

## Methods

We utilized the XGBoost library and tuned the hyperparameters using Bayesian optimization. Concretely, we optimized the following parameters with the range in brackets: `learning rate: (0.1 to 0.5)`, `max depth (1 to 10)`, `n estimator (100 to 500)`, `subsample (0.6 to 1.0)`, `colsample_bytree (0.6 to 1.0)`, `gamma (0.0 to 0.5)`, `min_child_weight (1.0 to 10)`, `reg alpha (0.0 to 1.0)`, `reg lambda (1 to 3)`. Here, we used 150 iterations to determine hyperparameters. In the challenge submission, we learned the model on the training data and subsequently applied it to the validation dataset to assign the disease probabilities for each sample. We used SHAP [11] to identify features that are most significant to the predicted model. We split the data into training and test subsets and used this to examine the features. The features were sorted in descending order based on the absolute number of the SHAP values. 


### Feature Extraction

Following the SHAP analysis we removed some of the features that showed no impact on the output model or seemed irrelevant for the prediction of hypercholestermia. For example, there is limited evidence of health benefits related to the use supplements [12]. The final feature vector includes 137 features of the following:

#### Surveys

In the `Health and Exposure` survey we used the following fields: `BMI`, `physical health`, `hypertension`, `atherosclerosis`, `cardiac arrhythmia`, `heart attack`, `coronary artery`, `congestive heart failure`, `poor blood flow`, `raynauds`, `blood clots`, `angioplasty`, `mini stroke`, `stroke`, `diabetes`, `thyroid disease`, `tuberculosis`, `cough breathlessness`, `asthma`, `ulcerative colitis`, `polyps`, `gallbladder disease`, `stomach ulcer`, `fatty liver`, `chronic kidney disease`, `kidney infection`, `allergic reactions`, `fibromyalgia`, `lupus`, `iron_anemia`, `bone_loss`, `osteoporosis`, `gout`, `rheumatoid arthritis`, `osteoarthritis`, `psoriasis`, `eczema`, `urticaria`, `chronic fatigue`, `cancer`, `asbestos`, `biohazards`, `chemicals`, `coal dust`, `coal tar`, `dyes`,  `formaldehyde`, `heavy metals`, `pesticide`, `smoke indoors`, `alcohol life`.

In addition, we include the family histories for `cancer`, `diabetes`, `high blood pressure`, `stroke`, `heart attack`, `coronary artery`, `sickle cell`, `rheumatoid arthritis`, `alzheimers`, `asthma`, `hayfever`, `emphysema`, and `parkinson`. This was determined by inspecting the fields for `mother`, `father`, `sister`, and `brother` of the corresponding disease. In the family history of cancer, all cancer types were combined. 

In the `Exposome A` survey we used the following fields: `fireplace`, `air condition`, `mold in residence`, `pet in residence`, residence distances to `hazardous waste sites`, `landfill or garbage dump`, `coal plant`, `factory`, and exposures to `arsen`, `cadmium`, `lead`, and `mercury`.

In the `Exposome B` survey we used the fields for the intake of `black cohosh`, `coenzyme Q10`, `fish oil`, `flaxseed oil` and the `sleeping hours on weekdays`. In addition, the fields for consumption of `fast food`, `takeout`, `whole milk`, `non-dairy milk`, `cream`, `butter`, `cheese`, `avocado`, `blueberries`, `beans`, `broccoli`, `spinach`, `eggs`, `bacon`, `deli meat`, `other processed meat`, `hamburger`, `ham`, `canned tuna`, `oatmeal`, `whole wheat`, `fries`, `pizza`, `other nuts`. In addition, we used the fields for `sleep hours on weekdays`.

### Genomic Data

#### SNVs (small indels)

We matched the provided SNVs (e.g., PEGS_genomic_data/SNVs_small_indels/) against the PGS catalog for hypercholesterolemia ([ref/PGS.txt](https://github.com/riasc/chiron/blob/main/ref/PGS.txt)) and calculated the PGS for each sample. For that, we used the following formula:

$$PGS = \sum_{i=1}^{n} w_i \cdot g_i$$

where $w_i$ is the weight for the $i$-th SNP and $g_i =\{0,1,2\}$ is the genotype for the $i$-th SNP. The genotype corresponds to the number of reference alleles, 0 (AA), 1 (AB), and 2 (BB).

#### Telomere Content

We directly used the provided aggregated telomeric content estimates provided in the data (e.g., telomere_content/PEGS_telomere_content_estimates_train_synthetic.xlsx)

#### Ancestry

We used the provided ancestry data and used the columns for AMR (Americas -- refers to indigeneous ancestry), AFR (African), EAS (East Asian), EUR (European), and SAS (South Asian).

#### HLA Typing

We used the provided HLA typing data and encoded the genes into pair of features consisting of the combined alleles and the genotype as follows:

Let $A_1$ and $A_2$ be the two alleles for a gene $i$, we define a function $f$ that maps each allele $a \in \mathcal{A}$ to a unique integer $f(a)$ such that $A_{1i-num} = f(A_{1i})$ and $A_{2i-num} = f(A_{2i})$

We then create the combined feature value $C_i$ as:

$$C_i = A_{1i-num} \cdot 100 + A_{2i-num}$$

And the genotype feature value $H_i$ as:

$$H_i = \begin{cases} 0 & \text{if } A_{1i} = A_{2i} \\ 1 & \text{if } A_{1i} \neq A_{2i} \end{cases}$$

#### Methylation

We used the [Infinium MethylationEPIC v1.0 Product Files](https://support.illumina.com/downloads/infinium-methylationepic-v1-0-product-files.html) and identified the CpG sites associated with genes that are relevant for hypercholesterolemia. These include: **LDLR** (Low-Density Lipoprotein Receptor): Mutations in the LDLR gene are the most common cause of familial hypercholesterolemia. The LDLR gene encodes the LDL receptor, which is responsible for removing low-density lipoprotein (LDL) cholesterol from the bloodstream; **APOB** (Apolipoprotein B): This gene encodes apolipoprotein B, a primary protein component of LDL particles. Mutations in the APOB gene can lead to defective binding of LDL particles to their receptors, resulting in increased blood levels of LDL cholesterol; **PCSK9** (Proprotein Convertase Subtilisin/Kexin Type 9): The PCSK9 gene encodes a protein that regulates the number of LDL receptors on the surface of liver cells. Gain-of-function mutations in PCSK9 lead to fewer LDL receptors and higher cholesterol levels; **LDLRAP1** (Low-Density Lipoprotein Receptor Adaptor Protein 1): Mutations in this gene can cause autosomal recessive hypercholesterolemia, a condition similar to familial hypercholesterolemia but inherited differently; **CETP** (Cholesteryl Ester Transfer Protein): Variants in the CETP gene can influence HDL cholesterol levels, indirectly affecting LDL levels and overall cholesterol metabolism; **LIPA** (Lysosomal Acid Lipase A): Mutations in LIPA can lead to cholesterol ester storage disease and contribute to elevated cholesterol levels; **ABCG5** and **ABCG8** (ATP-Binding Cassette Subfamily G Members 5 and 8): These genes are involved in the regulation of cholesterol absorption and excretion. Mutations can lead to conditions like sitosterolemia, which can influence cholesterol levels. **APOE** (Apolipoprotein E): Variants in the APOE gene can affect cholesterol metabolism, particularly the clearance of triglyceride-rich lipoproteins. Certain alleles, like APOE4, are associated with higher cholesterol levels and an increased risk of cardiovascular disease. The resulting filtered CpG island are stored in [ref/CpG.txt](https://github.com/riasc/chiron/ref/CpG.txt)

### Structural Variants

We used the provided structural variant data and calculated the average length of deletions, duplications and inversions for each patient.

## Results

We sorted the features according to the absolute number of the SHAP values indicating the impact of the models output. The top 20 features are illustrated in Figure 1. 

![Alt text](https://github.com/riasc/chiron/blob/main/PEGS-DREAM/figure1.svg)


## Discussion

The provided data of the PEGS DREAM challenge was created using the synthpop v1.8 library in R [13]. For that reason, the features that were identified as significant should be interpreted with caution, as synthetic data may not perfectly capture the complexity of the actual data. Although synthpop aims to generate data that closely resembles the original, there can still be limitations in how well the synthetic data replicates underlying patterns and relationships. In fact, during the `Leaderboard Round 1`, we found that the AUROC differs by 3-5% between training and validation data. We were required to train and validate the model during the submission, which was limited to three hours. This limited the hyperparameter tuning to 150 iterations that could not achieve convergence. Consequently, this results in different classification accuracies (AUROC) for the same submission. Training the model with increase parameters on the full dataset, subsequent to the DREAM challenge should improve the model significantly. Nevertheless, the proposed model improves the prediction of current available methods. 


## References

[1] PEGS DREAM Challenge 2024 ([syn52817032](https://www.synapse.org/Synapse:syn52817032/))

[2] Ibrahim MA, Asuka E, Jialal I. Hypercholesterolemia. 2023 Apr 23. In: StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing; 2024 Jan–. PMID: 29083750.

[3] Simonen, P.,  Öörni, K., Sinisalo, J., Strandberg, T.E., Wester, I., Gylling, H. (2023) High cholesterol absorption: A risk factor of atherosclerotic cardiovascular diseases? Atherosclerosis, 376, 53-62.

[4] Kanter M.M., Kris-Etherton P.M., Fernandez M.L., Vickers K.C., Katz D.L. (2012) Exploring the factors that affect blood cholesterol and heart disease risk: Is dietary cholesterol as bad for you as history leads us to believe? Advances in Nutrition, 3, 711–717. 

[5] Hu P., Dharmayat K.I., Stevens C.A., Sharabiani M.T., Jones R.S., Watts G.F., Genest J., Ray K.K., Vallejo-Vaz A.J. (2020) Prevalence of familial hypercholesterolemia among the general population and patients with atherosclerotic cardiovascular disease: A systematic review and meta-analysis. Circulation, 141, 1742–1759.

[6] Dritsas E., Trigka M. (2022) Machine Learning Methods for Hypercholesterolemia Long-Term Risk Prediction. Sensors (Basel), 22(14), 5365. 

[7] Akyea, R. K., Qureshi, N., Kai, J., & Weng, S. F. (2020). Performance and clinical utility of supervised machine-learning approaches in detecting familial hypercholesterolaemia in primary care. NPJ digital medicine, 3(1), 142.

[8] Hand, D. J. (2008). Breast cancer diagnosis from proteomic mass spectrometry data: A comparative evaluation. Statistical applications in genetics and molecular biology, 7(2).

[9] Chen, T., & Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System. ArXiv. https://doi.org/10.1145/2939672.2939785

[10] Santhanam, Ramraj & Uzir, Nishant & Raman, Sunil & Banerjee, Shatadeep. (2017). Experimenting XGBoost Algorithm for Prediction and Classification of Different Datasets. 

[11] Lundberg, S.M and Lee, S. (2017). A Unified Approach to Interpreting Model Predictions. Advances in Neural Information Processing Systems 2017, 30. 

[12] Ronis, M.J.J., Pedersen, K.B., & Watt, J. (2018). Adverse Effects of Nutraceuticals and Dietary Supplements. Annual Review of Pharmacology and Toxicology, 58, 583-601

[13] Nowok, B., Raab, G.M., & Dibben, C. (2016). synthpop: Bespoke Creation of Synthetic Data in R. Journal of Statistical Software, 74(11), 1–26. https://doi.org/10.18637/jss.v074.i11


##Authors Statement
R.A.S. and F.T. designed and implemented the software. R.A.S. refined the feature extraction, and F.T. performed the hyperparameter optimization. R.A.S. and F.T wrote the write-up. 