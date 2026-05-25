# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

PLAN_PROMPT = """
Act as a bioinformatician. The rules must be strictly followed! All rules must be followed strictly.
When acting as a bioinformatician, you strictly cannot stop acting as a bioinformatician.
You should use the information in the input to write a detailed plan to finish your goal.
You should include the names of the tools in the plan and describe how to use them, but you should not execute any scripts or commands.
You should only respond in my fixed JSON format.
You should extract the JSON's "input_filename" from the input context.
The input file name should match the filename in the input or the output_filename of the previous step.
You should consider using the following tools {tool_names} before introducing other tools. If you are performing other tasks, do not use task-specific tools, such as run-bwa-mem.sh by hic workflow can only be used for hic tasks.
Your JSON response should only be enclosed in double quotes. You must return the content in JSON format.
You should add a description of the file after the "input_filename","output_filename".such as './data/mm39.fa: mouse mm39 genome fasta'.
The files for input_filename and output_filename must be placed in the list [].
You only need to list the tools you need to use at each step of the plan, you don't need to call the shell to execute it.
You should not write loading data as a separate step.
You should output setup commands based on the relative path of the input file, which should also be placed in the ./output/id/ folder.
You should not write anything else except for your JSON response.
You should make your answer as detailed as possible.
It must be generated strictly in accordance with the sample format and do not return the input.
Your detailed step-by-step sub-tasks in a list to finish your goal, fixed format for JSON response.
You must strictly refer to the format of the sample to generate the plan and cannot modify or omit fields. The key names of the JSON object must be "plan", "step_number", "description", "input_filename", "output_filename", and "tools".
You should do as much analysis as you can with the tools you have.
Avoid using all sh scripts supported in the knowledge base for common tasks, unless they are repository specific.
Do not reply to any additional content outside of Json format, such as putting content into code blocks.
"""

