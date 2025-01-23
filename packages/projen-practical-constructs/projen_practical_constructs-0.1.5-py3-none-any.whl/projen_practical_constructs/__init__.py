r'''
# projen-practical-constructs

Constructs and utilities for managing projects with Projen enforcing solid build, test and linting structures.

This repo have additional Constructs not present in [official projen repo](https://github.com/projen/projen) such as RUFF, Makefile etc.

Currently there is support for Python projects, but in the future more will be added.

Check in /examples folder the target structure that these project types will produce.

## For Python project types

Project type name: python_basic

The basic stack supported by this project is:

* Makefile: scripts management
* pip: virtual environments management
* Mypy: code Type check
* RUFF: code formatting and linting
* pytest + coverage: test management
* pip-audit: dependencies vulnerability checks
* pip-tools: dependencies lock file generation (contrainsts.txt)
* vs-code plugins: code editor feedback

[This project](https://github.com/flaviostutz/monorepo-spikes/tree/main/shared/python/hello_world_reference) was used as reference for the target project structure created by this projen project type.

## Usage

```sh
npx projen new --from projen_practical_constructs python_basic
```

The constructs can be used separately to adapt to your specific needs, but you can use the PythonProject construct with a default configuration of the entire stack to easily have a full project structure with build, test and linting capabilities.

## Development

### Tests

* We use a lot of snapshots on our tests, which in general is not a good practice. But in our case we decided to use it because there are lots of files and the snapshots will check if the file contents were changed.
* Be careful checking manually the errors on snapshots before updating them to be sure that it's not a breaking change to the users of the library

### JSII

* The options of the constructs have to be "interface", not "types" because they are exposed to JSII and it works well only with interfaces
* The Project type must have an attribute with name "options" in constructor
* https://aws.github.io/jsii/specification/2-type-system/

### References

* Projen quick start: https://projen.io/docs/quick-starts/python/hello-world/
* https://projen.io/docs/concepts/projects/building-your-own/
* Sample code for Python contructs: https://github.com/projen/projen/blob/main/src/python/pip.ts
* https://kennethwinner.com/2021/03/07/projen-external-module-github/
* Example project of a Python Projen Type: https://github.com/kcwinner/projen-github-demo
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *

import projen as _projen_04054675


@jsii.data_type(
    jsii_type="projen-practical-constructs.Build0Options",
    jsii_struct_bases=[],
    name_mapping={"package": "package", "pip": "pip"},
)
class Build0Options:
    def __init__(
        self,
        *,
        package: typing.Optional[typing.Union["PackageOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        pip: typing.Optional[typing.Union["PipOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param package: 
        :param pip: 
        '''
        if isinstance(package, dict):
            package = PackageOptions(**package)
        if isinstance(pip, dict):
            pip = PipOptions(**pip)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e20a491b2a5a4f8ee18f05888a4892e7e41c691d596b28ee23e4eec41be056ba)
            check_type(argname="argument package", value=package, expected_type=type_hints["package"])
            check_type(argname="argument pip", value=pip, expected_type=type_hints["pip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if package is not None:
            self._values["package"] = package
        if pip is not None:
            self._values["pip"] = pip

    @builtins.property
    def package(self) -> typing.Optional["PackageOptions"]:
        result = self._values.get("package")
        return typing.cast(typing.Optional["PackageOptions"], result)

    @builtins.property
    def pip(self) -> typing.Optional["PipOptions"]:
        result = self._values.get("pip")
        return typing.cast(typing.Optional["PipOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Build0Options(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BuildTarget(
    _projen_04054675.Component,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen-practical-constructs.BuildTarget",
):
    '''Python project build configurations.'''

    def __init__(
        self,
        project: _projen_04054675.Project,
        task_opts: typing.Union["TaskOptions", typing.Dict[builtins.str, typing.Any]],
        *,
        package: typing.Optional[typing.Union["PackageOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        pip: typing.Optional[typing.Union["PipOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param project: -
        :param task_opts: -
        :param package: 
        :param pip: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7baf093ce1415d71f61d9818afeb26e3072bbd9a78db8ca4ffdf96dcf200c73)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument task_opts", value=task_opts, expected_type=type_hints["task_opts"])
        opts = Build0Options(package=package, pip=pip)

        jsii.create(self.__class__, self, [project, task_opts, opts])


class CoveragercFile(
    _projen_04054675.FileBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen-practical-constructs.CoveragercFile",
):
    def __init__(
        self,
        project: _projen_04054675.Project,
        *,
        format: typing.Optional[builtins.str] = None,
        min_coverage: typing.Optional[jsii.Number] = None,
        omit_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        skip_covered: typing.Optional[builtins.bool] = None,
        skip_empty: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param project: -
        :param format: Coverage report format. Default: 'text'
        :param min_coverage: Minimum coverage required to pass the test. Default: 80
        :param omit_patterns: List of file patterns to omit from coverage. Default: []
        :param skip_covered: Skip reporting files that are covered. Default: false
        :param skip_empty: Skip reporting files that are empty. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__159e518f7881abcb6abee9cf04ea6e882729784c5e0b7a737f6522baa1f5a152)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        opts = CoveragercFileOptions(
            format=format,
            min_coverage=min_coverage,
            omit_patterns=omit_patterns,
            skip_covered=skip_covered,
            skip_empty=skip_empty,
        )

        jsii.create(self.__class__, self, [project, opts])

    @jsii.member(jsii_name="synthesizeContent")
    def _synthesize_content(
        self,
        _resolver: _projen_04054675.IResolver,
    ) -> typing.Optional[builtins.str]:
        '''Implemented by derived classes and returns the contents of the file to emit.

        :param _resolver: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83d971dfa627ffd4740ef400fe2c07260cfc8a850bb5f15117be52c28cf8aacb)
            check_type(argname="argument _resolver", value=_resolver, expected_type=type_hints["_resolver"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "synthesizeContent", [_resolver]))


@jsii.data_type(
    jsii_type="projen-practical-constructs.CoveragercFileOptions",
    jsii_struct_bases=[],
    name_mapping={
        "format": "format",
        "min_coverage": "minCoverage",
        "omit_patterns": "omitPatterns",
        "skip_covered": "skipCovered",
        "skip_empty": "skipEmpty",
    },
)
class CoveragercFileOptions:
    def __init__(
        self,
        *,
        format: typing.Optional[builtins.str] = None,
        min_coverage: typing.Optional[jsii.Number] = None,
        omit_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        skip_covered: typing.Optional[builtins.bool] = None,
        skip_empty: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param format: Coverage report format. Default: 'text'
        :param min_coverage: Minimum coverage required to pass the test. Default: 80
        :param omit_patterns: List of file patterns to omit from coverage. Default: []
        :param skip_covered: Skip reporting files that are covered. Default: false
        :param skip_empty: Skip reporting files that are empty. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf0f342ecc7c849d461adb9b6dac4d82650ef73565eff25d53bbcfb2b3c5479d)
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument min_coverage", value=min_coverage, expected_type=type_hints["min_coverage"])
            check_type(argname="argument omit_patterns", value=omit_patterns, expected_type=type_hints["omit_patterns"])
            check_type(argname="argument skip_covered", value=skip_covered, expected_type=type_hints["skip_covered"])
            check_type(argname="argument skip_empty", value=skip_empty, expected_type=type_hints["skip_empty"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if format is not None:
            self._values["format"] = format
        if min_coverage is not None:
            self._values["min_coverage"] = min_coverage
        if omit_patterns is not None:
            self._values["omit_patterns"] = omit_patterns
        if skip_covered is not None:
            self._values["skip_covered"] = skip_covered
        if skip_empty is not None:
            self._values["skip_empty"] = skip_empty

    @builtins.property
    def format(self) -> typing.Optional[builtins.str]:
        '''Coverage report format.

        :default: 'text'
        '''
        result = self._values.get("format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_coverage(self) -> typing.Optional[jsii.Number]:
        '''Minimum coverage required to pass the test.

        :default: 80
        '''
        result = self._values.get("min_coverage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def omit_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of file patterns to omit from coverage.

        :default: []
        '''
        result = self._values.get("omit_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def skip_covered(self) -> typing.Optional[builtins.bool]:
        '''Skip reporting files that are covered.

        :default: false
        '''
        result = self._values.get("skip_covered")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def skip_empty(self) -> typing.Optional[builtins.bool]:
        '''Skip reporting files that are empty.

        :default: true
        '''
        result = self._values.get("skip_empty")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CoveragercFileOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LintTarget(
    _projen_04054675.Component,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen-practical-constructs.LintTarget",
):
    '''Python project lint configurations.'''

    def __init__(
        self,
        project: _projen_04054675.Project,
        task_options: typing.Union["TaskOptions", typing.Dict[builtins.str, typing.Any]],
        *,
        attach_fix_task_to: typing.Optional[builtins.str] = None,
        add_to_existing_rules: typing.Optional[builtins.bool] = None,
        ignore_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
        mccabe_max_complexity: typing.Optional[jsii.Number] = None,
        per_file_ignores: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[builtins.str]]] = None,
        select_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
        target_python_version: typing.Optional[builtins.str] = None,
        unsafe_fixes: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param project: -
        :param task_options: -
        :param attach_fix_task_to: Attach lint fix tasks to parent.
        :param add_to_existing_rules: Add rules defined here to the ignoreRules and selectRules (on top of the default rules) or replace them by this contents? Default: true
        :param ignore_rules: Default: pre-selected set of rules
        :param mccabe_max_complexity: Default: 14
        :param per_file_ignores: Default: ignore doc-string code format for test files
        :param select_rules: Default: pre-selected set of rules
        :param target_python_version: Default: py313
        :param unsafe_fixes: Default: false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a024fae964b162f23bca5eaaea17d6482838424ff147cbcf777078f73bfeb68)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument task_options", value=task_options, expected_type=type_hints["task_options"])
        opts = LintOptions(
            attach_fix_task_to=attach_fix_task_to,
            add_to_existing_rules=add_to_existing_rules,
            ignore_rules=ignore_rules,
            mccabe_max_complexity=mccabe_max_complexity,
            per_file_ignores=per_file_ignores,
            select_rules=select_rules,
            target_python_version=target_python_version,
            unsafe_fixes=unsafe_fixes,
        )

        jsii.create(self.__class__, self, [project, task_options, opts])


class MyPy(
    _projen_04054675.Component,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen-practical-constructs.MyPy",
):
    def __init__(
        self,
        project: _projen_04054675.Project,
        *,
        venv_path: builtins.str,
        attach_tasks_to: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param project: -
        :param venv_path: Path to the python virtual environment directory used in this project.
        :param attach_tasks_to: Existing task to attach new tasks to. It will be included as "spawn" tasks in new steps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0a177ef285e9d814c79f51d94f6a5469ba5493c4e5b3b7f83c91a7cb2308c59)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        task_opts = TaskOptions(venv_path=venv_path, attach_tasks_to=attach_tasks_to)

        jsii.create(self.__class__, self, [project, task_opts])


class MyPyIniFile(
    _projen_04054675.FileBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen-practical-constructs.MyPyIniFile",
):
    def __init__(self, project: _projen_04054675.Project) -> None:
        '''
        :param project: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4de587b589ba9e007f9440a8c64dc04332c03c6a61c1fbeab978cb77f04fc58)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        jsii.create(self.__class__, self, [project])

    @jsii.member(jsii_name="synthesizeContent")
    def _synthesize_content(
        self,
        _resolver: _projen_04054675.IResolver,
    ) -> typing.Optional[builtins.str]:
        '''Implemented by derived classes and returns the contents of the file to emit.

        :param _resolver: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05af635c22d0af271080341bf52a1ec29b58a9cb63c5ea1521a193ee6570270e)
            check_type(argname="argument _resolver", value=_resolver, expected_type=type_hints["_resolver"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "synthesizeContent", [_resolver]))


class Package(
    _projen_04054675.Component,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen-practical-constructs.Package",
):
    def __init__(
        self,
        project: _projen_04054675.Project,
        *,
        license: typing.Optional[builtins.str] = None,
        author_email: typing.Optional[builtins.str] = None,
        author_name: typing.Optional[builtins.str] = None,
        classifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        homepage: typing.Optional[builtins.str] = None,
        keywords: typing.Optional[typing.Sequence[builtins.str]] = None,
        license_file: typing.Optional[builtins.str] = None,
        package_name: typing.Optional[builtins.str] = None,
        readme: typing.Optional[builtins.str] = None,
        requires_python: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param project: -
        :param license: License name in spdx format. e.g: ``MIT``, ``Apache-2.0``
        :param author_email: Author's e-mail.
        :param author_name: Author's name.
        :param classifiers: A list of PyPI trove classifiers that describe the project.
        :param description: A short description of the package.
        :param homepage: A URL to the website of the project.
        :param keywords: Keywords to add to the package.
        :param license_file: License file.
        :param package_name: Name of the python package. E.g. "my_python_package". Must only consist of alphanumeric characters and underscores. Default: Name of the directory
        :param readme: README file.
        :param requires_python: Python version required to run this package.
        :param version: Version of the package.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62f3584f77ee44c76622dd4d1bcb61319421c6ff75dc347a3de1892c0baf9086)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        opts = PackageOptions(
            license=license,
            author_email=author_email,
            author_name=author_name,
            classifiers=classifiers,
            description=description,
            homepage=homepage,
            keywords=keywords,
            license_file=license_file,
            package_name=package_name,
            readme=readme,
            requires_python=requires_python,
            version=version,
        )

        jsii.create(self.__class__, self, [project, opts])


class Pip(
    _projen_04054675.Component,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen-practical-constructs.Pip",
):
    def __init__(
        self,
        project: _projen_04054675.Project,
        task_opts: typing.Union["TaskOptions", typing.Dict[builtins.str, typing.Any]],
        *,
        lock_file: typing.Optional[builtins.str] = None,
        lock_file_dev: typing.Optional[builtins.str] = None,
        python_exec: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param project: -
        :param task_opts: -
        :param lock_file: Name of the file used to install dependencies from This file is derived from pyproject.toml and have to be manually updated if pyproject.toml is updated by using the projen task 'update-lockfile'. This lock won't include "dev" dependencies Read more at https://stackoverflow.com/questions/34645821/pip-constraints-files. Default: constraints.txt
        :param lock_file_dev: Same as lockFile, but it includes all dev dependencies. Default: constraints-dev.txt
        :param python_exec: Python executable path to be used while creating the virtual environment used in this project. Default: python
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6c809477032f6e6abdbfbf18de97c940c11e01375028ae0f5ecb6b8e973a50f)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument task_opts", value=task_opts, expected_type=type_hints["task_opts"])
        opts = PipOptions(
            lock_file=lock_file, lock_file_dev=lock_file_dev, python_exec=python_exec
        )

        jsii.create(self.__class__, self, [project, task_opts, opts])

    @jsii.member(jsii_name="postSynthesize")
    def post_synthesize(self) -> None:
        '''Called after synthesis.

        Order is *not* guaranteed.
        '''
        return typing.cast(None, jsii.invoke(self, "postSynthesize", []))


class PipAudit(
    _projen_04054675.Component,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen-practical-constructs.PipAudit",
):
    def __init__(
        self,
        project: _projen_04054675.Project,
        *,
        venv_path: builtins.str,
        attach_tasks_to: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param project: -
        :param venv_path: Path to the python virtual environment directory used in this project.
        :param attach_tasks_to: Existing task to attach new tasks to. It will be included as "spawn" tasks in new steps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82328de1f2fc16d559d0de14506a0fa6977eaf5050623900f5ab343c6be250cb)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        opts = TaskOptions(venv_path=venv_path, attach_tasks_to=attach_tasks_to)

        jsii.create(self.__class__, self, [project, opts])


@jsii.data_type(
    jsii_type="projen-practical-constructs.PipOptions",
    jsii_struct_bases=[],
    name_mapping={
        "lock_file": "lockFile",
        "lock_file_dev": "lockFileDev",
        "python_exec": "pythonExec",
    },
)
class PipOptions:
    def __init__(
        self,
        *,
        lock_file: typing.Optional[builtins.str] = None,
        lock_file_dev: typing.Optional[builtins.str] = None,
        python_exec: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param lock_file: Name of the file used to install dependencies from This file is derived from pyproject.toml and have to be manually updated if pyproject.toml is updated by using the projen task 'update-lockfile'. This lock won't include "dev" dependencies Read more at https://stackoverflow.com/questions/34645821/pip-constraints-files. Default: constraints.txt
        :param lock_file_dev: Same as lockFile, but it includes all dev dependencies. Default: constraints-dev.txt
        :param python_exec: Python executable path to be used while creating the virtual environment used in this project. Default: python
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ab0570fbeee15a743ac44aee78db6330a9da7a8cb0af29bcd9bbd26f212ec73)
            check_type(argname="argument lock_file", value=lock_file, expected_type=type_hints["lock_file"])
            check_type(argname="argument lock_file_dev", value=lock_file_dev, expected_type=type_hints["lock_file_dev"])
            check_type(argname="argument python_exec", value=python_exec, expected_type=type_hints["python_exec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if lock_file is not None:
            self._values["lock_file"] = lock_file
        if lock_file_dev is not None:
            self._values["lock_file_dev"] = lock_file_dev
        if python_exec is not None:
            self._values["python_exec"] = python_exec

    @builtins.property
    def lock_file(self) -> typing.Optional[builtins.str]:
        '''Name of the file used to install dependencies from This file is derived from pyproject.toml and have to be manually updated if pyproject.toml is updated by using the projen task 'update-lockfile'. This lock won't include "dev" dependencies Read more at https://stackoverflow.com/questions/34645821/pip-constraints-files.

        :default: constraints.txt
        '''
        result = self._values.get("lock_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lock_file_dev(self) -> typing.Optional[builtins.str]:
        '''Same as lockFile, but it includes all dev dependencies.

        :default: constraints-dev.txt
        '''
        result = self._values.get("lock_file_dev")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def python_exec(self) -> typing.Optional[builtins.str]:
        '''Python executable path to be used while creating the virtual environment used in this project.

        :default: python
        '''
        result = self._values.get("python_exec")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PyProjectTomlFile(
    _projen_04054675.FileBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen-practical-constructs.PyProjectTomlFile",
):
    '''pyproject.toml synthetisation.'''

    def __init__(
        self,
        project: _projen_04054675.Project,
        *,
        author_email: typing.Optional[builtins.str] = None,
        author_name: typing.Optional[builtins.str] = None,
        classifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        homepage: typing.Optional[builtins.str] = None,
        keywords: typing.Optional[typing.Sequence[builtins.str]] = None,
        license_file: typing.Optional[builtins.str] = None,
        package_name: typing.Optional[builtins.str] = None,
        readme: typing.Optional[builtins.str] = None,
        requires_python: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param project: -
        :param author_email: Author's e-mail.
        :param author_name: Author's name.
        :param classifiers: A list of PyPI trove classifiers that describe the project.
        :param description: A short description of the package.
        :param homepage: A URL to the website of the project.
        :param keywords: Keywords to add to the package.
        :param license_file: License file.
        :param package_name: Name of the python package. E.g. "my_python_package". Must only consist of alphanumeric characters and underscores. Default: Name of the directory
        :param readme: README file.
        :param requires_python: Python version required to run this package.
        :param version: Version of the package.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6d7a3b8b4177596f54f16f91bd9df59e0a45d86f401871b1e9b3b29ce78328b)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        opts = PyProjectTomlOptions(
            author_email=author_email,
            author_name=author_name,
            classifiers=classifiers,
            description=description,
            homepage=homepage,
            keywords=keywords,
            license_file=license_file,
            package_name=package_name,
            readme=readme,
            requires_python=requires_python,
            version=version,
        )

        jsii.create(self.__class__, self, [project, opts])

    @jsii.member(jsii_name="synthesizeContent")
    def _synthesize_content(
        self,
        _resolver: _projen_04054675.IResolver,
    ) -> typing.Optional[builtins.str]:
        '''Implemented by derived classes and returns the contents of the file to emit.

        :param _resolver: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4507ce8637891a717163abf9982165de1dcb742ca0621e122de9e18450c7727b)
            check_type(argname="argument _resolver", value=_resolver, expected_type=type_hints["_resolver"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "synthesizeContent", [_resolver]))


@jsii.data_type(
    jsii_type="projen-practical-constructs.PyProjectTomlOptions",
    jsii_struct_bases=[],
    name_mapping={
        "author_email": "authorEmail",
        "author_name": "authorName",
        "classifiers": "classifiers",
        "description": "description",
        "homepage": "homepage",
        "keywords": "keywords",
        "license_file": "licenseFile",
        "package_name": "packageName",
        "readme": "readme",
        "requires_python": "requiresPython",
        "version": "version",
    },
)
class PyProjectTomlOptions:
    def __init__(
        self,
        *,
        author_email: typing.Optional[builtins.str] = None,
        author_name: typing.Optional[builtins.str] = None,
        classifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        homepage: typing.Optional[builtins.str] = None,
        keywords: typing.Optional[typing.Sequence[builtins.str]] = None,
        license_file: typing.Optional[builtins.str] = None,
        package_name: typing.Optional[builtins.str] = None,
        readme: typing.Optional[builtins.str] = None,
        requires_python: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param author_email: Author's e-mail.
        :param author_name: Author's name.
        :param classifiers: A list of PyPI trove classifiers that describe the project.
        :param description: A short description of the package.
        :param homepage: A URL to the website of the project.
        :param keywords: Keywords to add to the package.
        :param license_file: License file.
        :param package_name: Name of the python package. E.g. "my_python_package". Must only consist of alphanumeric characters and underscores. Default: Name of the directory
        :param readme: README file.
        :param requires_python: Python version required to run this package.
        :param version: Version of the package.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05a4f19c0ac4e3b053533fffc4e6b5d4ec292f9c4073fe33392b6cfca5185ea0)
            check_type(argname="argument author_email", value=author_email, expected_type=type_hints["author_email"])
            check_type(argname="argument author_name", value=author_name, expected_type=type_hints["author_name"])
            check_type(argname="argument classifiers", value=classifiers, expected_type=type_hints["classifiers"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument homepage", value=homepage, expected_type=type_hints["homepage"])
            check_type(argname="argument keywords", value=keywords, expected_type=type_hints["keywords"])
            check_type(argname="argument license_file", value=license_file, expected_type=type_hints["license_file"])
            check_type(argname="argument package_name", value=package_name, expected_type=type_hints["package_name"])
            check_type(argname="argument readme", value=readme, expected_type=type_hints["readme"])
            check_type(argname="argument requires_python", value=requires_python, expected_type=type_hints["requires_python"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if author_email is not None:
            self._values["author_email"] = author_email
        if author_name is not None:
            self._values["author_name"] = author_name
        if classifiers is not None:
            self._values["classifiers"] = classifiers
        if description is not None:
            self._values["description"] = description
        if homepage is not None:
            self._values["homepage"] = homepage
        if keywords is not None:
            self._values["keywords"] = keywords
        if license_file is not None:
            self._values["license_file"] = license_file
        if package_name is not None:
            self._values["package_name"] = package_name
        if readme is not None:
            self._values["readme"] = readme
        if requires_python is not None:
            self._values["requires_python"] = requires_python
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def author_email(self) -> typing.Optional[builtins.str]:
        '''Author's e-mail.'''
        result = self._values.get("author_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def author_name(self) -> typing.Optional[builtins.str]:
        '''Author's name.'''
        result = self._values.get("author_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def classifiers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of PyPI trove classifiers that describe the project.

        :see: https://pypi.org/classifiers/
        '''
        result = self._values.get("classifiers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A short description of the package.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def homepage(self) -> typing.Optional[builtins.str]:
        '''A URL to the website of the project.'''
        result = self._values.get("homepage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keywords(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Keywords to add to the package.'''
        result = self._values.get("keywords")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def license_file(self) -> typing.Optional[builtins.str]:
        '''License file.'''
        result = self._values.get("license_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def package_name(self) -> typing.Optional[builtins.str]:
        '''Name of the python package.

        E.g. "my_python_package".
        Must only consist of alphanumeric characters and underscores.

        :default: Name of the directory
        '''
        result = self._values.get("package_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def readme(self) -> typing.Optional[builtins.str]:
        '''README file.'''
        result = self._values.get("readme")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def requires_python(self) -> typing.Optional[builtins.str]:
        '''Python version required to run this package.'''
        result = self._values.get("requires_python")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version of the package.'''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PyProjectTomlOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PyTest(
    _projen_04054675.Component,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen-practical-constructs.PyTest",
):
    def __init__(
        self,
        project: _projen_04054675.Project,
        task_opts: typing.Union["TaskOptions", typing.Dict[builtins.str, typing.Any]],
        *,
        format: typing.Optional[builtins.str] = None,
        min_coverage: typing.Optional[jsii.Number] = None,
        omit_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        skip_covered: typing.Optional[builtins.bool] = None,
        skip_empty: typing.Optional[builtins.bool] = None,
        verbose: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param project: -
        :param task_opts: -
        :param format: Coverage report format. Default: 'text'
        :param min_coverage: Minimum coverage required to pass the test. Default: 80
        :param omit_patterns: List of file patterns to omit from coverage. Default: []
        :param skip_covered: Skip reporting files that are covered. Default: false
        :param skip_empty: Skip reporting files that are empty. Default: true
        :param verbose: Run pytest with the ``--verbose`` flag. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42e05408896599bbf022ad6a7e60a821d61cad81416e62f8e87333465af34cc8)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument task_opts", value=task_opts, expected_type=type_hints["task_opts"])
        opts = PyTestOptions(
            format=format,
            min_coverage=min_coverage,
            omit_patterns=omit_patterns,
            skip_covered=skip_covered,
            skip_empty=skip_empty,
            verbose=verbose,
        )

        jsii.create(self.__class__, self, [project, task_opts, opts])


class PyTestIniFile(
    _projen_04054675.FileBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen-practical-constructs.PyTestIniFile",
):
    def __init__(
        self,
        project: _projen_04054675.Project,
        *,
        verbose: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param project: -
        :param verbose: Run pytest with the ``--verbose`` flag. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44a3acc3982cbac42b7f244f2b7a0629ea77dbb3fbeb16b462809daed3316bc1)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        opts = PyTestIniOptions(verbose=verbose)

        jsii.create(self.__class__, self, [project, opts])

    @jsii.member(jsii_name="synthesizeContent")
    def _synthesize_content(
        self,
        _resolver: _projen_04054675.IResolver,
    ) -> typing.Optional[builtins.str]:
        '''Implemented by derived classes and returns the contents of the file to emit.

        :param _resolver: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__975893dbb0771af51870157408a643ffcf74cf8fc037cc71b062959406638251)
            check_type(argname="argument _resolver", value=_resolver, expected_type=type_hints["_resolver"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "synthesizeContent", [_resolver]))

    @builtins.property
    @jsii.member(jsii_name="opts")
    def opts(self) -> "PyTestIniOptions":
        return typing.cast("PyTestIniOptions", jsii.get(self, "opts"))

    @opts.setter
    def opts(self, value: "PyTestIniOptions") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ef765f0b3b01e999545322392822791093e2b72fca8c2d619f6f3c52c5dfcd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "opts", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="projen-practical-constructs.PyTestIniOptions",
    jsii_struct_bases=[],
    name_mapping={"verbose": "verbose"},
)
class PyTestIniOptions:
    def __init__(self, *, verbose: typing.Optional[builtins.bool] = None) -> None:
        '''
        :param verbose: Run pytest with the ``--verbose`` flag. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d4ca4cf98a7701cf69a33f919512afaccabd7bb8ee6ac702d86b6b686e85c40)
            check_type(argname="argument verbose", value=verbose, expected_type=type_hints["verbose"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if verbose is not None:
            self._values["verbose"] = verbose

    @builtins.property
    def verbose(self) -> typing.Optional[builtins.bool]:
        '''Run pytest with the ``--verbose`` flag.

        :default: true
        '''
        result = self._values.get("verbose")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PyTestIniOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen-practical-constructs.PyTestOptions",
    jsii_struct_bases=[CoveragercFileOptions, PyTestIniOptions],
    name_mapping={
        "format": "format",
        "min_coverage": "minCoverage",
        "omit_patterns": "omitPatterns",
        "skip_covered": "skipCovered",
        "skip_empty": "skipEmpty",
        "verbose": "verbose",
    },
)
class PyTestOptions(CoveragercFileOptions, PyTestIniOptions):
    def __init__(
        self,
        *,
        format: typing.Optional[builtins.str] = None,
        min_coverage: typing.Optional[jsii.Number] = None,
        omit_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        skip_covered: typing.Optional[builtins.bool] = None,
        skip_empty: typing.Optional[builtins.bool] = None,
        verbose: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param format: Coverage report format. Default: 'text'
        :param min_coverage: Minimum coverage required to pass the test. Default: 80
        :param omit_patterns: List of file patterns to omit from coverage. Default: []
        :param skip_covered: Skip reporting files that are covered. Default: false
        :param skip_empty: Skip reporting files that are empty. Default: true
        :param verbose: Run pytest with the ``--verbose`` flag. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__384e63be7810bf945d6fb782fc3c891fca1787094bf35586a2dcbb2d81ce2867)
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument min_coverage", value=min_coverage, expected_type=type_hints["min_coverage"])
            check_type(argname="argument omit_patterns", value=omit_patterns, expected_type=type_hints["omit_patterns"])
            check_type(argname="argument skip_covered", value=skip_covered, expected_type=type_hints["skip_covered"])
            check_type(argname="argument skip_empty", value=skip_empty, expected_type=type_hints["skip_empty"])
            check_type(argname="argument verbose", value=verbose, expected_type=type_hints["verbose"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if format is not None:
            self._values["format"] = format
        if min_coverage is not None:
            self._values["min_coverage"] = min_coverage
        if omit_patterns is not None:
            self._values["omit_patterns"] = omit_patterns
        if skip_covered is not None:
            self._values["skip_covered"] = skip_covered
        if skip_empty is not None:
            self._values["skip_empty"] = skip_empty
        if verbose is not None:
            self._values["verbose"] = verbose

    @builtins.property
    def format(self) -> typing.Optional[builtins.str]:
        '''Coverage report format.

        :default: 'text'
        '''
        result = self._values.get("format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_coverage(self) -> typing.Optional[jsii.Number]:
        '''Minimum coverage required to pass the test.

        :default: 80
        '''
        result = self._values.get("min_coverage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def omit_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of file patterns to omit from coverage.

        :default: []
        '''
        result = self._values.get("omit_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def skip_covered(self) -> typing.Optional[builtins.bool]:
        '''Skip reporting files that are covered.

        :default: false
        '''
        result = self._values.get("skip_covered")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def skip_empty(self) -> typing.Optional[builtins.bool]:
        '''Skip reporting files that are empty.

        :default: true
        '''
        result = self._values.get("skip_empty")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def verbose(self) -> typing.Optional[builtins.bool]:
        '''Run pytest with the ``--verbose`` flag.

        :default: true
        '''
        result = self._values.get("verbose")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PyTestOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PythonBasicProject(
    _projen_04054675.Project,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen-practical-constructs.PythonBasicProject",
):
    '''Python project with basic configurations for linting, testing, building etc.

    :pjid: python_basic
    '''

    def __init__(
        self,
        *,
        deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        dev_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        lint: typing.Optional[typing.Union["LintOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        sample: typing.Optional[builtins.bool] = None,
        test: typing.Optional[typing.Union["TestOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        name: builtins.str,
        commit_generated: typing.Optional[builtins.bool] = None,
        git_ignore_options: typing.Optional[typing.Union[_projen_04054675.IgnoreFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        git_options: typing.Optional[typing.Union[_projen_04054675.GitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        logging: typing.Optional[typing.Union[_projen_04054675.LoggerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        outdir: typing.Optional[builtins.str] = None,
        parent: typing.Optional[_projen_04054675.Project] = None,
        projen_command: typing.Optional[builtins.str] = None,
        projenrc_json: typing.Optional[builtins.bool] = None,
        projenrc_json_options: typing.Optional[typing.Union[_projen_04054675.ProjenrcJsonOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        renovatebot: typing.Optional[builtins.bool] = None,
        renovatebot_options: typing.Optional[typing.Union[_projen_04054675.RenovatebotOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        package: typing.Optional[typing.Union["PackageOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        pip: typing.Optional[typing.Union[PipOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        attach_tasks_to: typing.Optional[builtins.str] = None,
        venv_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param deps: Package dependencies in format ``['package==1.0.0', 'package2==2.0.0']``.
        :param dev_deps: Development dependencies in format ``['package==1.0.0', 'package2==2.0.0']``.
        :param lint: Linting configurations such as rules selected etc.
        :param sample: Create sample code and test (if dir doesn't exist yet). Default: true
        :param test: Test configurations.
        :param name: (experimental) This is the name of your project. Default: $BASEDIR
        :param commit_generated: (experimental) Whether to commit the managed files by default. Default: true
        :param git_ignore_options: (experimental) Configuration options for .gitignore file.
        :param git_options: (experimental) Configuration options for git.
        :param logging: (experimental) Configure logging options such as verbosity. Default: {}
        :param outdir: (experimental) The root directory of the project. Relative to this directory, all files are synthesized. If this project has a parent, this directory is relative to the parent directory and it cannot be the same as the parent or any of it's other subprojects. Default: "."
        :param parent: (experimental) The parent project, if this project is part of a bigger project.
        :param projen_command: (experimental) The shell command to use in order to run the projen CLI. Can be used to customize in special environments. Default: "npx projen"
        :param projenrc_json: (experimental) Generate (once) .projenrc.json (in JSON). Set to ``false`` in order to disable .projenrc.json generation. Default: false
        :param projenrc_json_options: (experimental) Options for .projenrc.json. Default: - default options
        :param renovatebot: (experimental) Use renovatebot to handle dependency upgrades. Default: false
        :param renovatebot_options: (experimental) Options for renovatebot. Default: - default options
        :param package: 
        :param pip: 
        :param attach_tasks_to: Existing task to attach new tasks to. It will be included as "spawn" tasks in new steps
        :param venv_path: Path to the python virtual environment directory used in this project. Default: .venv
        '''
        options = PythonBasicOptions(
            deps=deps,
            dev_deps=dev_deps,
            lint=lint,
            sample=sample,
            test=test,
            name=name,
            commit_generated=commit_generated,
            git_ignore_options=git_ignore_options,
            git_options=git_options,
            logging=logging,
            outdir=outdir,
            parent=parent,
            projen_command=projen_command,
            projenrc_json=projenrc_json,
            projenrc_json_options=projenrc_json_options,
            renovatebot=renovatebot,
            renovatebot_options=renovatebot_options,
            package=package,
            pip=pip,
            attach_tasks_to=attach_tasks_to,
            venv_path=venv_path,
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="addDep")
    def add_dep(self, package_name_version: builtins.str) -> None:
        '''Add a runtime dependency in format [package-name][==version] E.g: ``addDep('package==1.0.0')``.

        :param package_name_version: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c514a60a75f071c20ec30de634506e6c296b1d91b281bd1a0ff69ec8551d7bf7)
            check_type(argname="argument package_name_version", value=package_name_version, expected_type=type_hints["package_name_version"])
        return typing.cast(None, jsii.invoke(self, "addDep", [package_name_version]))

    @jsii.member(jsii_name="addDevDep")
    def add_dev_dep(self, package_name_version: builtins.str) -> None:
        '''Add a development dependency in format [package-name][==version].

        :param package_name_version: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6803cea798ee4a60e65efc9b0cc675daf469d702cfb43e7595aed132004e56e3)
            check_type(argname="argument package_name_version", value=package_name_version, expected_type=type_hints["package_name_version"])
        return typing.cast(None, jsii.invoke(self, "addDevDep", [package_name_version]))


class PythonBasicSample(
    _projen_04054675.Component,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen-practical-constructs.PythonBasicSample",
):
    '''Python code sample.'''

    def __init__(self, project: _projen_04054675.Project) -> None:
        '''
        :param project: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f89bc9b2d760f7dbf6c765c850ee98f08ad2b9abd29b30723839469f113ac71)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        jsii.create(self.__class__, self, [project])


class PythonVersionFile(
    _projen_04054675.FileBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen-practical-constructs.PythonVersionFile",
):
    def __init__(
        self,
        project: _projen_04054675.Project,
        *,
        python_version: builtins.str,
    ) -> None:
        '''
        :param project: -
        :param python_version: The version of Python to be added to the file.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b56632f9602060a9026f4ff094af75115f54480ed5cffe451781d662b51d31f1)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        opts = PythonVersionOptions(python_version=python_version)

        jsii.create(self.__class__, self, [project, opts])

    @jsii.member(jsii_name="synthesizeContent")
    def _synthesize_content(
        self,
        _resolver: _projen_04054675.IResolver,
    ) -> typing.Optional[builtins.str]:
        '''Implemented by derived classes and returns the contents of the file to emit.

        :param _resolver: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3eb4c7d952a99bdea958131725c8145a2e4d0ef325b48ac55d83275c5cdd0c0)
            check_type(argname="argument _resolver", value=_resolver, expected_type=type_hints["_resolver"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "synthesizeContent", [_resolver]))


@jsii.data_type(
    jsii_type="projen-practical-constructs.PythonVersionOptions",
    jsii_struct_bases=[],
    name_mapping={"python_version": "pythonVersion"},
)
class PythonVersionOptions:
    def __init__(self, *, python_version: builtins.str) -> None:
        '''
        :param python_version: The version of Python to be added to the file.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fb02140f15e42d4186643add56e5f0ffe0d004d6540a470bf2ae03d136a627b)
            check_type(argname="argument python_version", value=python_version, expected_type=type_hints["python_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "python_version": python_version,
        }

    @builtins.property
    def python_version(self) -> builtins.str:
        '''The version of Python to be added to the file.

        :required: true
        '''
        result = self._values.get("python_version")
        assert result is not None, "Required property 'python_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PythonVersionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ReadmeFile(
    _projen_04054675.Component,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen-practical-constructs.ReadmeFile",
):
    def __init__(
        self,
        project: _projen_04054675.Project,
        *,
        project_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param project: -
        :param project_name: 
        :param description: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e121cdedc0beed1c682d7a460ce0e7ed3201b3597d0675df06b9bc467a25a42)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        opts = ReadmeOptions(project_name=project_name, description=description)

        jsii.create(self.__class__, self, [project, opts])


@jsii.data_type(
    jsii_type="projen-practical-constructs.ReadmeOptions",
    jsii_struct_bases=[],
    name_mapping={"project_name": "projectName", "description": "description"},
)
class ReadmeOptions:
    def __init__(
        self,
        *,
        project_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param project_name: 
        :param description: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f16ff3cf7a0826918909ecb12dfd4f0ec1385aa6bdc84176767f6109162ecdc)
            check_type(argname="argument project_name", value=project_name, expected_type=type_hints["project_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "project_name": project_name,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def project_name(self) -> builtins.str:
        result = self._values.get("project_name")
        assert result is not None, "Required property 'project_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReadmeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Ruff(
    _projen_04054675.Component,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen-practical-constructs.Ruff",
):
    def __init__(
        self,
        project: _projen_04054675.Project,
        task_opts: typing.Union["TaskOptionsWithFix", typing.Dict[builtins.str, typing.Any]],
        *,
        attach_fix_task_to: typing.Optional[builtins.str] = None,
        add_to_existing_rules: typing.Optional[builtins.bool] = None,
        ignore_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
        mccabe_max_complexity: typing.Optional[jsii.Number] = None,
        per_file_ignores: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[builtins.str]]] = None,
        select_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
        target_python_version: typing.Optional[builtins.str] = None,
        unsafe_fixes: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param project: -
        :param task_opts: -
        :param attach_fix_task_to: Attach lint fix tasks to parent.
        :param add_to_existing_rules: Add rules defined here to the ignoreRules and selectRules (on top of the default rules) or replace them by this contents? Default: true
        :param ignore_rules: Default: pre-selected set of rules
        :param mccabe_max_complexity: Default: 14
        :param per_file_ignores: Default: ignore doc-string code format for test files
        :param select_rules: Default: pre-selected set of rules
        :param target_python_version: Default: py313
        :param unsafe_fixes: Default: false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92e6719177912c0eae0ee85cfc203cb22854f3f273cc256898396282ba7d42fe)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument task_opts", value=task_opts, expected_type=type_hints["task_opts"])
        opts = RuffOptions(
            attach_fix_task_to=attach_fix_task_to,
            add_to_existing_rules=add_to_existing_rules,
            ignore_rules=ignore_rules,
            mccabe_max_complexity=mccabe_max_complexity,
            per_file_ignores=per_file_ignores,
            select_rules=select_rules,
            target_python_version=target_python_version,
            unsafe_fixes=unsafe_fixes,
        )

        jsii.create(self.__class__, self, [project, task_opts, opts])


class RuffTomlFile(
    _projen_04054675.TomlFile,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen-practical-constructs.RuffTomlFile",
):
    '''ruff.toml synthetisation.'''

    def __init__(
        self,
        project: _projen_04054675.Project,
        *,
        add_to_existing_rules: typing.Optional[builtins.bool] = None,
        ignore_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
        mccabe_max_complexity: typing.Optional[jsii.Number] = None,
        per_file_ignores: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[builtins.str]]] = None,
        select_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
        target_python_version: typing.Optional[builtins.str] = None,
        unsafe_fixes: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param project: -
        :param add_to_existing_rules: Add rules defined here to the ignoreRules and selectRules (on top of the default rules) or replace them by this contents? Default: true
        :param ignore_rules: Default: pre-selected set of rules
        :param mccabe_max_complexity: Default: 14
        :param per_file_ignores: Default: ignore doc-string code format for test files
        :param select_rules: Default: pre-selected set of rules
        :param target_python_version: Default: py313
        :param unsafe_fixes: Default: false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__515cf86a84df0b6b18941ab4c2a73e7eef40e0260fab3c698c6cabcef8227d71)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        opts = RuffTomlFileOptions(
            add_to_existing_rules=add_to_existing_rules,
            ignore_rules=ignore_rules,
            mccabe_max_complexity=mccabe_max_complexity,
            per_file_ignores=per_file_ignores,
            select_rules=select_rules,
            target_python_version=target_python_version,
            unsafe_fixes=unsafe_fixes,
        )

        jsii.create(self.__class__, self, [project, opts])


@jsii.data_type(
    jsii_type="projen-practical-constructs.RuffTomlFileOptions",
    jsii_struct_bases=[],
    name_mapping={
        "add_to_existing_rules": "addToExistingRules",
        "ignore_rules": "ignoreRules",
        "mccabe_max_complexity": "mccabeMaxComplexity",
        "per_file_ignores": "perFileIgnores",
        "select_rules": "selectRules",
        "target_python_version": "targetPythonVersion",
        "unsafe_fixes": "unsafeFixes",
    },
)
class RuffTomlFileOptions:
    def __init__(
        self,
        *,
        add_to_existing_rules: typing.Optional[builtins.bool] = None,
        ignore_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
        mccabe_max_complexity: typing.Optional[jsii.Number] = None,
        per_file_ignores: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[builtins.str]]] = None,
        select_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
        target_python_version: typing.Optional[builtins.str] = None,
        unsafe_fixes: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param add_to_existing_rules: Add rules defined here to the ignoreRules and selectRules (on top of the default rules) or replace them by this contents? Default: true
        :param ignore_rules: Default: pre-selected set of rules
        :param mccabe_max_complexity: Default: 14
        :param per_file_ignores: Default: ignore doc-string code format for test files
        :param select_rules: Default: pre-selected set of rules
        :param target_python_version: Default: py313
        :param unsafe_fixes: Default: false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce7087163e4218666b985f90db1006536d982decdeb6854261778dfc1f07f506)
            check_type(argname="argument add_to_existing_rules", value=add_to_existing_rules, expected_type=type_hints["add_to_existing_rules"])
            check_type(argname="argument ignore_rules", value=ignore_rules, expected_type=type_hints["ignore_rules"])
            check_type(argname="argument mccabe_max_complexity", value=mccabe_max_complexity, expected_type=type_hints["mccabe_max_complexity"])
            check_type(argname="argument per_file_ignores", value=per_file_ignores, expected_type=type_hints["per_file_ignores"])
            check_type(argname="argument select_rules", value=select_rules, expected_type=type_hints["select_rules"])
            check_type(argname="argument target_python_version", value=target_python_version, expected_type=type_hints["target_python_version"])
            check_type(argname="argument unsafe_fixes", value=unsafe_fixes, expected_type=type_hints["unsafe_fixes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if add_to_existing_rules is not None:
            self._values["add_to_existing_rules"] = add_to_existing_rules
        if ignore_rules is not None:
            self._values["ignore_rules"] = ignore_rules
        if mccabe_max_complexity is not None:
            self._values["mccabe_max_complexity"] = mccabe_max_complexity
        if per_file_ignores is not None:
            self._values["per_file_ignores"] = per_file_ignores
        if select_rules is not None:
            self._values["select_rules"] = select_rules
        if target_python_version is not None:
            self._values["target_python_version"] = target_python_version
        if unsafe_fixes is not None:
            self._values["unsafe_fixes"] = unsafe_fixes

    @builtins.property
    def add_to_existing_rules(self) -> typing.Optional[builtins.bool]:
        '''Add rules defined here to the ignoreRules and selectRules (on top of the default rules) or replace them by this contents?

        :default: true
        '''
        result = self._values.get("add_to_existing_rules")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ignore_rules(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :default: pre-selected set of rules
        '''
        result = self._values.get("ignore_rules")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def mccabe_max_complexity(self) -> typing.Optional[jsii.Number]:
        '''
        :default: 14
        '''
        result = self._values.get("mccabe_max_complexity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def per_file_ignores(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.List[builtins.str]]]:
        '''
        :default: ignore doc-string code format for test files
        '''
        result = self._values.get("per_file_ignores")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.List[builtins.str]]], result)

    @builtins.property
    def select_rules(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :default: pre-selected set of rules
        '''
        result = self._values.get("select_rules")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def target_python_version(self) -> typing.Optional[builtins.str]:
        '''
        :default: py313
        '''
        result = self._values.get("target_python_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def unsafe_fixes(self) -> typing.Optional[builtins.bool]:
        '''
        :default: false
        '''
        result = self._values.get("unsafe_fixes")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RuffTomlFileOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen-practical-constructs.TaskOptions",
    jsii_struct_bases=[],
    name_mapping={"venv_path": "venvPath", "attach_tasks_to": "attachTasksTo"},
)
class TaskOptions:
    def __init__(
        self,
        *,
        venv_path: builtins.str,
        attach_tasks_to: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param venv_path: Path to the python virtual environment directory used in this project.
        :param attach_tasks_to: Existing task to attach new tasks to. It will be included as "spawn" tasks in new steps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60bbd600395432f8000b4758eea0d98c9c8e225b40399a70f2bd14d84ef3bb0f)
            check_type(argname="argument venv_path", value=venv_path, expected_type=type_hints["venv_path"])
            check_type(argname="argument attach_tasks_to", value=attach_tasks_to, expected_type=type_hints["attach_tasks_to"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "venv_path": venv_path,
        }
        if attach_tasks_to is not None:
            self._values["attach_tasks_to"] = attach_tasks_to

    @builtins.property
    def venv_path(self) -> builtins.str:
        '''Path to the python virtual environment directory used in this project.'''
        result = self._values.get("venv_path")
        assert result is not None, "Required property 'venv_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attach_tasks_to(self) -> typing.Optional[builtins.str]:
        '''Existing task to attach new tasks to.

        It will be included as "spawn" tasks in new steps
        '''
        result = self._values.get("attach_tasks_to")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen-practical-constructs.TaskOptionsTarget",
    jsii_struct_bases=[],
    name_mapping={"attach_tasks_to": "attachTasksTo", "venv_path": "venvPath"},
)
class TaskOptionsTarget:
    def __init__(
        self,
        *,
        attach_tasks_to: typing.Optional[builtins.str] = None,
        venv_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param attach_tasks_to: Existing task to attach new tasks to. It will be included as "spawn" tasks in new steps
        :param venv_path: Path to the python virtual environment directory used in this project. Default: .venv
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ebef6526107b290f8f3024aa58a74f546f6c2dcee9f6faa53295f3c7402ac4a)
            check_type(argname="argument attach_tasks_to", value=attach_tasks_to, expected_type=type_hints["attach_tasks_to"])
            check_type(argname="argument venv_path", value=venv_path, expected_type=type_hints["venv_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attach_tasks_to is not None:
            self._values["attach_tasks_to"] = attach_tasks_to
        if venv_path is not None:
            self._values["venv_path"] = venv_path

    @builtins.property
    def attach_tasks_to(self) -> typing.Optional[builtins.str]:
        '''Existing task to attach new tasks to.

        It will be included as "spawn" tasks in new steps
        '''
        result = self._values.get("attach_tasks_to")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def venv_path(self) -> typing.Optional[builtins.str]:
        '''Path to the python virtual environment directory used in this project.

        :default: .venv
        '''
        result = self._values.get("venv_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskOptionsTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen-practical-constructs.TaskOptionsWithFix",
    jsii_struct_bases=[TaskOptions],
    name_mapping={
        "venv_path": "venvPath",
        "attach_tasks_to": "attachTasksTo",
        "attach_fix_tasks_to": "attachFixTasksTo",
    },
)
class TaskOptionsWithFix(TaskOptions):
    def __init__(
        self,
        *,
        venv_path: builtins.str,
        attach_tasks_to: typing.Optional[builtins.str] = None,
        attach_fix_tasks_to: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param venv_path: Path to the python virtual environment directory used in this project.
        :param attach_tasks_to: Existing task to attach new tasks to. It will be included as "spawn" tasks in new steps
        :param attach_fix_tasks_to: Attach task to fix.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e45cbb8bf0d46096fadb00e45bbfbb7e0f37f040d7543c11c8fece01826bd20)
            check_type(argname="argument venv_path", value=venv_path, expected_type=type_hints["venv_path"])
            check_type(argname="argument attach_tasks_to", value=attach_tasks_to, expected_type=type_hints["attach_tasks_to"])
            check_type(argname="argument attach_fix_tasks_to", value=attach_fix_tasks_to, expected_type=type_hints["attach_fix_tasks_to"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "venv_path": venv_path,
        }
        if attach_tasks_to is not None:
            self._values["attach_tasks_to"] = attach_tasks_to
        if attach_fix_tasks_to is not None:
            self._values["attach_fix_tasks_to"] = attach_fix_tasks_to

    @builtins.property
    def venv_path(self) -> builtins.str:
        '''Path to the python virtual environment directory used in this project.'''
        result = self._values.get("venv_path")
        assert result is not None, "Required property 'venv_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attach_tasks_to(self) -> typing.Optional[builtins.str]:
        '''Existing task to attach new tasks to.

        It will be included as "spawn" tasks in new steps
        '''
        result = self._values.get("attach_tasks_to")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def attach_fix_tasks_to(self) -> typing.Optional[builtins.str]:
        '''Attach task to fix.'''
        result = self._values.get("attach_fix_tasks_to")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskOptionsWithFix(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen-practical-constructs.TestOptions",
    jsii_struct_bases=[PyTestOptions],
    name_mapping={
        "format": "format",
        "min_coverage": "minCoverage",
        "omit_patterns": "omitPatterns",
        "skip_covered": "skipCovered",
        "skip_empty": "skipEmpty",
        "verbose": "verbose",
    },
)
class TestOptions(PyTestOptions):
    def __init__(
        self,
        *,
        format: typing.Optional[builtins.str] = None,
        min_coverage: typing.Optional[jsii.Number] = None,
        omit_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        skip_covered: typing.Optional[builtins.bool] = None,
        skip_empty: typing.Optional[builtins.bool] = None,
        verbose: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param format: Coverage report format. Default: 'text'
        :param min_coverage: Minimum coverage required to pass the test. Default: 80
        :param omit_patterns: List of file patterns to omit from coverage. Default: []
        :param skip_covered: Skip reporting files that are covered. Default: false
        :param skip_empty: Skip reporting files that are empty. Default: true
        :param verbose: Run pytest with the ``--verbose`` flag. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6ce63ffedc17816d4e10d303db52b112c4a018db5d7b81c720790d591a43e4e)
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument min_coverage", value=min_coverage, expected_type=type_hints["min_coverage"])
            check_type(argname="argument omit_patterns", value=omit_patterns, expected_type=type_hints["omit_patterns"])
            check_type(argname="argument skip_covered", value=skip_covered, expected_type=type_hints["skip_covered"])
            check_type(argname="argument skip_empty", value=skip_empty, expected_type=type_hints["skip_empty"])
            check_type(argname="argument verbose", value=verbose, expected_type=type_hints["verbose"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if format is not None:
            self._values["format"] = format
        if min_coverage is not None:
            self._values["min_coverage"] = min_coverage
        if omit_patterns is not None:
            self._values["omit_patterns"] = omit_patterns
        if skip_covered is not None:
            self._values["skip_covered"] = skip_covered
        if skip_empty is not None:
            self._values["skip_empty"] = skip_empty
        if verbose is not None:
            self._values["verbose"] = verbose

    @builtins.property
    def format(self) -> typing.Optional[builtins.str]:
        '''Coverage report format.

        :default: 'text'
        '''
        result = self._values.get("format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_coverage(self) -> typing.Optional[jsii.Number]:
        '''Minimum coverage required to pass the test.

        :default: 80
        '''
        result = self._values.get("min_coverage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def omit_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of file patterns to omit from coverage.

        :default: []
        '''
        result = self._values.get("omit_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def skip_covered(self) -> typing.Optional[builtins.bool]:
        '''Skip reporting files that are covered.

        :default: false
        '''
        result = self._values.get("skip_covered")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def skip_empty(self) -> typing.Optional[builtins.bool]:
        '''Skip reporting files that are empty.

        :default: true
        '''
        result = self._values.get("skip_empty")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def verbose(self) -> typing.Optional[builtins.bool]:
        '''Run pytest with the ``--verbose`` flag.

        :default: true
        '''
        result = self._values.get("verbose")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TestOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TestTarget(
    _projen_04054675.Component,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen-practical-constructs.TestTarget",
):
    '''Python project lint configurations.'''

    def __init__(
        self,
        project: _projen_04054675.Project,
        task_opts: typing.Union[TaskOptions, typing.Dict[builtins.str, typing.Any]],
        *,
        format: typing.Optional[builtins.str] = None,
        min_coverage: typing.Optional[jsii.Number] = None,
        omit_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        skip_covered: typing.Optional[builtins.bool] = None,
        skip_empty: typing.Optional[builtins.bool] = None,
        verbose: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param project: -
        :param task_opts: -
        :param format: Coverage report format. Default: 'text'
        :param min_coverage: Minimum coverage required to pass the test. Default: 80
        :param omit_patterns: List of file patterns to omit from coverage. Default: []
        :param skip_covered: Skip reporting files that are covered. Default: false
        :param skip_empty: Skip reporting files that are empty. Default: true
        :param verbose: Run pytest with the ``--verbose`` flag. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0658c3d7fe54aaec02fcef6987c7705125d952a65e7b4f1cde8ad8b0b36e7aa8)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument task_opts", value=task_opts, expected_type=type_hints["task_opts"])
        opts = TestOptions(
            format=format,
            min_coverage=min_coverage,
            omit_patterns=omit_patterns,
            skip_covered=skip_covered,
            skip_empty=skip_empty,
            verbose=verbose,
        )

        jsii.create(self.__class__, self, [project, task_opts, opts])


@jsii.data_type(
    jsii_type="projen-practical-constructs.PackageOptions",
    jsii_struct_bases=[PyProjectTomlOptions],
    name_mapping={
        "author_email": "authorEmail",
        "author_name": "authorName",
        "classifiers": "classifiers",
        "description": "description",
        "homepage": "homepage",
        "keywords": "keywords",
        "license_file": "licenseFile",
        "package_name": "packageName",
        "readme": "readme",
        "requires_python": "requiresPython",
        "version": "version",
        "license": "license",
    },
)
class PackageOptions(PyProjectTomlOptions):
    def __init__(
        self,
        *,
        author_email: typing.Optional[builtins.str] = None,
        author_name: typing.Optional[builtins.str] = None,
        classifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        homepage: typing.Optional[builtins.str] = None,
        keywords: typing.Optional[typing.Sequence[builtins.str]] = None,
        license_file: typing.Optional[builtins.str] = None,
        package_name: typing.Optional[builtins.str] = None,
        readme: typing.Optional[builtins.str] = None,
        requires_python: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
        license: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param author_email: Author's e-mail.
        :param author_name: Author's name.
        :param classifiers: A list of PyPI trove classifiers that describe the project.
        :param description: A short description of the package.
        :param homepage: A URL to the website of the project.
        :param keywords: Keywords to add to the package.
        :param license_file: License file.
        :param package_name: Name of the python package. E.g. "my_python_package". Must only consist of alphanumeric characters and underscores. Default: Name of the directory
        :param readme: README file.
        :param requires_python: Python version required to run this package.
        :param version: Version of the package.
        :param license: License name in spdx format. e.g: ``MIT``, ``Apache-2.0``
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__769a6aad7aea164b73af332f179b064a5d119bdb8838de929422452d3b88c50c)
            check_type(argname="argument author_email", value=author_email, expected_type=type_hints["author_email"])
            check_type(argname="argument author_name", value=author_name, expected_type=type_hints["author_name"])
            check_type(argname="argument classifiers", value=classifiers, expected_type=type_hints["classifiers"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument homepage", value=homepage, expected_type=type_hints["homepage"])
            check_type(argname="argument keywords", value=keywords, expected_type=type_hints["keywords"])
            check_type(argname="argument license_file", value=license_file, expected_type=type_hints["license_file"])
            check_type(argname="argument package_name", value=package_name, expected_type=type_hints["package_name"])
            check_type(argname="argument readme", value=readme, expected_type=type_hints["readme"])
            check_type(argname="argument requires_python", value=requires_python, expected_type=type_hints["requires_python"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument license", value=license, expected_type=type_hints["license"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if author_email is not None:
            self._values["author_email"] = author_email
        if author_name is not None:
            self._values["author_name"] = author_name
        if classifiers is not None:
            self._values["classifiers"] = classifiers
        if description is not None:
            self._values["description"] = description
        if homepage is not None:
            self._values["homepage"] = homepage
        if keywords is not None:
            self._values["keywords"] = keywords
        if license_file is not None:
            self._values["license_file"] = license_file
        if package_name is not None:
            self._values["package_name"] = package_name
        if readme is not None:
            self._values["readme"] = readme
        if requires_python is not None:
            self._values["requires_python"] = requires_python
        if version is not None:
            self._values["version"] = version
        if license is not None:
            self._values["license"] = license

    @builtins.property
    def author_email(self) -> typing.Optional[builtins.str]:
        '''Author's e-mail.'''
        result = self._values.get("author_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def author_name(self) -> typing.Optional[builtins.str]:
        '''Author's name.'''
        result = self._values.get("author_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def classifiers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of PyPI trove classifiers that describe the project.

        :see: https://pypi.org/classifiers/
        '''
        result = self._values.get("classifiers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A short description of the package.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def homepage(self) -> typing.Optional[builtins.str]:
        '''A URL to the website of the project.'''
        result = self._values.get("homepage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keywords(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Keywords to add to the package.'''
        result = self._values.get("keywords")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def license_file(self) -> typing.Optional[builtins.str]:
        '''License file.'''
        result = self._values.get("license_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def package_name(self) -> typing.Optional[builtins.str]:
        '''Name of the python package.

        E.g. "my_python_package".
        Must only consist of alphanumeric characters and underscores.

        :default: Name of the directory
        '''
        result = self._values.get("package_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def readme(self) -> typing.Optional[builtins.str]:
        '''README file.'''
        result = self._values.get("readme")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def requires_python(self) -> typing.Optional[builtins.str]:
        '''Python version required to run this package.'''
        result = self._values.get("requires_python")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version of the package.'''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def license(self) -> typing.Optional[builtins.str]:
        '''License name in spdx format.

        e.g: ``MIT``, ``Apache-2.0``
        '''
        result = self._values.get("license")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PackageOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen-practical-constructs.PythonBasicOptions",
    jsii_struct_bases=[
        _projen_04054675.ProjectOptions, Build0Options, TaskOptionsTarget
    ],
    name_mapping={
        "name": "name",
        "commit_generated": "commitGenerated",
        "git_ignore_options": "gitIgnoreOptions",
        "git_options": "gitOptions",
        "logging": "logging",
        "outdir": "outdir",
        "parent": "parent",
        "projen_command": "projenCommand",
        "projenrc_json": "projenrcJson",
        "projenrc_json_options": "projenrcJsonOptions",
        "renovatebot": "renovatebot",
        "renovatebot_options": "renovatebotOptions",
        "package": "package",
        "pip": "pip",
        "attach_tasks_to": "attachTasksTo",
        "venv_path": "venvPath",
        "deps": "deps",
        "dev_deps": "devDeps",
        "lint": "lint",
        "sample": "sample",
        "test": "test",
    },
)
class PythonBasicOptions(
    _projen_04054675.ProjectOptions,
    Build0Options,
    TaskOptionsTarget,
):
    def __init__(
        self,
        *,
        name: builtins.str,
        commit_generated: typing.Optional[builtins.bool] = None,
        git_ignore_options: typing.Optional[typing.Union[_projen_04054675.IgnoreFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        git_options: typing.Optional[typing.Union[_projen_04054675.GitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        logging: typing.Optional[typing.Union[_projen_04054675.LoggerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        outdir: typing.Optional[builtins.str] = None,
        parent: typing.Optional[_projen_04054675.Project] = None,
        projen_command: typing.Optional[builtins.str] = None,
        projenrc_json: typing.Optional[builtins.bool] = None,
        projenrc_json_options: typing.Optional[typing.Union[_projen_04054675.ProjenrcJsonOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        renovatebot: typing.Optional[builtins.bool] = None,
        renovatebot_options: typing.Optional[typing.Union[_projen_04054675.RenovatebotOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        package: typing.Optional[typing.Union[PackageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        pip: typing.Optional[typing.Union[PipOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        attach_tasks_to: typing.Optional[builtins.str] = None,
        venv_path: typing.Optional[builtins.str] = None,
        deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        dev_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
        lint: typing.Optional[typing.Union["LintOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        sample: typing.Optional[builtins.bool] = None,
        test: typing.Optional[typing.Union[TestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: (experimental) This is the name of your project. Default: $BASEDIR
        :param commit_generated: (experimental) Whether to commit the managed files by default. Default: true
        :param git_ignore_options: (experimental) Configuration options for .gitignore file.
        :param git_options: (experimental) Configuration options for git.
        :param logging: (experimental) Configure logging options such as verbosity. Default: {}
        :param outdir: (experimental) The root directory of the project. Relative to this directory, all files are synthesized. If this project has a parent, this directory is relative to the parent directory and it cannot be the same as the parent or any of it's other subprojects. Default: "."
        :param parent: (experimental) The parent project, if this project is part of a bigger project.
        :param projen_command: (experimental) The shell command to use in order to run the projen CLI. Can be used to customize in special environments. Default: "npx projen"
        :param projenrc_json: (experimental) Generate (once) .projenrc.json (in JSON). Set to ``false`` in order to disable .projenrc.json generation. Default: false
        :param projenrc_json_options: (experimental) Options for .projenrc.json. Default: - default options
        :param renovatebot: (experimental) Use renovatebot to handle dependency upgrades. Default: false
        :param renovatebot_options: (experimental) Options for renovatebot. Default: - default options
        :param package: 
        :param pip: 
        :param attach_tasks_to: Existing task to attach new tasks to. It will be included as "spawn" tasks in new steps
        :param venv_path: Path to the python virtual environment directory used in this project. Default: .venv
        :param deps: Package dependencies in format ``['package==1.0.0', 'package2==2.0.0']``.
        :param dev_deps: Development dependencies in format ``['package==1.0.0', 'package2==2.0.0']``.
        :param lint: Linting configurations such as rules selected etc.
        :param sample: Create sample code and test (if dir doesn't exist yet). Default: true
        :param test: Test configurations.
        '''
        if isinstance(git_ignore_options, dict):
            git_ignore_options = _projen_04054675.IgnoreFileOptions(**git_ignore_options)
        if isinstance(git_options, dict):
            git_options = _projen_04054675.GitOptions(**git_options)
        if isinstance(logging, dict):
            logging = _projen_04054675.LoggerOptions(**logging)
        if isinstance(projenrc_json_options, dict):
            projenrc_json_options = _projen_04054675.ProjenrcJsonOptions(**projenrc_json_options)
        if isinstance(renovatebot_options, dict):
            renovatebot_options = _projen_04054675.RenovatebotOptions(**renovatebot_options)
        if isinstance(package, dict):
            package = PackageOptions(**package)
        if isinstance(pip, dict):
            pip = PipOptions(**pip)
        if isinstance(lint, dict):
            lint = LintOptions(**lint)
        if isinstance(test, dict):
            test = TestOptions(**test)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c54d357164afec478ab317ef798bb3d8a0ac8c35182918abf6dfd0025c70bc86)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument commit_generated", value=commit_generated, expected_type=type_hints["commit_generated"])
            check_type(argname="argument git_ignore_options", value=git_ignore_options, expected_type=type_hints["git_ignore_options"])
            check_type(argname="argument git_options", value=git_options, expected_type=type_hints["git_options"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument outdir", value=outdir, expected_type=type_hints["outdir"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument projen_command", value=projen_command, expected_type=type_hints["projen_command"])
            check_type(argname="argument projenrc_json", value=projenrc_json, expected_type=type_hints["projenrc_json"])
            check_type(argname="argument projenrc_json_options", value=projenrc_json_options, expected_type=type_hints["projenrc_json_options"])
            check_type(argname="argument renovatebot", value=renovatebot, expected_type=type_hints["renovatebot"])
            check_type(argname="argument renovatebot_options", value=renovatebot_options, expected_type=type_hints["renovatebot_options"])
            check_type(argname="argument package", value=package, expected_type=type_hints["package"])
            check_type(argname="argument pip", value=pip, expected_type=type_hints["pip"])
            check_type(argname="argument attach_tasks_to", value=attach_tasks_to, expected_type=type_hints["attach_tasks_to"])
            check_type(argname="argument venv_path", value=venv_path, expected_type=type_hints["venv_path"])
            check_type(argname="argument deps", value=deps, expected_type=type_hints["deps"])
            check_type(argname="argument dev_deps", value=dev_deps, expected_type=type_hints["dev_deps"])
            check_type(argname="argument lint", value=lint, expected_type=type_hints["lint"])
            check_type(argname="argument sample", value=sample, expected_type=type_hints["sample"])
            check_type(argname="argument test", value=test, expected_type=type_hints["test"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if commit_generated is not None:
            self._values["commit_generated"] = commit_generated
        if git_ignore_options is not None:
            self._values["git_ignore_options"] = git_ignore_options
        if git_options is not None:
            self._values["git_options"] = git_options
        if logging is not None:
            self._values["logging"] = logging
        if outdir is not None:
            self._values["outdir"] = outdir
        if parent is not None:
            self._values["parent"] = parent
        if projen_command is not None:
            self._values["projen_command"] = projen_command
        if projenrc_json is not None:
            self._values["projenrc_json"] = projenrc_json
        if projenrc_json_options is not None:
            self._values["projenrc_json_options"] = projenrc_json_options
        if renovatebot is not None:
            self._values["renovatebot"] = renovatebot
        if renovatebot_options is not None:
            self._values["renovatebot_options"] = renovatebot_options
        if package is not None:
            self._values["package"] = package
        if pip is not None:
            self._values["pip"] = pip
        if attach_tasks_to is not None:
            self._values["attach_tasks_to"] = attach_tasks_to
        if venv_path is not None:
            self._values["venv_path"] = venv_path
        if deps is not None:
            self._values["deps"] = deps
        if dev_deps is not None:
            self._values["dev_deps"] = dev_deps
        if lint is not None:
            self._values["lint"] = lint
        if sample is not None:
            self._values["sample"] = sample
        if test is not None:
            self._values["test"] = test

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) This is the name of your project.

        :default: $BASEDIR

        :stability: experimental
        :featured: true
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def commit_generated(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to commit the managed files by default.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("commit_generated")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def git_ignore_options(self) -> typing.Optional[_projen_04054675.IgnoreFileOptions]:
        '''(experimental) Configuration options for .gitignore file.

        :stability: experimental
        '''
        result = self._values.get("git_ignore_options")
        return typing.cast(typing.Optional[_projen_04054675.IgnoreFileOptions], result)

    @builtins.property
    def git_options(self) -> typing.Optional[_projen_04054675.GitOptions]:
        '''(experimental) Configuration options for git.

        :stability: experimental
        '''
        result = self._values.get("git_options")
        return typing.cast(typing.Optional[_projen_04054675.GitOptions], result)

    @builtins.property
    def logging(self) -> typing.Optional[_projen_04054675.LoggerOptions]:
        '''(experimental) Configure logging options such as verbosity.

        :default: {}

        :stability: experimental
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[_projen_04054675.LoggerOptions], result)

    @builtins.property
    def outdir(self) -> typing.Optional[builtins.str]:
        '''(experimental) The root directory of the project.

        Relative to this directory, all files are synthesized.

        If this project has a parent, this directory is relative to the parent
        directory and it cannot be the same as the parent or any of it's other
        subprojects.

        :default: "."

        :stability: experimental
        '''
        result = self._values.get("outdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent(self) -> typing.Optional[_projen_04054675.Project]:
        '''(experimental) The parent project, if this project is part of a bigger project.

        :stability: experimental
        '''
        result = self._values.get("parent")
        return typing.cast(typing.Optional[_projen_04054675.Project], result)

    @builtins.property
    def projen_command(self) -> typing.Optional[builtins.str]:
        '''(experimental) The shell command to use in order to run the projen CLI.

        Can be used to customize in special environments.

        :default: "npx projen"

        :stability: experimental
        '''
        result = self._values.get("projen_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def projenrc_json(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Generate (once) .projenrc.json (in JSON). Set to ``false`` in order to disable .projenrc.json generation.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("projenrc_json")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def projenrc_json_options(
        self,
    ) -> typing.Optional[_projen_04054675.ProjenrcJsonOptions]:
        '''(experimental) Options for .projenrc.json.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("projenrc_json_options")
        return typing.cast(typing.Optional[_projen_04054675.ProjenrcJsonOptions], result)

    @builtins.property
    def renovatebot(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use renovatebot to handle dependency upgrades.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("renovatebot")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def renovatebot_options(
        self,
    ) -> typing.Optional[_projen_04054675.RenovatebotOptions]:
        '''(experimental) Options for renovatebot.

        :default: - default options

        :stability: experimental
        '''
        result = self._values.get("renovatebot_options")
        return typing.cast(typing.Optional[_projen_04054675.RenovatebotOptions], result)

    @builtins.property
    def package(self) -> typing.Optional[PackageOptions]:
        result = self._values.get("package")
        return typing.cast(typing.Optional[PackageOptions], result)

    @builtins.property
    def pip(self) -> typing.Optional[PipOptions]:
        result = self._values.get("pip")
        return typing.cast(typing.Optional[PipOptions], result)

    @builtins.property
    def attach_tasks_to(self) -> typing.Optional[builtins.str]:
        '''Existing task to attach new tasks to.

        It will be included as "spawn" tasks in new steps
        '''
        result = self._values.get("attach_tasks_to")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def venv_path(self) -> typing.Optional[builtins.str]:
        '''Path to the python virtual environment directory used in this project.

        :default: .venv
        '''
        result = self._values.get("venv_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Package dependencies in format ``['package==1.0.0', 'package2==2.0.0']``.'''
        result = self._values.get("deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dev_deps(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Development dependencies in format ``['package==1.0.0', 'package2==2.0.0']``.'''
        result = self._values.get("dev_deps")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def lint(self) -> typing.Optional["LintOptions"]:
        '''Linting configurations such as rules selected etc.'''
        result = self._values.get("lint")
        return typing.cast(typing.Optional["LintOptions"], result)

    @builtins.property
    def sample(self) -> typing.Optional[builtins.bool]:
        '''Create sample code and test (if dir doesn't exist yet).

        :default: true
        '''
        result = self._values.get("sample")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def test(self) -> typing.Optional[TestOptions]:
        '''Test configurations.'''
        result = self._values.get("test")
        return typing.cast(typing.Optional[TestOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PythonBasicOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen-practical-constructs.RuffOptions",
    jsii_struct_bases=[RuffTomlFileOptions],
    name_mapping={
        "add_to_existing_rules": "addToExistingRules",
        "ignore_rules": "ignoreRules",
        "mccabe_max_complexity": "mccabeMaxComplexity",
        "per_file_ignores": "perFileIgnores",
        "select_rules": "selectRules",
        "target_python_version": "targetPythonVersion",
        "unsafe_fixes": "unsafeFixes",
        "attach_fix_task_to": "attachFixTaskTo",
    },
)
class RuffOptions(RuffTomlFileOptions):
    def __init__(
        self,
        *,
        add_to_existing_rules: typing.Optional[builtins.bool] = None,
        ignore_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
        mccabe_max_complexity: typing.Optional[jsii.Number] = None,
        per_file_ignores: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[builtins.str]]] = None,
        select_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
        target_python_version: typing.Optional[builtins.str] = None,
        unsafe_fixes: typing.Optional[builtins.bool] = None,
        attach_fix_task_to: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param add_to_existing_rules: Add rules defined here to the ignoreRules and selectRules (on top of the default rules) or replace them by this contents? Default: true
        :param ignore_rules: Default: pre-selected set of rules
        :param mccabe_max_complexity: Default: 14
        :param per_file_ignores: Default: ignore doc-string code format for test files
        :param select_rules: Default: pre-selected set of rules
        :param target_python_version: Default: py313
        :param unsafe_fixes: Default: false
        :param attach_fix_task_to: Attach lint fix tasks to parent.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d207008bfccd269e92e2aa9ed31161d7e45bab33efb79344ae36a97c2eddcff)
            check_type(argname="argument add_to_existing_rules", value=add_to_existing_rules, expected_type=type_hints["add_to_existing_rules"])
            check_type(argname="argument ignore_rules", value=ignore_rules, expected_type=type_hints["ignore_rules"])
            check_type(argname="argument mccabe_max_complexity", value=mccabe_max_complexity, expected_type=type_hints["mccabe_max_complexity"])
            check_type(argname="argument per_file_ignores", value=per_file_ignores, expected_type=type_hints["per_file_ignores"])
            check_type(argname="argument select_rules", value=select_rules, expected_type=type_hints["select_rules"])
            check_type(argname="argument target_python_version", value=target_python_version, expected_type=type_hints["target_python_version"])
            check_type(argname="argument unsafe_fixes", value=unsafe_fixes, expected_type=type_hints["unsafe_fixes"])
            check_type(argname="argument attach_fix_task_to", value=attach_fix_task_to, expected_type=type_hints["attach_fix_task_to"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if add_to_existing_rules is not None:
            self._values["add_to_existing_rules"] = add_to_existing_rules
        if ignore_rules is not None:
            self._values["ignore_rules"] = ignore_rules
        if mccabe_max_complexity is not None:
            self._values["mccabe_max_complexity"] = mccabe_max_complexity
        if per_file_ignores is not None:
            self._values["per_file_ignores"] = per_file_ignores
        if select_rules is not None:
            self._values["select_rules"] = select_rules
        if target_python_version is not None:
            self._values["target_python_version"] = target_python_version
        if unsafe_fixes is not None:
            self._values["unsafe_fixes"] = unsafe_fixes
        if attach_fix_task_to is not None:
            self._values["attach_fix_task_to"] = attach_fix_task_to

    @builtins.property
    def add_to_existing_rules(self) -> typing.Optional[builtins.bool]:
        '''Add rules defined here to the ignoreRules and selectRules (on top of the default rules) or replace them by this contents?

        :default: true
        '''
        result = self._values.get("add_to_existing_rules")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ignore_rules(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :default: pre-selected set of rules
        '''
        result = self._values.get("ignore_rules")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def mccabe_max_complexity(self) -> typing.Optional[jsii.Number]:
        '''
        :default: 14
        '''
        result = self._values.get("mccabe_max_complexity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def per_file_ignores(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.List[builtins.str]]]:
        '''
        :default: ignore doc-string code format for test files
        '''
        result = self._values.get("per_file_ignores")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.List[builtins.str]]], result)

    @builtins.property
    def select_rules(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :default: pre-selected set of rules
        '''
        result = self._values.get("select_rules")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def target_python_version(self) -> typing.Optional[builtins.str]:
        '''
        :default: py313
        '''
        result = self._values.get("target_python_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def unsafe_fixes(self) -> typing.Optional[builtins.bool]:
        '''
        :default: false
        '''
        result = self._values.get("unsafe_fixes")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def attach_fix_task_to(self) -> typing.Optional[builtins.str]:
        '''Attach lint fix tasks to parent.'''
        result = self._values.get("attach_fix_task_to")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RuffOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen-practical-constructs.LintOptions",
    jsii_struct_bases=[RuffOptions],
    name_mapping={
        "add_to_existing_rules": "addToExistingRules",
        "ignore_rules": "ignoreRules",
        "mccabe_max_complexity": "mccabeMaxComplexity",
        "per_file_ignores": "perFileIgnores",
        "select_rules": "selectRules",
        "target_python_version": "targetPythonVersion",
        "unsafe_fixes": "unsafeFixes",
        "attach_fix_task_to": "attachFixTaskTo",
    },
)
class LintOptions(RuffOptions):
    def __init__(
        self,
        *,
        add_to_existing_rules: typing.Optional[builtins.bool] = None,
        ignore_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
        mccabe_max_complexity: typing.Optional[jsii.Number] = None,
        per_file_ignores: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[builtins.str]]] = None,
        select_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
        target_python_version: typing.Optional[builtins.str] = None,
        unsafe_fixes: typing.Optional[builtins.bool] = None,
        attach_fix_task_to: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param add_to_existing_rules: Add rules defined here to the ignoreRules and selectRules (on top of the default rules) or replace them by this contents? Default: true
        :param ignore_rules: Default: pre-selected set of rules
        :param mccabe_max_complexity: Default: 14
        :param per_file_ignores: Default: ignore doc-string code format for test files
        :param select_rules: Default: pre-selected set of rules
        :param target_python_version: Default: py313
        :param unsafe_fixes: Default: false
        :param attach_fix_task_to: Attach lint fix tasks to parent.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3438e7eef6485f46108347648af5008e12c90c19bfd98c01816e34421622428c)
            check_type(argname="argument add_to_existing_rules", value=add_to_existing_rules, expected_type=type_hints["add_to_existing_rules"])
            check_type(argname="argument ignore_rules", value=ignore_rules, expected_type=type_hints["ignore_rules"])
            check_type(argname="argument mccabe_max_complexity", value=mccabe_max_complexity, expected_type=type_hints["mccabe_max_complexity"])
            check_type(argname="argument per_file_ignores", value=per_file_ignores, expected_type=type_hints["per_file_ignores"])
            check_type(argname="argument select_rules", value=select_rules, expected_type=type_hints["select_rules"])
            check_type(argname="argument target_python_version", value=target_python_version, expected_type=type_hints["target_python_version"])
            check_type(argname="argument unsafe_fixes", value=unsafe_fixes, expected_type=type_hints["unsafe_fixes"])
            check_type(argname="argument attach_fix_task_to", value=attach_fix_task_to, expected_type=type_hints["attach_fix_task_to"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if add_to_existing_rules is not None:
            self._values["add_to_existing_rules"] = add_to_existing_rules
        if ignore_rules is not None:
            self._values["ignore_rules"] = ignore_rules
        if mccabe_max_complexity is not None:
            self._values["mccabe_max_complexity"] = mccabe_max_complexity
        if per_file_ignores is not None:
            self._values["per_file_ignores"] = per_file_ignores
        if select_rules is not None:
            self._values["select_rules"] = select_rules
        if target_python_version is not None:
            self._values["target_python_version"] = target_python_version
        if unsafe_fixes is not None:
            self._values["unsafe_fixes"] = unsafe_fixes
        if attach_fix_task_to is not None:
            self._values["attach_fix_task_to"] = attach_fix_task_to

    @builtins.property
    def add_to_existing_rules(self) -> typing.Optional[builtins.bool]:
        '''Add rules defined here to the ignoreRules and selectRules (on top of the default rules) or replace them by this contents?

        :default: true
        '''
        result = self._values.get("add_to_existing_rules")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ignore_rules(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :default: pre-selected set of rules
        '''
        result = self._values.get("ignore_rules")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def mccabe_max_complexity(self) -> typing.Optional[jsii.Number]:
        '''
        :default: 14
        '''
        result = self._values.get("mccabe_max_complexity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def per_file_ignores(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.List[builtins.str]]]:
        '''
        :default: ignore doc-string code format for test files
        '''
        result = self._values.get("per_file_ignores")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.List[builtins.str]]], result)

    @builtins.property
    def select_rules(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :default: pre-selected set of rules
        '''
        result = self._values.get("select_rules")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def target_python_version(self) -> typing.Optional[builtins.str]:
        '''
        :default: py313
        '''
        result = self._values.get("target_python_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def unsafe_fixes(self) -> typing.Optional[builtins.bool]:
        '''
        :default: false
        '''
        result = self._values.get("unsafe_fixes")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def attach_fix_task_to(self) -> typing.Optional[builtins.str]:
        '''Attach lint fix tasks to parent.'''
        result = self._values.get("attach_fix_task_to")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LintOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Build0Options",
    "BuildTarget",
    "CoveragercFile",
    "CoveragercFileOptions",
    "LintOptions",
    "LintTarget",
    "MyPy",
    "MyPyIniFile",
    "Package",
    "PackageOptions",
    "Pip",
    "PipAudit",
    "PipOptions",
    "PyProjectTomlFile",
    "PyProjectTomlOptions",
    "PyTest",
    "PyTestIniFile",
    "PyTestIniOptions",
    "PyTestOptions",
    "PythonBasicOptions",
    "PythonBasicProject",
    "PythonBasicSample",
    "PythonVersionFile",
    "PythonVersionOptions",
    "ReadmeFile",
    "ReadmeOptions",
    "Ruff",
    "RuffOptions",
    "RuffTomlFile",
    "RuffTomlFileOptions",
    "TaskOptions",
    "TaskOptionsTarget",
    "TaskOptionsWithFix",
    "TestOptions",
    "TestTarget",
]

publication.publish()

def _typecheckingstub__e20a491b2a5a4f8ee18f05888a4892e7e41c691d596b28ee23e4eec41be056ba(
    *,
    package: typing.Optional[typing.Union[PackageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    pip: typing.Optional[typing.Union[PipOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7baf093ce1415d71f61d9818afeb26e3072bbd9a78db8ca4ffdf96dcf200c73(
    project: _projen_04054675.Project,
    task_opts: typing.Union[TaskOptions, typing.Dict[builtins.str, typing.Any]],
    *,
    package: typing.Optional[typing.Union[PackageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    pip: typing.Optional[typing.Union[PipOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__159e518f7881abcb6abee9cf04ea6e882729784c5e0b7a737f6522baa1f5a152(
    project: _projen_04054675.Project,
    *,
    format: typing.Optional[builtins.str] = None,
    min_coverage: typing.Optional[jsii.Number] = None,
    omit_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    skip_covered: typing.Optional[builtins.bool] = None,
    skip_empty: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83d971dfa627ffd4740ef400fe2c07260cfc8a850bb5f15117be52c28cf8aacb(
    _resolver: _projen_04054675.IResolver,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf0f342ecc7c849d461adb9b6dac4d82650ef73565eff25d53bbcfb2b3c5479d(
    *,
    format: typing.Optional[builtins.str] = None,
    min_coverage: typing.Optional[jsii.Number] = None,
    omit_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    skip_covered: typing.Optional[builtins.bool] = None,
    skip_empty: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a024fae964b162f23bca5eaaea17d6482838424ff147cbcf777078f73bfeb68(
    project: _projen_04054675.Project,
    task_options: typing.Union[TaskOptions, typing.Dict[builtins.str, typing.Any]],
    *,
    attach_fix_task_to: typing.Optional[builtins.str] = None,
    add_to_existing_rules: typing.Optional[builtins.bool] = None,
    ignore_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
    mccabe_max_complexity: typing.Optional[jsii.Number] = None,
    per_file_ignores: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[builtins.str]]] = None,
    select_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_python_version: typing.Optional[builtins.str] = None,
    unsafe_fixes: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0a177ef285e9d814c79f51d94f6a5469ba5493c4e5b3b7f83c91a7cb2308c59(
    project: _projen_04054675.Project,
    *,
    venv_path: builtins.str,
    attach_tasks_to: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4de587b589ba9e007f9440a8c64dc04332c03c6a61c1fbeab978cb77f04fc58(
    project: _projen_04054675.Project,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05af635c22d0af271080341bf52a1ec29b58a9cb63c5ea1521a193ee6570270e(
    _resolver: _projen_04054675.IResolver,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62f3584f77ee44c76622dd4d1bcb61319421c6ff75dc347a3de1892c0baf9086(
    project: _projen_04054675.Project,
    *,
    license: typing.Optional[builtins.str] = None,
    author_email: typing.Optional[builtins.str] = None,
    author_name: typing.Optional[builtins.str] = None,
    classifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    homepage: typing.Optional[builtins.str] = None,
    keywords: typing.Optional[typing.Sequence[builtins.str]] = None,
    license_file: typing.Optional[builtins.str] = None,
    package_name: typing.Optional[builtins.str] = None,
    readme: typing.Optional[builtins.str] = None,
    requires_python: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6c809477032f6e6abdbfbf18de97c940c11e01375028ae0f5ecb6b8e973a50f(
    project: _projen_04054675.Project,
    task_opts: typing.Union[TaskOptions, typing.Dict[builtins.str, typing.Any]],
    *,
    lock_file: typing.Optional[builtins.str] = None,
    lock_file_dev: typing.Optional[builtins.str] = None,
    python_exec: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82328de1f2fc16d559d0de14506a0fa6977eaf5050623900f5ab343c6be250cb(
    project: _projen_04054675.Project,
    *,
    venv_path: builtins.str,
    attach_tasks_to: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ab0570fbeee15a743ac44aee78db6330a9da7a8cb0af29bcd9bbd26f212ec73(
    *,
    lock_file: typing.Optional[builtins.str] = None,
    lock_file_dev: typing.Optional[builtins.str] = None,
    python_exec: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6d7a3b8b4177596f54f16f91bd9df59e0a45d86f401871b1e9b3b29ce78328b(
    project: _projen_04054675.Project,
    *,
    author_email: typing.Optional[builtins.str] = None,
    author_name: typing.Optional[builtins.str] = None,
    classifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    homepage: typing.Optional[builtins.str] = None,
    keywords: typing.Optional[typing.Sequence[builtins.str]] = None,
    license_file: typing.Optional[builtins.str] = None,
    package_name: typing.Optional[builtins.str] = None,
    readme: typing.Optional[builtins.str] = None,
    requires_python: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4507ce8637891a717163abf9982165de1dcb742ca0621e122de9e18450c7727b(
    _resolver: _projen_04054675.IResolver,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05a4f19c0ac4e3b053533fffc4e6b5d4ec292f9c4073fe33392b6cfca5185ea0(
    *,
    author_email: typing.Optional[builtins.str] = None,
    author_name: typing.Optional[builtins.str] = None,
    classifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    homepage: typing.Optional[builtins.str] = None,
    keywords: typing.Optional[typing.Sequence[builtins.str]] = None,
    license_file: typing.Optional[builtins.str] = None,
    package_name: typing.Optional[builtins.str] = None,
    readme: typing.Optional[builtins.str] = None,
    requires_python: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42e05408896599bbf022ad6a7e60a821d61cad81416e62f8e87333465af34cc8(
    project: _projen_04054675.Project,
    task_opts: typing.Union[TaskOptions, typing.Dict[builtins.str, typing.Any]],
    *,
    format: typing.Optional[builtins.str] = None,
    min_coverage: typing.Optional[jsii.Number] = None,
    omit_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    skip_covered: typing.Optional[builtins.bool] = None,
    skip_empty: typing.Optional[builtins.bool] = None,
    verbose: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44a3acc3982cbac42b7f244f2b7a0629ea77dbb3fbeb16b462809daed3316bc1(
    project: _projen_04054675.Project,
    *,
    verbose: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__975893dbb0771af51870157408a643ffcf74cf8fc037cc71b062959406638251(
    _resolver: _projen_04054675.IResolver,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ef765f0b3b01e999545322392822791093e2b72fca8c2d619f6f3c52c5dfcd7(
    value: PyTestIniOptions,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d4ca4cf98a7701cf69a33f919512afaccabd7bb8ee6ac702d86b6b686e85c40(
    *,
    verbose: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__384e63be7810bf945d6fb782fc3c891fca1787094bf35586a2dcbb2d81ce2867(
    *,
    format: typing.Optional[builtins.str] = None,
    min_coverage: typing.Optional[jsii.Number] = None,
    omit_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    skip_covered: typing.Optional[builtins.bool] = None,
    skip_empty: typing.Optional[builtins.bool] = None,
    verbose: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c514a60a75f071c20ec30de634506e6c296b1d91b281bd1a0ff69ec8551d7bf7(
    package_name_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6803cea798ee4a60e65efc9b0cc675daf469d702cfb43e7595aed132004e56e3(
    package_name_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f89bc9b2d760f7dbf6c765c850ee98f08ad2b9abd29b30723839469f113ac71(
    project: _projen_04054675.Project,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b56632f9602060a9026f4ff094af75115f54480ed5cffe451781d662b51d31f1(
    project: _projen_04054675.Project,
    *,
    python_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3eb4c7d952a99bdea958131725c8145a2e4d0ef325b48ac55d83275c5cdd0c0(
    _resolver: _projen_04054675.IResolver,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fb02140f15e42d4186643add56e5f0ffe0d004d6540a470bf2ae03d136a627b(
    *,
    python_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e121cdedc0beed1c682d7a460ce0e7ed3201b3597d0675df06b9bc467a25a42(
    project: _projen_04054675.Project,
    *,
    project_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f16ff3cf7a0826918909ecb12dfd4f0ec1385aa6bdc84176767f6109162ecdc(
    *,
    project_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92e6719177912c0eae0ee85cfc203cb22854f3f273cc256898396282ba7d42fe(
    project: _projen_04054675.Project,
    task_opts: typing.Union[TaskOptionsWithFix, typing.Dict[builtins.str, typing.Any]],
    *,
    attach_fix_task_to: typing.Optional[builtins.str] = None,
    add_to_existing_rules: typing.Optional[builtins.bool] = None,
    ignore_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
    mccabe_max_complexity: typing.Optional[jsii.Number] = None,
    per_file_ignores: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[builtins.str]]] = None,
    select_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_python_version: typing.Optional[builtins.str] = None,
    unsafe_fixes: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__515cf86a84df0b6b18941ab4c2a73e7eef40e0260fab3c698c6cabcef8227d71(
    project: _projen_04054675.Project,
    *,
    add_to_existing_rules: typing.Optional[builtins.bool] = None,
    ignore_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
    mccabe_max_complexity: typing.Optional[jsii.Number] = None,
    per_file_ignores: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[builtins.str]]] = None,
    select_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_python_version: typing.Optional[builtins.str] = None,
    unsafe_fixes: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce7087163e4218666b985f90db1006536d982decdeb6854261778dfc1f07f506(
    *,
    add_to_existing_rules: typing.Optional[builtins.bool] = None,
    ignore_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
    mccabe_max_complexity: typing.Optional[jsii.Number] = None,
    per_file_ignores: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[builtins.str]]] = None,
    select_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_python_version: typing.Optional[builtins.str] = None,
    unsafe_fixes: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60bbd600395432f8000b4758eea0d98c9c8e225b40399a70f2bd14d84ef3bb0f(
    *,
    venv_path: builtins.str,
    attach_tasks_to: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ebef6526107b290f8f3024aa58a74f546f6c2dcee9f6faa53295f3c7402ac4a(
    *,
    attach_tasks_to: typing.Optional[builtins.str] = None,
    venv_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e45cbb8bf0d46096fadb00e45bbfbb7e0f37f040d7543c11c8fece01826bd20(
    *,
    venv_path: builtins.str,
    attach_tasks_to: typing.Optional[builtins.str] = None,
    attach_fix_tasks_to: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6ce63ffedc17816d4e10d303db52b112c4a018db5d7b81c720790d591a43e4e(
    *,
    format: typing.Optional[builtins.str] = None,
    min_coverage: typing.Optional[jsii.Number] = None,
    omit_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    skip_covered: typing.Optional[builtins.bool] = None,
    skip_empty: typing.Optional[builtins.bool] = None,
    verbose: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0658c3d7fe54aaec02fcef6987c7705125d952a65e7b4f1cde8ad8b0b36e7aa8(
    project: _projen_04054675.Project,
    task_opts: typing.Union[TaskOptions, typing.Dict[builtins.str, typing.Any]],
    *,
    format: typing.Optional[builtins.str] = None,
    min_coverage: typing.Optional[jsii.Number] = None,
    omit_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    skip_covered: typing.Optional[builtins.bool] = None,
    skip_empty: typing.Optional[builtins.bool] = None,
    verbose: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__769a6aad7aea164b73af332f179b064a5d119bdb8838de929422452d3b88c50c(
    *,
    author_email: typing.Optional[builtins.str] = None,
    author_name: typing.Optional[builtins.str] = None,
    classifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    homepage: typing.Optional[builtins.str] = None,
    keywords: typing.Optional[typing.Sequence[builtins.str]] = None,
    license_file: typing.Optional[builtins.str] = None,
    package_name: typing.Optional[builtins.str] = None,
    readme: typing.Optional[builtins.str] = None,
    requires_python: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
    license: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c54d357164afec478ab317ef798bb3d8a0ac8c35182918abf6dfd0025c70bc86(
    *,
    name: builtins.str,
    commit_generated: typing.Optional[builtins.bool] = None,
    git_ignore_options: typing.Optional[typing.Union[_projen_04054675.IgnoreFileOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    git_options: typing.Optional[typing.Union[_projen_04054675.GitOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    logging: typing.Optional[typing.Union[_projen_04054675.LoggerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    outdir: typing.Optional[builtins.str] = None,
    parent: typing.Optional[_projen_04054675.Project] = None,
    projen_command: typing.Optional[builtins.str] = None,
    projenrc_json: typing.Optional[builtins.bool] = None,
    projenrc_json_options: typing.Optional[typing.Union[_projen_04054675.ProjenrcJsonOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    renovatebot: typing.Optional[builtins.bool] = None,
    renovatebot_options: typing.Optional[typing.Union[_projen_04054675.RenovatebotOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    package: typing.Optional[typing.Union[PackageOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    pip: typing.Optional[typing.Union[PipOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    attach_tasks_to: typing.Optional[builtins.str] = None,
    venv_path: typing.Optional[builtins.str] = None,
    deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    dev_deps: typing.Optional[typing.Sequence[builtins.str]] = None,
    lint: typing.Optional[typing.Union[LintOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    sample: typing.Optional[builtins.bool] = None,
    test: typing.Optional[typing.Union[TestOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d207008bfccd269e92e2aa9ed31161d7e45bab33efb79344ae36a97c2eddcff(
    *,
    add_to_existing_rules: typing.Optional[builtins.bool] = None,
    ignore_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
    mccabe_max_complexity: typing.Optional[jsii.Number] = None,
    per_file_ignores: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[builtins.str]]] = None,
    select_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_python_version: typing.Optional[builtins.str] = None,
    unsafe_fixes: typing.Optional[builtins.bool] = None,
    attach_fix_task_to: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3438e7eef6485f46108347648af5008e12c90c19bfd98c01816e34421622428c(
    *,
    add_to_existing_rules: typing.Optional[builtins.bool] = None,
    ignore_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
    mccabe_max_complexity: typing.Optional[jsii.Number] = None,
    per_file_ignores: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[builtins.str]]] = None,
    select_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_python_version: typing.Optional[builtins.str] = None,
    unsafe_fixes: typing.Optional[builtins.bool] = None,
    attach_fix_task_to: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
