import base64
from typing import Any, List, Optional

import easymaker
from easymaker.api.request_body import PipelineUploadBody
from easymaker.common.base_model.easymaker_base_model import EasyMakerBaseModel


class Pipeline(EasyMakerBaseModel):
    pipeline_id: Optional[str] = None
    pipeline_name: Optional[str] = None
    pipeline_parameter_spec_list: Optional[List[Any]] = None
    pipeline_status_code: Optional[str] = None
    pipeline_spec_manifest: Optional[Any] = None

    def _fetch(self):
        response = easymaker.easymaker_config.api_sender.get_pipeline_by_id(self.pipeline_id)
        super().__init__(**response)

    def upload(
        self,
        pipeline_name,
        pipeline_spec_manifest_path,
        description,
        tag_list,
        wait=True,
    ):

        with open(pipeline_spec_manifest_path, "rb") as file:
            pipeline_spec_manifest = file.read()
        base64_pipeline_spec_manifest = base64.b64encode(pipeline_spec_manifest).decode("utf-8")

        response = easymaker.easymaker_config.api_sender.upload_pipeline(
            PipelineUploadBody(
                pipeline_name=pipeline_name,
                base64_pipeline_spec_manifest=base64_pipeline_spec_manifest,
                description=description,
                tag_list=tag_list,
            )
        )
        super().__init__(**response)
        print(f"[AI EasyMaker] Pipeline upload request complete. Pipeline ID : {self.pipeline_id}")
        if wait:
            self.wait(action="upload")

        return self

    def delete(self):
        if self.pipeline_id:
            easymaker.easymaker_config.api_sender.delete_pipeline_by_id(self.pipeline_id)
            super().__init__()
            print(f"[AI EasyMaker] Pipeline delete request complete. Pipeline ID : {self.pipeline_id}")
        else:
            print("[AI EasyMaker] Failed to delete pipeline. The pipeline_id is empty.")


def delete(pipeline_id: str):
    if pipeline_id:
        easymaker.easymaker_config.api_sender.delete_pipeline_by_id(pipeline_id)
        print(f"[AI EasyMaker] Pipeline delete request complete. Pipeline ID : {pipeline_id}")
    else:
        print("[AI EasyMaker] Failed to delete pipeline. The pipeline_id is empty.")
