import argparse
from pathlib import Path
from importlib.metadata import distributions
import sys
import importlib.util
from typing import Dict, Set, List, Tuple, Optional
import ast
import json
from packaging import version
import requests
import yaml
from time import sleep
from packaging.utils import canonicalize_name
from autodpd.version import __version__
from autodpd.static import STDLIB_LIST, PACKAGE_ALIAS_MAP

class autodpd:
    def __init__(self):
        """Initialize autodpd with standard library list and cache"""
        self.stdlib_list = STDLIB_LIST
        self.pypi_cache = {}  # Cache for PyPI lookups
        self.deps = None
        self.package_alias_map = PACKAGE_ALIAS_MAP

    def analyze_python_version_notebook(self, file_path: Path) -> Set[float]:
        """
        Analyze a Jupyter notebook to determine minimum Python version requirements
        """
        required_versions = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                notebook = json.load(file)
                
            # Extract code from all code cells
            code_cells = [
                cell['source'] 
                for cell in notebook['cells'] 
                if cell['cell_type'] == 'code'
            ]
            
            # Combine all code cells and analyze as a single Python file
            combined_code = '\n'.join(
                source if isinstance(source, str) else ''.join(source)
                for source in code_cells
            )
            
            tree = ast.parse(combined_code)
            # Reuse the same version detection logic
            for node in ast.walk(tree):
                if isinstance(node, ast.AnnAssign):
                    required_versions.add(3.5)
                if isinstance(node, ast.JoinedStr):
                    required_versions.add(3.6)
                if isinstance(node, ast.ClassDef):
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Name) and decorator.id == 'dataclass':
                            required_versions.add(3.7)
                if isinstance(node, ast.NamedExpr):
                    required_versions.add(3.8)
                if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
                    if isinstance(node.left, ast.Dict) or isinstance(node.right, ast.Dict):
                        required_versions.add(3.9)
                if hasattr(ast, 'Match') and isinstance(node, ast.Match):
                    required_versions.add(3.10)
                    
        except (json.JSONDecodeError, KeyError, SyntaxError):
            print(f"Warning: Could not analyze Python version in notebook {file_path}")
        
        return required_versions

    def map_alias(self, package_name: str) -> str:
        """Map package alias to its official PyPI name"""
        # Remove version if present
        base_name = package_name.split('==')[0] if '==' in package_name else package_name
        
        # Check if package has an alias mapping
        if base_name in self.package_alias_map:
            mapped_name = self.package_alias_map[base_name]
            # Preserve version if it existed
            if '==' in package_name:
                version = package_name.split('==')[1]
                return f"{mapped_name}=={version}"
            return mapped_name
        
        return package_name

    def detect_project_dependencies(self, directory: str = '.', include_versions: bool = False, quiet: bool = False) -> Dict[str, List[str]]:
        """
        Detect dependencies by analyzing Python files and Jupyter notebooks in a directory
        """
        directory = Path(directory).resolve()
        if not directory.exists():
            raise ValueError(f"Directory does not exist: {directory}")
        
        dependencies = {
            'third_party': set(),
            'standard_lib': set(),
            'unknown': set(),
            'local': set()
        }

        # Get all Python files and notebooks recursively
        python_files = list(directory.rglob('*.py'))
        notebook_files = list(directory.rglob('*.ipynb'))
        
        if not quiet:
            print(f"Found {len(python_files)} Python files and {len(notebook_files)} Jupyter notebooks")
        
        # Get local modules
        local_modules = {path.stem for path in python_files if path.stem != '__init__'}

        def verify_package(package_name: str) -> Tuple[str, bool, Optional[str]]:
            """Verify package on PyPI and return name, exists flag, and version"""
            try:
                response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
                if response.status_code == 200:
                    data = response.json()
                    return data['info']['name'], True, data['info']['version']
                return package_name, False, None
            except:
                return package_name, False, None

        def process_content(content, file_path):
            try:
                tree = ast.parse(content)
                
                # Check for specific import patterns
                if 'import community' in content:
                    dependencies['third_party'].add('python-louvain')
                
                # Check for h5 file operations
                if '.h5' in content or '.hdf5' in content:
                    dependencies['third_party'].add('h5py')
                
                # Check for scanpy/AnnData usage
                if 'scanpy' in content or 'AnnData' in content or 'adata' in content:
                    dependencies['third_party'].add('anndata')
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for name in node.names:
                            base_name = name.name.split('.')[0].lower()
                            
                            # Check if it's a local import
                            if base_name in local_modules:
                                dependencies['local'].add(base_name)
                            elif base_name in self.stdlib_list:
                                dependencies['standard_lib'].add(base_name)
                            else:
                                # Map alias before adding to third_party
                                mapped_name = self.map_alias(base_name)
                                pkg_name, exists, version = verify_package(mapped_name)
                                if exists:
                                    if include_versions and version:
                                        dependencies['third_party'].add(f"{pkg_name}=={version}")
                                    else:
                                        dependencies['third_party'].add(pkg_name)
                                else:
                                    dependencies['unknown'].add(base_name)
                
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            base_name = node.module.split('.')[0]
                            if base_name in local_modules:
                                dependencies['local'].add(base_name)
                            elif base_name in self.stdlib_list:
                                dependencies['standard_lib'].add(base_name)
                            else:
                                # Map alias before adding to third_party
                                mapped_name = self.map_alias(base_name)
                                pkg_name, exists, version = verify_package(mapped_name)
                                if exists:
                                    if include_versions and version:
                                        dependencies['third_party'].add(f"{pkg_name}=={version}")
                                    else:
                                        dependencies['third_party'].add(pkg_name)
                                else:
                                    dependencies['unknown'].add(base_name)
            except Exception as e:
                if not quiet:
                    print(f"Error parsing {file_path}: {e}")

        # Process Python files
        for file_path in python_files:
            if not quiet:
                print(f"Analyzing Python file: {file_path}")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    process_content(content, file_path)
            except Exception as e:
                if not quiet:
                    print(f"Error reading {file_path}: {e}")

        # Process Jupyter notebooks
        for file_path in notebook_files:
            if not quiet:
                print(f"Analyzing Jupyter notebook: {file_path}")
            try:
                import json
                with open(file_path, 'r', encoding='utf-8') as f:
                    notebook = json.load(f)
                    for cell in notebook['cells']:
                        if cell['cell_type'] == 'code':
                            content = ''.join(cell['source'])
                            process_content(content, file_path)
            except Exception as e:
                if not quiet:
                    print(f"Error reading notebook {file_path}: {e}")

        # Remove local modules from unknown dependencies
        dependencies['unknown'] = {
            dep for dep in dependencies['unknown']
            if dep not in dependencies['local']
        }

        if not quiet:
            print("\n" + "="*60)
            print(" "*20 + "DEPENDENCY ANALYSIS REPORT")
            print("="*60 + "\n")

            # Third-party dependencies
            print("Third-Party Dependencies:")
            if dependencies['third_party']:
                for dep in sorted(dependencies['third_party'], key=str.lower):
                    print(f"   • {dep}")
            else:
                print("   No third-party dependencies found")
            print()

            # Standard library imports
            print("Python Standard Library:")
            if dependencies['standard_lib']:
                for lib in sorted(dependencies['standard_lib'], key=str.lower):
                    print(f"   • {lib}")
            else:
                print("   No standard library imports found")
            print()

            # Local imports
            print("Local Imports:")
            if dependencies['local']:
                for local in sorted(dependencies['local'], key=str.lower):
                    print(f"   • {local}")
            else:
                print("   No local imports found")
            print()

            # Unknown packages
            if dependencies['unknown']:
                print("Unknown Imports (not included in requirements):")
                for unknown in sorted(dependencies['unknown'], key=str.lower):
                    print(f"   • {unknown}")
                print()

            print("="*60)

        return {
            'third_party': sorted(list(dependencies['third_party']), key=str.lower),
            'standard_lib': sorted(list(dependencies['standard_lib']), key=str.lower),
            'local': sorted(list(dependencies['local']), key=str.lower)
        }

    def analyze_python_version(self, file_path: Path) -> Set[float]:
        """
        Analyze a Python file to determine minimum Python version requirements
        based on syntax features
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                tree = ast.parse(file.read())
            except SyntaxError:
                return set()

        required_versions = set()
        
        for node in ast.walk(tree):
            # Python 3.5+: Type hints
            if isinstance(node, ast.AnnAssign):
                required_versions.add(3.5)
            
            # Python 3.6+: f-strings
            if isinstance(node, ast.JoinedStr):
                required_versions.add(3.6)
            
            # Python 3.7+: dataclasses
            if isinstance(node, ast.ClassDef):
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Name) and decorator.id == 'dataclass':
                        required_versions.add(3.7)
            
            # Python 3.8+: walrus operator
            if isinstance(node, ast.NamedExpr):
                required_versions.add(3.8)
            
            # Python 3.9+: Dictionary union operators
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
                if isinstance(node.left, ast.Dict) or isinstance(node.right, ast.Dict):
                    required_versions.add(3.9)
            
            # Python 3.10+: match statements
            if hasattr(ast, 'Match') and isinstance(node, ast.Match):
                required_versions.add(3.10)

        return required_versions

    def get_python_version(self, directory: str = '.') -> float:
        """
        Get recommended Python version without generating requirements
        """
        min_python_version = 3.5  # Default minimum
        required_versions = set()
        
        # Analyze all Python files and Jupyter notebooks
        for file_path in Path(directory).rglob('*'):
            if file_path.suffix == '.py':
                file_versions = self.analyze_python_version(file_path)
            elif file_path.suffix == '.ipynb':
                file_versions = self.analyze_python_version_notebook(file_path)
            else:
                continue
                
            required_versions.update(file_versions)
        
        if required_versions:
            min_python_version = max(required_versions)
        
        return min_python_version

    def generate_environment(self, directory: str = '.', save_files: bool = True, include_versions: bool = False, quiet: bool = False) -> Dict[str, any]:
        """
        Analyze project files to generate Python environment specifications and save requirement files
        """
        # Get Python version and dependencies
        python_version = self.get_python_version(directory)
        self.deps = self.detect_project_dependencies(directory, include_versions=include_versions, quiet=quiet)
        
        # Only use third-party dependencies for requirements
        all_deps = sorted(list(self.deps['third_party']), key=str.lower)
        
        # Get environment name from directory
        env_name = Path(directory).resolve().name
        if env_name == '.':  # If current directory
            env_name = Path.cwd().name
        
        if save_files:
            # Save conda environment
            with open('environment.yml', 'w') as f:
                yaml.safe_dump(
                    {
                        'name': env_name,  # Use directory name as environment name
                        'channels': ['defaults', 'conda-forge'],
                        'dependencies': [
                            f'python>={python_version}',
                            'pip',
                            {'pip': all_deps}
                        ]
                    },
                    f,
                    default_flow_style=False,
                    sort_keys=False
                )
            
            if not quiet:
                print(f"Generated environment.yml with name: {env_name}")
            
            # Save requirements
            with open('requirements.txt', 'w') as f:
                f.write(f"# Python >= {python_version}\n")
                if include_versions:
                    f.write("# Generated with version numbers (--versions flag)\n")
                f.write("\n")
                for dep in all_deps:
                    f.write(f"{dep}\n")
            
            if not quiet:
                print("Generated requirements.txt")
        
        return {
            'recommended_python_version': python_version,
            'dependencies': all_deps,
            'environment_name': env_name
        }

    def _get_version_reasoning(self, python_version: float) -> List[str]:
        """Helper function to generate version reasoning messages"""
        reasoning = []
        version_features = [
            (3.10, "Match statements detected (Python 3.10+)"),
            (3.9, "Dictionary union operators detected (Python 3.9+)"),
            (3.8, "Walrus operator detected (Python 3.8+)"),
            (3.7, "Dataclasses detected (Python 3.7+)"),
            (3.6, "F-strings detected (Python 3.6+)"),
            (3.5, "Type hints detected (Python 3.5+)")
        ]
        
        for ver, msg in version_features:
            if python_version >= ver:
                reasoning.append(msg)
        
        return reasoning

    def save_conda_environment(self, env_specs: Dict[str, any], output_file: str = 'environment.yml') -> None:
        """
        Save conda environment specifications to a YAML file
        """
        conda_env = {
            'name': env_specs['conda_environment_yaml']['name'],
            'channels': env_specs['conda_environment_yaml']['channels'],
            'dependencies': env_specs['conda_environment_yaml']['dependencies']
        }
        
        with open(output_file, 'w') as f:
            yaml.safe_dump(conda_env, f, default_flow_style=False, sort_keys=False)
        
        print(f"\nConda environment configuration saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(
        description='Analyze Python project dependencies and generate environment specifications'
    )
    parser.add_argument(
        '-d', '--directory',
        type=str,
        default='.',
        help='Path to the Python project directory (default: current directory)'
    )
    parser.add_argument(
        '--no-save',
        action='store_true',
        help='Skip generating requirement files'
    )
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Suppress detailed output'
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'%(prog)s {__version__}',
        help='Show program version'
    )
    
    parser.add_argument(
        '--versions',
        action='store_true',
        help='Include package version numbers in requirements'
    )
    
    args = parser.parse_args()
    
    detector = autodpd()
    env_specs = detector.generate_environment(
        directory=args.directory,
        save_files=not args.no_save,
        include_versions=args.versions,
        quiet=args.quiet
    )
    
    if args.quiet:
        # Only show minimal output in quiet mode
        print(f"Python version: {env_specs['recommended_python_version']}")
        print(f"Dependencies: {len(env_specs['dependencies'])}")

if __name__ == "__main__":
    main()
