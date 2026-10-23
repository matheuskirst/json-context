# JSONContext
A simple Object-Relational Mapping framework for JSON files in Python

## Setup
```python
from JSONContext import JsonContext

# define your model
@dataclass
class User:
    name: str
    password: str

# inherit from JsonContext
class AppContext(JsonContext):
    def __init__(self) -> None:
        super().__init__()

        # set or inject your json path
        users_json = "users.json"

        # define a JsonSet, passing the respective model type and json path to it
        self.users = self.JsonSet(model_class=User, json_path=users_json)

# where query
context = AppContext()
result = context.users.where(lambda u: u.name == "John").to_list()
```

## Creating
Create an object and add it to the list of tracked items with `.add()`
```python
user = User()
context.users.add(user)
context.users.save_changes()
```

## Deleting
There are two ways to delete items with `.delete()`  
1. By using the item itself:
```python
user = context.users.first()

deleted_user = context.users.delete(user)

context.users.save_changes()
```
2. By filtering:
```python
# removing all users named 'John'
deleted_users = context.users.where(lambda u: u.name == "John").delete()

context.users.save_changes()
```
Both methods returns the deleted objects.

## Filtering
### Where:
The `.where()` method receives a `lambda` function to filter the loaded items list
```python
# get first user named John
user = context.users.where(lambda u: u.name == "John").first()

# get all users of age 22
users = context.users.where(lambda u: u.age == 22).to_list()
```

### Order By:
The `.order_by()` and `.order_by_descending()` methods receives the object's field name as a `string` to sort the items
```python
# Sorting by name
loaded_users = [User(name="John"), User(name="Lucia"), User(name="Albert")]

sorted_users = context.users.order_by('name').to_list()
print(sorted_users)
# [User(name="Albert"), User(name="John"), User(name="Lucia")]

reverse_sorted_users = context.users.order_by_descending('name').to_list()
print(reverse_sorted_users)
# [User(name="Lucia"), User(name="John"), User(name="Albert")]
```

## Saving and updating the JSON
To persist the modifications, use `.save_changes()` after CRUD methods
```python
context.users.add(some_object)
context.users.save_changes()
```
