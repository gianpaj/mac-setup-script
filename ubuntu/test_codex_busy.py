import asyncio
import contextlib
import importlib.machinery
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import AsyncMock, patch

loader = importlib.machinery.SourceFileLoader("codex_busy", str(Path(__file__).with_name("codex-busy")))
spec = importlib.util.spec_from_loader(loader.name, loader)
monitor = importlib.util.module_from_spec(spec)
loader.exec_module(monitor)


def state(active=(), updated_at=1000):
    return {"active": list(active), "updated_at": updated_at}


class PolicyTests(unittest.TestCase):
    def test_long_turn_is_busy_even_without_recent_updates(self):
        self.assertTrue(monitor.is_busy(state(["remote"]), state(["remote"]), 10000))

    def test_idle_open_chat_does_not_block(self):
        self.assertFalse(monitor.is_busy(state(), state(), 10000))

    def test_completion_resets_timer_once(self):
        self.assertTrue(monitor.is_busy(state(), state(["remote"]), 10000))
        self.assertFalse(monitor.is_busy(state(), state(), 10000))

    def test_new_update_resets_timer_once_without_an_extra_grace_window(self):
        self.assertTrue(monitor.is_busy(state(updated_at=2000), state(), 2000))
        self.assertFalse(monitor.is_busy(state(updated_at=2000), state(updated_at=2000), 2001))

    def test_first_sample_protects_recent_work(self):
        self.assertTrue(monitor.is_busy(state(), None, 1899))
        self.assertFalse(monitor.is_busy(state(), None, 1900))

    def test_inspection_does_not_consume_updates(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            path.write_text(json.dumps(state()))
            original = path.read_text()
            with patch.object(monitor, "snapshot", AsyncMock(return_value=state(updated_at=2000))):
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(0, monitor.check(Path("socket"), path, inspect=True))
                self.assertEqual(original, path.read_text())
                self.assertEqual(0, monitor.check(Path("socket"), path))
                self.assertEqual(1, monitor.check(Path("socket"), path))

    def test_api_and_state_errors_keep_machine_awake(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            path.write_text("invalid json")
            args = ["codex-busy", "--socket", "/test", "--state-file", str(path)]
            with patch("sys.argv", args), contextlib.redirect_stderr(io.StringIO()):
                with patch.object(monitor, "snapshot", AsyncMock(return_value=state())):
                    self.assertEqual(0, monitor.main())
                with patch.object(monitor, "snapshot", AsyncMock(side_effect=TimeoutError)):
                    self.assertEqual(0, monitor.main())


class ProtocolTests(unittest.IsolatedAsyncioTestCase):
    async def test_missing_daemon_is_idle(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(state(updated_at=0), await monitor.snapshot(Path(directory) / "absent.sock"))

    async def test_pages_loaded_threads_and_uses_persisted_updates(self):
        import websockets
        methods = []

        async def handler(connection):
            async for raw in connection:
                request = json.loads(raw)
                method = request["method"]
                methods.append(method)
                params = request.get("params", {})
                if method == "initialized":
                    continue
                if method == "initialize":
                    result = {}
                elif method == "thread/loaded/list":
                    if params["cursor"] is None:
                        result = {"data": ["idle"], "nextCursor": "page2"}
                    else:
                        result = {"data": ["remote"], "nextCursor": None}
                elif method == "thread/read":
                    self.assertFalse(params["includeTurns"])
                    kind = "active" if params["threadId"] == "remote" else "idle"
                    result = {"thread": {"status": {"type": kind}, "updatedAt": 999999}}
                elif method == "thread/list":
                    self.assertTrue(params["useStateDbOnly"])
                    self.assertIn("appServer", params["sourceKinds"])
                    self.assertIn("subAgent", params["sourceKinds"])
                    self.assertEqual("updated_at", params["sortKey"])
                    result = {"data": [{"updatedAt": 2000 if params["archived"] else 1000}]}
                else:
                    self.fail(f"Unexpected mutating/subscription method: {method}")
                await connection.send(json.dumps({"id": request["id"], "result": result}))

        with tempfile.TemporaryDirectory() as directory:
            socket = Path(directory) / "server.sock"
            async with websockets.unix_serve(handler, str(socket)):
                result = await asyncio.wait_for(monitor.snapshot(socket), 3)
        self.assertEqual(state(["remote"], updated_at=2000), result)
        self.assertEqual(2, methods.count("thread/loaded/list"))

    async def test_rpc_errors_are_not_treated_as_idle(self):
        import websockets

        async def handler(connection):
            request = json.loads(await connection.recv())
            await connection.send(json.dumps({"id": request["id"], "error": {"code": -1}}))

        with tempfile.TemporaryDirectory() as directory:
            socket = Path(directory) / "server.sock"
            async with websockets.unix_serve(handler, str(socket)):
                with self.assertRaises(RuntimeError):
                    await monitor.snapshot(socket)


if __name__ == "__main__":
    unittest.main()
