args <- commandArgs(trailingOnly = TRUE)
rds_file <- args[1]
csv_file <- args[2]

# read the RDS file
data <- readRDS(rds_file)

# write the CSV file
write.csv(data, csv_file, row.names = TRUE)
