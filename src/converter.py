"""
Rojo Converter - Converts parsed RBXMX/RBXLX/RBXM/RBXL instances to Rojo project structure
"""
import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Set
from parser import RobloxInstance, RBXMXParser


class RojoConverter:
    """Converts RBXMX/RBXLX/RBXM/RBXL instances to Rojo project structure"""
    
    SCRIPT_CLASSES = {'Script', 'LocalScript', 'ModuleScript'}
    RESPECTED_SERVICES = {
        'Workspace', 'Players', 'Lighting', 'ReplicatedFirst',
        'ReplicatedStorage', 'ServerScriptService', 'ServerStorage',
        'StarterGui', 'StarterPack', 'StarterPlayer', 'Teams',
        'SoundService', 'Chat', 'LocalizationService', 'TestService'
    }
    
    def __init__(self, output_path: str):
        self.output_path = Path(output_path)
        self.src_path = self.output_path / 'src'
        self.project_tree: Dict[str, any] = {}
        self.parser = RBXMXParser()
    
    def convert(self, rbxmx_file: str) -> bool:
        """Convert RBXMX/RBXLX/RBXM/RBXL file to Rojo project"""
        try:
            # Determine file type
            file_ext = Path(rbxmx_file).suffix.lower()
            
            # Parse the file
            if file_ext in ['.rbxm', '.rbxl']:
                # Binary format - try to parse with rbx_binary if available
                try:
                    import rbx_binary
                    with open(rbxmx_file, 'rb') as f:
                        tree = rbx_binary.from_reader(f)
                    root_instances = [tree.get_by_ref(ref) for ref in tree.root().children()]
                except ImportError:
                    raise Exception(
                        "Binary format (.rbxm/.rbxl) requires 'rbx-binary' package.\n"
                        "Install it with: pip install rbx-binary\n"
                        "Or use XML format (.rbxmx/.rbxlx) instead."
                    )
            else:
                # XML format
                root_instances = self.parser.parse_file(rbxmx_file)
            
            # Create output directories
            self.output_path.mkdir(parents=True, exist_ok=True)
            self.src_path.mkdir(parents=True, exist_ok=True)
            
            # Process each root instance
            for instance in root_instances:
                self._process_instance(instance, self.src_path)
            
            # Write project file
            self._write_project_file()
            
            return True
        except Exception as e:
            print(f"Conversion error: {str(e)}")
            return False
    
    def _process_instance(self, instance: RobloxInstance, base_path: Path) -> Optional[Dict]:
        """Process an instance and create appropriate files/folders"""
        # Skip instances without scripts
        if not self.parser.has_scripts(instance):
            return None
        
        class_name = instance.class_name
        instance_name = instance.name
        
        # Handle different class types
        if class_name in self.SCRIPT_CLASSES:
            return self._process_script(instance, base_path)
        elif class_name == 'Folder':
            return self._process_folder(instance, base_path)
        else:
            return self._process_other_instance(instance, base_path)
    
    def _process_script(self, instance: RobloxInstance, base_path: Path) -> Optional[Dict]:
        """Process Script, LocalScript, or ModuleScript"""
        source = instance.properties.get('Source', '')
        script_name = instance.name
        
        # Determine extension
        extension = ''
        if instance.class_name == 'LocalScript':
            extension = '.client'
        elif instance.class_name == 'Script':
            extension = '.server'
        # ModuleScript has no extension
        
        # Count script children
        script_children = [c for c in instance.children if self.parser.has_scripts(c)]
        total_children = len(instance.children)
        
        if len(script_children) == total_children and total_children > 0:
            # All children are scripts - create folder with init file
            folder_path = base_path / script_name
            folder_path.mkdir(parents=True, exist_ok=True)
            
            # Write init file
            init_file = folder_path / f'init{extension}.lua'
            init_file.write_text(source, encoding='utf-8')
            
            # Process children
            for child in instance.children:
                self._process_instance(child, folder_path)
            
            return {
                '$path': f'src/{folder_path.relative_to(self.src_path).as_posix()}'
            }
        
        elif len(script_children) == 0:
            # No script children - create single file with meta
            script_file = base_path / f'{script_name}{extension}.lua'
            script_file.write_text(source, encoding='utf-8')
            
            # Create meta file if there are non-script children
            if total_children > 0:
                meta_file = base_path / f'{script_name}.meta.json'
                meta_content = {
                    'ignoreUnknownInstances': True
                }
                meta_file.write_text(json.dumps(meta_content, indent=2), encoding='utf-8')
            
            return {
                '$path': f'src/{script_file.relative_to(self.src_path).as_posix()}'
            }
        
        else:
            # Mixed children - create folder with init file and meta
            folder_path = base_path / script_name
            folder_path.mkdir(parents=True, exist_ok=True)
            
            # Write init file
            init_file = folder_path / f'init{extension}.lua'
            init_file.write_text(source, encoding='utf-8')
            
            # Write meta file
            meta_file = folder_path / 'init.meta.json'
            meta_content = {
                'ignoreUnknownInstances': True
            }
            meta_file.write_text(json.dumps(meta_content, indent=2), encoding='utf-8')
            
            # Process children
            for child in instance.children:
                self._process_instance(child, folder_path)
            
            return {
                '$path': f'src/{folder_path.relative_to(self.src_path).as_posix()}'
            }
    
    def _process_folder(self, instance: RobloxInstance, base_path: Path) -> Optional[Dict]:
        """Process Folder instance"""
        folder_path = base_path / instance.name
        folder_path.mkdir(parents=True, exist_ok=True)
        
        # Create meta file
        meta_file = folder_path / 'init.meta.json'
        meta_content = {
            'ignoreUnknownInstances': True
        }
        meta_file.write_text(json.dumps(meta_content, indent=2), encoding='utf-8')
        
        # Process children
        for child in instance.children:
            self._process_instance(child, folder_path)
        
        return {
            '$path': f'src/{folder_path.relative_to(self.src_path).as_posix()}'
        }
    
    def _process_other_instance(self, instance: RobloxInstance, base_path: Path) -> Optional[Dict]:
        """Process other instance types (Models, Parts, etc.)"""
        # Only process if it has scripts
        if not self.parser.has_scripts(instance):
            return None
        
        folder_path = base_path / instance.name
        folder_path.mkdir(parents=True, exist_ok=True)
        
        # Create meta file with class name
        meta_file = folder_path / 'init.meta.json'
        meta_content = {
            'className': instance.class_name,
            'ignoreUnknownInstances': True
        }
        meta_file.write_text(json.dumps(meta_content, indent=2), encoding='utf-8')
        
        # Process children
        for child in instance.children:
            self._process_instance(child, folder_path)
        
        return {
            '$className': instance.class_name,
            '$path': f'src/{folder_path.relative_to(self.src_path).as_posix()}'
        }
    
    def _write_project_file(self):
        """Write the default.project.json file"""
        # Build tree from src directory
        tree = {'$className': 'DataModel'}
        
        # Add each top-level folder/file in src to the tree
        if self.src_path.exists():
            for item in self.src_path.iterdir():
                if item.is_dir():
                    tree[item.name] = {
                        '$path': f'src/{item.name}'
                    }
        
        project = {
            'name': self.output_path.name,
            'tree': tree
        }
        
        project_file = self.output_path / 'default.project.json'
        project_file.write_text(json.dumps(project, indent=2), encoding='utf-8')
