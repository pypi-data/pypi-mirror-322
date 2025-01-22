# SPDX-FileCopyrightText: © 2024 Hugues Bruant <hugues.bruant@gmail.com>

"""
This module is an implementation detail: there is no guarantee of forward
or backwards compatibility, even across patch releases.
"""

import contextlib
import importlib
import importlib.util
import io
import os
import sys
import traceback

from typing import Callable, Dict, List, Set, Optional, Tuple

try:
    import pytest

    SkippedTest = pytest.skip.Exception
except ImportError:

    class SkippedTest(Exception):  # type: ignore[no-redef]
        pass


from .args import Arg, parse_args
from .graph import ModuleGraph
from .api import ValidatorHook
from .tracker import Tracker, print_clean_traceback
from .util import (
    print_with_timestamp,
    load_import_graph,
    load_hook_or_default,
)


def import_with_capture(fq: str, c_out: bool, c_err: bool) -> None:
    """import a single module, with optional capture of stdout and/or stderr"""
    with io.StringIO() as f:
        with contextlib.redirect_stdout(
            f
        ) if c_out else contextlib.nullcontext(), contextlib.redirect_stderr(
            f
        ) if c_err else contextlib.nullcontext():
            try:
                importlib.__import__(fq, fromlist=())
            except:
                if c_out or c_err:
                    print_with_timestamp(f"--- captured output for: {fq}")
                    sys.stderr.write(f.getvalue())
                raise


def recursive_import_tests(
    path: str, import_prefix: str, hook: ValidatorHook, errors: Dict[str, BaseException]
) -> Set[str]:
    """
    Recursively walk down a file tree, importing every file that looks like a test file.

    NB: all __init__.py are imported, even in packages that do not actually contain any
    test code.
    """
    imported: Set[str] = set()

    # process __init__.py first if present
    init_py = os.path.join(path, "__init__.py")
    if os.path.exists(init_py):
        try:
            import_with_capture(
                import_prefix,
                hook.should_capture_stdout(),
                hook.should_capture_stderr(),
            )
        except BaseException as ex:
            # NB: this should not happen, report so it can be fixed and proceed
            errors[init_py] = ex
    else:
        # stop recursion if not a python package
        return imported

    with os.scandir(path) as it:
        for e in it:
            if e.is_dir():
                imported |= recursive_import_tests(
                    e.path, import_prefix + "." + e.name, hook, errors
                )
            elif e.is_file() and hook.is_test_file(e.name):
                hook.before_file(e, import_prefix)
                fq = import_prefix + "." + e.name[:-3]
                try:
                    import_with_capture(
                        fq, hook.should_capture_stdout(), hook.should_capture_stderr()
                    )
                    imported.add(fq)
                except SkippedTest:
                    # pytest.importorskip ...
                    pass
                except BaseException as ex:
                    # NB: this should not happen, report so it can be fixed and proceed
                    errors[e.path] = ex
                hook.after_file(e, import_prefix)

    return imported


def validate_subset(
    py_tracked: Dict[str, Set[str]],
    rust_graph: ModuleGraph,
    filter_fn: Callable[[str], bool],
    package: Optional[str] = None,
) -> int:
    """
    Validate that a subset of tracked matching the given `filter_fn` are safely
    covered by the import graph (i.e. that the set of dependencies tracked by the statically
    derived import graph is a superset of the set of dependencies caught by the dynamic
    import Tracker while importing the actual Python modules)
    """
    diff_count = 0
    for module, pydeps in py_tracked.items():
        if not filter_fn(module):
            continue
        rdeps = rust_graph.module_depends_on(module, package) or frozenset()

        # NB: we only care about anything that the rust code might be missing
        # it's safe to consider extra dependencies, and in fact expected since
        # the rust parser goes deep and tracks import statements inside code
        # that might never get executed whereas by design the python validation
        # will only track anything that gets executed during the import phase
        rust_missing = pydeps - rdeps
        if rust_missing:
            diff_count += 1
            print(
                f"{module} rust {len(rdeps)} / py {len(pydeps)}: rust missing {len(rust_missing)} {rust_missing}"
            )
    return diff_count


