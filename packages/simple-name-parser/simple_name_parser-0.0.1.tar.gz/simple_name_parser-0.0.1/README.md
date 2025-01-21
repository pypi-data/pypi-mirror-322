# Name Parser

This package is really a single class written as yet another solution to an already-solved problem. While writing a Django app to create estate planning documents for the law firm at which I work, I had to decide how to handle client names. While the documents use names in a natural order, referring to clients in typical given name, middle name, last name order, conventional indexing and sorting of names (in English usage, anyway) for administrative purposes necessitates a last name, first name sorting. The obvious and perfectly serviceable solution is to collect the parts of clients' names in discrete fields: a given name (or first name) field, middle name field, last name field. The parts can be easily concantenated to use names in a natural order but can just as easily be sorted by last name (or any other name part). This is the approach taken by a software suite we use in our real estate practice area and it works great. However, I find it much easier simply to enter names in a natural order. Rather than type "John" in a first name field, tab to a middle name field and type "Mark", tab to a last name field and type "Smith", and finally tab to a suffix field and type "Jr.", I'd much rather just type John Mark Smith, Jr. and get on with it. This class allows me to do just that and yet sort the names any way I'd like.  

## Installation  
```python
>>> python -m pip install simple_name_parser
```  

## Usage
The package contains a single class, `NameParser(self, lang="es")`. Typical usage begins by creating an instance of NameParser. There are actually two parsers available, one for English language names and another for Spanish language names (which are typically sorted by the paternal surname which appears next to last in the natural written order). The English parser is set as the default. For the Spanish parser, set `lang` to "es".
```python
>>> from simple_name_parser import NameParser 

>>> english_parser = NameParser(lang="en")
>>> spanish_parser = NameParser(lang="es")
```

The NameParser class uses 2 methods:  

`parse_name(name: str)` takes a string containing a name in natural order as an argument and returns a named tuple.
```python
>>> english_name = "John Mark Smith, Jr."
>>> english_parser.parse_name(english_name)
Name(given_name='John', middle_name='Mark', surname='Smith', suffix='Jr.')
>>> spanish_name = "Carlos Alberto García López"
>>> spanish_parser.parse_name(spanish_name)
Name(given_name='Carlos', middle_name='Alberto', surname='García López', suffix='')
```  

`sort_names(names: list, sort_key: str="surname")` takes two arguments: a list of strings containing names and a string containing a sort_key of "given_name", "middle_name", or "surname", with "surname" being the default.  
```python
>>> english_names = ["John Mark Smith", "Alfred E. Neumann", "Charles Emerson Winchester, III", "Florence Nightingale"]
>>> english_parser.sort_names(english_names, "surname")
['Alfred E. Neumann', 'Florence Nightingale', 'John Mark Smith', 'Charles Emerson Winchester, III']
>>> english_parser.sort_names(english_names, "given_name")
['Alfred E. Neumann', 'Charles Emerson Winchester, III', 'Florence Nightingale', 'John Mark Smith']
>>> spanish_names = ["Carlos Alberto García López", "María Elena Fernández Pérez", "Javier Eduardo Martínez Sánchez", "Sofía Isabel Rodríguez Díaz"]
>>> spanish_parser.sort_names(spanish_names, "surname")
['María Elena Fernández Pérez', 'Carlos Alberto García López', 'Javier Eduardo Martínez Sánchez', 'Sofía Isabel Rodríguez Díaz']

```

Honestly, the sort_names() method is really kind of superfluous as it's just a simple lambda sort method that's easily reproducible with just a little more code than it takes to call the method. I added it just to make my life a little easier.

This package is very, very beta. Neither parser (especially the Spanish parser) has been extensively tested, particularly in edge cases. At this point, it serves my (limited) purpose. More refinements to come ...