![Python Version](https://img.shields.io/badge/python-3.12-blue)

# Yangson inventory builder

This tool generates the inventory file, which is used by the [Yangson](https://github.com/CZ-NIC/yangson) python library 
to create a python object representation of an YANG model.

# Installation and usage

To install the tool:
```
pip install yangson-inventory-builder
```

At the moment only Nokia YANG models are processed. For example, [7x50 YANG Model version 20.10](https://github.com/nokia/7x50_YangModels/tree/master/latest_sros_20.10).

To prepare an inventory file:

```commandline
from yangson_inventory_builder.inventory_builder import NokiaYangsonInventory
from yangson_inventory_builder.inventory_classes import YangsonInventoryRequest

inventory_request: YangsonInventoryRequest = YangsonInventoryRequest(
    yang_directory=Path("7x50_YangModels-sros_20.10/YANG/"),
    root_config_module=Path("7x50_YangModels-sros_20.10/YANG/nokia-conf.yang"),
    target_inventory_file_name=Path("nokia_20_10_yangson_library.json")
)

yangson_inventory: NokiaYangsonInventory = NokiaYangsonInventory(inventory_request)
yangson_inventory.create_inventory_file()
```

Then use it in a Yangson to get a root container:

```commandline
from yangson.datamodel import DataModel
yangson_data_model: DataModel = DataModel.from_file(name=inventory_request.target_inventory_file_name.__str__(),
                                                        mod_path=(inventory_request.yang_directory.__str__(),))
root_container: list = yangson_data_model.schema.children[0].children
```