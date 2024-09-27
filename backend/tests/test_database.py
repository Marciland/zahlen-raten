from unittest.mock import MagicMock, patch

import pytest
from modules import Highscore, Player, create_connection_pool


@pytest.mark.parametrize('connection_string, expected_tables', [
    ('something_player.db', [Player.__table__]),
    ('something_score.db', [Highscore.__table__])
])
def test_create_connection_pool(connection_string: str, expected_tables: list):
    mock_engine = MagicMock()
    with patch('database.create_engine') as mock_create_engine, \
            patch('database.Base.metadata.create_all') as mock_create_all:
        mock_create_engine.return_value = mock_engine
        create_connection_pool(connection_string)
        mock_create_engine.assert_called_once_with(connection_string)
        mock_create_all.assert_called_once_with(
            mock_engine, tables=expected_tables)
