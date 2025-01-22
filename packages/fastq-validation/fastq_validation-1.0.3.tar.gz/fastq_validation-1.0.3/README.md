# fastq_validation
Ensure input files are vaild and fit the expected profile of the instrument platform.
Aimed at pathogen sequence data due to expected file sizes

Should use near constant RAM usage due to not storing more than 10MB of a given file at any given time

## Checks

### All platforms
If any of the following checks fail, an error is thrown:
* Ensures files are valid fastq
* Ensures valid gzip format (if gzipped)
* Restricts maximum (decompressed) file size to 100GB to guard against zip bombs
* Restricts maximum line length to 10MB to guard against zip bombs


### Illumina
* Matches lines in files to ensure only matched reads exist
* Checks that read length is >30% the same (some variation exists in routine samples) and < 350 bases

### ONT
* Checks that mean read length >= 350 bases
* Checks that reads have sufficient variation in length to be ONT sequenced