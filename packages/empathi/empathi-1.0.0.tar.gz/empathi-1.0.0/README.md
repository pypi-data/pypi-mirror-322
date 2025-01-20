
<span style="font-size:2em;">**EmPATHi**</span><br>
<span style="font-size:1.15em;">**Embedding-based Phage Protein Annotation Tool by Hierarchical assignment**</span>


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
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## About the Project

Little description.

Preprint can be found at: [link]


## Getting Started
EmPATHi has been packaged in [PyPI](https://pypi.org/project/empathi/0.0.1/) and as an Apptainer container for ease of use. \
The source code can also be downloaded from [HuggingFace](https://huggingface.co/AlexandreBoulay/EmPATHi).

### Prerequisites
The full list of dependencies and versions we tested to be compatible can be found in [requirements.txt](https://huggingface.co/AlexandreBoulay/EmPATHi/blob/main/requirements.txt).
Dependencies are taken care of by pip and Apptainer. See instructions below.
```
python/3.11.5
joblib==1.2.0
numpy==1.26.4
pandas==2.2.1
matplotlib==3.9.0
torch==2.3.0
scipy==1.13.1
scikit-learn==1.5.0
transformers==4.43.1
sentencepiece==0.2.0
seaborn==0.13.2
```

The models used by EmPATHi must be obtained seperately. See instructions below.\
The [models](https://huggingface.co/AlexandreBoulay/EmPATHi/tree/main/models) folder for EmPATHi must be obtained from HuggingFace.\
[ProtT5](https://huggingface.co/Rostlab/prot_t5_xl_half_uniref50-enc) must also be downloaded from HuggingFace.


### Installation
First, create a virtual environement in python 3.11.5. This can be done using tools such as conda and virtualenv.

Download models for EmPATHi and ProtT5:
```
git lfs install
git clone https://huggingface.co/AlexandreBoulay/EmPATHi
git clone https://huggingface.co/Rostlab/prot_t5_xl_half_uniref50-enc Rostlab/prot_t5_xl_half_uniref50-enc
export PATH="/path/to/EmPATHi/models:$PATH"
export PATH="/path/to/Rostlab/prot_t5_xl_half_uniref50-enc:$PATH"
```

#### 1. PIP
```
pip install empathi
```

#### 2. Apptainer


#### 3. From source code
Clone the repo if it isn't already done:
```
git lfs install
git clone https://huggingface.co/AlexandreBoulay/EmPATHi
```

Install dependencies:
```
cd EmPATHi
pip install -r requirements.txt
```

### Usage
For pip:
```
python
from empathi import empathi
empathi(input_file, name, output_folder="path/to/output")
```

For Apptainer:

From command line:
```
python src/empathi/empathi.py -h
```

Options:
 - input_file: Path to input file containing protein sequencs (.fa*) or protein embeddings (.pkl/.csv).
 - name: Name of file you want to save to (wOut extension). Should be different between runs to avoid overwriting files.
 - --models_folder: Path to folder containing EmPATHi models. Can be left unspecified if it was added to PATH earlier.
 - --only_embeddings: Whether to only calculate embeddings (no functional prediction).
 - --output_folder: Path to the output folder. Default is ./empathi_out/.
 - --mode: Which types of proteins you want to predict. Accepted arguments are "all", "pvp", "rbp", "lysin", "regulator"...

When launching from python omit the '--' in front of args.

## Contact

