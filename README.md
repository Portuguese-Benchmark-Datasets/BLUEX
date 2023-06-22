# BLUEX

Despite Portuguese being the fifth most widely spoken language, there is a lack of freely available resources for evaluating language models in Portuguese. This repository contains a multimodal dataset consisting of the two leading university entrance exams conducted in Brazil: Convest (Unicamp) and Fuvest (USP), spanning from 2018 to 2023. The dataset comprises a total of 1095 questions, of which 638 do not have accompanying images.

## Collection methodology

The dataset was generated through manual annotation of exam questions using the following format:

```
{
    "question": str,
    "number": int,
    "id": str,
    "alternatives": List[str],
    "associated_images": List[str],
    "answer": str,
    "has_associated_images": bool,
    "alternatives_type": str,
    "subject": List[str],
    "PRK": bool,
    "TU": bool,
    "IU": bool,
    "MR": bool,
    "ML": bool,
    "BK": bool
}
```
Additionally, we modified the text of the questions to include a tag indicating the placement of images, such as [IMAGE 0], which corresponds to the first image in the associated_images list.

### Downloading the dataset

The dataset can be downloaded automatically by following the steps below. We also provide a zip file containing the dataset.

### How to use

```bash
pip install -r requirements.txt
```

```Python
# Loads the dataset
from load_bluex import BluexLoader

loader = BluexLoader()

# Gets the full dataset
full_dataset = loader.get_all_questions()

# Gets the dataset filtered by params
filtered_dataset = loader.filtered_by(params)

# Gets the dataset generator
generator = loader.get_bluex_generator(dataset)

# Gets the dataset distribution
# years = [2018, 2023]
# university = ["unicamp", "usp"]
info = loader.get_info(year, university)
```

## How to cite