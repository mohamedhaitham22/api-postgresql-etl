import json
from datetime import datetime
from pathlib import Path
from typing import Any

from ..config import settings
from ..utils import get_logger


logger = get_logger(__name__)


class LocalStorage:
    def __init__(self) -> None:
        self.raw_data_dir = Path(settings.RAW_DATA_DIR)
        self.processed_data_dir = Path(settings.PROCESSED_DATA_DIR)

    def save_json(self, data: Any, directory: str) -> Path:

        output_dir = self.raw_data_dir / directory
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        file_path = output_dir / f"{timestamp}.json"

        with file_path.open(
            mode="w",
            encoding="utf-8",
        ) as file:
            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False,
            )

        logger.info("Raw data saved to %s", file_path)

        return file_path