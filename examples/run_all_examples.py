# Run all python files in examples/
import os
from pathlib import Path

if __name__ == "__main__":
    containing_dir = Path(__file__).parent
    script_logs = containing_dir / "logs"
    script_logs.mkdir(exist_ok=True)

    for file in containing_dir.glob("example_*.py"):
        logs_file = script_logs / f"{file.stem}.log"
        print(f"Running {file} with output to {logs_file}")
        exit_status = os.system(f"python {file} > {logs_file} 2>&1")
        print(f"Exit status: {exit_status}")
