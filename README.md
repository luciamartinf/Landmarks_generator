# Title

### Lucía Martín Fernández
#

Short Description


## Basic usage:

```
./emapper_profiler.py --input_dir data
```
`data` is a directory 
`file` is a file

### Execution modes 

* Execution of , for ; 

```
code
```

* Execution of, for , and  settings .

```
code
```

* Execution of  .

```
code
```

## Parameters main.py 

## General Options

* `--version`

     show version and exit.
  
* `--verbose`

     show version and exit.
  
* `--help` `-h`

     show version and exit.

## Input options 

* `--inputdir DIR`,`-i DIR`

     Input directory containing CoverM and eggNOG-mapper results. Required.

* `--coverm_suffix SUFFIX`, `-c SUFFIX`

     The suffix of your CoverM files. By default, _coverage_values

* `--sample_file FILE`,`-s FILE`

     Text file with a list of the samples that need to be processed. If not provided, the sample list will be generated given the input file. 

* `--kegg_dict DIR`, `-k DIR`

     Directory containing KEGG_pathway and KEGG_kos json dictionaries. This files are provided in this repository together with the source code.
  
## Output Options

* `--outputdir DIR`,`-o DIR`

     Output directory to store the generated tsv files. By default, output directory is called results.

* `--unit [tpm, rpkm, tm]`, `-u [tpm, rpkm, tm]`
  
     Specify the output relative abundance normalization units. Options are `rpkm`, Reads per kilobase per million transcripts (RPKM), `tpm`, Transcripts per million (TPM),  and `tm`, trimmed mean. Default is `rpkm`)

* `--filter_euk`, `-e`

     Remove eukaryotes

* `--filter_virus`, `-v`

     Remove viruses

## Options for Novel gene families mode

* `--novel_fam`, `-f`

     Include functional profiling for novel gene families

* `--nf_dir DIR`

     Input directory that contains the novel families annotations. By default considers a directory called novel_families inside the input directory


## Output files

| **Files**                           | **Description**                                                                                                 |                                                   
|:----------------------------------------|:----------------------------------------------------------------------------------------------------------------|
|`ko_relabundance.tsv`                                |  Relative abundance per sample of KEGG orthologs acompanied by its description and symbol. Unmapped proportion of functions is included                      |                  
|`og_relabundance.tsv`                                  | Relative abundance per sample of orthologous groups from the eggNOG database annotated at the kingdom taxonomic level acompanied by its description. Unmapped proportion of functions is included          |                                                               
|`ko_totalabundance.tsv`                                | Abundance per sample of KEGG orthologs acompanied by its description and symbol                      |                  
|`og_totalabundance.tsv`                                  | Abundance per sample of orthologous groups from the eggNOG database annotated at the kingdom taxonomic level acompanied by its description          |  
|`pathway_coverage.tsv`                                  |  KEGG pathway's completness percentage per sample according to the annotated KEGG ortholog. Pathway's description is included.                      |     
|                |         **if `--novel_fam` flag is on**                                                                                                 |      
|`nf_relabundance.tsv`                                  |  Relative abundance per sample of novel gene families. Unmapped proportion of functions is included          |                                                       
|`nf_totalabundance.tsv`                                  | Abundance per sample of novel gene families          |                                                               

## Usage Example

The [data_resume](data_resume) folder contains an example files required for *emapper-profiler* execution. The [results_resume](results_resume) folder contains the outputs generated when executing *emapper-profiler* with the following command line:

```
./emapper_profiler.py --inputdir data_resume --outputdir results_tpm --filer_euk --unit tpm --filter_virus --novel_fam

```

Complete results generated for all dataset are included in the [results](results) folder. 

## Software requirements

* Python 3.7 (or greater)
