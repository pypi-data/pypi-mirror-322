def module_to_check(module_name):
    """
    module_to_check(module_name[, module]) -> string
    This function is used to get all method and attribute of module.
    usage:
    import pyhaven;print(pyhaven.expTools.module_to_check(pyhaven))
    """
    instruction = """"""
    instruction += f"checing module '{module_name.__name__}'\n"
    for attribute_name in dir(module_name):
        attribute_value = getattr(module_name, attribute_name)
        if callable(attribute_value):
            instruction += f"method '{attribute_name}' came from module '{attribute_value.__module__}'\n"
            instruction += f"method '{attribute_name}' docstring is:\n'{attribute_value.__doc__}'\n"
        else:
            instruction += (
                f"attribute '{attribute_name}' value is '{attribute_value}'\n"
            )
        instruction += "_" * 80 + "\n"
    # return None
    return instruction
