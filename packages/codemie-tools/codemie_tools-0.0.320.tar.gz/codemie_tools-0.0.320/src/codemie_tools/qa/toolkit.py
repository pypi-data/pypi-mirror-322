from typing import Optional, List, Tuple, Dict, Any

from codemie_tools.base.base_toolkit import BaseToolkit
from codemie_tools.base.models import ToolKit, ToolSet, Tool
from codemie_tools.qa.tools_vars import ZEPHYR_TOOL
from codemie_tools.qa.zephyr.generic_tool import ZephyrConfig, ZephyrGenericTool
from langchain_core.tools import BaseTool

# Entity and method that is used for integration healthcheck
ZEPHYR_HEALTHCHECK_ENTITY = "healthcheck"
ZEPHYR_HEALTHCHECK_METHOD = "get_health"

class QualityAssuranceToolkitUI(ToolKit):
    toolkit: ToolSet = ToolSet.QUALITY_ASSURANCE
    tools: List[Tool] = [
        Tool.from_metadata(ZEPHYR_TOOL, settings_config=True),
    ]
    label: str = ToolSet.QUALITY_ASSURANCE.value


class QualityAssuranceToolkit(BaseToolkit):
    zephyr_config: Optional[ZephyrConfig] = None

    @classmethod
    def get_tools_ui_info(cls):
        return QualityAssuranceToolkitUI().model_dump()

    def get_tools(self, **kwargs) -> List[BaseTool]:
        tools = [
            ZephyrGenericTool(zephyr_config=self.zephyr_config),
        ]
        return tools

    @classmethod
    def get_toolkit(cls, configs: Dict[str, Any] = None):
        zephyr_config = ZephyrConfig(**configs["zephyr"] if "zephyr" in configs else None)
        return cls(zephyr_config=zephyr_config)

    @classmethod
    def zephyr_integration_healthcheck(cls, zephyr_config: Dict[str, Any] = None) -> Tuple[bool, str]:
        try:
            tool = ZephyrGenericTool(zephyr_config=ZephyrConfig(**zephyr_config))
            tool.execute(entity_str=ZEPHYR_HEALTHCHECK_ENTITY, method_str=ZEPHYR_HEALTHCHECK_METHOD)
        except Exception as e:
            return False, str(e)

        return True, ""
