# JSONContext
Uma framework ORM em Python para arquivos JSON.

## Setup
```python
from JSONContext import JsonContext

# defina o seu modelo
@dataclass
class User:
    name: str
    password: str

# crie uma classe herdando de JsonContext
class AppContext(JsonContext):
    def __init__(self) -> None:
        super().__init__()

        # configure o caminho do arquivo JSON
        users_json = "users.json"

        # crie um objeto JsonSet com o modelo e o caminho JSON
        # este objeto terá a referência das entidades 'User' carregadas do JSON
        self.users = self.JsonSet(model_class=User, json_path=users_json)

# exemplo de uma query where
context = AppContext()
result = context.users.where(lambda u: u.name == "John").to_list()
```

## Adicionando
Crie um objeto e o adicione para a lista de entidades rastreadas com `.add()`

```python
user = User()
context.users.add(user)
context.users.save_changes()
```

## Deletando
Existem dois modos de deletar uma entidade com `.delete()`

1. Usando a referência da própria entidade:
```python
user = context.users.first()

deleted_user = context.users.delete(user)

context.users.save_changes()
```
2. Filtrando:
```python
deleted_user = context.users.where(lambda u: u.name == "John Marston").delete()

context.users.save_changes()
```
Ambos os métodos retornam o objeto deletado.

## Filtrando
### Onde (Where):
O método `.where()` recebe uma função `lambda` para filtrar a lista de entidades.

```python
# usuário chamado 'John Marston'
user = context.users.where(lambda u: u.name == "John Marston").first()

# todos usuários com 22 anos
users = context.users.where(lambda u: u.age == 22).to_list()
```

### Ordernando (Order By):
Os métodos `.order_by()` e `.order_by_descending()` recebem o nome do campo da entidade como uma `string` para ordenar os itens.

```python
# Ordenando por nome
loaded_users = [User(name="John"), User(name="Lucia"), User(name="Albert")]

sorted_users = context.users.order_by('name').to_list()

print(sorted_users)
# Resultado: [User(name="Albert"), User(name="John"), User(name="Lucia")]

reverse_sorted_users = context.users.order_by_descending('name').to_list()

print(reverse_sorted_users)
# Resultado: [User(name="Lucia"), User(name="John"), User(name="Albert")]
```

## Salvando e atualizando o JSON
Para persistir as modificações, chame `.save_changes()` no `JsonSet` relevante.

```python
context.users.add(new_user)
context.users.save_changes()
```

## To do
- Métodos update
