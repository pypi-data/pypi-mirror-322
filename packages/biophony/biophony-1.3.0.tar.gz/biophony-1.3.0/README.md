# Genetic data files generator for testing purposes

`biophony` is a package for generating random genetic data files intended specifically for testing and validation.
Real genetic data is often too large, lacks flexibility, or raises privacy concerns, making it
unsuitable for thorough testing.
`biophony` makes it simpler to test software in different scenarios without needing real data,
enabling focused and efficient development and validation.

## Installation

`biophony` requires at least Python 3.11 to work.

To install with `pip`, run:

```bash
pip install biophony
```

## Usage

### Command Line Interfaces

`biophony` provides the following CLIs to generate data:

- `gen-cov`: generates a BED file with custom depth,
- `gen-fasta`: generates a FASTA file with a custom size sequence,
- `gen-fastavar`: generates a FASTA file with custom size sequences,
  each with `n` variants with control over insertion, deletion and mutation rate,
- `gen-fastq`: generates a FASTQ file with custom read count and size,
- `gen-vcf`: generates a VCF file from a FASTA file, with control over insertion, deletion and mutation rate.

CLIs that read and / or write data do it on `stdin` and `stdout` by default,
thus permitting to chain operations with the pipe operator `|`.

For exemple, run the following command to generate a VCF with 2% SNP, 1% INS and 1% DEL:

```bash
gen-fasta | gen-vcf --snp-rate 0.02 --ins-rate 0.01 --del-rate 0.01
```

To save the generated content, you can either use the regular output operator `>` to redirect `stdout` to a file or
use the dedicated option:

```bash
gen-fasta | gen-vcf --snp-rate 0.02 --ins-rate 0.01 --del-rate 0.01 > test.vcf  # redirect
gen-fasta | gen-vcf --snp-rate 0.02 --ins-rate 0.01 --del-rate 0.01 -o test.vcf  # dedicated option
```

### Python API

You can also use the Python API to generate random genetic data files in your scripts.

Link to the Python API documentation: https://cnrgh.gitlab.io/databases/biophony/.