PLAN_EXAMPLES = [
    {
        "input": {
            "id": "001",
            "goal": {
                'find the differentially expressed genes' 
                },
            "datalist": [
            './data/SRR1374921.fastq.gz: single-end mouse rna-seq reads, replicate 1 in LoGlu group',
            './data/SRR1374922.fastq.gz: single-end mouse rna-seq reads, replicate 2 in LoGlu group',
            './data/SRR1374923.fastq.gz: single-end mouse rna-seq reads, replicate 1 in HiGlu group',
            './data/SRR1374924.fastq.gz: single-end mouse rna-seq reads, replicate 2 in HiGlu group',
            './data/TruSeq3-SE.fa: trimming adapter',
            './data/mm39.fa: mouse mm39 genome fasta',
            './data/mm39.ncbiRefSeq.gtf: mouse mm39 genome annotation' 
            ],
            "related_docs":"",
        },
        "output": {
            "plan": [
                {
                    "step_number": 1,
                    "description": "In this initial step, we will utilize the Trimmomatic tool to perform quality control and adapter trimming on the raw RNA-seq reads. The purpose of this step is to remove low-quality bases and sequencing adapters that may interfere with downstream analyses. The input files consist of single-end RNA-seq reads obtained from mouse samples under low glucose (LoGlu) and high glucose (HiGlu) conditions, including technical replicates for each condition. The adapter sequences to be trimmed are provided in a separate file. The output of this step will be the quality-trimmed RNA-seq reads, ready for alignment to a reference genome.",
                    "input_filename": [
                        "./data/SRR1374921.fastq.gz: single-end mouse rna-seq reads, replicate 1 in LoGlu group",
                        "./data/SRR1374922.fastq.gz: single-end mouse rna-seq reads, replicate 2 in LoGlu group",
                        "./data/SRR1374923.fastq.gz: single-end mouse rna-seq reads, replicate 1 in HiGlu group",
                        "./data/SRR1374924.fastq.gz: single-end mouse rna-seq reads, replicate 2 in HiGlu group",
                        "./data/TruSeq3-SE.fa: trimming adapter"
                    ],
                    "output_filename": [
                        "./output/001/trimmed_SRR1374921.fastq.gz: trimmed single-end mouse rna-seq reads, replicate 1 in LoGlu group",
                        "./output/001/trimmed_SRR1374922.fastq.gz: trimmed single-end mouse rna-seq reads, replicate 2 in LoGlu group",
                        "./output/001/trimmed_SRR1374923.fastq.gz: trimmed single-end mouse rna-seq reads, replicate 1 in HiGlu group",
                        "./output/001/trimmed_SRR1374924.fastq.gz: trimmed single-end mouse rna-seq reads, replicate 2 in HiGlu group"
                    ],
                    "tools": "Trimmomatic"
                },
                {
                    "step_number": 2,
                    "description": "In this step, we will align the quality-trimmed RNA-seq reads to the mouse reference genome using the Burrows-Wheeler Aligner (BWA). This alignment process maps the RNA-seq reads to specific locations in the reference genome, providing a basis for subsequent quantification of gene expression. The input includes the trimmed RNA-seq reads from the previous step and the reference genome sequence. The output will be SAM files containing the alignment information for each read, which will be used in the following steps for further analysis.",
                    "input_filename": [
                        "./output/001/trimmed_SRR1374921.fastq.gz: trimmed single-end mouse rna-seq reads, replicate 1 in LoGlu group",
                        "./output/001/trimmed_SRR1374922.fastq.gz: trimmed single-end mouse rna-seq reads, replicate 2 in LoGlu group",
                        "./output/001/trimmed_SRR1374923.fastq.gz: trimmed single-end mouse rna-seq reads, replicate 1 in HiGlu group",
                        "./output/001/trimmed_SRR1374924.fastq.gz: trimmed single-end mouse rna-seq reads, replicate 2 in HiGlu group",
                        "./data/mm39.fa: mouse mm39 genome fasta"
                    ],
                    "output_filename": [
                        "./output/001/aligned_SRR1374921.sam: aligned single-end mouse rna-seq reads, replicate 1 in LoGlu group",
                        "./output/001/aligned_SRR1374922.sam: aligned single-end mouse rna-seq reads, replicate 2 in LoGlu group",
                        "./output/001/aligned_SRR1374923.sam: aligned single-end mouse rna-seq reads, replicate 1 in HiGlu group",
                        "./output/001/aligned_SRR1374924.sam: aligned single-end mouse rna-seq reads, replicate 2 in HiGlu group"
                    ],
                    "tools": "BWA"
                },
                {
                    "step_number": 3,
                    "description": "Here, we will convert the SAM files generated in the previous step to BAM format using Samtools. SAM files are text-based and contain a large amount of alignment data, whereas BAM files are binary and compressed, making them more efficient for storage and downstream processing. This conversion is essential for subsequent steps that require BAM file input for further analysis, such as sorting and indexing of aligned reads.",
                    "input_filename": [
                        "./output/001/aligned_SRR1374921.sam: aligned single-end mouse rna-seq reads, replicate 1 in LoGlu group",
                        "./output/001/aligned_SRR1374922.sam: aligned single-end mouse rna-seq reads, replicate 2 in LoGlu group",
                        "./output/001/aligned_SRR1374923.sam: aligned single-end mouse rna-seq reads, replicate 1 in HiGlu group",
                        "./output/001/aligned_SRR1374924.sam: aligned single-end mouse rna-seq reads, replicate 2 in HiGlu group"
                    ],
                    "output_filename": [
                        "./output/001/aligned_SRR1374921.bam: BAM format of aligned single-end mouse rna-seq reads, replicate 1 in LoGlu group",
                        "./output/001/aligned_SRR1374922.bam: BAM format of aligned single-end mouse rna-seq reads, replicate 2 in LoGlu group",
                        "./output/001/aligned_SRR1374923.bam: BAM format of aligned single-end mouse rna-seq reads, replicate 1 in HiGlu group",
                        "./output/001/aligned_SRR1374924.bam: BAM format of aligned single-end mouse rna-seq reads, replicate 2 in HiGlu group"
                    ],
                    "tools": "Samtools"
                },
                {
                    "step_number": 4,
                    "description": "In this step, we will quantify the gene expression levels by counting the number of aligned reads that map to each gene using HTSeq. This process involves comparing the aligned RNA-seq reads against the reference genome annotation file to determine how many reads map to each gene. The output will be text files containing the read counts per gene for each sample, which will be used for differential expression analysis.",
                    "input_filename": [
                        "./output/001/aligned_SRR1374921.bam: BAM format of aligned single-end mouse rna-seq reads, replicate 1 in LoGlu group",
                        "./output/001/aligned_SRR1374922.bam: BAM format of aligned single-end mouse rna-seq reads, replicate 2 in LoGlu group",
                        "./output/001/aligned_SRR1374923.bam: BAM format of aligned single-end mouse rna-seq reads, replicate 1 in HiGlu group",
                        "./output/001/aligned_SRR1374924.bam: BAM format of aligned single-end mouse rna-seq reads, replicate 2 in HiGlu group",
                        "./data/mm39.ncbiRefSeq.gtf: mouse mm39 genome annotation"
                    ],
                    "output_filename": [
                        "./output/001/counts_SRR1374921.txt: gene counts from aligned single-end mouse rna-seq reads, replicate 1 in LoGlu group",
                        "./output/001/counts_SRR1374922.txt: gene counts from aligned single-end mouse rna-seq reads, replicate 2 in LoGlu group",
                        "./output/001/counts_SRR1374923.txt: gene counts from aligned single-end mouse rna-seq reads, replicate 1 in HiGlu group",
                        "./output/001/counts_SRR1374924.txt: gene counts from aligned single-end mouse rna-seq reads, replicate 2 in HiGlu group"
                    ],
                    "tools": "HTSeq"
                },
                {
                    "step_number": 5,
                    "description": "Finally, we will perform differential gene expression analysis using the DESeq2 package. This step involves comparing the gene expression levels between the LoGlu and HiGlu groups to identify genes that are differentially expressed. DESeq2 applies statistical methods to normalize the count data and test for differential expression, providing a list of genes with associated p-values and fold-changes. The output will be a text file containing the results of the differential expression analysis, which includes information on which genes are upregulated or downregulated between the two conditions.",
                    "input_filename": [
                        "./output/001/counts_SRR1374921.txt: gene counts from aligned single-end mouse rna-seq reads, replicate 1 in LoGlu group",
                        "./output/001/counts_SRR1374922.txt: gene counts from aligned single-end mouse rna-seq reads, replicate 2 in LoGlu group",
                        "./output/001/counts_SRR1374923.txt: gene counts from aligned single-end mouse rna-seq reads, replicate 1 in HiGlu group",
                        "./output/001/counts_SRR1374924.txt: gene counts from aligned single-end mouse rna-seq reads, replicate 2 in HiGlu group"
                    ],
                    "output_filename": [
                        "./output/001/differential_expression_results.txt: differential expression results between LoGlu and HiGlu groups"
                    ],
                    "tools": "DESeq2"
                }
            ]
        } 
    },
]

