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

        def reset_tracking(self):
            self._is_querying = False
            self._found_items.clear()

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

            self.reset_tracking()
            return values_list

        def first(self) -> T | None:
            if not self._is_querying and len(self._found_items) == 0:
                result = self._tracked_items[0] if self._tracked_items else None
                return result

            result = self._found_items[0] if self._found_items else None
            self.reset_tracking()
            return result

        def to_list(self) -> list[T] | None:
            if not self._is_querying and len(self._found_items) == 0:
                return self._tracked_items

            result = self._found_items.copy()
            self.reset_tracking()
            return result

        def count(self) -> int:
            try:
                if not self._is_querying and len(self._found_items) == 0:
                    result = len(self._tracked_items)
                    return result

                result = len(self._found_items.copy())
                return result
            finally:
                self.reset_tracking()

        def update(self, field, value) -> list[T]:
            updated_items: list[T] = []
            for item in self._found_items:
                index = self._tracked_items.index(item)
                setattr(item, field, value)
                self._tracked_items[index] = item
                updated_items.append(item)

            self.reset_tracking()
            return updated_items

        def delete(self, item: T | None) -> list[T] | T:
            try:
                if item is not None:
                    index = self._tracked_items.index(item)
                    removed = self._tracked_items.pop(index)
                    return removed

                removed_items: list[T] = []
                for items in self._found_items:
                    index = self._tracked_items.index(items)
                    removed = self._tracked_items.pop(index)
                    removed_items.append(removed)

                return removed_items
            finally:
                self.reset_tracking()

        def save_changes(self):
            self.reset_tracking()
            with open(self.file_path, "w", encoding="utf-8") as f:
                data = [asdict(item) for item in self._tracked_items]
                json.dump(data, f, indent=4)
