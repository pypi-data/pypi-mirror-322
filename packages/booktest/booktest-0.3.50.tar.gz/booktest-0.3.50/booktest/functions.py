import copy
import functools
import hashlib
import os
import pickle
import json
import sys

from booktest import TestCaseRun
from booktest.coroutines import maybe_async_call
from booktest.snapshots import frozen_snapshot_path, out_snapshot_path, have_snapshots_dir
from booktest.utils import open_file_or_resource, file_or_resource_exists


class FunctionCall:

    def __init__(self, json_object):
        self.json_object = json_object

        hash_code = self.json_object.get("hash")

        if hash_code is None:
            h = hashlib.sha1()
            h.update(json.dumps(self.json_object).encode())
            hash_code = str(h.hexdigest())
            self.json_object["hash"] = hash_code

        self.hash = hash_code

    def func(self):
        return self.json_object["func"]

    def args(self):
        # tuple is used by default in python
        return self.json_object["args"]

    def kwargs(self):
        return self.json_object["kwargs"]

    def to_json_object(self, hide_details):
        rv = copy.copy(self.json_object)
        rv["hash"] = self.hash
        return rv

    @staticmethod
    def from_properties(func, args, kwargs):
        json_object = {
            "func": str(func.__qualname__),
            "args": list(args),
            "kwargs": dict(kwargs)
        }
        return FunctionCall(json_object)

    def __eq__(self, other):
        return isinstance(other, FunctionCall) and self.hash == other.hash


class FunctionCallSnapshot:

    def __init__(self,
                 call,
                 result):
        self.call = call
        self.result = result

    def match(self, call: FunctionCall):
        return self.call == call

    @staticmethod
    def from_json_object(json_object):
        return FunctionCallSnapshot(FunctionCall(json_object["call"]),
                                    json_object["result"])

    def json_object(self):
        rv = {
            "call": self.call.json_object,
            "result": self.result
        }
        return rv

    def hash(self):
        return self.call.hash

    def __eq__(self, other):
        return isinstance(other, FunctionCallSnapshot) and self.hash() == other.hash()


class FunctionSnapshotter:

    def __init__(self, t: TestCaseRun, func):
        self.t = t
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.t.snapshot(self.func, *args, **kwargs)

    def __repr__(self):
        return str(self.func)


def set_function(func, value):
    target = None
    if hasattr(func, "__self__"):
        target = func.__self__
    elif hasattr(func, "__module__"):
        target = sys.modules[func.__module__]
    name = func.__name__
    setattr(target, name, value)


class SnapshotFunctions:

    def __init__(self, t: TestCaseRun, snapshot_funcs: list = None):
        self.t = t

        if snapshot_funcs is None:
            snapshot_funcs = []

        self.snapshot_funcs = snapshot_funcs

        self.snapshot_file = frozen_snapshot_path(t, "functions.json")
        self.snapshot_out_file = out_snapshot_path(t, "functions.json")

        self.refresh_snapshots = t.config.get("refresh_snapshots", False)
        self.complete_snapshots = t.config.get("complete_snapshots", False)

        self.capture_snapshots = self.refresh_snapshots or self.complete_snapshots

        self.snapshots = None
        self.calls = None
        self.snapshotters = None

    def snapshot(self, func, *args, **kwargs):
        call = FunctionCall.from_properties(func, args, kwargs)

        for snapshot in reversed(self.snapshots):
            if snapshot.match(call):
                if snapshot not in self.calls:
                    self.calls.append(snapshot)
                return snapshot.result

        if not self.capture_snapshots:
            raise ValueError(f"missing snapshot for function call {call.func()} - {call.hash}. "
                             f"try running booktest with '-s' flag to capture the missing snapshot")

        rv = func(*args, **kwargs)

        # remove old version, it may have been timeout
        self.calls = list([i for i in self.calls if not i.call == call])
        self.calls.append(FunctionCallSnapshot(call, rv))

        return rv

    def start(self):
        if self.snapshots is not None:
            raise RuntimeError('FunctionSnapshots has already been started')

        snapshots = []

        if file_or_resource_exists(self.snapshot_file, self.t.resource_snapshots) and not self.refresh_snapshots:
            with open_file_or_resource(self.snapshot_file, self.t.resource_snapshots) as f:
                for value in json.load(f):
                    snapshot = FunctionCallSnapshot.from_json_object(value)
                    snapshots.append(snapshot)

        snapshotters = []

        for func in self.snapshot_funcs:
            snapshotter = FunctionSnapshotter(self, func)
            set_function(func, snapshotter)
            snapshotters.append(snapshotter)

        self.snapshots = snapshots
        self.calls = []
        self.snapshotters = snapshotters

    def stop(self):
        for snapshotter in self.snapshotters:
            func = snapshotter.func
            set_function(func, func)

        stored = []
        for snapshot in self.calls:
            stored.append(snapshot.json_object())

        have_snapshots_dir(self.t)
        with open(self.snapshot_out_file, "w") as f:
            json.dump(stored, f, indent=4)

        self.snapshotters = None
        self.snapshots = None
        self.calls = None

    def t_snapshots(self):
        self.t.h1("function call snapshots:")
        for i in self.calls:
            self.t.tln(f" * {i.call.func()} - {i.call.hash}")

    def __enter__(self):
        self.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.t_snapshots()
        self.stop()


def snapshot_functions(*snapshot_funcs):
    """
    @param lose_request_details Saves no request details to avoid leaking keys
    @param ignore_headers Ignores all headers (True) or specific header list
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            from booktest import TestBook
            if isinstance(args[0], TestBook):
                t = args[1]
            else:
                t = args[0]
            with SnapshotFunctions(t, snapshot_funcs):
                return await maybe_async_call(func, args, kwargs)
        wrapper._original_function = func
        return wrapper

    return decorator


class MockFunctions:

    def __init__(self, mock_funcs: dict = None):
        if mock_funcs is None:
            mock_funcs = {}

        self.mock_funcs = mock_funcs
        self._original_funcs = None

    def start(self):
        if self._original_funcs is not None:
            raise RuntimeError('FunctionSnapshots has already been started')

        original_funcs = []

        for func, mock in self.mock_funcs.items():
            set_function(func, mock)
            original_funcs.append(func)

        self._original_funcs = original_funcs

    def stop(self):
        for func in self._original_funcs:
            set_function(func, func)

        self._original_funcs = None

    def __enter__(self):
        self.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


def mock_functions(mock_funcs):
    """
    @param lose_request_details Saves no request details to avoid leaking keys
    @param ignore_headers Ignores all headers (True) or specific header list
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            from booktest import TestBook
            if isinstance(args[0], TestBook):
                t = args[1]
            else:
                t = args[0]
            with MockFunctions(mock_funcs):
                return await maybe_async_call(func, args, kwargs)
        wrapper._original_function = func
        return wrapper

    return decorator
