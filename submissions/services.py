import subprocess
import tempfile
import os

def run_python_code(code: str, inputs: str = "") -> dict:
    """Runs untrusted Python code in a safe Docker container and returns structured output."""
    with tempfile.TemporaryDirectory() as temp_dir:
        code_file = os.path.join(temp_dir, 'script.py')
        input_file = os.path.join(temp_dir, 'input.txt')

        with open(code_file, 'w') as f:
            f.write(code)

        with open(input_file, 'w') as f:
            f.write(inputs)

        # Basic constraints: max 64MB memory, 10s wall timeout
        cmd = [
            'timeout', '10', 'docker', '-H', 'unix:///var/run/docker.sock', 'run', '--rm',
            '--memory=64m', '--cpus=0.5',
            '--network', 'none',
            '-v', f'{temp_dir}:/app',
            '-w', '/app',
            'python:3.10-alpine',
            'sh', '-c', 'python script.py < input.txt'
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            
            # 124 is the exit code for 'timeout' command when it triggers
            if result.returncode == 124:
                return {
                    'stdout': '',
                    'stderr': 'Error: Execution timed out (Time Limit Exceeded - 10 seconds).',
                    'exit_code': 124
                }
            
            return {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'exit_code': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                'stdout': '',
                'stderr': 'Error: Execution timed out (Time Limit Exceeded - 10 seconds).',
                'exit_code': 124
            }
        except Exception as e:
            return {
                'stdout': '',
                'stderr': f"System Error: {str(e)}",
                'exit_code': -1
            }
