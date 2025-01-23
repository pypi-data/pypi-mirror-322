import os
import pytest
from textwrap import dedent
from unittest.mock import AsyncMock, patch
from py_pg_notify.notifier import Notifier
from py_pg_notify.pgmanager import (
    PGConfig,
)  # Assuming PGConfig is imported from the correct module


@pytest.mark.asyncio
class TestNotifier:
    @pytest.fixture
    def mock_config(self):
        return PGConfig(
            user="user",
            password="password",
            dbname="testdb",
            host="localhost",
            port=5432,
        )

    @pytest.fixture
    def mock_handler(self):
        async def handler(connection, pid, channel, payload):
            pass

        return handler

    async def test_notifier_initialization_missing_params(self):
        with pytest.raises(ValueError):
            Notifier(
                config=PGConfig(user="user", password="password")
            )  # Missing dbname

    @patch("asyncpg.connect", new_callable=AsyncMock)
    async def test_connect_successful(self, mock_connect, mock_config):
        notifier = Notifier(config=mock_config)
        await notifier.connect()
        mock_connect.assert_called_once_with(mock_config.dsn)
        assert notifier.conn == mock_connect.return_value

    @patch("asyncpg.connect", new_callable=AsyncMock)
    async def test_connect_already_connected(self, mock_connect, mock_config):
        notifier = Notifier(config=mock_config)
        notifier.conn = AsyncMock()
        await notifier.connect()
        mock_connect.assert_not_called()  # No new connection should be created

    @patch("asyncpg.connect", new_callable=AsyncMock)
    async def test_create_trigger_function_successful(self, mock_connect, mock_config):
        notifier = Notifier(config=mock_config)
        await notifier.connect()

        await notifier.create_trigger_function("test_function", "test_channel")
        expected_query = dedent(
            """
            CREATE OR REPLACE FUNCTION test_function()
            RETURNS TRIGGER AS $$ 
            BEGIN 
                PERFORM pg_notify(
                    'test_channel', 
                    json_build_object(
                        'trigger', TG_NAME, 
                        'timing', TG_WHEN, 
                        'event', TG_OP, 
                        'new', NEW, 
                        'old', OLD
                    )::text 
                ); 
                RETURN NEW; 
            END; 
            $$ LANGUAGE plpgsql;
            """
        )

        actual_query = mock_connect.return_value.execute.call_args[0][0]
        assert " ".join(actual_query.split()) == " ".join(expected_query.split())

    async def test_create_trigger_function_without_connection(self):
        notifier = Notifier(
            config=PGConfig(user="user", password="password", dbname="testdb")
        )
        with pytest.raises(RuntimeError):
            await notifier.create_trigger_function("test_function", "test_channel")

    @patch("asyncpg.connect", new_callable=AsyncMock)
    async def test_get_trigger_functions_successful(self, mock_connect, mock_config):
        notifier = Notifier(config=mock_config)
        await notifier.connect()

        mock_connect.return_value.fetch.return_value = [
            {"function_name": "test_function"}
        ]
        functions = await notifier.get_trigger_functions("test_table")
        assert functions == ["test_function"]

    async def test_get_trigger_functions_without_connection(self):
        notifier = Notifier(
            config=PGConfig(user="user", password="password", dbname="testdb")
        )
        with pytest.raises(RuntimeError):
            await notifier.get_trigger_functions("test_table")

    @patch("asyncpg.connect", new_callable=AsyncMock)
    async def test_remove_trigger_function_successful(self, mock_connect, mock_config):
        notifier = Notifier(config=mock_config)
        await notifier.connect()

        await notifier.remove_trigger_function("test_function")
        mock_connect.return_value.execute.assert_called_once_with(
            "DROP FUNCTION IF EXISTS test_function CASCADE;"
        )

    async def test_remove_trigger_function_without_connection(self):
        notifier = Notifier(
            config=PGConfig(user="user", password="password", dbname="testdb")
        )
        with pytest.raises(RuntimeError):
            await notifier.remove_trigger_function("test_function")

    @patch("asyncpg.connect", new_callable=AsyncMock)
    async def test_create_trigger_successful(self, mock_connect, mock_config):
        notifier = Notifier(config=mock_config)
        await notifier.connect()

        await notifier.create_trigger(
            "test_table", "test_trigger", "test_function", "INSERT"
        )
        expected_query = dedent(
            """
            CREATE TRIGGER test_trigger
            AFTER INSERT ON test_table
            FOR EACH ROW
            EXECUTE FUNCTION test_function();
            """
        )

        actual_query = mock_connect.return_value.execute.call_args[0][0]
        assert " ".join(actual_query.split()) == " ".join(expected_query.split())

    async def test_create_trigger_without_connection(self):
        notifier = Notifier(
            config=PGConfig(user="user", password="password", dbname="testdb")
        )
        with pytest.raises(RuntimeError):
            await notifier.create_trigger(
                "test_table", "test_trigger", "test_function", "INSERT"
            )

    @patch("asyncpg.connect", new_callable=AsyncMock)
    async def test_get_triggers_successful(self, mock_connect, mock_config):
        notifier = Notifier(config=mock_config)
        await notifier.connect()

        mock_connect.return_value.fetch.return_value = [
            {"trigger_name": "test_trigger"}
        ]
        triggers = await notifier.get_triggers("test_table")
        assert triggers == ["test_trigger"]

    async def test_get_triggers_without_connection(self):
        notifier = Notifier(
            config=PGConfig(user="user", password="password", dbname="testdb")
        )
        with pytest.raises(RuntimeError):
            await notifier.get_triggers("test_table")

    @patch("asyncpg.connect", new_callable=AsyncMock)
    async def test_remove_trigger_successful(self, mock_connect, mock_config):
        notifier = Notifier(config=mock_config)
        await notifier.connect()

        await notifier.remove_trigger("test_table", "test_trigger")
        mock_connect.return_value.execute.assert_called_once_with(
            "DROP TRIGGER IF EXISTS test_trigger ON test_table;"
        )

    async def test_remove_trigger_without_connection(self):
        notifier = Notifier(
            config=PGConfig(user="user", password="password", dbname="testdb")
        )
        with pytest.raises(RuntimeError):
            await notifier.remove_trigger("test_table", "test_trigger")

    @patch("asyncpg.connect", new_callable=AsyncMock)
    async def test_context_manager(self, mock_connect, mock_config):
        notifier = Notifier(config=mock_config)

        async with notifier as n:
            assert n.conn == mock_connect.return_value

        mock_connect.return_value.close.assert_called_once()

    async def test_close_without_connection(self):
        notifier = Notifier(
            config=PGConfig(user="user", password="password", dbname="testdb")
        )
        await notifier.close()  # Should not raise an error if no connection exists

    @pytest.mark.parametrize(
        "config, expected_dsn",
        [
            (
                PGConfig(
                    user="user",
                    password="password",
                    dbname="testdb",
                    host="localhost",
                    port=5432,
                ),
                "postgresql://user:password@localhost:5432/testdb",
            ),
            (
                PGConfig(
                    user="user",
                    password="password",
                    dbname="testdb",
                    host="localhost",
                    port=5432,
                ),
                "postgresql://user:password@localhost:5432/testdb",
            ),
        ],
    )
    async def test_notifier_initialization_various_inputs(self, config, expected_dsn):
        notifier = Notifier(config=config)
        assert notifier.dsn == expected_dsn
        assert notifier.conn is None

    @patch("asyncpg.connect", new_callable=AsyncMock)
    async def test_get_triggers_varying_mock_data(self, mock_connect, mock_config):
        notifier = Notifier(config=mock_config)
        await notifier.connect()

        # Case 1: No triggers
        mock_connect.return_value.fetch.return_value = []
        triggers = await notifier.get_triggers("test_table")
        assert triggers == []

        # Case 2: Single trigger
        mock_connect.return_value.fetch.return_value = [
            {"trigger_name": "test_trigger"}
        ]
        triggers = await notifier.get_triggers("test_table")
        assert triggers == ["test_trigger"]

        # Case 3: Multiple triggers
        mock_connect.return_value.fetch.return_value = [
            {"trigger_name": "trigger_one"},
            {"trigger_name": "trigger_two"},
        ]
        triggers = await notifier.get_triggers("test_table")
        assert triggers == ["trigger_one", "trigger_two"]

    @patch("asyncpg.connect", new_callable=AsyncMock)
    async def test_get_trigger_functions_varying_mock_data(
        self, mock_connect, mock_config
    ):
        notifier = Notifier(config=mock_config)
        await notifier.connect()

        # Case 1: No trigger functions
        mock_connect.return_value.fetch.return_value = []
        functions = await notifier.get_trigger_functions("test_table")
        assert functions == []

        # Case 2: Single trigger function
        mock_connect.return_value.fetch.return_value = [
            {"function_name": "test_function"}
        ]
        functions = await notifier.get_trigger_functions("test_table")
        assert functions == ["test_function"]

        # Case 3: Multiple trigger functions
        mock_connect.return_value.fetch.return_value = [
            {"function_name": "function_one"},
            {"function_name": "function_two"},
        ]
        functions = await notifier.get_trigger_functions("test_table")
        assert functions == ["function_one", "function_two"]

    @patch("asyncpg.connect", new_callable=AsyncMock)
    async def test_connect_raises_exception(self, mock_connect, mock_config):
        mock_connect.side_effect = Exception("Connection error")
        notifier = Notifier(config=mock_config)

        with pytest.raises(Exception, match="Connection error"):
            await notifier.connect()

    @patch("asyncpg.connect", new_callable=AsyncMock)
    async def test_create_trigger_function_duplicate_error(
        self, mock_connect, mock_config
    ):
        notifier = Notifier(config=mock_config)
        await notifier.connect()

        mock_connect.return_value.execute.side_effect = Exception(
            "Function already exists"
        )
        with pytest.raises(Exception, match="Function already exists"):
            await notifier.create_trigger_function("duplicate_function", "test_channel")

    @patch("asyncpg.connect", new_callable=AsyncMock)
    async def test_create_trigger_sql_error(self, mock_connect, mock_config):
        notifier = Notifier(config=mock_config)
        await notifier.connect()

        mock_connect.return_value.execute.side_effect = Exception("SQL syntax error")
        with pytest.raises(Exception, match="SQL syntax error"):
            await notifier.create_trigger(
                "test_table", "test_trigger", "invalid_function", "INSERT"
            )

    @patch("asyncpg.connect", new_callable=AsyncMock)
    async def test_remove_trigger_not_exists(self, mock_connect, mock_config):
        notifier = Notifier(config=mock_config)
        await notifier.connect()

        mock_connect.return_value.execute.side_effect = Exception(
            "Trigger does not exist"
        )
        with pytest.raises(Exception, match="Trigger does not exist"):
            await notifier.remove_trigger("test_table", "non_existent_trigger")

    @patch("asyncpg.connect", new_callable=AsyncMock)
    async def test_remove_trigger_function_not_exists(self, mock_connect, mock_config):
        notifier = Notifier(config=mock_config)
        await notifier.connect()

        mock_connect.return_value.execute.side_effect = Exception(
            "Function does not exist"
        )
        with pytest.raises(Exception, match="Function does not exist"):
            await notifier.remove_trigger_function("non_existent_function")

    @patch("asyncpg.connect", new_callable=AsyncMock)
    async def test_close_handles_connection_error(self, mock_connect, mock_config):
        notifier = Notifier(config=mock_config)
        await notifier.connect()

        # Simulate connection close failure
        mock_connect.return_value.close.side_effect = Exception("Close error")
        with pytest.raises(Exception, match="Close error"):
            await notifier.close()

    @pytest.mark.parametrize(
        "config_dict, expected_dsn",
        [
            (
                {
                    "user": "user",
                    "password": "password",
                    "dbname": "testdb",
                    "host": "localhost",
                    "port": 5432,
                },
                "postgresql://user:password@localhost:5432/testdb",
            ),
        ],
    )
    async def test_notifier_initialization_with_dict(self, config_dict, expected_dsn):
        config = PGConfig(**config_dict)
        notifier = Notifier(config=config)
        assert notifier.dsn == expected_dsn
        assert notifier.conn is None

    @patch("asyncpg.connect", new_callable=AsyncMock)
    async def test_notifier_initialization_with_env(self, mock_connect):
        # Set environment variables
        os.environ["PG_USER"] = "user"
        os.environ["PG_PASSWORD"] = "password"
        os.environ["PG_DBNAME"] = "testdb"
        os.environ["PG_HOST"] = "localhost"
        os.environ["PG_PORT"] = "5432"

        # Initialize the notifier using the environment variables
        config = PGConfig()
        notifier = Notifier(config)
        expected_dsn = "postgresql://user:password@localhost:5432/testdb"

        assert notifier.dsn == expected_dsn
        assert notifier.conn is None

        # Clean up environment variables
        del os.environ["PG_USER"]
        del os.environ["PG_PASSWORD"]
        del os.environ["PG_DBNAME"]
        del os.environ["PG_HOST"]
        del os.environ["PG_PORT"]

    @patch("asyncpg.connect", new_callable=AsyncMock)
    async def test_notify_success(self, mock_connect, mock_config):
        mock_conn = AsyncMock()
        mock_connect.return_value = mock_conn
        mock_conn.execute = AsyncMock(return_value=None)

        notifier = Notifier(config=mock_config)
        await notifier.connect()
        await notifier.notify("ch_01", "message")

        expected_query = "SELECT pg_notify('ch_01', 'message');"
        mock_conn.execute.assert_called_once_with(expected_query)

    @patch("asyncpg.connect", new_callable=AsyncMock)
    async def test_notify_error_during_execution(self, mock_connect, mock_config):
        mock_conn = AsyncMock()
        mock_connect.return_value = mock_conn
        mock_conn.execute = AsyncMock(side_effect=Exception("Database error"))

        notifier = Notifier(config=mock_config)
        await notifier.connect()

        with pytest.raises(Exception, match="Error while sending the notification: Database error"):
            await notifier.notify("ch_01", "message")

    @patch("asyncpg.connect", new_callable=AsyncMock)
    async def test_notify_with_handler(self, mock_connect, mock_config):
        mock_conn = AsyncMock()
        mock_connect.return_value = mock_conn
        mock_conn.execute = AsyncMock(return_value=None)

        notifier = Notifier(config=mock_config)
        await notifier.connect()

        await notifier.notify("ch_01", "message")

        expected_query = "SELECT pg_notify('ch_01', 'message');"
        mock_conn.execute.assert_called_once_with(expected_query)

    @patch("asyncpg.connect", new_callable=AsyncMock)
    async def test_notify_invalid_channel(self, mock_connect, mock_config):
        mock_conn = AsyncMock()
        mock_connect.return_value = mock_conn
        mock_conn.execute = AsyncMock(side_effect=Exception("Invalid channel"))

        notifier = Notifier(config=mock_config)
        await notifier.connect()

        with pytest.raises(Exception, match="Invalid channel"):
            await notifier.notify("invalid_channel", "message")

