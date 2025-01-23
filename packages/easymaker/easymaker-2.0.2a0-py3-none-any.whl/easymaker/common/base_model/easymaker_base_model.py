import json
import time
from datetime import timedelta
from typing import Any, List, Optional, Union, get_args, get_origin

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from easymaker.common import constants, exceptions, utils

complete_status = [
    "COMPLETE",
    "ACTIVE",
    "ENABLED",
]

fail_status = [
    "FAIL",
    "STOP",
]


class EasyMakerBaseModel(BaseModel):
    # camelCase의 API 응답을 snake_case 형태의 필드값에 셋팅할 수 있도록 camel 형태의 alias 일괄 추가 및 snake_case 입력도 처리하도록 설정
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        protected_namespaces=(),  # model_ 로 시작하는 필드명은 Pydantic에서 예약된 이름이라 충돌 가능성이 있어 발생하는 경고 끄는 옵션 (model_name은 충돌나는 이름)
    )

    description: Optional[str] = None
    tag_list: Optional[List[Any]] = None
    app_key: Optional[str] = None
    created_datetime: Optional[str] = None

    def __init__(self, *args, **kwargs):
        fields = self.__class__.__annotations__
        # 모든 Optional 필드에 기본값으로 None 설정
        default_data = {field: None for field in fields if get_origin(fields[field]) is Union and type(None) in get_args(fields[field])}
        default_data.update(kwargs)

        # 키워드로 입력된 값이 없고, 아규먼트로 입력된 값이 있을 경우
        # 아규먼트로 입력된 값을 ID로 사용
        if not default_data.get(self.id_field) and len(args) == 1:
            default_data[self.id_field] = args[0]

        super().__init__(**default_data)
        if self.id and not self.status:
            self._fetch()

    def __setattr__(self, key: str, value: Any) -> None:
        read_only_fields = set(attribute_name for attribute_name, model_field in self.model_fields.items() if model_field.repr is False)
        if key in read_only_fields:
            return
        super().__setattr__(key, value)

    def model_dump(self, **kwargs):
        return super().model_dump(by_alias=True, **kwargs)

    def print_info(self):
        print(json.dumps(self.model_dump(), indent=4, ensure_ascii=False))

    def _fetch(self):
        raise NotImplementedError

    @property
    def id_field(self) -> str:
        name = utils.pascal_to_snake(self.__class__.__name__)
        return f"{name}_id"

    @property
    def status_field(self) -> str:
        name = utils.pascal_to_snake(self.__class__.__name__)
        return f"{name}_status_code"

    @property
    def id(self) -> str | None:
        return getattr(self, self.id_field, None)

    @property
    def status(self) -> str | None:
        return getattr(self, self.status_field, None)

    def wait(self, action: str = "create", wait_interval_seconds: int = constants.EASYMAKER_API_WAIT_INTERVAL_SECONDS):
        class_name = self.__class__.__name__
        waiting_time_seconds = 0
        while self.status not in complete_status:
            print(f"[AI EasyMaker] {class_name} {action} status: {self.status} ({timedelta(seconds=waiting_time_seconds)}) Please wait...")
            time.sleep(wait_interval_seconds)
            waiting_time_seconds += wait_interval_seconds
            self._fetch()
            if any(fail in self.status for fail in fail_status):
                raise exceptions.EasyMakerError(f"{class_name} {action} failed with status: {self.status}.")
        print(f"[AI EasyMaker] {class_name} {action} complete. {self.id_field}: {self.id}")
