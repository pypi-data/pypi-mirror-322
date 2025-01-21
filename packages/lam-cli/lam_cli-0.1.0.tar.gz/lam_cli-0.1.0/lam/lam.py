#!/usr/bin/env python3

import json
import logging
import os
import shutil
import socket
import subprocess
import sys
import tempfile
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

import click
import psutil
from logtail import LogtailHandler
from posthog import Posthog

# Initialize analytics and logging
posthog = Posthog(project_api_key='phc_wfeHFG0p5yZIdBpjVYy00o5x1HbEpggdMzIuFYgNPSK', 
                  host='https://app.posthog.com')

logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

handler = LogtailHandler(source_token="TYz3WrrvC8ehYjXdAEGGyiDp")
logger.addHandler(handler)

class LAMError(Exception):
    """Base exception for LAM errors"""
    pass

class UserError(LAMError):
    """Errors caused by user input"""
    pass

class SystemError(LAMError):
    """Errors caused by system issues"""
    pass

class ResourceLimitError(LAMError):
    """Errors caused by resource limits"""
    pass

def check_resource_limits(modules_dir: Optional[Path] = None) -> None:
    """Check system resource availability"""
    # Check disk space
    disk = shutil.disk_usage(tempfile.gettempdir())
    if disk.free < 100 * 1024 * 1024:  # 100MB minimum
        raise ResourceLimitError("Insufficient disk space")
    
    # Check shared modules size if provided
    if modules_dir and modules_dir.exists():
        modules_size = sum(
            os.path.getsize(os.path.join(dirpath, filename))
            for dirpath, _, filenames in os.walk(modules_dir)
            for filename in filenames
        )
        if modules_size > 500 * 1024 * 1024:  # 500MB limit
            logger.warning("Shared modules exceeding size limit, cleaning up")
            shutil.rmtree(modules_dir)
            modules_dir.mkdir(exist_ok=True)

class Stats:
    """Track execution statistics"""
    def __init__(self):
        self.start_time = datetime.now()
        self.memory_start = self.get_memory_usage()
    
    def get_memory_usage(self):
        import psutil
        process = psutil.Process()
        return process.memory_info().rss
    
    def finalize(self):
        return {
            'duration_ms': (datetime.now() - self.start_time).total_seconds() * 1000,
            'memory_used_mb': (self.get_memory_usage() - self.memory_start) / (1024 * 1024),
            'timestamp': datetime.now().isoformat()
        }

class EngineType(Enum):
    JQ = "jq"
    JAVASCRIPT = "js"

class ProcessingError(Exception):
    """Custom exception for processing errors"""
    pass

class Engine:
    """Base class for execution engines"""
    def __init__(self, workspace_id: str, flow_id: str, execution_id: str):
        self.workspace_id = workspace_id
        self.flow_id = flow_id
        self.execution_id = execution_id
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    def get_log_file(self) -> str:
        return f"lam_run_{self.workspace_id}_{self.flow_id}_{self.execution_id}_{self.timestamp}.log"

    def get_result_file(self) -> str:
        return f"lam_result_{self.workspace_id}_{self.flow_id}_{self.execution_id}_{self.timestamp}.json"

    def track_event(self, event_name: str, properties: Dict[str, Any]) -> None:
        """Track events with PostHog"""
        try:
            distinct_id = f"{os.getuid()}_{socket.gethostname()}_{self.workspace_id}_{self.flow_id}"
            properties |= {
                'workspace_id': self.workspace_id,
                'flow_id': self.flow_id,
                'engine': self.__class__.__name__,
            }
            posthog.capture(distinct_id=distinct_id, event=event_name, properties=properties)
        except Exception as e:
            logger.error(f"Error tracking event: {e}")