def validate_folder(
    fs: str, py: str, hook: ValidatorHook, t: Tracker, g: ModuleGraph
) -> Tuple[int, int]:
    # print_with_timestamp(f"--- {base}")
    # put package path first in sys.path to ensure finding test files
    sys.path.insert(0, os.path.abspath(os.path.dirname(fs)))
    old_k = set(sys.modules.keys())

    hook.before_folder(fs, py)

    errors: Dict[str, BaseException] = {}

    # we want to import every test file in that package, recursively,
    # while preserving the appropriate import name, to allow for:
    #  - resolution of __init__.py
    #  - resolution of test helpers, via absolute or relative import
    imported = recursive_import_tests(fs, py, hook, errors)

    if errors:
        print(f"{len(errors)} exceptions encountered in {fs} / {py}!")

        for filepath, ex in errors.items():
            print_with_timestamp(f"--- {filepath}")
            print(f"{type(ex)} {ex}")
            print_clean_traceback(traceback.extract_tb(ex.__traceback__))

    is_local_ns = py.partition(".")[0] in hook.local_namespaces()

    if is_local_ns:
        with_dynamic = {}
        for m in imported:
            with_dynamic[m] = t.with_dynamic(m)

        # NB: do validation at the package level for the local namespace
        # this is necessary because it is not a unified namespace. There can be
        # conflicts between similarly named test modules across packages.
        #
        # NB: we only validate test files, not test helpers. This is because, for
        # performance reason, some dynamic dependencies are only applied to leaves
        # of the import graph (i.e modules not imported by any other module)
        # This is fine because the purpose of this validation is to ensure that we
        # can determine a set of affected *test files* from a given set of modified
        # files, so as long as we validate that tests have matching imports between
        # python and Rust, we're good to go.
        def is_local_test_module(module: str) -> bool:
            last = module.rpartition(".")[2]
            return module.startswith(py) and hook.is_test_file(last + ".py")

        num_mismatching_files = validate_subset(
            with_dynamic, g, package=fs, filter_fn=is_local_test_module
        )

        # cleanup to avoid contaminating subsequent iterations
        new_k = sys.modules.keys() - old_k
        for m in new_k:
            if m.startswith(py) and (len(m) <= len(py) or m[len(py)] == "."):
                del t.tracked[m]
                if m in t.dynamic_users:
                    del t.dynamic_users[m]
                del sys.modules[m]
    else:
        num_mismatching_files = 0

    sys.path = sys.path[1:]

    hook.after_folder(fs, py)

    return len(errors), num_mismatching_files


def validate(
    hook_path: Optional[str], graph_path: Optional[str] = None
) -> Tuple[int, int]:
    hook = load_hook_or_default(hook_path)

    t = Tracker()
    t.start_tracking(
        hook.global_namespaces() | hook.local_namespaces(),
        patches=hook.import_patches(),
        record_dynamic=True,
        implicit_anchor_aggregation=hook.implicit_anchor_aggregation(),
        dynamic_anchors=hook.dynamic_anchors(),
        dynamic_ignores=hook.dynamic_ignores(),
        ignore_prefixes=hook.external_imports(),
        log_file=hook.tracker_log(),
    )

    # NB: must be called after tracker, before module graph
    hook.setup()

    g = load_import_graph(hook, graph_path)
    if graph_path and not os.path.exists(graph_path):
        print_with_timestamp("--- saving import graph")
        g.to_file(graph_path)

    # keep track or errors and import differences
    files_with_missing_imports = 0
    error_count = 0

    # TODO: user-defined order (toposort of package dep graph...)
    print_with_timestamp("--- tracking python imports")
    for fs, py in sorted(hook.test_folders().items()):
        n_errors, n_mismatching_files = validate_folder(fs, py, hook, t, g)

        files_with_missing_imports += n_mismatching_files
        error_count += n_errors

    t.stop_tracking()

    if t.dynamic and hook.record_dynamic():
        print_with_timestamp("--- locations of dynamic imports")
        dedup_stack = set()
        for dyn_stack in t.dynamic:
            as_tuple = tuple((f.filename, f.lineno) for f in dyn_stack)
            if as_tuple in dedup_stack:
                continue
            dedup_stack.add(as_tuple)
            print("---")
            traceback.print_list(dyn_stack, file=sys.stdout)

    # validate global namespace once all packages have been processed
    print_with_timestamp("--- comparing code import graphs")
    files_with_missing_imports += validate_subset(
        t.tracked,
        g,
        filter_fn=lambda module: module.partition(".")[0] in hook.global_namespaces(),
    )

    return error_count, files_with_missing_imports


def main(args: List[str]) -> None:
    """
    main entry point for the import-time validator
    """
    p = parse_args(args, supported_args={Arg.hook_path, Arg.graph_path})

    # TODO: support override from hook
    from ._prunepytest import configure_logger

    configure_logger("/dev/stdout", "info")

    n_err, m_missing = validate(hook_path=p.hook_path, graph_path=p.graph_path)

    print_with_timestamp("--- validation result")
    if n_err + m_missing == 0:
        print("The rust module graph can be trusted")
        sys.exit(0)
    else:
        if m_missing:
            print("The rust module graph is missing some imports")
            print("You may need to make some dynamic imports explicit")
        if n_err:
            print("Errors prevented validation of the rust module graph")
            print("Fix them and try again...")
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