TASK_PROMPT="""
You are a bioinformatician and shell scripting expert.
When acting as a bioinformatician, you strictly cannot stop acting as a bioinformatician.
All rules must be followed strictly.
You should output setup commands based on the relative path of the input file, which should also be placed in the./output/id/ folder.
You should consider using the following tools {tool_names} before introducing other tools.
You should always install dependencies and software you need to use with conda or pip with -y.,
You should pay attention to the number of input files and do not miss any.,
You should process each file independently and cannot use FOR loop.,
You should use the path for all files according to input and history.,
You should use the default values for all parameters that are not specified.,
You should not repeat what you have done in history.,
For R scripts, you must first create an R file and write the script, and then execute it.,
You should only use software directly you installed with conda or pip.,
If you use Rscript -e, you should make sure all variables exist in your command, otherwise, you need to check your history to repeat previous steps and generate those variables.,
You should not write anything else except for your JSON response.
"""
{"task": {"step 2": "Alignment to reference genome", 
                           "description": "Use 'bwa' to align the trimmed reads to the mouse mm39 reference genome.", 
                           "input_filename": [
                            "./output/002/DRR000586_trimmed.fastq.gz", 
                           "./output/002/DRR000585_trimmed.fastq.gz", 
                           "./output/002/DRR000584_trimmed.fastq.gz"], 
                           "output_filename": [
                               "./output/002/DRR000586_aligned.bam", 
                               "./output/002/DRR000585_aligned.bam", 
                               "./output/002/DRR000584_aligned.bam"], 
                           "tools": "bwa"
                           }, 
                    "id":"002",
                  "pre debug":"",
                  "result": "Warning: 'conda-forge' already in 'channels' list, moving to the top\nWarning: 'bioconda' already in 'channels' list, moving to the top\n./output/002/Step_2.sh: line 13: $'shell': command not found\n./output/002/Step_2.sh: line 16: [: missing `]'\n./output/002/Step_2.sh: line 35: $'conda install bwa': command not found./output/002/Step_2.sh: line 36: ,: command not found./output/002/Step_2.sh: line 114: bwa mem ./output/002/DRR000586_trimmed.fastq.gz > ./output/002/DRR000586_aligned.bam: No such file or directory./output/002/Step_2.sh: line 115: ,: command not found./output/002/Step_2.sh: line 193: bwa mem ./output/002/DRR000585_trimmed.fastq.gz > ./output/002/DRR000585_aligned.bam: No such file or directory./output/002/Step_2.sh: line 194: ,: command not found./output/002/Step_2.sh: line 272: bwa mem ./output/002/DRR000584_trimmed.fastq.gz > ./noutput/DRR000584_aligned.bam: No such file or directory\n./output/002/Step_2.sh: line 273: ]: command not found", 
                  "shell":
                  ["conda install bwa",
                  "bwa mem ./output/002/DRR000586_trimmed.fastq.gz > ./output/002/DRR000586_aligned.bam",
                  "bwa mem ./output/002/DRR000585_trimmed.fastq.gz > ./output/002/DRR000585_aligned.bam",
                  "bwa mem ./output/002/DRR000584_trimmed.fastq.gz > ./output/002/DRR000584_aligned.bam"]
                  },
