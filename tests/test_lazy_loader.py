import asyncio
from unittest.mock import AsyncMock, patch

from api.lazy_loader import LazyLoader


def test_lazy_loader_init():
    """Testa a inicialização do LazyLoader."""
    loader = LazyLoader()
    assert loader._data is None


@patch("api.lazy_loader.get_data", new_callable=AsyncMock)
def test_lazy_loader_get_data_first_call(mock_get_data):
    """Testa a primeira chamada ao get_data, que deve carregar os dados."""
    mock_get_data.return_value = {"test": "data"}
    loader = LazyLoader()
    result = asyncio.run(loader.get_data())
    mock_get_data.assert_called_once()
    assert result == {"test": "data"}
    assert loader._data == {"test": "data"}


@patch("api.lazy_loader.get_data", new_callable=AsyncMock)
def test_lazy_loader_get_data_second_call(mock_get_data):
    """Testa a segunda chamada ao get_data, que deve retornar os dados em cache."""
    loader = LazyLoader()
    loader._data = {"cached": "data"}
    result = asyncio.run(loader.get_data())
    mock_get_data.assert_not_called()
    assert result == {"cached": "data"}
