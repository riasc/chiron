# chiron
Predict hypercholesterolemia

# Usage

In the challenge data is mounted on /input

```
SYNAPSE_METADATA_MANIFEST.tsv
train_data
val_data
```


# Training Data

We looked at the 'train_data_synthetic/ and inspected the data

## Survey

We inspected the `health and exposure` data and for a number of preselected columns, we looked at the number of missing (`.M`) or skipped (`.S`) values.

| column name | number of missing/skipped values |
| ------------| ---------------------------------|
| epr_number | 0 |
| he_age_derived | 0 |
| he_bmi_cat_derived | 37 |
| he_a005_physical_health | 15 |
| he_b007_hypertension_PARQ | 14 |
| he_b008_high_cholesterol | 33 |
| he_b009_atherosclerosis | 44 |
| he_b010_cardiac_arrhythmia | 54 |
| he_b012_heart_attack | 52 |
| he_b013_coronary_artery | 58 |
| he_b014_congestive_heart_failure | 56 |
| he_b015_poor_blood_flow | 64 |
| he_b016_raynauds | 55 |
| he_b017_blood_clots | 62 |
| he_b018_angioplasty | 55 |
| he_b019_stroke_mini | 23 |
| he_b020_stroke_PARQ | 113 |
| he_c022_diabetes_PARQ | 196 |
| he_c023_thyroid_disease_PARQ | 68 |
| he_d027_tb_PARQ | 50 |
| he_d028_cough_breathlessness | 32 |
| he_d030_asthma_PARQ | 92 |
| he_e031_epilepsy | 42 |
| he_e032_migraine | 47 |
| he_e033_parkinsons | 46 |
| he_e034_ptsd | 36 |
| he_e035_alzheimers | 33 |
| he_e036_ms | 37 |
| he_f037_celiac | 47 |
| he_f038_lactose_intolerance | 47 |
| he_f039_crohns | 60 |
| he_f040_ulcerative_colitis | 53 |
| he_f041_polyps | 33 |
| he_f042_gallbladder_disease | 58 |
| he_f043_stomach_ulcer | 30 |
| he_f044_cirrhosis | 54 |
| he_f045_fatty_liver | 45 |
| he_f046_hepatitis_PARQ | 55 |
| he_f046a_hep_a_CHILDQ | 2989 |
| he_f046b_hep_b_CHILDQ | 2977 |
| he_f046c_hep_c_CHILDQ | 2987 |
| he_g047_ckd | 49 |
| he_g048_esrd | 43 |
| he_g049_kidney_stones | 40 |
| he_g050_kidney_infection | 35 |
| he_g051_pkd | 35 |
| he_h052_allergic_reactions | 33 |
| he_h053_scleroderma | 32 |
| he_h054_shingles | 31 |
| he_h055_fibromyalgia | 54 |
| he_h056_lupus | 32 |
| he_h057_sjogrens | 10 |
| he_i058_hemochromatosis | 27 |
| he_i059_iron_anemia | 35 |
| he_i060_pernicious_anemia | 40 |
| he_i061_sickle_cell | 36 |
| he_j062_bone_loss | 49 |
| he_j063_osteoporosis | 35 |
| he_j064_gout | 44 |
| he_j065_myositis | 46 |
| he_j066_rheu_arthritis_PARQ | 213 |
| he_j067_osteoarthritis_PARQ | 200 |
| he_k069_psoriasis | 60 |
| he_k070_eczema | 33 |
| he_k071_urticaria | 49 |
| he_k072_sunburn | 32 |
| he_k073_scars | 76 |
| he_l080_chronic_fatigue | 15 |
| he_o103_cancer_PARQ | 41 |
| he_q140_asbestos_PARQ | 0 |
| he_q141_biohazards_PARQ | 0 |
| he_q142_chemicals_PARQ | 0 |
| he_q143_coal_dust_PARQ | 0 |
| he_q144_coal_tar_PARQ | 0 |
| he_q145_diesel_PARQ | 0 |
| he_q146_dyes_PARQ | 0 |
| he_q147_formaldehyde_PARQ | 0 |
| he_q148_gasoline_PARQ | 0 |
| he_q149_heavy_metals_PARQ | 0 |
| he_q150_pesticide_PARQ | 0 |
| he_q151_sand_PARQ | 0 |
| he_q152_other_dust_PARQ | 0 |
| he_q153_textiles_PARQ | 0 |
| he_q154_wood_dust_PARQ | 0 |
| he_q155_xrays_PARQ | 0 |
| he_r166a_diabetes_mom | 0 |
| he_r166b_diabetes_dad | 0 |
| he_r167a_hbp_mom | 0 |
| he_r167b_hbp_dad | 0 |
| he_r168a_stroke_mom | 0 |
| he_r168b_stroke_dad | 0 |
| he_r169a_heart_attack_mom | 0 |
| he_r169b_heart_attack_dad | 0 |
| he_r170a_coronary_artery_mom | 0 |
| he_r170b_coronary_artery_dad | 0 |
| he_r171a_sickle_cell_mom | 0 |
| he_r171b_sickle_cell_dad | 0 |
| he_r172a_rheu_arthritis_mom | 0 |
| he_r172b_rheu_arthritis_dad | 0 |
| he_r173a_alzheimers_mom | 0 |
| he_r173b_alzheimers_dad | 0 |
| he_r174a_asthma_mom | 0 |
| he_r174b_asthma_dad | 0 |
| he_r175a_autism_mom | 0 |
| he_r175b_autism_dad | 0 |
| he_r176a_hayfever_mom | 0 |
| he_r176b_hayfever_dad | 0 |
| he_r177a_emphysema_mom | 0 |
| he_r177b_emphysema_dad | 0 |
| he_r178a_parkinsons_mom | 0 |
| he_r178b_parkinsons_dad | 0 |
| he_s180_smoke_PARQ_CHILDQ | 1769 |
| he_s185_smoke_indoors | 116 |
| he_s187_alcohol_life_PARQ | 31 |
| he_s192_sleep_hours | 84 |

Although this dataset is only synthetic data, we excluded columns with more than 20% of missing data (N=3062)  `he_f046a_hep_a_CHILDQ`, `he_f046b_hep_b_CHILDQ`, `he_f046c_hep_c_CHILDQ`, `he_s180_smoke_PARQ_CHILDQ`.


# Output

| Column Name | Column type | Description |
| ----------- | ----------- | ----------- |
| `epr_number` | str | EPR number | Sample/Participant IDs must be unique and match with those in the input files; there must be one prediction per sample ID or participant ID for PEGS participants. |
| `disease_probability` | float | All probabilities must be a number between 0 (indicating no likelihood of the disease) and 1 (indicating 100% likelihood of having the disease); null/NaN values are not accepted |
