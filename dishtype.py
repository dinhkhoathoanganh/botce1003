import string
from collections import OrderedDict

type_options =['American', 'Italian', 'Asian', 'Mexican', 'French', 'Southwestern', 'Barbecue', 'Indian', 'Chinese', 'English', 'Mediterranean', 'Greek', 'Spanish', 'German', 'Thai', 'Moroccan', 'Irish', 'Japanese', 'Cuban', 'Hawaiin', 'Swedish', 'Hungarian', 'Portugese']
diet_options =['Pescetarian', 'Vegan', 'Vegetarian']

dish = OrderedDict(zip(string.ascii_lowercase, type_options))
diet = OrderedDict(zip(map(str, range(3 + 1)), diet_options))
# search_type = input("Choose your type: ")
# print(search_type)
# print(search_type in dish)

# print(search_type in diet) #######

# print(diet)
# print(dish)
