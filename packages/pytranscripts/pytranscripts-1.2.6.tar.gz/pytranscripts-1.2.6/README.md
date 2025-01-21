# pytranscripts
An Open source👨‍🔧 Python Library for Automated classification of Electronic Medical records 

## Installation
To install the latest version , simply use

```sh
pip install -U pytranscripts
```

## Pipeline Summary
![pipeline image](assets/edited_nlp_workflow.png)

### Stages
1. Data Extraction
2. Target Identification
3. Finetuning Annotated Data on Pretrained models (Bert & Electra)
4. Extracting Interviwer/Interviewee records from the specified docx file storage
5. Metrics Evaluation (Accuracy & Cohen Kappa Score)
6. Reordering records as a neatly arranged and flagged spreadsheet, alongside metrics and reports from pretrained models.

## Example Usage

#### Mount Google Drive (Optional)
If using Google Drive as the data source:

```python
from google.colab import drive
drive.mount('/content/drive')
```


## Automate Data Export

To export and combine all .docx files from a folder into a single file:


```python

from pytranscripts import export_docx_from_folder

# Define input and output paths
INPUT_FOLDER = "/content/drive/MyDrive/Your/Path/To/Dataset/"
OUTPUT_FILE = "output.csv"

# Define labels for structured data
LABELS = [
    'Value equation',
    'Credentialing / Quality Assurance Infrastructure',
    'Financial Impact',
    'Health System Characteristics',
    'Clinical utility & efficiency - Provider perspective',
    'Workflow related problems',
    'Provider Characteristics',
    'Training',
    'Patient/Physician interaction in LUS',
    'Imaging modalities in general',
]

# Export data
export_docx_from_folder(
    input_directory=INPUT_FOLDER,
    output_file=OUTPUT_FILE,
    labels=LABELS
)
```

This will:

- Read all .docx files from INPUT_FOLDER.
- Combine their content into a single file.
- Apply the defined labels to create a structured dataset.

## Requirements
Python 3.6 or later
GPU access recommended for optimal performance (if using Jupyter Notebook).
pytranscripts version 1.2.4 or higher.


## Model Training
Now , the detailed class shows how to properly use our transcript trainer in making training and inference easy based on your document


```python
from pytranscripts import TranscriptTrainer


trainer = TranscriptTrainer(
    input_file='/content/drive/MyDrive/Kalu+Deola/OLD NLP/CompletedMerged.xlsx',  # Path to the CSV / XLSX file containing the tagged documents. This is the main data source for training and evaluation.

    destination_path='/content/',  # Directory where all the training results, models, and logs will be saved. , We are using colab path to make things seamless

    text_column='full_quote',  # Specifies the column name in the CSV file that contains the text data to be used for training.

    test_size=0.2,  # Determines the fraction of the data that will be used for testing the model, instead of training it. Here, 20% of data will be used for testing.

    max_length=512, #The maximum number of tokens to include in each input sequence, this helps in managing memory and computational resources. Sequences longer than this will be truncated.

    num_train_epochs=1, # The number of times the model will iterate over the entire training dataset during training. More epochs will mean more training.

    learning_rate_distilbert=2e-5, # Learning rate for the DistilBERT model. This controls the step size during model optimization, lower values mean smaller updates to the model.

    learning_rate_electra=3e-5,  # Learning rate for the Electra model.  This controls the step size during model optimization, lower values mean smaller updates to the model.

    labels=[ # A list of labels used for the multi-label classification task. Each label corresponds to a category the model will try to identify in the text.
            'Value equation',
            'Credentialing / Quality Assurance Infrastructure',
            'Finanicial Impact',
            'Health System Characteristics',
            'Clinical utility & efficiency-Provider perspective',
            'Workflow related problems',
            'Provider Characteristics',
            'Training',
            'Patient/Physican interaction in LUS',
            'Imaging modalities in general'
    ], # PLEASE MAKE SURE THAT THE LIST YOU ARE GOING TO BE USING HERE MATCHES THE ONE IN YOUR INPUT FILE


    upper_lower_mapping = { # Dictionary for mapping high level categories to lower level categories
        "multi_level_org_char": [ #High level category name
            "Provider Characteristics", #lower level category names
            "Health System Characteristics" #lower level category names
        ],
        "multi_level_org_perspect": [ #High level category name
            "Imaging modalities in general", #lower level category names
            'Value equation', #lower level category names
            "Clinical utility & efficiency-Provider perspective", #lower level category names
            "Patient/Physican interaction in LUS", #lower level category names
            'Workflow related problems' #lower level category names
        ],
        "impl_sust_infra": [ #High level category name
            "Training",  #lower level category names
            'Credentialing / Quality Assurance Infrastructure', #lower level category names
            "Finanicial Impact"  #lower level category names
        ]
    }
)
```

## Contributing
We welcome contributions! Please follow the contributing guidelines.

## License
This project is licensed under the MIT License. See the LICENSE file for details.



