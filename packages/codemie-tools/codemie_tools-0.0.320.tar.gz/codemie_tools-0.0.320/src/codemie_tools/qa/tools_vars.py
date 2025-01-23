from codemie_tools.base.models import ToolMetadata

ZEPHYR_TOOL = ToolMetadata(
    name="ZephyrCloud",
    description=
    """
    Zephyr Tool that provides access to the zephyr-python-api package, enabling interaction with Zephyr test cases, 
    cycles or executions etc.
    You mist provide the following args: entity_str, method_str and body.
    1. 'entity_str': ZephyrScale entity requested by user. It must be accessible from ZephyrScale().api
    2. 'method_str': Zephyr method that is accessible from that entity. E.g. method 'get_test_cases' is accessible from ZephyrScale().api.test_cases.
        It can be equal to 'dir' so that you can list all available methods in requested entity.
    3. 'body': (Optional) Valid JSON object with parameters that must be passed to method.
    If some required information is not provided by user, try find by querying API, if not found ask user.
    If method you requested is not exists, try to execute tool with method 'dir' to get list of available methods.
    """.strip(),
    label="Zephyr Cloud",
    user_description="""
    Provides access to the zephyr-python-api package, enabling interaction with Zephyr test cases, cycles or executions.
    Before using it, it is necessary to add a new integration for the tool by providing:
    1. Alias (A friendly name for the Zephyr Cloud integration)
    2. Url (base url of the Zephyr Scale Cloud)
    3. Token (API access token)
    Usage Note:
    Use this tool when you need to manage Zephyr test cases, cycles or executions.
    """.strip()
)
