# TChoice

Lightweight implementation of Django-like `TextChoices` and `IntegerChoices` 
for Python applications.

## Problem Statement

When working with FastAPI or other frameworks, it's often useful to have 
enumerations with labels for better readability and usability in models, 
forms, and APIs. While Django provides `TextChoices` and `IntegerChoices` 
for this purpose, they are tightly coupled to the Django framework. 
`tchoice` offers a standalone solution, allowing you to use similar 
functionality without requiring Django.

## Installation

Install the package via pip:

```bash
pip install tchoice
```

## How to Use

### Defining Choices
You can define your choices using `TextChoices` or `IntegerChoices`:

```python
from tchoice import TextChoices, IntegerChoices

class ColorChoices(TextChoices):
    RED = "red", "Red Color"
    GREEN = "green", "Green Color"
    BLUE = "blue", "Blue Color"

class SizeChoices(IntegerChoices):
    SMALL = 1, "Small Size"
    MEDIUM = 2, "Medium Size"
    LARGE = 3, "Large Size"
```

### Accessing Labels and Values

```python
print(ColorChoices.RED)          # Output: red
print(ColorChoices.RED.label)    # Output: Red Color

print(SizeChoices.SMALL)         # Output: 1
print(SizeChoices.SMALL.label)   # Output: Small Size
```

### Using Choices in Models

For FastAPI and Pydantic:

```python
from pydantic import BaseModel
from tchoice import TextChoices

class ColorChoices(TextChoices):
    RED = "red", "Red Color"
    GREEN = "green", "Green Color"
    BLUE = "blue", "Blue Color"

class Item(BaseModel):
    name: str
    color: ColorChoices

# Example usage
item = Item(name="Example Item", color=ColorChoices.RED)
print(item.color)           # Output: red
print(item.color.label)     # Output: Red Color
```

---

## License

This project is licensed under the terms of the [MIT license](https://github.com/ispaneli/tchoice/blob/master/LICENSE).

