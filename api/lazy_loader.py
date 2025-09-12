import asyncio
from typing import Any, Dict

from api.fundamentus import get_data


class LazyLoader:
    """Carrega e armazena em cache os dados da API Fundamentus sob demanda."""

    def __init__(self):
        """Inicializa o LazyLoader."""
        self._data = None

    async def get_data(self) -> Dict[str, Any]:
        """Retorna os dados da API Fundamentus, carregando-os se necessário."""
        if self._data is None:
            self._data = await get_data()
        return self._data


lazy_loader = LazyLoader()
