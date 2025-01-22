from __future__ import annotations

__all__ = ["NextJS"]

import os
import subprocess
from typing import Any

from verse.core import Context, Operation, Provider


class NextJS(Provider):
    path: str | None

    _template_path = "../templates/nextjs-latest"

    def __init__(
        self,
        path: str | None = None,
        **kwargs,
    ):
        self.path = path

    def __run__(
        self,
        operation: Operation | None = None,
        context: Context | None = None,
        **kwargs,
    ) -> Any:
        shell = os.name == "nt"
        if self.path:
            path = self.path
        else:
            path = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    self._template_path,
                )
            )
        os.chdir(path)
        subprocess.run(["npm", "install"], shell=shell, check=True)
        subprocess.run(["npm", "run", "dev"], shell=shell, check=True)
