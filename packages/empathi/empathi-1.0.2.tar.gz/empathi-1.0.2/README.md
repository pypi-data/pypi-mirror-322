
<span style="font-size:2em;">**Empathi**</span><br>
<span style="font-size:1.15em;">**Embedding-based Phage Protein Annotation Tool by Hierarchical Assignment**</span>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About the Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage details</a></li>
  </ol>
</details>

## About the Project

Empathi is a tool for the prediction of bacteriophage protein functions. It utilizes the highly informative ProtT5 
protein embeddings to make predictions. In addition, new functional groups were defined to be better suited for
machine-learning than the often-overlapping [PHROG](https://phrogs.lmge.uca.fr/) categories.

A preprint is available [here](https://doi.org/10.1101/2024.12.31.630607).


## Getting Started
Empathi has been packaged in [PyPI](https://pypi.org/project/empathi/) and as an 
[Apptainer container](https://cloud.sylabs.io/library/alexandreboulay/empathi/empathi) for ease of use. \
The source code can also be downloaded from [HuggingFace](https://huggingface.co/AlexandreBoulay/empathi).

### Prerequisites
The full list of dependencies and versions can be found in [requirements.txt](https://huggingface.co/AlexandreBoulay/EmPATHi/blob/main/requirements.txt).
Dependencies are taken care of by pip and Apptainer. See instructions below.
```
python/3.11.5
joblib==1.2.0
numpy==1.26.4
pandas==2.2.1
torch==2.3.0
scipy==1.13.1
scikit-learn==1.5.0
transformers==4.43.1
sentencepiece==0.2.0
```


### Installation
There are three ways of installing Empathi: through PyPI, as an Apptainer container or as source code.


#### 1. PIP
First, create a virtual environement in python 3.11.5.
```
conda create -n empathi_env python=3.11.5
conda activate empathi_env
```

Download models for Empathi:
```
git lfs install
git clone https://huggingface.co/AlexandreBoulay/empathi
export PATH="/path/to/empathi/models:$PATH"
```

Install dependencies:
```
pip install empathi
```

Usage
```
python
from empathi import empathi
empathi.empathi("input_file", "name", output_folder="path/to/output")
```


#### 2. Apptainer
Download [Apptainer](https://apptainer.org/docs/admin/main/installation.html) or singularity. On windows, this will require a virtual machine. 
[WSL](https://learn.microsoft.com/en-us/windows/wsl/install) works well.

Fetch Empathi from [Sylabs](https://cloud.sylabs.io/library/alexandreboulay/empathi/empathi):
```
apptainer pull empathi.sif library://alexandreboulay/empathi/empathi
```

Launch Empathi
```
apptainer run empathi.sif path/to/input_file name
```


#### 3. From source code
First, create a virtual environement in python 3.11.5.
```
conda create -n empathi_env python=3.11.5
conda activate empathi_env
```

Clone the repo.
```
git lfs install
git clone https://huggingface.co/AlexandreBoulay/empathi
```

Install dependencies:
```
cd empathi
pip install -r requirements.txt
```

Usage
```
python src/empathi/empathi.py input_file name
```

### Usage details
A fasta file of protein sequences or a csv file of protein embeddings can be used as input.

Specifying the option --only_embeddings will only compute embeddings. This step is much faster with a GPU.
The embeddings file can then be reinputted using the same command (without --only_embeddings) and specifying the new file as input file. 

Options:
 - input_file: Path to input file containing protein sequencs (.fa*) or protein embeddings (.pkl/.csv).
 - name: Name of file you want to save to (wOut extension). Should be different between runs to avoid overwriting files.
 - --models_folder: Path to folder containing EmPATHi models. Can be left unspecified if it was added to PATH earlier.
 - --only_embeddings: Whether to only calculate embeddings (no functional prediction).
 - --output_folder: Path to the output folder. Default is ./empathi_out/.
 - --mode: Which types of proteins you want to predict. Accepted arguments are "all", "pvp", "rbp", "lysin", "regulator"...

When launching from python omit the '--' in front of args.
