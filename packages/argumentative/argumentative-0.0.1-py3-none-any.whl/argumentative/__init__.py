import msgspec, sys
from typing import Any, Callable
import inspect
import libcst as cst

class DocstringCollector(cst.CSTVisitor):
    METADATA_DEPENDENCIES = (cst.metadata.parent_node_provider.ParentNodeProvider,)

    def __init__(self, target_class: str):
        self.target_class = target_class
        self.field_docs: dict[str, str] = {}
        self.in_target_class = False
        
    def visit_ClassDef(self, node: cst.ClassDef) -> bool:
        if node.name.value == self.target_class:
            self.in_target_class = True
        return True
        
    def leave_ClassDef(self, node: cst.ClassDef) -> None:
        if node.name.value == self.target_class:
            self.in_target_class = False
            
    def visit_AnnAssign(self, node: cst.AnnAssign) -> bool:
        if not self.in_target_class:
            return True
            
        # Get field name
        if isinstance(node.target, cst.Name):
            field_name = node.target.value

            parent = self.get_metadata(cst.metadata.parent_node_provider.ParentNodeProvider, node)
            
            # Look for trailing comment
            if (isinstance(parent, cst.SimpleStatementLine) and 
                parent.trailing_whitespace.comment is not None):
                comment = parent.trailing_whitespace.comment.value
                # Strip leading # and whitespace
                self.field_docs[field_name] = comment.lstrip("#").strip()
                
            # Look for leading comment/docstring
            elif isinstance(parent, cst.SimpleStatementLine):
                for line in parent.leading_lines:
                    if line.comment is not None:
                        comment = line.comment.value
                        self.field_docs[field_name] = comment.lstrip("#").strip()
                        break
                        
        return True

def _get_field_docstring(cls: type[msgspec.Struct], field: msgspec.structs.FieldInfo) -> str:
    path = inspect.getsourcefile(cls)
    with open(path, "r") as file:
        contents = file.read()
    
    tree = cst.metadata.MetadataWrapper(cst.parse_module(contents))
    collector = DocstringCollector(cls.__name__)
    tree.visit(collector)
    
    return collector.field_docs.get(field.name, "")

def argumentative(exit_on_error: bool = False, custom_help_message: str | None = None):
    def decorator(cls: type[msgspec.Struct]):
        fields = msgspec.structs.fields(cls)

        def from_args(argv: list[str] = sys.argv[1:]):
            argv = argv.copy()

            for arg in argv:
                if arg == "--help" or arg == "-h":
                    if custom_help_message is not None:
                        print(custom_help_message)
                    else:
                        name = sys.argv[0]
                        print(cls.__doc__.strip())
                        print(f"Usage: {name} ", end="")
                        for field in fields:
                            if field.required:
                                print(f"<{field.name}>", end=" ")
                        for field in fields:
                            if not field.required:
                                if field.type != bool:
                                    print(f"[--{field.name} <{field.type.__name__}>]", end=" ")
                                else:
                                    print(f"[--{field.name}]", end=" ")
                        print("\n\nArguments:")
                        for field in fields:
                            if field.required:
                                print(f"{field.name} <{field.type.__name__}> - {_get_field_docstring(cls, field)}")
                        print("\nOptions:")
                        for field in fields:
                            if not field.required:
                                print(f"--{field.name} <{field.type.__name__}> - {_get_field_docstring(cls, field)}")
                    exit(0)

            positional_arg_processors: dict[msgspec.structs.FieldInfo, Callable[[list[str]], tuple[Any, list[str]]]] = {}
            optional_arg_processors: dict[msgspec.structs.FieldInfo, Callable[[list[str]], tuple[Any, list[str]]]] = {}

            for field in fields:
                if field.required:
                    def scope():
                        field_name = field.name
                        field_type = field.type
                        def processor(remaining_args: list[str]):
                            try:
                                arg = remaining_args.pop(0)
                            except IndexError:
                                raise ValueError(f"No argument found for {field_name}")
                            arg = msgspec.convert(arg, field_type, strict=False)
                            return (field_name, arg, remaining_args)
                        positional_arg_processors[field_name] = processor
                    scope()
                else:
                    def scope():
                        field_name = field.name
                        field_type = field.type
                        field_default = field.default
                        def processor(remaining_args: list[str]):
                            res = (field_name, field_default if field_default is not msgspec.NODEFAULT else None, remaining_args)
                            for idx, arg in enumerate(remaining_args):
                                if arg.startswith(f"--{field_name}"):
                                    remaining_args.pop(idx)
                                    result = None

                                    if arg[len(f"--{field_name}"):].startswith("="):
                                        result = arg[len(f"--{field_name}") + 1:]
                                    elif field_type == bool:
                                        result = True
                                    else:
                                        try:
                                            result = remaining_args.pop(idx)
                                        except IndexError:
                                            raise ValueError(f"No argument found for {field_name}")
                                    
                                    if result is not None:
                                        result = msgspec.convert(result, field_type, strict=False)
                                        res = (field_name, result, remaining_args)
                                        break
                            return res
                        optional_arg_processors[field_name] = processor
                    scope()

            positional_args = []
            optional_args = {}

            for processor in optional_arg_processors.values():
                    field_name, arg, argv = processor(argv)
                    optional_args[field_name] = arg

            for field_name, processor in positional_arg_processors.items():
                try:
                    _, arg, argv = processor(argv)
                    positional_args.append(arg)
                except ValueError as e:
                    if exit_on_error:
                        print(f"`{field_name}` is a required argument!")
                        exit(1)
                    else:
                        raise ValueError(f"{e}\n{field_name} is a required argument")
                    
            return cls(*positional_args, **optional_args)

        cls.from_args = from_args

        return cls
    return decorator