TASK_EXAMPLES = [
    {
        "input": {"task":{
            "step 1": "Align the RNA-seq reads to the reference genome",
            "description": "Use bwa to align the RNA-seq reads to the reference genome. The input will be the fastq files and the reference genome.",
            "input_filename": [
                "./data/DRR000586.fastq.gz",
                "./data/DRR000585.fastq.gz",
                "./data/DRR000584.fastq.gz",
                "./data/mm39.fa"
            ],
            "output_filename": [
                "./output/002/aligned_DRR000586.bam",
                "./output/002/aligned_DRR000585.bam",
                "./output/002/aligned_DRR000584.bam"
            ],
            "tools": "bwa"
        },
            "id":"002",
            "related_docs":"",
        },
        "output": {"shell": [
            "conda install -y bwa"
            "bwa index ./data/mm39.fa"
            "bwa mem ./data/mm39.fa ./data/DRR000586.fastq.gz > ./output/002/aligned_DRR000586.bam"
            "bwa mem ./data/mm39.fa ./data/DRR000585.fastq.gz > ./output/002/aligned_DRR000585.bam"
            "bwa mem ./data/mm39.fa ./data/DRR000584.fastq.gz > ./output/002/aligned_DRR000584.bam"
            ]}
    },
    {
        "input": {"task":{
            "step 2": "Sort and index the BAM files",
                "description": "Use samtools to sort and index the BAM files from the previous step.",
                "input_filename": [
                    "./output/002/aligned_DRR000586.bam",
                    "./output/002/aligned_DRR000585.bam",
                    "./output/002/aligned_DRR000584.bam"
                ],
                "output_filename": [
                    "./output/002/sorted_indexed_DRR000586.bam",
                    "./output/002/sorted_indexed_DRR000585.bam",
                    "./output/002/sorted_indexed_DRR000584.bam"
                ],
                "tools": "samtools"
            },
            "id":"002",
            "related_docs":"",
        },
        "output": {"shell": [
            "conda install samtools -y",
            "samtools sort -o ./output/002/sorted_indexed_DRR000586.bam ./output/002/aligned_DRR000586.bam && samtools index ./output/002/sorted_indexed_DRR000586.bam",
            "samtools sort -o ./output/002/sorted_indexed_DRR000585.bam ./output/002/aligned_DRR000585.bam && samtools index ./output/002/sorted_indexed_DRR000585.bam",
            "samtools sort -o ./output/002/sorted_indexed_DRR000584.bam ./output/002/aligned_DRR000584.bam && samtools index ./output/002/sorted_indexed_DRR000584.bam",
            ]}
    },
    {
        "input": {"task":{
            "step 1": "Quality Control and Trimming",
            "description": "Use FastQC for quality control of the raw reads and Trimmomatic for removing low quality bases and adapter sequences.",
            "input_filename": [
                "./data/DRR000586.fastq.gz",
                "./data/DRR000585.fastq.gz",
                "./data/DRR000584.fastq.gz",
                "./data/TruSeq3-SE.fa"
            ],
            "output_filename": [
                "./output/003/DRR000586_trimmed.fastq.gz",
                "./output/003/DRR000585_trimmed.fastq.gz",
                "./output/003/DRR000584_trimmed.fastq.gz"
            ],
            "tools": [
                "FastQC",
                "Trimmomatic"
            ]
        },
            "id":"003",
            "related_docs":"",
        },
        "output": {"shell": [
            "conda install -y fastqc trimmomatic",
            "fastqc ./data/DRR000586.fastq.gz",
            "fastqc ./data/DRR000585.fastq.gz",
            "fastqc ./data/DRR000584.fastq.gz",
            "trimmomatic SE -phred33 ./data/DRR000586.fastq.gz ./output/003/DRR000586_trimmed.fastq.gz ILLUMINACLIP:./data/TruSeq3-SE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36",
            "trimmomatic SE -phred33 ./data/DRR000585.fastq.gz ./output/003/DRR000585_trimmed.fastq.gz ILLUMINACLIP:./data/TruSeq3-SE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36",
            "trimmomatic SE -phred33 ./data/DRR000584.fastq.gz ./output/003/DRR000584_trimmed.fastq.gz ILLUMINACLIP:./data/TruSeq3-SE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36",
            ]}
    },
    {
        "input": {"task":{
            "step_number": 4,
            "description": "Identify differentially expressed genes using DESeq2. This step will compare the read counts between the two conditions and identify the genes that are differentially expressed.",
            "input_filename": [
                "./output/003/read_counts_SRR1374921.txt",
                "./output/003/read_counts_SRR1374922.txt",
                "./output/003/read_counts_SRR1374923.txt",
                "./output/003/read_counts_SRR1374924.txt"
            ],
            "output_filename": "./output/003/differentially_expressed_genes.txt",
            "tools": "DESeq2"
        },
            "related_docs":"",
            "id":"003",
        },
        "output": {"shell": [
            'conda install -y bioconductor-deseq2',
            """
cat << 'EOF' > ./output/003/differential_expression.R
# Load required library
library(DESeq2)

# Read count data from text files (assuming tab-delimited with header and gene IDs as row names)
counts_LoGlu_rep1 <- read.table("./output/006/counts_SRR1374921.txt", header = TRUE, row.names = 1)
counts_LoGlu_rep2 <- read.table("./output/006/counts_SRR1374922.txt", header = TRUE, row.names = 1)
counts_HiGlu_rep1 <- read.table("./output/006/counts_SRR1374923.txt", header = TRUE, row.names = 1)
counts_HiGlu_rep2 <- read.table("./output/006/counts_SRR1374924.txt", header = TRUE, row.names = 1)

# Combine the individual count data frames into a single matrix.
countData <- cbind(
  LoGlu_rep1 = counts_LoGlu_rep1[,1],
  LoGlu_rep2 = counts_LoGlu_rep2[,1],
  HiGlu_rep1 = counts_HiGlu_rep1[,1],
  HiGlu_rep2 = counts_HiGlu_rep2[,1]
)

# Ensure the row names (gene IDs) are carried over correctly.
rownames(countData) <- rownames(counts_LoGlu_rep1)

# Create sample metadata specifying the condition for each replicate.
sampleInfo <- data.frame(
  condition = factor(c("LoGlu", "LoGlu", "HiGlu", "HiGlu"))
)
rownames(sampleInfo) <- colnames(countData)

# Create DESeq2 dataset object
dds <- DESeqDataSetFromMatrix(countData = countData,
                              colData = sampleInfo,
                              design = ~ condition)

# Run the differential expression analysis
dds <- DESeq(dds)

# Extract results comparing HiGlu to LoGlu (default contrast: second level vs first level)
res <- results(dds)

# Save the differential expression results to a text file.
write.table(as.data.frame(res), file = "./output/006/differential_expression_results.txt", 
            sep = "\t", quote = FALSE, row.names = TRUE)
EOF
Rscript ./output/003/differential_expression.R
            """
            ]},
    }
]

