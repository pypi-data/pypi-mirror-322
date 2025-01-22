import signal
import sys
from typing import Any

from verse.core import ArgParser, Context, Operation, Provider


class Default(Provider):
    def __run__(
        self,
        operation: Operation | None = None,
        context: Context | None = None,
        **kwargs,
    ) -> Any:
        signal.signal(signal.SIGINT, self._signal_handler)
        print("Welcome to Verse CLI. Use Verse QL to run operations.")
        while True:
            try:
                statement = input("> ")
                if statement.strip():
                    try:
                        operation = ArgParser.convert_execute_operation(
                            statement, None
                        )
                        output = self.get_component().component.__run__(
                            operation=operation
                        )
                        print(output)
                    except Exception as e:
                        print(f"{type(e).__name__}: {e}")
            except EOFError:
                print("\nExiting!")
                sys.exit(0)

    def _signal_handler(self, signal, frame):
        print("\nExiting!")
        sys.exit(0)
