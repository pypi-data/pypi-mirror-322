import httpx

class MealDB:

    def __init__(self, api_key):
      self.api_key = api_key
      self.base_url = f'https://www.themealdb.com/api/json/v1/{api_key}'

    def get_meal_by_name(self,name) -> list:  
        """
        Retrieves a list of meals by name from the MealDB API.

        Args:
            name (str): The name of the meal to search for. (e.g. Arrabiata, Potato Salad, Blini Pancakes).

        Returns:
            list: A list of meals matching the search query.

        Raises:
            httpx.HTTPError: Check httpx's documentation for all possible exceptions.

        """
        r = httpx.get(f'{self.base_url}/search.php?s={name}')
        data = r.json()
        meal = data['meals']
        return list(meal)
    
    def get_latest_meal(self) -> list:
        """
        Retrieves the latest meal data from the API.

        Returns:
            list: A list containing the latest meal data, or a message indicating that the user needs to subscribe to access the endpoint.

        Raises:
            httpx.HTTPError: Check httpx's documentation for all possible exceptions.
        """
        r = httpx.get(f'{self.base_url}/latest.php')
        data = r.json()
        meal = data['meals']
        if len(meal) == 3:
            return "You need to subscribe to The Meal DB API to access this endpoint"
        else:
            return list(meal)
           
    def meal_details_by_id(self,id) -> list:
        """
        Retrieves the details of a meal by its ID from the MealDB API.

        Args:
            id (int): The ID of the meal to retrieve. (e.g. 52772).

        Returns:
            list: A list containing the details of the meal.

        Raises:
            httpx.HTTPError: Check httpx's documentation for all possible exceptions.
        """
        r = httpx.get(f'{self.base_url}/lookup.php?i={id}')
        data = r.json()
        meal = data['meals']
        
        return list(meal)

    def single_random_meal(self) -> list:
        """
        Retrieves a single random meal from the MealDB API.

        Returns:
            list: A list containing the details of a random meal.

        Raises:
            httpx.HTTPError: Check httpx's documentation for all possible exceptions.

        """
        r = httpx.get(f'{self.base_url}/random.php')
        data = r.json()
        meal = data['meals']
        
        return list(meal)


    def list_all_meals(self,letter) -> list:
        """
        Retrieves a list of meals starting with a specific letter from the MealDB API.

        Args:
            letter (str): The letter to search for (e.g. 'a', 'b', etc.).

        Returns:
            list: A list of meals starting with the specified letter.

        Raises:
            httpx.HTTPError: Check httpx's documentation for all possible exceptions.
        """
        r = httpx.get(f'{self.base_url}/search.php?f={letter}')
        data = r.json()
        meals = data['meals']
        
        return list(meals)


    def list_meal_categories(self) -> list:
        """
        Retrieves a list of meal categories from the MealDB API.

        Returns:
            dict: A dictionary containing the list of meal categories.

        Raises:
            httpx.HTTPError: Check httpx's documentation for all possible exceptions.
        """
        r = httpx.get(f'{self.base_url}/categories.php')
        data = r.json()
        categories = data['categories']
        
        return list(categories)

    def list_all_categories(self) -> list:
        """
        Retrieves a list of all categories from the MealDB API.

        Returns:
            list: A list of dictionaries containing the categories.

        Raises:
            httpx.HTTPError: Check httpx's documentation for all possible exceptions.
        """
        r = httpx.get(f'{self.base_url}/categories.php')
        data = r.json()
        
        return list(data)

    def list_all_areas(self) -> list:
        """
        Retrieves a list of all areas from the MealDB API.

        Returns:
            list: A list of dictionaries containing the areas.

        Raises:
            httpx.HTTPError: Check httpx's documentation for all possible exceptions.
        """
        r = httpx.get(f'{self.base_url}/list.php?a=list')
        data = r.json()
        areas = data['meals']
        
        return list(areas)

    def list_all_ingredients(self) -> list:
        """
        Retrieves a list of all ingredients from the MealDB API.

        Returns:
            list: A list of dictionaries containing the ingredients.

        Raises:
            httpx.HTTPError: Check httpx's documentation for all possible exceptions.
        """
        r = httpx.get(f'{self.base_url}/list.php?i=list')
        data = r.json()
        ingredients = data['meals']
        
        return list(ingredients)

    def list_all(self) -> list:
        """
        Retrieves a list of all categories, areas, and ingredients from the MealDB API.

        Returns:
            list: A list of dictionaries containing the categories, areas, and ingredients.

        Raises:
            httpx.HTTPError: If any of the API requests fail.
        """
        r1 = httpx.get(f'{self.base_url}/list.php?c=list')
        data1 = r1.json()
        
        r2 = httpx.get(f'{self.base_url}/list.php?a=list')
        data2 = r2.json()

        r3 = httpx.get(f'{self.base_url}/list.php?i=list')
        data3 = r3.json()

        answers = [data1, data2, data3]

        return answers

    def filter_by_ingredient(self,ingredient) -> list:
        """
        Retrieves a list of meals that include a specific ingredient from the MealDB API.

        Args:
            ingredient (str): The ingredient to filter by (e.g. Chicken, Salmon, Beef).

        Returns:
            list: A list of dictionaries containing the meals that include the specified ingredient.

        Raises:
            httpx.HTTPError: Check httpx's documentation for all possible exceptions.
        """
        r = httpx.get(f'{self.base_url}/filter.php?i={ingredient}')
        data = r.json()
        meal = data['meals']
        
        return list(meal)
    
    def filter_by_category(self,category) -> list:
        """
        Retrieves a list of meals that belong to a specific category from the MealDB API.

        Args:
            category (str): The category to filter by. (e.g. Seafood)

        Returns:
            list: A list of dictionaries containing the meals that belong to the specified category.

        Raises:
            httpx.HTTPError: Check httpx's documentation for all possible exceptions.
        """
        r = httpx.get(f'{self.base_url}/filter.php?c={category}')
        data = r.json()
        meal = data['meals']
        
        return list(meal)

    def filter_by_area(self,area) -> list:
        """
        Retrieves a list of meals that originate from a specific area from the MealDB API.

        Args:
            area (str): The area to filter by (e.g. Canadian, Mexican).

        Returns:
            list: A list of dictionaries containing the meals that originate from the specified area.

        Raises:
            httpx.HTTPError: Check httpx's documentation for all possible exceptions.
        """
        r = httpx.get(f'{self.base_url}/filter.php?a={area}')
        data = r.json()
        meal = data['meals']
        
        return list(meal)
    
    def get_ingredient_image(self,ingredient) -> any:
        """
        Fetches an image of the specified ingredient from TheMealDB and saves it locally.

        Args:
            ingredient (str): The name of the ingredient for which the image is to be fetched.

        Returns:
            str: A message indicating the successful fetching and saving of the image.

        Raises:
            httpx.HTTPError: If the API request fails
        """
        r =  httpx.get(f'https://www.themealdb.com/images/ingredients/{ingredient}.png')
        image_data = r.content
        with open(f'{ingredient}.png', 'wb') as file:
            file.write(image_data)
    
        return "Fetched Image Successfully"
        
    def get_ingredient_image_small(self,ingredient) -> any:
        """
        Fetches an scaled down image of the specified ingredient from TheMealDB and saves it locally.

        Args:
            ingredient (str): The name of the ingredient for which the image is to be fetched.

        Returns:
            str: A message indicating the successful fetching and saving of the image.

        Raises:
            httpx.HTTPError: If the API request fails
        """
        r =  httpx.get( f'https://www.themealdb.com/images/ingredients/{ingredient}-Small.png')
        image_data = r.content
        with open(f'{ingredient}-small.png', 'wb') as file:
            file.write(image_data)
    
        return "Fetched Image Successfully"