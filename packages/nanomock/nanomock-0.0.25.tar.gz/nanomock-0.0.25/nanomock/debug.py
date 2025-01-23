from nanomock_manager import NanoLocalManager
from modules.nl_rpc import NanoRpc
import asyncio


# # Setup code here
# manager = NanoLocalManager("unit_tests/configs", "unittest")
# nano_rpc = NanoRpc("http://127.0.0.1:45900")


async def main():

    manager = NanoLocalManager("unit_tests/configs", "unittest")
    nano_rpc = NanoRpc("http://127.0.0.1:45900")
    await manager.execute_command("down")
    await manager.execute_command("create")
    await manager.execute_command("start")
    log = await manager.init_nodes()
    await manager.execute_command("destroy")


asyncio.run(main())


# from nanomock.modules.nl_parse_config import ConfigParser
# import platform
# from nanomock_manager import NanoLocalManager


# os_name = platform.system()


# def _load_modify_conf_edit(nested_path, nested_value):
#     conf_dir = "unit_tests/configs/mock_nl_config"
#     conf_name = "conf_edit_config.toml"

#     config_parser = ConfigParser(conf_dir, conf_name)
#     modified_config = config_parser.modify_nanolocal_config(nested_path,
#                                                             nested_value,
#                                                             save=False)
#     conf_file = config_parser.conf_rw.read_toml(f"{conf_dir}/{conf_name}")

#     return conf_file, modified_config.data


# manager = NanoLocalManager(
#     "unit_tests/configs/mock_nl_config",
#     "unittest",
#     config_file="enable_voting_config.toml")

# nested_path = "nanolooker_enable"
# nested_value = None

# loaded_config, modified_config = _load_modify_conf_edit(
#     nested_path, nested_value)

# # Add the new key-value pair to each node in the loaded_config
# loaded_config.pop(nested_path)

# assert loaded_config == modified_config
