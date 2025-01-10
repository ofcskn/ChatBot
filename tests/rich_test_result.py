from rich.console import Console
import unittest

class RichTestResult(unittest.TextTestResult):
    def addSuccess(self, test):
        super().addSuccess(test)
        Console().print(f"[green]✓ SUCCESS:[/green] {test.shortDescription()}")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        Console().print(f"[red]✗ FAILURE:[/red] {test.shortDescription()} - {err}")

    def addError(self, test, err):
        super().addError(test, err)
        Console().print(f"[yellow]⚠ ERROR:[/yellow] {test.shortDescription()} - {err}")

class RichTestRunner(unittest.TextTestRunner):
    def _makeResult(self):
        return RichTestResult(self.stream, self.descriptions, self.verbosity)
