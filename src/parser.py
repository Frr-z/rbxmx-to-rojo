"""
RBXMX/RBXLX Parser - Parses Roblox XML files and extracts instances
"""
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class RobloxInstance:
    """Represents a Roblox instance from RBXMX file"""
    class_name: str
    name: str
    referent: str
    properties: Dict[str, Any] = field(default_factory=dict)
    children: List['RobloxInstance'] = field(default_factory=list)
    parent: Optional['RobloxInstance'] = None


class RBXMXParser:
    """Parser for RBXMX/RBXLX (Roblox XML) files"""
    
    SCRIPT_CLASSES = {'Script', 'LocalScript', 'ModuleScript'}
    
    def __init__(self):
        self.instances: Dict[str, RobloxInstance] = {}
        self.root_instances: List[RobloxInstance] = []
    
    def parse_file(self, file_path: str) -> List[RobloxInstance]:
        """Parse RBXMX/RBXLX file and return root instances"""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Parse all items first
            items = root.find('Item')
            if items is not None:
                self._parse_item(items, None)
            else:
                # Try to find all Item elements
                for item in root.findall('.//Item'):
                    if item.get('referent') and item.get('class'):
                        self._parse_item(item, None)
            
            return self.root_instances
        except Exception as e:
            raise Exception(f"Failed to parse RBXMX file: {str(e)}")
    
    def _parse_item(self, item_element: ET.Element, parent: Optional[RobloxInstance]) -> RobloxInstance:
        """Parse an Item element recursively"""
        class_name = item_element.get('class', '')
        referent = item_element.get('referent', '')
        
        # Create instance
        instance = RobloxInstance(
            class_name=class_name,
            name='',  # Will be set from properties
            referent=referent,
            parent=parent
        )
        
        # Parse properties
        properties_element = item_element.find('Properties')
        if properties_element is not None:
            instance.properties = self._parse_properties(properties_element)
            instance.name = instance.properties.get('Name', class_name)
        
        # Store instance
        self.instances[referent] = instance
        
        # Add to parent or root
        if parent:
            parent.children.append(instance)
        else:
            self.root_instances.append(instance)
        
        # Parse children
        for child_item in item_element.findall('Item'):
            self._parse_item(child_item, instance)
        
        return instance
    
    def _parse_properties(self, properties_element: ET.Element) -> Dict[str, Any]:
        """Parse properties from Properties element"""
        properties = {}
        
        for prop in properties_element:
            name = prop.get('name', '')
            prop_type = prop.tag
            
            if prop_type == 'string':
                properties[name] = prop.text or ''
            elif prop_type == 'bool':
                properties[name] = prop.text == 'true'
            elif prop_type == 'int':
                properties[name] = int(prop.text or '0')
            elif prop_type == 'float':
                properties[name] = float(prop.text or '0.0')
            elif prop_type == 'ProtectedString':
                # This is usually script source code
                properties[name] = prop.text or ''
            elif prop_type == 'Content':
                # Asset references
                content_element = prop.find('url')
                if content_element is not None:
                    properties[name] = content_element.text or ''
                else:
                    properties[name] = prop.text or ''
            else:
                # Default: store as string
                properties[name] = prop.text or ''
        
        return properties
    
    def has_scripts(self, instance: RobloxInstance) -> bool:
        """Check if instance or any of its descendants contain scripts"""
        if instance.class_name in self.SCRIPT_CLASSES:
            return True
        
        for child in instance.children:
            if self.has_scripts(child):
                return True
        
        return False
