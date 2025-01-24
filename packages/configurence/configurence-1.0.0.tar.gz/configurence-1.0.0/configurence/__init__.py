# -*- coding: utf-8 -*-

"""
A simple CLI configuration management library
"""

from dataclasses import asdict, dataclass
from dataclasses import field as _field
from dataclasses import fields, MISSING, replace
import logging
import os
import os.path
from pathlib import Path
from typing import (
    Any,
    Callable,
    cast,
    Dict,
    get_args,
    get_origin,
    NoReturn,
    Optional,
    Set,
    Type,
    Union,
)

try:
    from typing import Self
except ImportError:
    Self = Any

from appdirs import user_config_dir
import yaml

try:
    from yaml import CDumper as Dumper
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Dumper, Loader

logger = logging.getLogger(__name__)


def global_file(name: str) -> str:
    """
    Get the global file path for the config.
    """

    return f"/etc/{name}.yaml"


def default_file(name: str) -> str:
    """
    Get the default file path for the config.
    """

    return os.path.join(user_config_dir(name), f"{name}.yaml")


def _read_config_file(file: str) -> Dict[str, Any]:
    with open(file, "r") as f:
        logger.debug(f"Loading config from {file}...")
        return yaml.load(f, Loader=Loader)


def _write_config_file(file: str, config: Dict[str, Any]) -> None:
    os.makedirs(Path(file).parent, exist_ok=True)

    with open(file, "w") as f:
        yaml.dump(config, f, Dumper=Dumper)

    logger.info(f"Wrote configuration to {file}.")


def field(
    *,
    default: Any = MISSING,
    default_factory: Any = MISSING,
    init: bool = True,
    repr: bool = True,
    hash: Any = None,
    compare: bool = True,
    metadata: Optional[Any] = None,
    env_var: Optional[str] = None,
    convert: Optional[Callable[[str], Any]] = None,
    kw_only: Any = MISSING,
) -> Any:
    md: Any = metadata
    if metadata:
        md = metadata
    else:
        md = dict()
    if isinstance(md, dict):
        md.update(
            env_var=env_var if env_var else md.get("env_var", None),
            convert=convert if convert else md.get("convert", None),
        )

    # TODO: I don't know why the type checker is unhappy with this call, but
    # Python seems fine with it and it matches Python's docs
    return cast(Any, _field)(
        default=default,
        default_factory=default_factory,
        init=init,
        repr=repr,
        hash=hash,
        compare=compare,
        metadata=md,
        kw_only=kw_only,
    )


def _from_environment(cls: Any, env_prefix: str) -> Dict[str, Any]:
    env: Dict[str, Any] = dict()
    for f in fields(cls):
        if f.metadata and "env_var" in f.metadata:
            env_var = f"{env_prefix}_{f.metadata['env_var']}"
            if env_var in os.environ:
                var: str = os.environ[env_var]
                # TODO: Buggy - test!
                env[f.name] = cast(Any, f.type)(var)
    return env