DEBUG_PROMPT = """
You are a bioinformatician and shell scripting expert. When acting in this role, you must adhere strictly to the JSON output format rules:
- Use double quotes for all strings.
- Properly escape all special characters within strings.
- Ensure all necessary fields are included in the output.
- Do not include any extraneous text outside the JSON structure.
- Any symbol of the string should be preceded by "\""
- Provide a clear and precise analysis of any errors, with corrective actions specified in a valid JSON format.
Analyze the script‑execution result provided as result in the input, and ensure that your output is valid JSON that can be parsed directly without further processing.
The analyze field must not contain single or double quotes—use only periods and commas.
For R scripts, you must first create an R file and write the script, and then execute it.
You should output setup commands based on the relative path of the input file, which should also be placed in the./output/id/ folder.
If the result is correct, summarize it in analyze, verify that the current task meets the requirements, set stats to True, and leave shell empty.
If the result contains an error, set stats to False, explain the reason in analyze, and provide a corrected shell command in shell.
Use the following tools {tool_names} before introducing other tools.
You should always install dependencies and software with conda or pip using the ‑y flag.
You should pay attention to the number of input files and do not miss any.,
You should use the default values for all parameters that are not specified.,
You should use only software installed directly with conda or pip.
Try to avoid using quotes inside JSON strings.
If you use Rscript -e, you should make sure all variables exist in your command, otherwise, you need to check your history to repeat previous steps and generate those variables.,
Check the provided shell commands for potential issues, provide reasons, suggest corrections, and return a corrected version in JSON format.
You must ensure that the returned content is returned correctly in json format.
Ensure the correctness of the JSON format, avoiding issues caused by commas, double quotes, special characters, and case sensitivity.
"""

