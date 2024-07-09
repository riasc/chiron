# chiron
Predict hypercholesterolemia

# Output

| Column Name | Column type | Description |
| ----------- | ----------- | ----------- |
| `epr_number` | str | EPR number | Sample/Participant IDs must be unique and match with those in the input files; there must be one prediction per sample ID or participant ID for PEGS participants. |
| `disease_probability` | float | All probabilities must be a number between 0 (indicating no likelihood of the disease) and 1 (indicating 100% likelihood of having the disease); null/NaN values are not accepted |
