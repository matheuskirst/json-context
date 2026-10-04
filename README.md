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

        # set your json path
        users_json = "users.json"

        # define a set and pass the model type and the json path to it
        self.users = self.JsonSet(model_class=User, json_path=users_json)

# query example
context = AppContext()
result = context.users.where(lambda u: u.name == "John").to_list()
```