class JQEngine(Engine):
    """JQ execution engine"""
    def validate_environment(self) -> bool:
        return shutil.which("jq") is not None

    def execute(self, program_file: str, input_data: str) -> Tuple[Union[Dict, str], Optional[str]]:
        logger.info(f"Executing JQ script: {program_file}")
        
        try:
            # Parse JQ program
            with open(program_file, 'r') as file:
                jq_script = ''.join(line for line in file if not line.strip().startswith('#'))

            # Run JQ
            process = subprocess.Popen(
                ["jq", "-c", jq_script],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            output, error = process.communicate(input=input_data)
            
            if error:
                raise ProcessingError(error)
                
            # Handle output
            try:
                return json.loads(output), None
            except json.JSONDecodeError:
                return {"lam.result": output}, None
                
        except Exception as e:
            self.track_event('lam.jq.error', {'error': str(e)})
            return {"lam.error": str(e)}, str(e)

class BunEngine(Engine):
    """Bun JavaScript execution engine"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Create a persistent temp directory for node_modules
        self.modules_dir = Path(tempfile.gettempdir()) / "lam_modules"
        self.modules_dir.mkdir(exist_ok=True)
        self._setup_shared_modules()
        
        self.runtime_template = '''
        // Secure runtime environment
        globalThis.process = undefined;
        globalThis.Deno = undefined;
        globalThis.fetch = undefined;
        
        import _ from 'lodash';
        import { format, parseISO } from 'date-fns';
        
        // Safe console methods
        const secureConsole = {
            log: console.log,
            error: console.error,
            warn: console.warn
        };
        globalThis.console = secureConsole;
        
        // Expose safe utilities
        globalThis._ = _;
        globalThis.format = format;
        globalThis.parseISO = parseISO;
        '''
    
    def _setup_shared_modules(self):
        """Setup shared node_modules once"""
        if not (self.modules_dir / "node_modules").exists():
            # Create package.json
            package_json = {
                "type": "module",
                "dependencies": {
                    "lodash": "^4.17.21",
                    "date-fns": "^2.30.0"
                }
            }
            with open(self.modules_dir / "package.json", "w") as f:
                json.dump(package_json, f, indent=2)

            # Install dependencies once
            try:
                subprocess.run(
                    [self.get_bun_path(), "install"],
                    cwd=self.modules_dir,
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=30  # Reasonable timeout for installation
                )
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to install shared dependencies: {e.stderr}")
                raise ProcessingError(
                    f"Failed to set up JavaScript environment: {e.stderr}"
                ) from e

    def create_wrapper(self, input_data: str, user_script: str) -> str:
        """Create the wrapper script with proper escaping"""
        return f'''
        import './runtime.js';

        // Utility function to handle circular references in JSON.stringify
        function safeStringify(obj) {{
            const seen = new WeakSet();
            return JSON.stringify(obj, (key, value) => {{
                if (typeof value === 'object' && value !== null) {{
                    if (seen.has(value)) {{
                        return '[Circular Reference]';
                    }}
                    seen.add(value);
                }}
                return value;
            }}, 2);
        }}

        // Validate transform function
        function validateTransform(fn) {{
            if (typeof fn !== 'function') {{
                throw new Error('Transform must be a function');
            }}
            if (fn.length !== 1) {{
                throw new Error('Transform function must accept exactly one argument (input)');
            }}
        }}

        // Execute transform immediately
        try {{
            // Parse input safely
            let input;
            try {{
                input = {input_data};
            }} catch (e) {{
                throw new Error(`Failed to parse input data: ${{e.message}}`);
            }}

            // Get transform function
            let transform;
            try {{
                transform = {user_script};
            }} catch (e) {{
                throw new Error(`Failed to parse transform function: ${{e.message}}`);
            }}

            // Validate transform
            validateTransform(transform);

            // Execute transform
            const result = transform(input);

            // Validate result is serializable
            try {{
                const serialized = safeStringify(result);
                console.log(serialized);
            }} catch (e) {{
                throw new Error(`Result is not JSON serializable: ${{e.message}}`);
            }}
        }} catch (error) {{
            console.error(JSON.stringify({{
                error: error.message,
                stack: error.stack,
                type: error.constructor.name
            }}));
            process.exit(1);
        }}
        '''
    
    def setup_environment(self, temp_dir: Path) -> None:
        """Set up the JavaScript environment with runtime"""
        # Write runtime file only
        runtime_path = temp_dir / "runtime.js"
        with open(runtime_path, "w") as f:
            f.write(self.runtime_template)
        
        # Symlink node_modules from shared directory
        os.symlink(self.modules_dir / "node_modules", temp_dir / "node_modules")


    def validate_environment(self) -> bool:
        # Check multiple locations for bun
        possible_locations = [
            "bun",  # System PATH
            os.path.join(os.path.dirname(sys.executable), "bun"),  # venv/bin
            os.path.join(os.path.dirname(os.path.dirname(sys.executable)), "bin", "bun")  # venv/bin (alternative)
        ]
        
        return any(shutil.which(loc) is not None for loc in possible_locations)

    def get_bun_path(self) -> str:
        """Get the appropriate bun executable path"""
        possible_locations = [
            "bun",
            os.path.join(os.path.dirname(sys.executable), "bun"),
            os.path.join(os.path.dirname(os.path.dirname(sys.executable)), "bin", "bun")
        ]
        
        for loc in possible_locations:
            if shutil.which(loc):
                return shutil.which(loc)
        
        raise EnvironmentError("Bun not found in environment")

    def execute(self, program_file: str, input_data: str) -> Tuple[Union[Dict, str], Optional[str]]:
        logger.info(f"Executing Bun script: {program_file}")
        stats = Stats()

        try:
            check_resource_limits(self.modules_dir)

            with tempfile.TemporaryDirectory() as temp_dir:
                temp_dir = Path(temp_dir)
                self.setup_environment(temp_dir)

                # Read user script
                with open(program_file, 'r') as f:
                    user_script = f.read()

                # Create wrapper script
                wrapper = self.create_wrapper(input_data, user_script)

                script_path = temp_dir / "script.js"
                with open(script_path, "w") as f:
                    f.write(wrapper)

                # Execute with Bun
                process = subprocess.Popen(
                    [
                        self.get_bun_path(),
                        "run",
                        "--no-fetch",    # Disable network
                        "--smol",        # Reduced memory
                        "--silent",      # Reduce Bun's own error noise
                        str(script_path)
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=temp_dir
                )

                try:
                    output, error = process.communicate(timeout=5)  # 5 second timeout
                except subprocess.TimeoutExpired as e:
                    process.kill()
                    raise ProcessingError("Script execution timed out") from e

                if error:
                    try:
                        error_data = json.loads(error)
                        error_msg = error_data.get('error', 'Unknown error')
                        if error_data.get('stack'):
                            error_msg = f"{error_msg}\nStack trace:\n{error_data['stack']}"
                    except json.JSONDecodeError:
                        error_msg = error.split('\n')[0]  # Just take the first line if not JSON
                    raise ProcessingError(error_msg)

                try:
                    return json.loads(output), None
                except json.JSONDecodeError:
                    return {"lam.result": output}, None

        except Exception as e:
            stats_data = stats.finalize()
            self.track_event('lam.bun.error', {
                'error': str(e),
                'error_type': e.__class__.__name__,
                **stats_data
            })
            return {"lam.error": str(e)}, str(e)

def get_engine(engine_type: str, workspace_id: str, flow_id: str, execution_id: str) -> Engine:
    """Factory function to get the appropriate execution engine"""
    engines = {
        EngineType.JQ.value: JQEngine,
        EngineType.JAVASCRIPT.value: BunEngine
    }
    
    engine_class = engines.get(engine_type)
    if not engine_class:
        raise ValueError(f"Unsupported engine type: {engine_type}")
    
    engine = engine_class(workspace_id, flow_id, execution_id)
    if not engine.validate_environment():
        raise EnvironmentError(f"Required dependencies not found for {engine_type}")
    
    return engine

def process_input(input: str) -> Tuple[str, Optional[str]]:
    """Process and validate input data"""
    if os.path.isfile(input):
        with open(input, 'r') as file:
            return file.read(), None
            
    try:
        json.loads(input)
        return input, None
    except json.JSONDecodeError as e:
        return None, str(e)

@click.group()
def lam():
    """LAM - Laminar Data Transformation Tool"""
    pass

@lam.command()
@click.argument('program_file', type=click.Path(exists=True))
@click.argument('input', type=str)
@click.option('--language', type=click.Choice(['jq', 'js']), default='jq',
              help='Script language (default: jq)')
@click.option('--workspace_id', default="local", help="Workspace ID")
@click.option('--flow_id', default="local", help="Flow ID")
@click.option('--execution_id', default="local", help="Execution ID")
@click.option('--as-json', is_flag=True, default=True, help="Output as JSON")
def run(program_file: str, input: str, language: str, workspace_id: str, 
        flow_id: str, execution_id: str, as_json: bool):
    """Execute a LAM transformation script"""
    stats = Stats()  # Start tracking stats at the top level
    
    # Initialize engine
    try:
        engine = get_engine(language, workspace_id, flow_id, execution_id)
    except (ValueError, EnvironmentError) as e:
        click.echo({"lam.error": str(e)}, err=True)
        return

    # Setup logging
    log_file = engine.get_log_file()
    result_file = engine.get_result_file()
    
    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)
    
    logger.info(f"Starting LAM execution with {language} engine")
    engine.track_event('lam.run.start', {
        'language': language,
        'program_file': program_file
    })

    try:
        # Process input
        input_data, error = process_input(input)
        if error:
            raise ProcessingError(f"Invalid input: {error}")

        # Execute transformation
        result, error = engine.execute(program_file, input_data)
        
        # Get final stats
        stats_data = stats.finalize()
        logger.info(f"Execution stats: duration={stats_data['duration_ms']:.2f}ms, "
                   f"memory_used={stats_data['memory_used_mb']:.2f}MB")
        
        if error:
            click.echo({"lam.error": error}, err=True)
            engine.track_event('lam.run.error', {'error': error, **stats_data})
        else:
            output = json.dumps(result, indent=4) if as_json else result
            click.echo(output)
            engine.track_event('lam.run.success', stats_data)
            
        # Save result with stats
        result_with_stats = {
            'result': result,
            'stats': stats_data,
            'error': error or None
        }
        with open(result_file, 'w') as f:
            json.dump(result_with_stats, f, indent=4)
            
    except Exception as e:
        stats_data = stats.finalize()
        logger.error(f"Execution failed: {e}")
        logger.error(f"Final stats: duration={stats_data['duration_ms']:.2f}ms, "
                    f"memory_used={stats_data['memory_used_mb']:.2f}MB")
        click.echo({"lam.error": str(e)}, err=True)
        engine.track_event('lam.run.error', {'error': str(e), **stats_data})
        
    finally:
        logger.info("Execution complete")
        logger.removeHandler(file_handler)

if __name__ == '__main__':
    lam()