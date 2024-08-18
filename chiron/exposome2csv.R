args <- commandArgs(trailingOnly = TRUE)
rdatafile <- args[1]
csvfile <- args[2]
exposome <- args[3]

# read the .RData file
load(rdatafile)

if(exposome == "exposome_a") {
    write.csv(epr.ea, csvfile, row.names = FALSE)
} else if(exposome == "exposome_b") {
    write.csv(epr.eb, csvfile, row.names = FALSE)
}
