# py-mealdb 

<p align="center" width="100%">
    <img width="33%" src="https://raw.githubusercontent.com/Sherwin-14/py-mealdb/refs/heads/main/burger.png" alt="Burger Icon" style="width:100px; height:100px;">
</p>

py-mealdb is a Python library that allows users to interact effortlessly with TheMealDB API, providing access to a vast collection of meal recipes, ingredients, and culinary inspiration from around the world.

## Installation

```py
pip install py-mealdb
```
## Quick Start

```py
from mealdb import MealDB

mb = MealDB(API_KEY)
meal = mb.get_meal_by_name('Potato Salad')

print(meal)
```

## Acknowledgment

I would like to extend our sincere gratitude to TheMealDB for providing their comprehensive and free API. Their extensive database of meal recipes, ingredients, and detailed culinary information has been invaluable in the development of py-mealdb. Without their robust and accessible API, this project would not have been possible.

Thank you, TheMealDB, for your dedication to sharing the love of cooking and helping food enthusiasts around the world discover new and exciting recipes!


