import os
import shutil
import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile


class OrcaPlotEngine:
    def __init__(self):
        pass

    def _get_executable(self, version: int = 6):
        executable = None
        match version:
            case 5:
                executable = os.getenv("ORCA_PLOT_5_BINARY")
            case _:
                executable = shutil.which("orca_plot")
        if executable is None:
            raise FileNotFoundError("Failed to find `orca_plot` executable.")
        return Path(executable).resolve()

    def plot(self, instructions: str, file: Path, version: int = 6):
        # For some reason its not creating the cube file, although it did once earlier..?
        executable = self._get_executable(version)
        with NamedTemporaryFile(mode="w+") as stdin:
            stdin.write(instructions)
            stdin.seek(0)
            result = subprocess.run(
                [executable, file.resolve(), "-i"],
                stdin=stdin,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            if "Wrong number of basis-sets stored!" in result.stderr:
                raise ValueError(
                    "ORCA 5 orbital file detected.\n"
                    "Please export your ORCA 5 orca_plot binary and retry.\n"
                    "Run the following command with the adjusted path or add it to your ~/.bashrc\n"
                    "\n"
                    'export ORCA_PLOT_5_BINARY="/path/to/orca5/orca_plot"\n'
                )