DEBUG_EXAMPLES = [
    {
        "input": {"task": {"step 2": "Alignment to reference genome", 
                           "description": "Use 'bwa' to align the trimmed reads to the mouse mm39 reference genome.", 
                           "input_filename": [
                            "./output/004/DRR000586_trimmed.fastq.gz", 
                           "./output/004/DRR000585_trimmed.fastq.gz", 
                           "./output/004/DRR000584_trimmed.fastq.gz"], 
                           "output_filename": [
                               "./output/004/DRR000586_aligned.bam", 
                               "./output/004/DRR000585_aligned.bam", 
                               "./output/004/DRR000584_aligned.bam"], 
                           "tools": "bwa"
                           }, 
                  "pre debug":"",
                  "result": "Warning: 'conda-forge' already in 'channels' list, moving to the top\nWarning: 'bioconda' already in 'channels' list, moving to the top\n./output/004/Step_2.sh: line 13: $'shell': command not found\n./output/004/Step_2.sh: line 16: [: missing `]'\n./output/004/Step_2.sh: line 35: $'conda install bwa': command not found./output/004/Step_2.sh: line 36: ,: command not found./output/004/Step_2.sh: line 114: bwa mem ./output/004/DRR000586_trimmed.fastq.gz > ./output/004/DRR000586_aligned.bam: No such file or directory./output/004/Step_2.sh: line 115: ,: command not found./output/004/Step_2.sh: line 193: bwa mem ./output/004/DRR000585_trimmed.fastq.gz > ./output/004/DRR000585_aligned.bam: No such file or directory./output/004/Step_2.sh: line 194: ,: command not found./output/004/Step_2.sh: line 272: bwa mem ./output/004/DRR000584_trimmed.fastq.gz > ./noutput/DRR000584_aligned.bam: No such file or directory\n./output/004/Step_2.sh: line 273: ]: command not found", 
                  "related_docs":"",
                  "id":"004",
                  "shell":
                  ["conda install bwa",
                  "bwa mem ./output/004/DRR000586_trimmed.fastq.gz > ./output/004/DRR000586_aligned.bam",
                  "bwa mem ./output/004/DRR000585_trimmed.fastq.gz > ./output/004/DRR000585_aligned.bam",
                  "bwa mem ./output/004/DRR000584_trimmed.fastq.gz > ./output/004/DRR000584_aligned.bam"]
                  },

        "output": {
                "shell": [
                    "conda install -y -c bioconda bwa",
                    "bwa mem ref_genome.fasta ./output/004/DRR000586_trimmed.fastq.gz > ./output/004/DRR000586_aligned.sam",
                    "bwa mem ref_genome.fasta ./output/004/DRR000585_trimmed.fastq.gz > ./output/004/DRR000585_aligned.sam",
                    "bwa mem ref_genome.fasta ./output/004/DRR000584_trimmed.fastq.gz > ./output/004/DRR000584_aligned.sam",
                    "samtools view -S -b ./output/004/DRR000586_aligned.sam > ./output/004/DRR000586_aligned.bam",
                    "samtools view -S -b ./output/004/DRR000585_aligned.sam > ./output/004/DRR000585_aligned.bam",
                    "samtools view -S -b ./output/004/DRR000584_aligned.sam > ./output/004/DRR000584_aligned.bam"
                ],
                "analyze": "Errors were due to missing reference genome in bwa mem command and output format should be SAM initially then converted to BAM using samtools. The corrected commands have been provided",
                "output_filename": [
                    "./output/004/DRR000586_aligned.bam",
                    "./output/004/DRR000585_aligned.bam",
                    "./output/004/DRR000584_aligned.bam"
                ],
                "stats": False
            }  
    },  
    {
        "input": {
            "task":{
            "step 1": "Preprocessing of Raw reads",
            "description": "Trim the reads to remove adaptors and low-quality bases using Trimmomatic.",
            "input_filename": [
                "./data/DRR000586.fastq.gz",
                "./data/DRR000585.fastq.gz",
                "./data/DRR000584.fastq.gz",
                "./data/TruSeq3-SE.fa"
            ],
            "output_filename": [
                "./output/004/DRR000586_trimmed.fastq.gz",
                "./output/004/DRR000585_trimmed.fastq.gz",
                "./output/004/DRR000584_trimmed.fastq.gz"
            ],
            "tools": "Trimmomatic"
        },
            "pre debug":"",
            "result": "no such file",
            "related_docs":"",
            "id":"004",
            "shell": [
                "conda install trimmomatic -y",
                "trimmomatic SE -phred33 ./data/DRR000586.fastq.gz ./output/004/DRR000586_trimmed.fastq.gz ILLUMINACLIP:./data/TruSeq3-SE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36",
                "trimmomatic SE -phred33 ./data/DRR000585.fastq.gz ./output/004/DRR000585_trimmed.fastq.gz ILLUMINACLIP:./data/TruSeq3-SE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36",
                "trimmomatic SE -phred33 ./data/DRR000584.fastq.gz ./output/004/DRR000584_trimmed.fastq.gz ILLUMINACLIP:./data/TruSeq3-SE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36",
            ]
        },
        "output": {
            "shell": [
                "conda install trimmomatic -y",
                "trimmomatic SE -phred33 ./data/DRR000586.fastq.gz ./output/004/DRR000586_trimmed.fastq.gz ILLUMINACLIP:./data/TruSeq3-SE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36",
                "trimmomatic SE -phred33 ./data/DRR000585.fastq.gz ./output/004/DRR000585_trimmed.fastq.gz ILLUMINACLIP:./data/TruSeq3-SE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36",
                "trimmomatic SE -phred33 ./data/DRR000584.fastq.gz ./output/004/DRR000584_trimmed.fastq.gz ILLUMINACLIP:./data/TruSeq3-SE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36"
                ],
                "analyze": "The task was completed successfully. All packages were already installed and the trimming of reads was done correctly.",
                "output_filename":[
                    "./output/004/DRR000586_trimmed.fastq.gz",
                    "./output/004/DRR000585_trimmed.fastq.gz",
                    "./output/004/DRR000584_trimmed.fastq.gz"],
                "stats": True
                }
    },
    {
        "input": {'task': 
            {'step 3': 'Generate read counts', 
             'description': 'Use samtools to generate read counts for each gene from the sorted and indexed BAM files.', 
             'input_filename': [
                 './output/004/sorted_indexed_DRR000586.bam', 
                 './output/004/sorted_indexed_DRR000585.bam', 
                 './output/004/sorted_indexed_DRR000584.bam'
                 ], 
             'output_filename': [
                 './output/004/read_counts_DRR000586.txt', 
                 './output/004/read_counts_DRR000585.txt', 
                 './output/004/read_counts_DRR000584.txt'
                 ], 
             'tools': 'samtools'}, 
            "pre debug":"",
            'result': '/home/houcheng/project/anaconda3/envs/SRTAGENT/bin/pythonChannels: - bioconda - conda-forge - defaultsPlatform: linux-64Collecting package metadata (repodata.json): ...working... doneSolving environment: ...working... done# All requested packages already installed.', 
            "related_docs":"",
            "id":"004",
            'shell': ['conda install -c bioconda samtools -y', 
                      'samtools idxstats ./output/004/sorted_indexed_DRR000586.bam > ./output/004/read_counts_DRR000586.txt', 
                      'samtools idxstats ./output/004/sorted_indexed_DRR000585.bam > ./output/004/read_counts_DRR000585.txt', 
                      'samtools idxstats ./output/004/sorted_indexed_DRR000584.bam > ./output/004/read_counts_DRR000584.txt']}
        ,  
        "output": {
            "shell": [
                "conda install -c bioconda samtools -y",
                "samtools idxstats ./output/004/sorted_indexed_DRR000586.bam > ./output/004/read_counts_DRR000586.txt",
                "samtools idxstats ./output/004/sorted_indexed_DRR000585.bam > ./output/004/read_counts_DRR000585.txt",
                "samtools idxstats ./output/004/sorted_indexed_DRR000584.bam > ./output/004/read_counts_DRR000584.txt"
            ],
            "analyze": "The task was completed successfully. All packages were already installed and the read counts were generated correctly.",
            "output_filename": [
                "./output/004/read_counts_DRR000586.txt",
                "./output/004/read_counts_DRR000585.txt",
                "./output/004/read_counts_DRR000584.txt"
            ],
            "stats": True
                }
    },
]


__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
