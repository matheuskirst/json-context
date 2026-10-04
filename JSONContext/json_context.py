import json
from dataclasses import asdict
from typing import Any

from .dataclass_helpers import DataclassInstance, fromdict

class JsonContext:
    """Manage and query json files.

    Setup::

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
    """

    class JsonSet[T: DataclassInstance]:
        def __init__(self, model_class: type[T], json_path) -> None:
            self.model_class = model_class
            self.file_path = json_path

            self._tracked_items: list[T] = self.__load() or []
            self._is_querying: bool = False
            self._found_items: list[Any] = []

        def __load(self) -> list[T]:
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return [fromdict(item, self.model_class) for item in data]
            except:
                return []

        def add(self, item: T):
            self._tracked_items.append(item)

        def where(self, function):
            self._is_querying = True
            self._found_items.clear()
            self._found_items = list(filter(function, self._tracked_items))
            return self

        def limit(self, n):
            if not self._is_querying and len(self._found_items) == 0:
                self._found_items = self._tracked_items.copy()
                
            self._is_querying = True
            self._found_items = self._found_items[0:n]
            return self

        def order_by(self, field):
            if not self._is_querying and len(self._found_items) == 0:
                self._found_items = self._tracked_items.copy()

            self._is_querying = True
            self._found_items = sorted(self._found_items, key=lambda v: getattr(v, field))
            return self

        def order_by_descending(self, field):
            if not self._is_querying and len(self._found_items) == 0:
                self._found_items = self._tracked_items.copy()

            self._is_querying = True
            self._found_items = sorted(self._found_items, key=lambda v: getattr(v, field), reverse=True)
            return self
    
        def select(self, *fields) -> Any | list[Any]:
            values_list: list[Any] = []

            if not self._is_querying and len(self._found_items) == 0:
                self._found_items = self._tracked_items.copy()

            self._is_querying = True
            for item in self._found_items:
                for field in fields:
                    value = getattr(item, field)
                    values_list.append(value)

            try:
                return values_list
            finally:
                self._is_querying = False
                self._found_items.clear()

        def first(self) -> T | None:
            try:
                if not self._is_querying and len(self._found_items) == 0:
                    return self._tracked_items[0] if self._tracked_items else None

                return self._found_items[0] if self._found_items else None
            finally:
                self._is_querying = False
                self._found_items.clear()

        def to_list(self) -> list[T] | None:
            try:
                if not self._is_querying and len(self._found_items) == 0:
                    return self._tracked_items
        
                return self._found_items.copy()
            finally:
                self._is_querying = False
                self._found_items.clear()

        def count(self) -> int:
            try:
                if not self._is_querying and len(self._found_items) == 0:
                    return len(self._tracked_items)
        
                return len(self._found_items.copy())
            finally:
                self._is_querying = False
                self._found_items.clear()

        def update(self, field, value) -> list[T]:
            updated_items: list[T] = []
            for item in self._found_items:
                index = self._tracked_items.index(item)
                setattr(item, field, value)
                self._tracked_items[index] = item
                updated_items.append(item)
            try:
                return updated_items
            finally:
                self._is_querying = False
                self._found_items.clear()

        def delete(self) -> list[T]:
            removed_items: list[T] = []
            for item in self._found_items:
                index = self._tracked_items.index(item)
                removed = self._tracked_items.pop(index)
                removed_items.append(removed)
            try:
                return removed_items
            finally:
                self._is_querying = False
                self._found_items.clear()

        def save_changes(self):
            with open(self.file_path, "w", encoding="utf-8") as f:
                data = [asdict(item) for item in self._tracked_items]
                json.dump(data, f, indent=4)
