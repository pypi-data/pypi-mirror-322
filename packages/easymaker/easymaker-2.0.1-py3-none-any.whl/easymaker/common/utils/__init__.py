from easymaker.common.exceptions import EasyMakerError


def from_name_to_id(list: list, name: str, resource_name: str) -> str:
    for item in list:
        if item["name"] == name:
            return item["id"]

    raise EasyMakerError(f"Invalid {resource_name} name : {name}")


def snake_to_kebab(snake_str: str):
    return snake_str.replace("_", "-")


def snake_to_pascal(snake_str: str):
    # snake_sace -> SnakeCase
    return "".join(word.title() for word in snake_str.split("_"))


def pascal_to_snake(pascal_str: str):
    # SnakeCase -> snake_case
    return "".join(["_" + i.lower() if i.isupper() else i for i in pascal_str]).lstrip("_")
