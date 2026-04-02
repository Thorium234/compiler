import subprocess
import tempfile
import os

def run_python_code(code: str, inputs: str = "") -> str:
    """Runs untrusted Python code in a safe Docker container."""
    with tempfile.TemporaryDirectory() as temp_dir:
        code_file = os.path.join(temp_dir, 'script.py')
        input_file = os.path.join(temp_dir, 'input.txt')

        with open(code_file, 'w') as f:
            f.write(code)

        with open(input_file, 'w') as f:
            f.write(inputs)

        # Basic constraints: max 64MB memory, 0.5 CPU, network isolated, 2s wall timeout
        cmd = [
            'timeout', '2', 'docker', 'run', '--rm',
            '--memory=64m', '--cpus=0.5',
            '--network', 'none',
            '-v', f'{temp_dir}:/app',
            '-w', '/app',
            'python:3.10-alpine',
            'sh', '-c', 'python script.py < input.txt'
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
            if result.returncode == 124:
                return "Error: Execution timed out (Time Limit Exceeded - 2 seconds)."
            
            output = result.stdout
            if result.stderr:
                output += "\nError Logs:\n" + result.stderr
            return output
        except subprocess.TimeoutExpired:
            return "Error: Execution timed out (Time Limit Exceeded - 2 seconds)."
        except Exception as e:
            return f"System Error: {str(e)}"
