from collections import namedtuple
from typing import List

Name = namedtuple("Name", "given_name, middle_name, surname, suffix")


class NameParser:
    def __init__(self, lang: str = "en"):
        """
        Initialize the NameParser with a specific language.
        """
        self.lang = lang
        self.suffixes = self._get_suffixes()
        self.parsers = {
            "en": self._parse_english_name,
            "es": self._parse_hispanic_name,
            # Add other language-specific parsers here
        }

    def parse_name(self, full_name: str) -> Name:
        """
        Parses a full name into its components based on the language.
        """
        if self.lang in self.parsers:
            return self.parsers[self.lang](full_name)
        else:
            raise ValueError(f"Unsupported language: {self.lang}")
        
    def sort_names(self, names: list, sort_key: str = "surname") -> list:       
        if sort_key == "given_name":
            return sorted(names, key= lambda x: self.parse_name(x).given_name)
        elif sort_key == "middle_name":
            return sorted(names, key= lambda x: self.parse_name(x).middle_name)   
        else:
            return sorted(names, key= lambda x: (self.parse_name(x).surname, self.parse_name(x).given_name))   

    def _get_suffixes(self) -> List[str]:
        """
        Returns a list of suffixes based on language.
        """
        if self.lang == "en":
            return [
                "Jr", "Jr.", "Sr", "Sr.", "I", "II", "III", "IV", "V",
                "Esq", "Esq.", "MD", "M.D.", "PhD", "Ph.D."
            ]
        elif self.lang == "es":
            return []  # Suffixes are rare in Hispanic names
        # Add suffixes for other languages if needed
        return []

    # def _parse_english_name(self, name_list: List[str]) -> Name:
    def _parse_english_name(self, full_name: str) -> Name:

        """
        Parses an English name into components.
        """
        name_list = full_name.split()

        if name_list[-1] in self.suffixes:
            if len(name_list) == 2:
                given_name, middle_name, surname, suffix = "", "", name_list[0], name_list[-1]
            elif len(name_list) == 3:
                given_name, middle_name, surname, suffix = name_list[0], "", name_list[1], name_list[-1]
            else:
                given_name, middle_name, surname, suffix = (
                    name_list[0],
                    " ".join(name_list[1:-2]),
                    name_list[-2],
                    name_list[-1],
                )
        else:
            if len(name_list) == 1:
                given_name, middle_name, surname, suffix = "", "", name_list[0], ""
            elif len(name_list) == 2:
                given_name, middle_name, surname, suffix = name_list[0], "", name_list[1], ""
            else:
                given_name, middle_name, surname, suffix = (
                    name_list[0],
                    " ".join(name_list[1:-1]),
                    name_list[-1],
                    "",
                )

        return Name(given_name, middle_name, surname.rstrip(","), suffix)

    def _parse_hispanic_name(self, full_name: str) -> Name:
        """
        Parses a Hispanic name into components.
        """
        name_list = full_name.split()

        if len(name_list) < 2:
            return Name(given_name=name_list[0], middle_name="", surname="", suffix="", sort_name=name_list[0])

        # Hispanic naming convention: [given_name] [middle_name] [father_surname] [mother_surname]
        given_name = name_list[0]
        if len(name_list) == 2:
            middle_name = ""
            surname = name_list[1]  # Only one surname
            sort_name = surname
        else:
            middle_name = name_list[1]
            surname = " ".join(name_list[2:])  # Concatenate father_surname and mother_surname
            sort_name = name_list[2]  # Sorting is on the father's surname

        return Name(given_name, middle_name, surname, suffix="", sort_name=sort_name)


