import logging
from collections import Counter, defaultdict
from typing import List
from datasets import load_dataset


class BluexLoader():
    def __init__(self):
        self.dataset = load_dataset("portuguese-benchmark-datasets/BLUEX")

    def get_all_questions(self):
        return self.dataset["questions"]
    
    def count_examples(self, feature: str, year: int = None, university: str = None) -> int:
        """
        Counts the number of examples that have the specified feature
        Args:
            feature (str): The feature to count
            year (int): The year of the questions
            university (str): The university of the questions
        Returns:
            int: The number of examples that have the specified feature
        """
        filtered_dataset = self.filtered_by(year=year, university=university, **{feature: feature})
        return len(filtered_dataset)
    
    def get_info(self, year: int = None, university: str = None) -> dict:
        """
        Gets information about the dataset such as the number of questions, number of questions with images, etc.
        Args:
            year (int): The year of the questions
            university (str): The university of the questions
        Returns:
            dict: A dictionary with the information
        """
        infos = defaultdict(dict)
        # Checks if the arguments are valid
        self.check_filter_args(None, year, university)
        # Features to count
        features_to_count = ["has_associated_images", "PRK", "TU", "IU", "MR", "ML", "BK"]
        filtered_dataset = self.filtered_by(year=year, university=university)

        infos["subjects"] = dict(Counter(subject for example in filtered_dataset for subject in example["subject"]))
        infos["total_questions"] = len(filtered_dataset)

        # Questions with len(subject) > 1 are multidisciplinary
        infos["multidisciplinary_questions"] = len([example for example in filtered_dataset if len(example["subject"]) > 1])
        for feature in features_to_count:
            infos[feature] = self.count_examples(feature, year, university)
        return dict(infos)

    @staticmethod
    def check_filter_args(subjects: List[str], year: int, university: str) -> None:
        """
        Checks if the arguments passed to the filter function are valid
        Args:
            subjects (List[str]): The subjects to filter
            year (int): The year of the questions
            university (str): The university of the questions
        """
        available_subjects = [
            "portuguese",
            "history",
            "mathematics",
            "english",
            "physics",
            "chemistry",
            "geography",
            "biology",
            "philosophy"
        ]
        if subjects:
            for subject in subjects:
                if subject not in available_subjects:
                    logging.warning(f" {subject} is not a valid subject. Available subjects are: {available_subjects}")
        if year and year not in range(2018, 2025):
            logging.warning(f" {year} is not a valid year. Available years are: {range(2018, 2024)}")
        if university and university.lower() not in ["unicamp", "usp"]:
            logging.warning(f" {university} is not a valid university. Available universities are: ['unicamp', 'usp']")

    def filtered_by(
        self,
        has_associated_images: bool = None,
        alternatives_type: str = None,
        subject: List[str] = None,
        PRK: bool = None,
        TU: bool = None,
        IU: bool = None,
        MR: bool = None,
        ML: bool = None,
        BK: bool = None,
        year: int = None,
        university: str = None,
        include_multidisciplinary: bool = True
    ) -> List[dict]:
        """
        Filters the dataset by the specified features
        Args:
            has_associated_images (bool): If the question has associated images
            alternatives_type (str): The type of the alternatives
            subject (List[str]): The subjects of the questions
            PRK (bool): If the question requires prior knowledge
            TU (bool): If the question requires text understanding
            IU (bool): If the question requires image understanding
            MR (bool): If the question requires mathematical reasoning
            ML (bool): If the question is multilingual
            BK (bool): If the question requires brazilian knowledge
            year (int): The year of the questions
            university (str): The university of the questions
            include_multidisciplinary (bool): If multidisciplinary questions should be included
        Returns:
            List[dict]: A list of questions that have the specified features
        """
        # Checks if the arguments are valid
        self.check_filter_args(subject, year, university)
        # Gets all the keys that were defined by the user
        keys = [k for k, v in locals().items() if v is not None and k not in ["self", "year", "university", "include_multidisciplinary"]]
        
        # Makes string arguments lowercase
        if university:
            university = university.lower()
        if subject:
            subject = [s.lower() for s in subject]

        # Filters the dataset
        filtered_dataset = []
        for question in self.dataset["questions"]:
            # Gets the university, year and question number
            question_university, question_year, _ = question["id"].split("_")
            question_university = question_university.lower()
            question_year = int(question_year)

            # Checks if the question has the specified university and year
            if (university and question_university != university) or (year and question_year != year):
                continue

            # Checks if the question is multidisciplinary
            if not include_multidisciplinary and len(question["subject"]) > 1:
                continue
            
            # Checks if the question has the specified subjects
            if subject and not any(s in question["subject"] for s in subject):
                continue

            # Checks if the question has the specified features
            if all(question[feature] for feature in keys):
                filtered_dataset.append(question)
                
        return filtered_dataset
    
    def get_bluex_generator(self, dataset: List[dict]):
        """
        Gets a generator that yields the questions in the format used by Bluex: (id, text, images, answer)
        Args:
            dataset (List[dict]): The dataset to get the generator from
        Returns:
            Generator: A generator that yields the questions
        """
        for question in dataset:
            # Builds the question text
            text = f"{question['question']}\n"
            text += "\n".join(question["alternatives"])
            yield (
                question["id"],
                text,
                question["associated_images"],
                question["answer"]
            )
        