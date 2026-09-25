import importlib
import pkgutil

import plugins

from plugins.base import LEAFPlugin


def discover_plugins(registry):

    discovered = []

    for module_info in pkgutil.iter_modules(
        plugins.__path__
    ):

        module_name = module_info.name

        if module_name.startswith("_"):
            continue

        if module_name in {
            "base",
            "registry",
            "loader",
        }:
            continue

        module = importlib.import_module(
            f"plugins.{module_name}"
        )

        for attribute_name in dir(module):

            attribute = getattr(
                module,
                attribute_name,
            )

            if (
                isinstance(attribute, type)
                and issubclass(attribute, LEAFPlugin)
                and attribute is not LEAFPlugin
                and attribute.__module__ == module.__name__
            ):

                plugin = attribute()

                plugin.register(registry)

                discovered.append(plugin)

    return discovered
