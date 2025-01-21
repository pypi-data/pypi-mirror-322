from abc import ABC, abstractmethod
from pathlib import Path
import re
import json
import yangson_inventory_builder.inventory_classes as ic
import uuid
import logging
logger = logging.getLogger("yang_parser_app")


class YangsonInventory(ABC):
    """
    JSON file constructor, formatted according to Yangson library requirements
    """

    @abstractmethod
    def create_inventory_file(self) -> None:
        """
        Create inventory and store it on a disk
        """
        pass


class JuniperYangsonInventory(YangsonInventory):

    def create_inventory_file(self) -> None:
        pass


class NokiaYangsonInventory(YangsonInventory):
    """
    Build Yangson JSON library file for Nokia YANG models
    """

    def __init__(self, inventory_request: ic.YangsonInventoryRequest):
        self.yang_directory: Path = inventory_request.yang_directory
        self.root_yang_file: Path = inventory_request.root_config_module
        self.target_inventory_file_name: Path = inventory_request.target_inventory_file_name
        self.yang_sub_model_collection: set[ic.YangModuleInventory] = set()
        self.yang_module_hashmap: dict[str, ic.YangModuleInventory] = dict()

    def get_yangson_inventory_file(self) -> None:
        pass

    def create_inventory_file(self) -> None:
        """
        Create Yangson style inventory file

        Pipeline:
        1. Walk over DIR and collect all modules and submodules
        2. Start from root module recursively collect all imported and included modules to the Root module
        3. Create inventory file
        """

        if self.target_inventory_file_name.is_file():
            logger.info(f'Yangson inventory file is already created: "{str(self.target_inventory_file_name)}"')
            return

        self.collect_modules()
        self.collect_root_module_inventory()

        inventory_dict: dict = {"ietf-yang-library:modules-state": {
            "module-set-id": str(uuid.uuid4()),
            "module": [module.as_module() for module in self.yang_module_hashmap.values()
                       if (module.is_part_of_root_module and module.module_type == ic.ModuleType.MODULE.value)],
        }}
        with self.target_inventory_file_name.open("w") as target_file:
            json.dump(inventory_dict, target_file, indent=4)
        logger.info(f'Inventory file for the Yangson is created: "{str(self.target_inventory_file_name)}"')
        return

    def get_absolute_file_name(self, file_name: str) -> Path:
        path_file_name: Path = self.yang_directory / Path(file_name)
        if not path_file_name.is_file():
            raise FileNotFoundError(f'File not found: "{path_file_name}", please check file format and directory')
        return path_file_name.absolute()

    def collect_modules(self) -> None:
        """
        Iterate over files in a YANG model directory - collect inventory data into self.yang_module_hashmap database
        """
        for yang_module in self.yang_directory.glob("*.yang"):
            if not yang_module.is_file():
                continue
            yang_module_file_name: str = str(yang_module.absolute())
            with yang_module.open() as f_name:
                yang_module_txt: str = f_name.read()

            self.yang_module_hashmap[yang_module_file_name] = ic.YangModuleInventory(
                module_type=self.get_module_type(yang_module_txt),
                file_name=yang_module_file_name,
                name=yang_module.name.replace(".yang", ""),
                revision=self.get_module_revision_date(yang_module_txt, yang_module_file_name),
                namespace=self.get_module_namespace(yang_module_txt),
                included_modules=self.get_module_include_statements(yang_module_txt),
                imported_modules=self.get_module_import_statements(yang_module_txt)
            )
        return

    def collect_root_module_inventory(self) -> None:
        """
        Starting from the root configuration module, recursively find imported modules and submodules
        Updates existing modules database - self.yang_module_hashmap
        """
        processed_modules: set[ic.YangModuleInventory] = set()
        modules_stack: list[str] = [str(self.root_yang_file)]

        while len(modules_stack) > 0:
            module_name: str = modules_stack.pop()
            module: ic.YangModuleInventory = self.yang_module_hashmap[module_name]
            processed_modules.add(module)

            module.is_part_of_root_module = True
            module.conformance_type = "implement" if module.file_name == str(self.root_yang_file) else "import"
            module.submodule = [self.yang_module_hashmap[sub_m].as_submodule() for sub_m in module.included_modules]
            self.yang_module_hashmap[module_name] = module

            for imp_module in module.imported_modules + module.included_modules:
                if self.yang_module_hashmap[imp_module] not in processed_modules:
                    modules_stack.append(imp_module)
        return

    @staticmethod
    def get_module_type(yang_file: str) -> str:
        """
        Get type of module: MODULE or SUBMODULE
        :param yang_file: module txt file
        :return: string ModuleType
        """
        if yang_file.startswith("submodule"):
            return ic.ModuleType.SUBMODULE.value
        else:
            return ic.ModuleType.MODULE.value

    def get_module_include_statements(self, yang_file: str) -> list[str]:
        """
        Get list of submodules included in the given module
        Nokia uses in their YANG modules:
            include <submodule name>;
        :param yang_file: module txt file
        :return : List of included submodules
        """
        submodule_list: list[str] = re.findall(r"^\s+include\s+(\S+);", yang_file, re.MULTILINE)
        return [str(self.get_absolute_file_name(submodule_file + ".yang")) for submodule_file in submodule_list]

    def get_module_import_statements(self, yang_file: str) -> list[str]:
        """
        Get list of modules imported in the given module
        Nokia uses in their YANG modules:
            import <module name> { }
        :param yang_file: module txt file
        :return : List of imported modules
        """
        module_list: list[str] = re.findall(r"^\s+import\s+(\S+)\s+\{", yang_file, re.MULTILINE)
        return [str(self.get_absolute_file_name(module_file + ".yang")) for module_file in module_list]

    @staticmethod
    def get_module_revision_date(yang_file: str, yang_file_name: str) -> str:
        """
        Get revision date of the YANG module. If multiple revisions in the module - the first is used
        Revision is crucial for Yangson to proceed with module parsing
        :param yang_file: YANG module txt file
        :param yang_file_name: YANG module file name
        :return: Revision date
        """
        revision_list: list[str] = re.findall(r"^\s+revision\s+\"*(\d+-\d+-\d+)\"*", yang_file, re.MULTILINE)
        if not revision_list:
            raise ic.RevisionNotFound(f'YANG model {yang_file_name} has no revision date, check the content of this model')
        return revision_list[0]

    @staticmethod
    def get_module_namespace(yang_file: str) -> str:
        """
        Get namespace of the YANG module
        :param yang_file: module txt file
        :return: Namespace
        """
        namespace: str = ''
        if namespace_re := re.search(r'^\s+namespace\s+"(\S+)";', yang_file, re.MULTILINE):
            namespace = namespace_re.group(1)
        return namespace