class BaseConfig:
    name: str
    _file: str

    @property
    def file(self: Self) -> str:
        """
        The configuration file path.
        """
        return self._file or default_file(self.name)

    @classmethod
    def from_environment(cls: Type[Self], name: str) -> Self:
        """
        Load configuration from the environment.
        """

        logger.debug("Loading config from environment...")
        return cls(**_from_environment(cls, name.upper()))

    @classmethod
    def from_file(
        cls: Type[Self],
        name: str,
        file: Optional[str] = None,
        global_: bool = False,
        load_environment: bool = False,
        create_file: bool = False,
    ) -> Self:
        """
        Load configuration from a file. Optionally load environment overrides and
        optionally create the file.
        """

        env_prefix = name.upper()
        env_config = f"{env_prefix}_CONFIG"

        if file:
            _file = file
        elif env_config in os.environ:
            _file = os.environ[env_config]
        elif global_:
            _file = global_file(name)
        else:
            _file = default_file(name)

        found_file = False
        kwargs: Dict[str, Any] = dict(name=name, _file=_file)
        try:
            found_file = True
            kwargs.update(_read_config_file(_file))
        except FileNotFoundError:
            try:
                kwargs.update(_read_config_file(global_file(name)))
            except FileNotFoundError:
                pass

        if load_environment:
            logger.debug("Loading environment overrides...")
            kwargs.update(_from_environment(cls, env_prefix))

        config = cls(**kwargs)

        if not found_file and create_file:
            config.to_file()

        return config

    def _assert_has(self: Self, name: str) -> None:
        if not hasattr(self, name) or name.startswith("_"):
            raise ValueError(f"Unknown configuration parameter {name}")

    def get(self: Self, name: str) -> Any:
        """
        Get a configuration parameter by name.
        """

        self._assert_has(name)
        return getattr(self, name)

    def _field_setters(self: Self) -> Dict[Any, Callable[[str, str], None]]:
        setters: Dict[Any, Callable[[str, str], None]] = {
            str: self.set_str,
            Optional[str]: self.set_str,
            bool: self.set_bool,
            Optional[bool]: self.set_bool,
            int: self.set_int,
            Optional[int]: self.set_int,
            float: self.set_float,
            Optional[float]: self.set_float,
        }

        for f in fields(cast(Any, self)):
            if f.metadata and f.type not in setters and "convert" in f.metadata:

                def setter(name: str, value: str) -> None:
                    setattr(self, name, f.metadata["convert"](value))

                setters[f.type] = setter

        return setters

    def _optional_field_types(self: Self) -> Set[Any]:
        optional: Set[Any] = set()

        for f in fields(cast(Any, self)):
            if get_origin(f.type) is Union and type(None) in get_args(f.type):
                optional.add(f.type)

        return optional

    def set(self: Self, name: str, value: str) -> None:
        """
        Set a configuration parameter by name and string value.
        """

        self._assert_has(name)

        setters = self._field_setters()

        for f in fields(cast(Any, self)):
            if f.name == name:
                if f.type in setters:
                    setters[f.type](name, value)
                    return
                else:
                    raise ValueError(f"Unknown type {f.type}")

    def set_str(self: Self, name: str, value: str) -> None:
        setattr(self, name, value)

    def set_bool(self: Self, name: str, value: str) -> None:
        if value.lower() in {"true", "yes", "y", "1"}:
            setattr(self, name, True)
        elif value.lower() in {"false", "no", "n", "0"}:
            setattr(self, name, False)
        else:
            raise ValueError(f"Can not convert {value} to bool")

    def set_float(self: Self, name: str, value: str) -> None:
        setattr(self, name, float(value))

    def set_int(self: Self, name: str, value: str) -> None:
        setattr(self, name, int(value))

    def unset(self: Self, name: str) -> None:
        """
        Unset an optional parameter.
        """

        self._assert_has(name)

        optional_types = self._optional_field_types()

        for f in fields(cast(Any, self)):
            if f.name == name:
                if f.type in optional_types:
                    self._unset(name)
                else:
                    self._required(name)

    def _required(self: Self, name: str) -> NoReturn:
        raise ValueError(f"{name} is a required configuraiton parameter")

    def _unset(self: Self, name: str) -> None:
        setattr(self, name, None)

    def as_dict(self: Self) -> Dict[str, Any]:
        inst = cast(Any, self)
        return {k: v for k, v in asdict(inst).items() if not k.startswith("_")}

    def to_file(self: Self, file: Optional[str] = None) -> Self:
        """
        Save the configuration to a file.
        """

        file = file or self.file
        inst = cast(Any, self)

        _write_config_file(file, self.as_dict())

        return replace(inst, _file=file)

    def __repr__(self: Self) -> str:
        return yaml.dump(self.as_dict(), Dumper=Dumper)


def config(cls: Type[Any]) -> Type[Any]:
    """
    A configuration object. This class is typically used by a CLI, but may
    also be useful for scripts or Jupyter notebooks using its configuration.
    """
    base_cls: Any = dataclass(BaseConfig)
    cfg_cls = dataclass(cls)

    @dataclass
    class new_cls(cfg_cls, base_cls):
        def __repr__(self) -> str:
            return BaseConfig.__repr__(self)

    new_cls.__name__ = cls.__name__

    for f in fields(base_cls):
        setattr(new_cls, f.name, f)

    for f in fields(cfg_cls):
        setattr(new_cls, f.name, f)

    return new_cls
