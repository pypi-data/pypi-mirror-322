import multiprocessing
import time
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
import pytest
from ruamel.yaml import YAML

from datamate import (
    Directory,
    Namespace,
    root,
    set_root_context,
    set_root_dir,
    delete_if_exists,
)
from datamate.directory import (
    ConfigWarning,
    ImplementationWarning,
    ModifiedWarning,
    _auto_doc,
)
from datamate.io import H5Reader
from datamate.diff import (
    DirectoryDiff,
    assert_equal_attributes,
    assert_equal_directories,
)
from datamate.metadata import (
    read_meta,
    MetadataValidationError,
)

# -- Helper functions ----------------------------------------------------------


def data_file(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(np.random.rand(3).tobytes())
    return path


def data_file_concat(path: Path, args: List[Path]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"".join(a.read_bytes() for a in args))
    return path


def assert_attributes_equal(directory: Directory, target: dict) -> None:
    if "__type__" in target:
        assert isinstance(directory, target.pop("__type__"))
    if "__path__" in target:
        assert directory.path == target.pop("__path__")
    if "__conf__" in target:
        assert directory._config == target.pop("__conf__")
    if "__meta__" in target:
        assert directory.meta == target.pop("__meta__")
    if "__doc__" in target:
        assert directory.__doc__ == target.pop("__doc__")
    if "__exists__" in target:
        assert directory.path.exists() == target.pop("__exists__")


def assert_directory_equals(directory: Directory, target: dict) -> None:
    assert_attributes_equal(directory, target)

    assert len(directory) == len(target)
    assert len(list(directory)) == len(target)

    for k, v in target.items():
        assert k in directory
        assert k in list(directory)
        assert hasattr(directory, k)

        if isinstance(v, dict):
            assert isinstance(directory[k], Directory)
            assert isinstance(getattr(directory, k), Directory)
            assert_directory_equals(directory[k], v)
            assert_directory_equals(getattr(directory, k), v)

        elif isinstance(v, Path):
            k_mod = k.replace(".", "__")
            assert (directory.path / k).is_file()
            assert isinstance(directory[k], Path)
            assert isinstance(getattr(directory, k), Path)
            assert directory[k].read_bytes() == v.read_bytes()
            assert getattr(directory, k).read_bytes() == v.read_bytes()
            assert getattr(directory, k_mod).read_bytes() == v.read_bytes()

        elif isinstance(v, pd.DataFrame):
            assert (directory.path / k).with_suffix(".csv").is_file()
            assert isinstance(directory[k], pd.DataFrame)
            assert isinstance(getattr(directory, k), pd.DataFrame)
            assert np.array_equal(directory[k].to_numpy(), v.to_numpy())
            assert np.array_equal(getattr(directory, k).to_numpy(), v.to_numpy())

        else:
            assert (directory.path / k).with_suffix(".h5").is_file()
            assert isinstance(directory[k], H5Reader)
            assert isinstance(getattr(directory, k), H5Reader)
            assert np.array_equal(directory[k][()], v)
            assert np.array_equal(getattr(directory, k)[()], v)
            assert directory[k].dtype == np.asarray(v).dtype
            assert getattr(directory, k).dtype == np.asarray(v).dtype


# -- [Base class tests] Empty directories --------------------------------------


def test_empty_directory_with_existing_dir(tmp_path: Path) -> None:
    a = Directory(tmp_path)
    assert_directory_equals(
        a,
        dict(
            __path__=tmp_path,
            __conf__=Namespace(type="Directory"),
            __meta__={"config": None, "status": "done"},
        ),
    )
    assert isinstance(a.nonexistent_entry, Directory)


def test_empty_directory_with_nonexistent_dir(tmp_path: Path) -> None:
    a = Directory(tmp_path / "new_dir")
    assert_directory_equals(
        a,
        dict(
            __path__=tmp_path / "new_dir",
            __conf__=Namespace(type="Directory"),
            __meta__={"config": None, "status": "done"},
        ),
    )
    assert isinstance(a.nonexistent_entry, Directory)
    assert not (tmp_path / "new_dir").exists()


# -- [Base class tests] Entry assignment ---------------------------------------


def test_float_assignment(tmp_path: Path) -> None:
    a = Directory(tmp_path)
    a.b = 1.5
    a.b = 2.5
    a["c"] = 3.5
    a["c"] = 4.5
    assert_directory_equals(a, {"b": 2.5, "c": 4.5})


def test_byte_string_assignment(tmp_path: Path) -> None:
    a = Directory(tmp_path)
    a.b = b"bee"
    a.b = b"buzz"
    a["c"] = b"sea"
    a["c"] = b"ahoy!"
    assert_directory_equals(a, {"b": b"buzz", "c": b"ahoy!"})


def test_list_assignment(tmp_path: Path) -> None:
    a = Directory(tmp_path)
    a.b = [1, 2, 3]
    a.b = [4, 5, 6]
    a["c"] = [[7, 8], [9, 10]]
    a["c"] = [[11, 12, 13], [14, 15, 16]]
    assert_directory_equals(a, {"b": [4, 5, 6], "c": [[11, 12, 13], [14, 15, 16]]})


def test_array_assignment(tmp_path: Path) -> None:
    a = Directory(tmp_path)
    a.b = np.ones((2, 3), dtype="float32")
    a.b = np.zeros((4, 5, 6), dtype="float32")
    a["c"] = np.ones((4, 5, 6), dtype="float32")
    a["c"] = np.ones((2, 3), dtype="uint16")
    assert_directory_equals(
        a,
        {
            "b": np.zeros((4, 5, 6), dtype="float32"),
            "c": np.ones((2, 3), dtype="uint16"),
        },
    )


def test_dataframe_assignment(tmp_path: Path) -> None:
    a = Directory(tmp_path)
    a.b = pd.DataFrame({"a": [0, 1, 2], "b": [3, 4, 5]})
    a.b = pd.DataFrame({"a": [3, 4, 5], "b": [0, 1, 2]})
    a["c"] = pd.DataFrame({"a": [0, 1], "b": [3, 4]})
    a["c"] = pd.DataFrame({"a": [3, 4], "b": [0, 1]})
    assert_directory_equals(
        a,
        {
            "b": pd.DataFrame({"a": [3, 4, 5], "b": [0, 1, 2]}),
            "c": pd.DataFrame({"a": [3, 4], "b": [0, 1]}),
        },
    )


def test_path_assignment(tmp_path: Path) -> None:
    a = Directory(tmp_path / "directory")
    a.b__bin = data_file(tmp_path / "b0.bin")
    a.b__bin = data_file(tmp_path / "b1.bin")
    a["c.bin"] = data_file(tmp_path / "c0.bin")
    a["c.bin"] = data_file(tmp_path / "c1.bin")
    assert_directory_equals(
        a, {"b.bin": tmp_path / "b1.bin", "c.bin": tmp_path / "c1.bin"}
    )


def test_dict_assignment(tmp_path: Path) -> None:
    a = Directory(tmp_path)
    a.dict = dict(a=[1, 2, 3], b=dict(c=[4], d=[5, 6]))
    assert_directory_equals(a, {"dict": {"a": [1, 2, 3], "b": {"c": [4], "d": [5, 6]}}})


def test_directory_assignment(tmp_path: Path) -> None:
    a_src = Directory(tmp_path / "a_src")
    a_src.b.c = b"bee sea"
    a_src.d.e = [1, 2, 3, 4]
    a_src.f.g__bin = data_file(tmp_path / "effigy.bin")
    a_dst = Directory(tmp_path / "a_dst")
    a_dst.a = a_src
    assert_directory_equals(
        a_dst,
        {
            "a": {
                "b": {"c": b"bee sea"},
                "d": {"e": [1, 2, 3, 4]},
                "f": {"g.bin": tmp_path / "effigy.bin"},
            }
        },
    )


# -- [Base class tests] Entry extension ----------------------------------------


def test_list_extension(tmp_path: Path) -> None:
    a = Directory(tmp_path)
    a.extend("b", [[7, 8], [9, 10]])
    a.extend("b", [[11, 12]])
    assert_directory_equals(a, {"b": [[7, 8], [9, 10], [11, 12]]})

    b = Directory(tmp_path)
    b.b = [[7, 8], [9, 10]]
    b.extend("b", [[11, 12]])
    assert_directory_equals(a, {"b": [[7, 8], [9, 10], [11, 12]]})


def test_array_extension(tmp_path: Path) -> None:
    a = Directory(tmp_path)
    a.extend("b", np.uint16([[7, 8], [9, 10]]))
    a.extend("b", np.uint16([[11, 12]]))
    assert_directory_equals(a, {"b": np.uint16([[7, 8], [9, 10], [11, 12]])})

    b = Directory(tmp_path)
    b.b = np.uint16([[7, 8], [9, 10]])
    b.extend("b", np.uint16([[11, 12]]))
    assert_directory_equals(b, {"b": np.uint16([[7, 8], [9, 10], [11, 12]])})


def test_dataframe_extension(tmp_path: Path) -> None:
    a = Directory(tmp_path)
    a.extend("b", pd.DataFrame({"a": [7, 9], "b": [8, 10]}))
    a.extend("b", pd.DataFrame({"a": [11], "b": [12]}))
    assert_directory_equals(a, {"b": pd.DataFrame({"a": [7, 9, 11], "b": [8, 10, 12]})})

    b = Directory(tmp_path)
    b.b = pd.DataFrame({"a": [7, 9], "b": [8, 10]})
    b.extend("b", pd.DataFrame({"a": [11], "b": [12]}))
    assert_directory_equals(b, {"b": pd.DataFrame({"a": [7, 9, 11], "b": [8, 10, 12]})})


def test_path_extension(tmp_path: Path) -> None:
    a = Directory(tmp_path / "a")
    a.extend("b.bin", data_file(tmp_path / "b0.bin"))
    a.extend("b.bin", data_file(tmp_path / "b1.bin"))
    assert_directory_equals(
        a,
        {
            "b.bin": data_file_concat(
                tmp_path / "b2.bin", [tmp_path / "b0.bin", tmp_path / "b1.bin"]
            )
        },
    )

    b = Directory(tmp_path / "a")
    b["b.bin"] = data_file(tmp_path / "b0.bin")
    b.extend("b.bin", data_file(tmp_path / "b1.bin"))
    assert_directory_equals(
        b,
        {
            "b.bin": data_file_concat(
                tmp_path / "b2.bin", [tmp_path / "b0.bin", tmp_path / "b1.bin"]
            )
        },
    )


def test_dict_extension(tmp_path: Path) -> None:
    a = Directory(tmp_path / "a")
    a.extend(
        "b",
        {
            "c": np.empty((0, 2), dtype="uint16"),
            "d.bin": data_file(tmp_path / "d0.bin"),
            "e": {"f": [0.1, 0.2]},
        },
    )
    a.extend(
        "b",
        {
            "c": np.uint16([[1, 2], [3, 4]]),
            "d.bin": data_file(tmp_path / "d1.bin"),
            "e": {"f": [0.3, 0.4, 0.5]},
        },
    )
    assert_directory_equals(
        a,
        {
            "b": {
                "c": np.uint16([[1, 2], [3, 4]]),
                "d.bin": data_file_concat(
                    tmp_path / "d2.bin", [tmp_path / "d0.bin", tmp_path / "d1.bin"]
                ),
                "e": {"f": [0.1, 0.2, 0.3, 0.4, 0.5]},
            }
        },
    )
    b = Directory(tmp_path / "b")
    b.b = {
        "c": np.empty((0, 2), dtype="uint16"),
        "d.bin": data_file(tmp_path / "d0.bin"),
        "e": {"f": [0.1, 0.2]},
    }
    b.extend(
        "b",
        {
            "c": np.uint16([[1, 2], [3, 4]]),
            "d.bin": data_file(tmp_path / "d1.bin"),
            "e": {"f": [0.3, 0.4, 0.5]},
        },
    )
    assert_directory_equals(
        b,
        {
            "b": {
                "c": np.uint16([[1, 2], [3, 4]]),
                "d.bin": data_file_concat(
                    tmp_path / "d2.bin", [tmp_path / "d0.bin", tmp_path / "d1.bin"]
                ),
                "e": {"f": [0.1, 0.2, 0.3, 0.4, 0.5]},
            }
        },
    )


def test_directory_extension(tmp_path: Path) -> None:
    a0 = Directory(tmp_path / "a0")
    a0.b = [b"hello"]
    a0.c__bin = data_file(tmp_path / "c0.bin")
    a0.d = {"e": [[0.0, 1.0]], "f.bin": data_file(tmp_path / "f0.bin")}

    a1 = Directory(tmp_path / "a1")
    a1.b = [b"good", b"bye"]
    a1.c__bin = data_file(tmp_path / "c1.bin")
    a1.d = {"e": np.empty((0, 2)), "f.bin": data_file(tmp_path / "f1.bin")}

    a2 = Directory(tmp_path / "a2")
    a2.extend("subdirectory", a0)
    a2.extend("subdirectory", a1)

    assert_directory_equals(
        a2,
        {
            "subdirectory": {
                "b": [b"hello", b"good", b"bye"],
                "c.bin": data_file_concat(
                    tmp_path / "c2.bin", [tmp_path / "c0.bin", tmp_path / "c1.bin"]
                ),
                "d": {
                    "e": [[0.0, 1.0]],
                    "f.bin": data_file_concat(
                        tmp_path / "f2.bin", [tmp_path / "f0.bin", tmp_path / "f1.bin"]
                    ),
                },
            }
        },
    )


# -- [Base class tests] Entry deletion -----------------------------------------


def test_array_file_deletion(tmp_path: Path) -> None:
    a = Directory(tmp_path / "a")
    a.b = [1, 2, 3]
    a.c = b"four five six"
    a.d = [7, 8]
    a.e = {"blue": b"jeans"}
    a.f__bin = data_file(tmp_path / "data.bin")
    del a.b
    del a["c"]
    assert_directory_equals(
        a, {"d": [7, 8], "e": {"blue": b"jeans"}, "f.bin": tmp_path / "data.bin"}
    )


def test_opaque_file_deletion(tmp_path: Path) -> None:
    a = Directory(tmp_path / "a")
    a.b__bin = data_file(tmp_path / "b.bin")
    a.c__bin = data_file(tmp_path / "c.bin")
    a.d = [7, 8]
    a.e = {"blue": b"jeans"}
    a.f__bin = data_file(tmp_path / "data.bin")
    del a.b__bin
    del a["c.bin"]
    assert_directory_equals(
        a, {"d": [7, 8], "e": {"blue": b"jeans"}, "f.bin": tmp_path / "data.bin"}
    )


def test_directory_deletion(tmp_path: Path) -> None:
    a = Directory(tmp_path / "a")
    a.b = {"aa": {"bb": 0, "cc": 1}}
    a.c = {"dd": {"ee": [2, 3, 4]}}
    a.d = [7, 8]
    a.e = {"blue": b"jeans"}
    a.f__bin = data_file(tmp_path / "data.bin")
    del a.b
    del a["c"]
    assert_directory_equals(
        a, {"d": [7, 8], "e": {"blue": b"jeans"}, "f.bin": tmp_path / "data.bin"}
    )


# -- [Subclass tests] Construction ---------------------------------------------


class CustomDirectory(Directory):
    n_calls = 0

    class Config:
        n_zeros: int
        n_ones: int

    def __init__(self, conf) -> None:
        CustomDirectory.n_calls += 1
        self.zeros = np.zeros(conf.n_zeros)
        self.ones = np.ones(conf.n_ones)


class AnotherDirectory(Directory):
    def __init__(self) -> None:
        AnotherDirectory.Config.n_calls += 1


def test_construction_from_nothing(tmp_path: Path) -> None:
    # Setup
    set_root_dir(tmp_path)
    AnotherDirectory.Config.n_calls = 0

    # Case 1: (not exists)
    with pytest.warns(ImplementationWarning):
        a0 = AnotherDirectory()
    assert AnotherDirectory.Config.n_calls == 0

    # Case 2: (exists, empty)
    path = a0.path
    with pytest.warns(ImplementationWarning):
        a1 = AnotherDirectory()
    assert path == a1.path

    # Case 3: (exists, non-empty)
    a0.__init__()
    with pytest.warns(ImplementationWarning):
        a1 = AnotherDirectory()
    assert AnotherDirectory.Config.n_calls == 1

    # Cleanup
    set_root_dir(Path("."))


def test_construction_from_path(tmp_path: Path) -> None:
    # Setup
    set_root_dir(tmp_path)
    CustomDirectory.n_calls = 0
    a0 = CustomDirectory(n_zeros=2, n_ones=3)

    # Case 1: (path_given, exists)
    a1 = CustomDirectory(a0.path)
    a2 = CustomDirectory(f"{a0.path}")
    a3 = CustomDirectory(f"@/{a0.path.name}")
    assert_directory_equals(a1, {"zeros": np.zeros(2), "ones": np.ones(3)})
    assert_directory_equals(a2, {"zeros": np.zeros(2), "ones": np.ones(3)})
    assert_directory_equals(a3, {"zeros": np.zeros(2), "ones": np.ones(3)})
    assert CustomDirectory.n_calls == 1

    # Case 2: (path_given, does_not_exists)
    with pytest.raises(FileNotFoundError):
        CustomDirectory(tmp_path / "invalid_path")

    # Cleanup
    set_root_dir(Path("."))


def test_construction_from_conf(tmp_path: Path) -> None:
    # Setup
    set_root_dir(tmp_path)
    CustomDirectory.n_calls = 0
    a0 = CustomDirectory(n_zeros=2, n_ones=3)

    # Case 1: (conf_given, exists)
    a1 = CustomDirectory(n_zeros=2, n_ones=3)
    a2 = CustomDirectory(dict(n_zeros=2, n_ones=3))
    assert_directory_equals(a1, {"zeros": np.zeros(2), "ones": np.ones(3)})
    assert_directory_equals(a2, {"zeros": np.zeros(2), "ones": np.ones(3)})
    assert a1.path == a0.path
    assert a2.path == a0.path
    assert CustomDirectory.n_calls == 1

    # Case 2: (conf_given, does_not_exist)
    a3 = CustomDirectory(n_zeros=2, n_ones=4)
    a4 = CustomDirectory(dict(n_zeros=1, n_ones=3))
    assert_directory_equals(a3, {"zeros": np.zeros(2), "ones": np.ones(4)})
    assert_directory_equals(a4, {"zeros": np.zeros(1), "ones": np.ones(3)})
    assert CustomDirectory.n_calls == 3

    # Cleanup
    set_root_dir(Path("."))


def test_construction_from_path_and_conf(tmp_path: Path) -> None:
    # Setup
    set_root_dir(tmp_path)
    CustomDirectory.n_calls = 0
    a0 = CustomDirectory(n_zeros=2, n_ones=3)

    # Case 1: (path_given, conf_given, exists_and_matches)
    a1 = CustomDirectory(a0.path, n_zeros=2, n_ones=3)
    a2 = CustomDirectory(a0.path, dict(n_zeros=2, n_ones=3))
    a3 = CustomDirectory(f"@/{a0.path.name}", n_zeros=2, n_ones=3)
    assert_directory_equals(a1, {"zeros": np.zeros(2), "ones": np.ones(3)})
    assert_directory_equals(a2, {"zeros": np.zeros(2), "ones": np.ones(3)})
    assert_directory_equals(a3, {"zeros": np.zeros(2), "ones": np.ones(3)})
    assert a1.path == a0.path
    assert a2.path == a0.path
    assert a3.path == a0.path
    assert CustomDirectory.n_calls == 1

    # Case 2: (path_given, conf_given, exists_and_does_not_match)
    with pytest.raises(FileExistsError):
        CustomDirectory(a0.path, n_zeros=1, n_ones=3)
    with pytest.raises(FileExistsError):
        CustomDirectory(a0.path, dict(n_zeros=1, n_ones=4))
    with pytest.raises(FileExistsError):
        CustomDirectory(f"@/{a0.path.name}", n_zeros=2, n_ones=4)
    assert CustomDirectory.n_calls == 1

    # Case 3: (path_given, conf_given, does_not_exist)
    a4 = CustomDirectory(tmp_path / "a4", n_zeros=1, n_ones=3)
    a5 = CustomDirectory(tmp_path / "a5", dict(n_zeros=1, n_ones=4))
    a6 = CustomDirectory("@/a6", n_zeros=2, n_ones=4)
    assert_directory_equals(a4, {"zeros": np.zeros(1), "ones": np.ones(3)})
    assert_directory_equals(a5, {"zeros": np.zeros(1), "ones": np.ones(4)})
    assert_directory_equals(a6, {"zeros": np.zeros(2), "ones": np.ones(4)})
    assert a4.path == tmp_path / "a4"
    assert a5.path == tmp_path / "a5"
    assert a6.path == tmp_path / "a6"
    assert CustomDirectory.n_calls == 4

    # Cleanup
    set_root_dir(Path("."))


def test_modified_error(tmp_path: Path) -> None:
    # Setup
    set_root_dir(tmp_path)
    CustomDirectory.n_calls = 0
    a0 = CustomDirectory(n_zeros=2, n_ones=3)

    # modify a0
    a0.zeros = np.ones(3)

    assert a0.meta.modified

    with pytest.warns(ModifiedWarning):
        CustomDirectory(n_zeros=2, n_ones=3)


# -- [Subclass tests] Build customization --------------------------------------


class DirectoryWithUnaryBuild(Directory):
    class Config:
        prop: int

    def __init__(self) -> None:
        self.field = self.config.prop


class DirectoryWithBinaryBuild(Directory):
    class Config:
        prop: int

    def __init__(self, conf) -> None:
        self.field = conf.prop


def test_build_customization(tmp_path: Path) -> None:
    a_unary = DirectoryWithUnaryBuild(tmp_path / "unary", prop=10)
    a_binary = DirectoryWithBinaryBuild(tmp_path / "binary", prop=10)
    assert a_unary.field[()] == 10
    assert a_binary.field[()] == 10


# -- Test root control ---------------------------------------------------------


@pytest.fixture(scope="session")
def rooted_dir(tmp_path_factory):
    path = tmp_path_factory.mktemp("rooted_dir")

    @root(path)
    class RootedDirectory(Directory):
        class Config:
            start: int
            stop: int
            step: int

        def __init__(self, config) -> None:
            self.array = np.arange(config.start, config.stop, config.step)

    return RootedDirectory, path


def test_root_dir_provided(tmp_path, rooted_dir):
    RootedDirectory, rooted_dir_root_path = rooted_dir

    assert rooted_dir_root_path != tmp_path

    # case 1: root dir provided in decorator
    dir = RootedDirectory(Namespace(start=0, stop=10, step=1))
    assert_directory_equals(
        dir,
        dict(
            __type__=RootedDirectory,
            __path__=rooted_dir_root_path / dir.path.name,
            array=np.arange(0, 10, 1),
        ),
    )

    # case 2: root dir provided and not within context
    set_root_dir(tmp_path)
    dir = RootedDirectory(Namespace(start=0, stop=10, step=1))
    assert_directory_equals(
        dir,
        dict(
            __type__=RootedDirectory,
            __path__=rooted_dir_root_path / dir.path.name,
            array=np.arange(0, 10, 1),
        ),
    )

    # case 3: root_dir provided and within context
    with set_root_context(tmp_path):
        dir = RootedDirectory(Namespace(start=0, stop=10, step=1))
        assert_directory_equals(
            dir,
            dict(
                __type__=RootedDirectory,
                __path__=tmp_path / dir.path.name,
                array=np.arange(0, 10, 1),
            ),
        )


@root()
class RootedDirectory(Directory):
    def __init__(self, config) -> None:
        self.array = np.arange(config.start, config.stop, config.step)


def test_root_dir_not_provided(tmp_path):
    set_root_dir(tmp_path)

    # case 4: root dir not provided and not within context
    with pytest.warns(ImplementationWarning):
        dir = RootedDirectory(Namespace(start=0, stop=10, step=1))
    assert_directory_equals(
        dir,
        dict(
            __type__=RootedDirectory,
            __path__=tmp_path / dir.path.name,
            array=np.arange(0, 10, 1),
        ),
    )
    # case 5: root dir not provided and within context
    with set_root_context(tmp_path / "subdir"):
        with pytest.warns(ImplementationWarning):
            dir = RootedDirectory(Namespace(start=0, stop=10, step=1))
        assert_directory_equals(
            dir,
            dict(
                __type__=RootedDirectory,
                __path__=tmp_path / "subdir" / dir.path.name,
                array=np.arange(0, 10, 1),
            ),
        )


# -- test default config


class DefaultConfigDir(Directory):
    class Config:
        x: int = 2

    def __init__(self, config) -> None:
        self.x = np.arange(config.x)


class BadImplementation(Directory):
    # Config has no attributes
    class Config:
        pass

    # but has init
    def __init__(self, config) -> None:
        self.x = np.arange(config.x)


def test_default_config(tmp_path):
    set_root_dir(tmp_path)

    # from default config
    dir = DefaultConfigDir()
    name = dir.path.name
    assert_directory_equals(
        dir,
        dict(
            __type__=DefaultConfigDir,
            __path__=tmp_path / name,
            __conf__=Namespace(type="DefaultConfigDir", x=2),
            __meta__={"config": {"type": "DefaultConfigDir", "x": 2}, "status": "done"},
            x=np.arange(2),
        ),
    )

    # again
    dir = DefaultConfigDir()
    assert name == dir.path.name

    # from custom config
    dir = DefaultConfigDir(x=3)
    assert_directory_equals(
        dir,
        dict(
            __type__=DefaultConfigDir,
            __path__=tmp_path / dir.path.name,
            __conf__=Namespace(type="DefaultConfigDir", x=3),
            __meta__={"config": {"type": "DefaultConfigDir", "x": 3}, "status": "done"},
            x=np.arange(3),
        ),
    )
    assert name != dir.path.name

    # rereference
    dir = DefaultConfigDir(dir.path.name)
    assert_directory_equals(
        dir,
        dict(
            __type__=DefaultConfigDir,
            __path__=tmp_path / dir.path.name,
            __conf__=Namespace(type="DefaultConfigDir", x=3),
            __meta__={"config": {"type": "DefaultConfigDir", "x": 3}, "status": "done"},
            x=np.arange(3),
        ),
    )

    # with path from default config
    dir = DefaultConfigDir(tmp_path / "test3")
    assert_directory_equals(
        dir,
        dict(
            __type__=DefaultConfigDir,
            __path__=tmp_path / "test3",
            __conf__=Namespace(type="DefaultConfigDir", x=2),
            __meta__={"config": {"type": "DefaultConfigDir", "x": 2}, "status": "done"},
            x=np.arange(2),
        ),
    )

    # with path and custom config
    dir = DefaultConfigDir(tmp_path / "test4", dict(x=3))
    assert_directory_equals(
        dir,
        dict(
            __type__=DefaultConfigDir,
            __path__=tmp_path / "test4",
            __conf__=Namespace(type="DefaultConfigDir", x=3),
            __meta__={"config": {"type": "DefaultConfigDir", "x": 3}, "status": "done"},
            x=np.arange(3),
        ),
    )

    # with name/ path from custom config but directory exists
    with pytest.raises(FileExistsError):
        dir = DefaultConfigDir(tmp_path / "test3", dict(x=3))

    # bad implementation warning
    with pytest.warns(ImplementationWarning):
        dir = BadImplementation()
        assert_directory_equals(
            dir,
            dict(
                __type__=BadImplementation,
                __path__=tmp_path / dir.path.name,
                __conf__=Namespace(type="BadImplementation"),
                __meta__={"config": None, "status": "done"},
            ),
        )

    with pytest.warns(ImplementationWarning):
        with pytest.raises(FileNotFoundError):
            dir = BadImplementation(tmp_path / "test8")

    # config has no default attributes but directory has init, with custom config
    with pytest.warns(ImplementationWarning):
        dir = BadImplementation(dict(x=2))
        assert_directory_equals(
            dir,
            dict(
                __type__=BadImplementation,
                __path__=tmp_path / dir.path.name,
                __conf__=Namespace(type="BadImplementation", x=2),
                __meta__={
                    "config": {"type": "BadImplementation", "x": 2},
                    "status": "done",
                },
                x=np.arange(2),
            ),
        )

    with pytest.warns(ImplementationWarning):
        dir = BadImplementation(tmp_path / "test10", dict(x=2))
        assert_directory_equals(
            dir,
            dict(
                __type__=BadImplementation,
                __path__=tmp_path / "test10",
                __conf__=Namespace(type="BadImplementation", x=2),
                __meta__={
                    "config": {"type": "BadImplementation", "x": 2},
                    "status": "done",
                },
                x=np.arange(2),
            ),
        )

    # config has no default attributes but directory has init, with custom, wrong config
    with pytest.raises(AttributeError):
        with pytest.warns(ImplementationWarning):
            dir = BadImplementation(dict(y=2))

    with pytest.raises(AttributeError):
        with pytest.warns(ImplementationWarning):
            dir = BadImplementation(tmp_path / "test12", dict(y=2))


# -- test auto docstring


class AutoDocConfigDir(Directory):
    """Dir to test auto docstring based on config."""

    class Config:
        x: int = 2
        y: float = 2.0
        q = Namespace(a=1, b=2)


class AutoDocInitDir(Directory):
    "Dir to test auto docstring based on config."

    def __init__(self, x: int = 2, y: float = 2.0, q=Namespace(a=1, b=2)):
        pass


class SoloConfigDocDir(Directory):
    class Config:
        x: int = 2
        y: float = 2.0
        q = Namespace(a=1, b=2)


class SoloInitDocDir(Directory):
    def __init__(self, x: int = 2, y: float = 2.0, q=Namespace(a=1, b=2)):
        pass


class EmptyConfigDocDir(Directory):
    """Dir to test auto docstring based on config."""

    class Config:
        pass


class EmptyInitDocDir(Directory):
    """Dir to test auto docstring based on config."""

    def __init__(self):
        pass


class NoConfigDocDir(Directory):
    """Dir to test auto docstring based on config."""

    pass


def test_auto_doc(tmp_path):
    a = AutoDocConfigDir()
    doc = "Dir to test auto docstring based on config.{}".format(
        _auto_doc(a, cls_doc=False)
    )
    # breakpoint()
    assert_directory_equals(
        a,
        dict(
            __doc__=doc,
            __exists__=False,
        ),
    )

    a1 = AutoDocInitDir()
    assert_directory_equals(
        a1,
        dict(
            __doc__=doc.replace("AutoDocConfigDir", "AutoDocInitDir"),
            __exists__=False,
        ),
    )

    b = SoloConfigDocDir()
    doc = _auto_doc(b, cls_doc=False)
    assert_directory_equals(
        b,
        dict(
            __doc__=doc,
            __exists__=False,
        ),
    )

    b1 = SoloInitDocDir()
    assert_directory_equals(
        b1,
        dict(
            __doc__=doc.replace("SoloConfigDocDir", "SoloInitDocDir"),
            __exists__=False,
        ),
    )

    c = EmptyConfigDocDir()
    doc = "Dir to test auto docstring based on config.{}".format(
        _auto_doc(c, cls_doc=False)
    )
    assert_directory_equals(
        c,
        dict(
            __doc__=doc,
            __exists__=False,
        ),
    )

    c1 = EmptyInitDocDir()
    assert_directory_equals(
        c1,
        dict(
            __doc__=doc,
            __exists__=False,
        ),
    )

    d = NoConfigDocDir()
    doc = "Dir to test auto docstring based on config.{}".format(
        _auto_doc(d, cls_doc=False)
    )
    assert_directory_equals(
        d,
        dict(__doc__=doc, __exists__=False),
    )


# --- test default config and init from init kwargs


class SmartDir(Directory):
    def __init__(self, foo: int = 2, bar: int = 3):
        self.foo = foo
        self.bar = bar


def test_init_from_kwargs(tmp_path):
    set_root_dir(tmp_path)
    dir = SmartDir()
    assert_directory_equals(
        dir,
        dict(
            __path__=tmp_path / dir.path.name,
            __conf__=Namespace(type="SmartDir", foo=2, bar=3),
            __meta__={
                "config": {"type": "SmartDir", "foo": 2, "bar": 3},
                "status": "done",
            },
            foo=2,
            bar=3,
        ),
    )

    dir = SmartDir(foo=5, bar=1)
    assert_directory_equals(
        dir,
        dict(
            __path__=tmp_path / dir.path.name,
            __conf__=Namespace(type="SmartDir", foo=5, bar=1),
            __meta__={
                "config": {"type": "SmartDir", "foo": 5, "bar": 1},
                "status": "done",
            },
            foo=5,
            bar=1,
        ),
    )
    name = dir.path.name

    dir = SmartDir(name)
    assert_directory_equals(
        dir,
        dict(
            __path__=tmp_path / name,
            __conf__=Namespace(type="SmartDir", foo=5, bar=1),
            __meta__={
                "config": {"type": "SmartDir", "foo": 5, "bar": 1},
                "status": "done",
            },
            foo=5,
            bar=1,
        ),
    )

    with pytest.raises(FileExistsError):
        dir = SmartDir(dir.path.name, foo=3, bar=2)


# --- test directory with Config but without init


class NetworkDir(Directory):
    class Config:
        tau: float = 200.0
        sigma: float = 0.1

    def train(self):
        del self.loss
        for i in range(self.config.N):
            self.extend(
                "loss",
                [np.exp(-i / self.config.tau) + np.random.rand() * self.config.sigma],
            )


def test_directory_with_config_without_init(tmp_path):
    set_root_dir(tmp_path)

    nnd = NetworkDir()
    assert_directory_equals(
        nnd,
        dict(
            __conf__=Namespace(type="NetworkDir", tau=200.0, sigma=0.1),
            __exists__=False,
        ),
    )

    nnd = NetworkDir(tmp_path / "test")
    assert_directory_equals(
        nnd,
        dict(
            __path__=tmp_path / "test",
            __conf__=Namespace(type="NetworkDir", tau=200.0, sigma=0.1),
            __exists__=False,
        ),
    )


# --- test merge of defaults


class ConIni1(Directory):
    class Config:
        sigma: float = 0.1

    def __init__(self, tau=200):
        pass


def test_cross_configs(tmp_path):
    """Test that default config and init kwargs are merged.

    Raises error if default config and init kwargs are not compatible.
    """
    set_root_dir(tmp_path)

    dir = ConIni1()
    assert_directory_equals(
        dir,
        dict(
            __conf__=Namespace(type="ConIni1", tau=200.0, sigma=0.1),
            __exists__=False,
        ),
    )

    with pytest.raises(ValueError):

        class ConIni2(Directory):
            class Config:
                tau: float = 200.0
                sigma: float = 0.1

            def __init__(self, sigma=2):
                pass


# --- test delete_if_exists context manager


def test_delete_if_exists(tmp_path):
    set_root_dir(tmp_path)

    name = "test"
    dir = DefaultConfigDir(name, x=2)
    assert_directory_equals(
        dir,
        dict(
            __type__=DefaultConfigDir,
            __path__=tmp_path / name,
            __conf__=Namespace(type="DefaultConfigDir", x=2),
            __meta__={"config": {"type": "DefaultConfigDir", "x": 2}, "status": "done"},
            x=np.arange(2),
        ),
    )

    with pytest.raises(FileExistsError):
        dir2 = DefaultConfigDir(name, config=dict(x=3))

    with delete_if_exists():
        dir2 = DefaultConfigDir(name, config=dict(x=3))
        assert_directory_equals(
            dir2,
            dict(
                __type__=DefaultConfigDir,
                __path__=tmp_path / name,
                __conf__=Namespace(type="DefaultConfigDir", x=3),
                __meta__={
                    "config": {"type": "DefaultConfigDir", "x": 3},
                    "status": "done",
                },
                x=np.arange(3),
            ),
        )

    with pytest.raises(FileExistsError):
        dir = DefaultConfigDir(name, x=2)

    dir = DefaultConfigDir(name, x=2, delete_if_exists=True)
    assert_directory_equals(
        dir,
        dict(
            __type__=DefaultConfigDir,
            __path__=tmp_path / name,
            __conf__=Namespace(type="DefaultConfigDir", x=2),
            __meta__={"config": {"type": "DefaultConfigDir", "x": 2}, "status": "done"},
            x=np.arange(2),
        ),
    )

    dir = DefaultConfigDir(name, x=2, delete_if_exists=False)
    assert_directory_equals(
        dir,
        dict(
            __type__=DefaultConfigDir,
            __path__=tmp_path / name,
            __conf__=Namespace(type="DefaultConfigDir", x=2),
            __meta__={"config": {"type": "DefaultConfigDir", "x": 2}, "status": "done"},
            x=np.arange(2),
        ),
    )


# --- test directory comparison


class CompDir(Directory):
    class Config:
        x: int = 2

    def __init__(self, x: int = 2):
        self.x = x


def test_comparison(tmp_path):
    set_root_dir(tmp_path)

    a = CompDir()
    b = CompDir()
    assert_equal_directories(a, b)
    assert a.path == b.path

    a = CompDir("a")
    b = CompDir("b")
    assert_equal_directories(a, b)
    assert a.path != b.path

    b = CompDir(x=3)
    with pytest.raises(AssertionError):
        assert_equal_directories(a, b)

    b.x = 2
    with pytest.raises(AssertionError):
        assert_equal_attributes(a, b)


def test_diff(tmp_path):
    set_root_dir(tmp_path)

    a = CompDir()
    b = CompDir(x=3)
    diff = DirectoryDiff(a, b)
    assert not diff.equal()
    assert a != b

    a = CompDir("a")
    b = CompDir("b")
    np.savez(b.y.path, np.ones(10))
    diff = DirectoryDiff(a, b)
    assert not diff.equal()
    assert a != b

    a = CompDir("aa")
    b = CompDir("bb")
    np.savez(a.y.path, np.ones(10))
    np.savez(b.y.path, np.ones(10))
    diff = DirectoryDiff(a, b)
    assert diff.equal()
    assert a == b

    df = pd.DataFrame(np.random.rand(10, 2), columns=["a", "b"])
    a = CompDir("aaa")
    b = CompDir("bbb")
    a.df = df
    b.df = df
    diff = DirectoryDiff(a, b)
    assert diff.equal()
    assert a == b

    df1 = pd.DataFrame(np.random.rand(10, 2), columns=["a", "b"])
    df2 = pd.DataFrame(np.random.rand(10, 2), columns=["a", "b"])
    a = CompDir("aaaa")
    b = CompDir("bbbb")
    a.df = df1
    b.df = df2
    diff = DirectoryDiff(a, b)
    assert not diff.equal()
    assert a != b

    a = Directory("aaaaa")
    a.x = 3
    b = Directory("bbbbb")
    b.x = 2
    assert a.diff(b) == {"aaaaa": ["≠x: 3"], "bbbbb": ["≠x: 2"]}


def test_read_meta(tmp_path):
    set_root_dir(tmp_path)

    directory = Directory("test")
    assert directory.meta == {"config": None, "status": "done"}
    assert not (directory.path / "_meta.yaml").exists()

    import yaml

    directory.path.mkdir()
    with open(directory.path / "_meta.yaml", "w") as f:
        yaml.dump({"x": 2}, f)

    with pytest.raises(
        MetadataValidationError, match="Missing required 'config' field"
    ):
        assert directory.config

    with open(directory.path / "_meta.yaml", "w") as f:
        yaml.dump({"config": 2}, f)

    with pytest.raises(MetadataValidationError, match="'config' must be a Namespace"):
        assert directory.config

    with open(directory.path / "_meta.yaml", "w") as f:
        yaml.dump({"config": {"x": 1}}, f)

    with pytest.raises(
        MetadataValidationError, match="Missing required 'status' field"
    ):
        assert directory.status

    with open(directory.path / "_meta.yaml", "w") as f:
        yaml.dump({"config": {"x": 1}, "status": 1}, f)

    with pytest.raises(MetadataValidationError, match="'status' must be a string"):
        assert directory.status


def test_write_config(tmp_path):
    set_root_dir(tmp_path)

    directory = Directory("test")
    directory.path.mkdir()
    assert directory.meta == {"config": None, "status": "done"}
    assert not (directory.path / "_meta.yaml").exists()

    with pytest.warns(ConfigWarning):
        directory.config = {"x": 2}

    assert read_meta(directory.path).config.to_dict() == {"x": 2}
    assert read_meta(directory.path).status == "manually written"
    assert directory.config == {"x": 2}


def test_root_precedence(tmp_path):
    @root(tmp_path / "test_dir", precedence=3)
    class MyDir(Directory):
        def __init__(self, file: str = "test", a=1, b=2) -> None:
            assert str(self.path.parent / file).endswith(file)
            self.file = bytes(file, "utf-8")

    with set_root_context(tmp_path / "other_dir"):
        dir = MyDir()
        assert dir.path.name.split(".")[-1] == "MyDir_0000"
        assert dir.file[()] == b"test"
        assert dir.path.parent.name == "test_dir"

    set_root_dir(tmp_path / "other_dir")
    dir = MyDir(file="test2", a=3, b=2)
    assert dir.file[()] == b"test2"
    assert dir.path.parent.name == "test_dir"

    with set_root_context(tmp_path / "test_dir"):
        dir = MyDir(dict(file="test2", a=3, b=1))
        assert dir.file[()] == b"test2"
        assert dir.path.parent.name == "test_dir"

    set_root_dir(tmp_path / "test_dir")
    dir = MyDir(**dict(file="test2", a=0, b=3))
    assert dir.file[()] == b"test2"
    assert dir.path.parent.name == "test_dir"


class ParallelDir(Directory):
    def __init__(self, time_asleep: float = 0.05):
        time.sleep(time_asleep)


def create_test_dir(root_path, retry):
    set_root_dir(root_path)
    ParallelDir(dict(time_asleep=0.05, retry=retry))


def test_parallel_creation(tmp_path):
    num_instances = 50
    num_retries = 3

    for i in range(num_retries):
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
        pool.starmap(create_test_dir, [(tmp_path, i) for i in range(num_instances)])
        pool.close()
        pool.join()


class ParentDir(Directory):
    pass


class InvalidConfigFieldDir(Directory):
    class Config:
        x: int = 2
        y: int = 3

    def __init__(self, x=2, y=3):
        self.q = 3


def test_copy_includes_config(tmp_path):
    set_root_dir(tmp_path)

    parent = ParentDir(tmp_path / "parent")

    dir = InvalidConfigFieldDir(tmp_path / "child")

    parent.child = dir

    # reinitialize directory in original place
    dir = InvalidConfigFieldDir(dir.path, config=dict(x=2, y=3))

    # reinitialize directory in new place
    dir = InvalidConfigFieldDir(parent.child.path, config=dict(x=2, y=3))

    yaml = YAML()
    # create meta file with invalid config field
    with open(dir.path / "_meta.yaml", "w") as f:
        yaml.dump({"config": None}, f)

    with pytest.raises(MetadataValidationError, match="'config' must be a Namespace"):
        dir = InvalidConfigFieldDir(parent.child.path, config=dict(x=2, y=3))
