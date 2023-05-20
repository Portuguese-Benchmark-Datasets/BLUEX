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
    "DS": bool,
    "TU": bool,
    "IU": bool,
    "MR": bool,
    "ML": bool,
    "BK": bool
}
```
Additionally, we modified the text of the questions to include a tag indicating the placement of images, such as [IMAGE 0], which corresponds to the first image in the associated_images list.

### Description of the data

Initially, the dataset could be downloaded automatically by following the steps below. However, due to the anonymous nature of the repository at that time, we provided a zip file containing the dataset for access. Once the paper is accepted, we will make the dataset available again for download.

### How to use

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
```

## Authors

* **Thiago Soares Laitz**
* **Thales Sales Almeida**
* **Giovana K. Bonás**
* **Rodrigo Nogueira**
