---
title: README
---

# Synopsis

Extensible on-demand data loader with caching. The library currently provides loaders for the following data sources:

* text (file or URL)
* JSON (file or URL)
* YAML (file or URL)
* Pandas DataFrame (file or database connection)

The user can easily add custom loaders for other data sources by subclassing the [LoaderBase](https://dalood-jrye-8d769402f410f1fc6671ade3a2c8943fe936c00f396ee9fb560.gitlabpages.inria.fr/dalood.loader.html#dalood.loader.base.LoaderBase) class or one of its subclasses (e.g. [FileLoaderBase](https://dalood-jrye-8d769402f410f1fc6671ade3a2c8943fe936c00f396ee9fb560.gitlabpages.inria.fr/dalood.loader.html#dalood.loader.file.FileLoaderBase), [URLLoaderBase](https://dalood-jrye-8d769402f410f1fc6671ade3a2c8943fe936c00f396ee9fb560.gitlabpages.inria.fr/dalood.loader.html#dalood.loader.url.UrlLoaderBase). Submissions of new loaders for inclusion in the library are welcome.


Data is managed by the [Manager](https://dalood-jrye-8d769402f410f1fc6671ade3a2c8943fe936c00f396ee9fb560.gitlabpages.inria.fr/dalood.html#dalood.manager.Manager) class. The user registers patterns to map data sources to corresponding loaders and then requests the data via the manager. These patterns are compiled to [Python regular expressions](https://docs.python.org/3/library/re.html) which are then matched against data requests sent to the manager to determine which loader to use to handle the request. The argument is then passed through to the loader, which will load the data upon the first request and keep it in memory for subsequent requests until the cache is cleared.

The manager provides several methods for managing the cached data, such as clearing everything, clearing by argument pattern, forcing a reload of all data, reloading only data from sources that report a modification, etc.

See the Usage section below for details.

# Links

[insert: links]: #

## GitLab

* [Homepage](https://gitlab.inria.fr/jrye/dalood)
* [Source](https://gitlab.inria.fr/jrye/dalood.git)
* [Documentation](https://jrye.gitlabpages.inria.fr/dalood)
* [Issues](https://gitlab.inria.fr/jrye/dalood/-/issues)
* [GitLab package registry](https://gitlab.inria.fr/jrye/dalood/-/packages)

## Other Repositories

* [Python Package Index](https://pypi.org/project/Dalood/)

[/insert: links]: #


# Usage

## Basic

In the following example, we instantiate a manager an configure it to load JSON and YAML filepaths via the JSONFileLoader and YAMLFileLoader, respectively.

~~~python
# Import the manager and loaders.
from dalood.manager import Manager
from dalood.loader.json import JSONFileLoader
from dalood.loader.yaml import YAMLFileLoader


# Instantiate the manager.
man = Manager()

# Register the JSON file loader for all arguments ending with the JSON extension
# (`.json`). The first argument is a Python regular expression, followed by a
# loader instance.
man.register_loader("^.*\.json$", JSONFileLoader())

# The regular expression syntax is a bit complex for new users. Dalood therefore
# supports other pattern types: glob patterns and literal strings.

# Register the YAML file loader for all arguments ending with the YAML extension
# (`.yaml`). Here we use a simpler glob pattern instead of a regular expression
# pattern
man.register_loader("*.yaml", YAMLFileLoader(), pattern_type="glob")

# For comparison, we would have registered the JSON loader with the following statement.
# man.register_loader("*.json", JSONFileLoader(), pattern_type="glob")

# Now that the loaders are registered, we can load JSON and YAML files by simply
# passing their paths to the manager via the `get()` method:

json_data = man.get("/tmp/examples/foo.json")
yaml_data = man.get("/tmp/examples/bar.yaml")

# The data remains in memory within the manager so subsequent requests for the
# same argument via `get()` will not reload the file from the disk. You can
# check which arguments are in memory by iterating over the manager.
for arg in man:
    print("Cached argument:", arg)

# Output:
#   /tmp/examples/foo.json
#   /tmp/examples/bar.yaml.json

# To force a refresh when requesting the data, pass the `reload` argument
# to`get()`:
json_data = man.get("/tmp/examples/foo.json", reload=True).

# You can also request a reload only if the source file reports a modification
# since the data was loaded by the manager:
json_data = man.get("/tmp/examples/foo.json", refresh=True).

# For application that load large amounts of data it may be desirable to
# periodically clear the cache according to different conditions. The
# `clear_cache()` method is provided for this purpose. Without any arguments,
# all cached data is cleared.
man.clear_cache()

for arg in man:
    print("Cached argument:", arg)

# Output: empty

# Re-requeesting data after clearing the cache will simply reload the data from
# the source and cache it again.

# Clearing everything is not always desirable so `clear_cache()` provides
# options to clear the cache by a pattern (e.g. all loaded YAML files), by age
# (e.g everything loaded more than an hour ago), or by last access time (e.g.
# everything that was last accessed more than 20 minutes ago). The following
# would clear all JSON files accessed more than 2 minutes ago:
man.clear_cache("*.json", pattern_type="glob", age={"minutes":2}, by_access_time=True)
~~~


## Literal Patterns And Customized Loaders

In additional to the regular expression and glob patterns, there are also
"literal" patterns that will only match the exact string of the pattern. These
can be used to load specific arguments with specific loaders. The following
example shows how to associate different CSV file loaders with different files
that use different separator characters (comma or space).


~~~python
from dalood.manager import Manager
from dalood.loader.pandas import DataFrameCSVLoader

man = Manager()
comma_csv_loader = DataFrameCSVLoader(sep=",")
space_csv_loader = DataFrameCSVLoader(sep=" ")
man.register_loader("/tmp/example/file1.csv", comma_csv_loader, pattern_type="literal")
man.register_loader("/tmp/example/file2.csv", comma_csv_loader, pattern_type="literal")
man.register_loader("/tmp/example/file1.csv", space_csv_loader, pattern_type="literal")

# This would be tedious for many different files that cannot be summarized via a
# pattern. In that case, a custom function could make this easier:
def register_comma_csv_loader_for_path(path):
    man.register_loader(path, comma_csv_loader, pattern_type="literal")
~~~

## Pattern Classes

All of the methods that accept a pattern string and optional `pattern_type` parameter also accept instances of `RegexPattern`, `GlobPattern` and `LiteralPattern` from [dalood.regex](https://dalood-jrye-8d769402f410f1fc6671ade3a2c8943fe936c00f396ee9fb560.gitlabpages.inria.fr/dalood.html#module-dalood.regex).

~~~python
from dalood.manager import Manager
from dalood.loader.text import TextFileLoader
from dalood.regex import GlobPattern

man = Manager()
pattern = GlobPattern("*.txt")
man.register_loader(pattern, TextFileLoader())
~~~

## User-Loaded Data

Dalood also provides loaders that simply hold references to user-provided data
in order to make it accessible via a common API. For example, the user may wich
to build a custom object in memory and then access it via the manager using a
simple name:

~~~python
from dalood.manager import Manager
from dalood.loader.memory import MemoryLoader

man = Manager()

# Assume that the user has defined 2 custom objects: "custom_obj1" and
# "custom_obj2". We can map them to arbitrary names either by passing a dict as
# the "mapping" parameter when instantiating MemoryLoader
mem_loader = MemoryLoader(mapping={"obj1": custom_obj1})

# or afterward using the "map" method.
mem_loader.map("obj2", custom_obj2).

Once mapped in the memory loader, we can register them via the manager:
mem_loader.register_patterns(man)


Now we can access the objects via the manager's "get()" method:
new_var_for_custom_obj1 = man.get("obj1")
~~~

## User-Defined Loaders

The user can define custom loaders and then register them with a manager using custom patterns:

~~~python
from dalood.manager import Manager
from dalood.loader.file import FileLoaderBase

# Create a custom loader for "foo" files. We'll make it load the first 10 bytes
# from the file.

import pathlib

class FooFileLoader(FileLoaderBase):
    def load(self, src):
        path = pathlib.Path(src)
        with path.open('rb') as handle:
            return handle.read(10)

# Register this loader to handle all arguments ending in ".foo".
man.register_loader("*.foo", FooFileLoader(), pattern_type="glob")
~~~
