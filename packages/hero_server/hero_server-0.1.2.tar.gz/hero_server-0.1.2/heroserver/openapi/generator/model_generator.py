from typing import Dict, List, Set, Any

class VlangCodeGenerator:
    pass

class ModelGenerator:
    def __init__(
        self, spec: Dict[str, Any], lang_code_generator: str
    ) -> None:
        self.spec = spec
        self.lang_code_generator = lang_code_generator
        # self.processed_objects: Dict[str, Dict[str, str]] = {}
        # self.ordered_objects: List[str] = []
        # self.used_names: Set[str] = set()

    def generate_models(self):
        if self.lang_code_generator != "vlang":
            raise ValueError('Unsupported language.')
        

        if not self.spec.get('components'):
            raise ValueError("No components found in spec")

        components = self.spec['components']

        if not components.get('schemas'):
            raise ValueError("No schemas found in components")

        schemas = components['schemas']
        schemas_path = ["components", "schemas"]
        for name, schema in schemas.items():
            self.jsonschema_to_type(
                path=schemas_path + [name],
                jsonschema=schema,
            )

        objects_code = ""
        for val in self.ordered_objects:
            if val == "":
                continue
            objects_code = f"{objects_code}{val}\n\n"

        print(f'debugzo4 {objects_code}')
        return objects_code

    # def jsonschema_to_type(
    #     self, path: List[str], jsonschema: SchemaObject | ReferenceObject
    # ) -> str:
    #     if isinstance(jsonschema, ReferenceObject):
    #         ref: str = jsonschema.ref

    #         ref_schema = self.spec.ref_to_schema(ref)
    #         ref_path = ref.split("/")[1:]

    #         if isinstance(ref_schema, ContentDescriptorObject):
    #             # TODO: implement
    #             raise Exception("unimplemented")
    #             # return self.content_descriptor_to_type(ref_path, ref_schema)

    #         return self.jsonschema_to_type(ref_path, ref_schema)

    #     path_str = "/".join([item.lower() for item in path])
    #     if path_str in self.processed_objects:
    #         return self.processed_objects[path_str]["name"]

    #     type_name = self.type_name_from_path(path)

    #     description = getattr(jsonschema, 'description', None)
    #     if jsonschema.enum:
    #         enum = jsonschema.enum
    #         type_code = self.lang_code_generator.generate_enum(enum, type_name)
    #         if self.lang_code_generator.is_primitive(type_code):
    #             return type_code

    #         self.add_object(path_str, type_code, type_name)
    #         return type_name

    #     if jsonschema.type:
    #         match jsonschema.type:
    #             case "string":
    #                 return self.lang_code_generator.string_primitive()

    #             case "integer":
    #                 return self.lang_code_generator.integer_primitive()

    #             case "number":
    #                 return self.lang_code_generator.number_primitive()

    #             case "array":
    #                 if isinstance(jsonschema.items, List):
    #                     raise Exception(
    #                         "array of different item types is not supported"
    #                     )

    #                 item_type_name = self.jsonschema_to_type(
    #                     path + ["item"], jsonschema.items
    #                 )
    #                 return self.lang_code_generator.array_of_type(
    #                     item_type_name
    #                 )

    #             case "boolean":
    #                 return self.lang_code_generator.bool_primitive()

    #             case "object":
    #                 # to prevent cyclic dependencies
    #                 self.add_object(path_str, "", type_name)

    #                 properties: Dict[str, PropertyInfo] = {}
    #                 for (
    #                     property_name,
    #                     property_schema,
    #                 ) in jsonschema.properties.items():
    #                     schema = property_schema
    #                     new_path = path + ["properties", property_name]
    #                     if isinstance(property_schema, ReferenceObject):
    #                         schema = self.spec.ref_to_schema(
    #                             property_schema.ref
    #                         )
    #                         new_path = property_schema.ref.split("/")[1:]

    #                     property_info = PropertyInfo(
    #                         name=property_name,
    #                         type_name=self.jsonschema_to_type(new_path, schema),
    #                         description=schema.description,
    #                         example=schema.example,
    #                     )

    #                     properties[property_name] = property_info

    #                 type_code = self.lang_code_generator.generate_object(
    #                     type_name, properties
    #                 )
    #                 self.add_object(path_str, type_code, type_name)
    #                 return type_name

    #             case "null":
    #                 return self.lang_code_generator.null_primitive()

    #             case _:
    #                 raise Exception(f"type {jsonschema.type} is not supported")

    #     if jsonschema.anyOf:
    #         type_names = []
    #         for i, item in enumerate(jsonschema.anyOf):
    #             type_names.append(
    #                 self.jsonschema_to_type(path + [f"anyOf{i}"], item)
    #             )

    #         return self.lang_code_generator.generate_multitype(type_names)
    #         # self.add_object(path_str, type_code, type_code)
    #         # return type_code

    #     elif jsonschema.oneOf:
    #         type_names = []
    #         for i, item in enumerate(jsonschema.oneOf):
    #             type_names.append(
    #                 self.jsonschema_to_type(path + [f"oneOf{i}"], item)
    #             )

    #         return self.lang_code_generator.generate_multitype(type_names)
    #         # self.add_object(path_str, type_code, type_code)
    #         # return type_code

    #     elif jsonschema.allOf:
    #         return self.lang_code_generator.encapsulate_types(jsonschema.allOf)
    #         # self.add_object(path_str, type_code, type_code)
    #         # return type_name

    #     raise Exception(f"type {jsonschema.type} is not supported")

    # def add_object(self, path_str: str, type_code: str, type_name: str):
    #     self.used_names.add(type_name)
    #     self.processed_objects[path_str] = {
    #         "code": type_code,
    #         "name": type_name,
    #     }
    #     print(f'debugzo21 {self.processed_objects[path_str]}')
    #     self.ordered_objects.append(type_code)

    # def type_name_from_path(self, path: List[str]) -> str:
    #     type_name = ""
    #     for item in reversed(path):
    #         type_name += item.title() if item.islower() else item
    #         if type_name not in self.used_names:
    #             return type_name

    #     raise Exception(f"failed to generate unique name from path: {path}")
