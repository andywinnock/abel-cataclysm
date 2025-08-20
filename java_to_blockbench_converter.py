#!/usr/bin/env python3
"""
Java Model to Blockbench Converter
Converts Minecraft Forge Java model files back to Blockbench .bbmodel format
"""

import re
import json
import uuid
from typing import Dict, List, Tuple, Any

class JavaToBlockbenchConverter:
    def __init__(self, java_content: str):
        self.java_content = java_content
        self.texture_width = 64
        self.texture_height = 64
        self.elements = []
        self.outliner = []
        
    def extract_texture_size(self) -> Tuple[int, int]:
        """Extract texture dimensions from LayerDefinition.create()"""
        pattern = r'LayerDefinition\.create\(meshdefinition,\s*(\d+),\s*(\d+)\)'
        match = re.search(pattern, self.java_content)
        if match:
            return int(match.group(1)), int(match.group(2))
        return 64, 64
    
    def parse_cube_definition(self, cube_text: str) -> Dict[str, Any]:
        """Parse a Java addBox() call into Blockbench cube format"""
        # Pattern: .texOffs(x, y).addBox(x, y, z, w, h, d, new CubeDeformation(f))
        tex_pattern = r'texOffs\((-?\d+(?:\.\d+)?),\s*(-?\d+(?:\.\d+)?)\)'
        box_pattern = r'addBox\((-?\d+(?:\.\d+)?)F?,\s*(-?\d+(?:\.\d+)?)F?,\s*(-?\d+(?:\.\d+)?)F?,\s*(-?\d+(?:\.\d+)?)F?,\s*(-?\d+(?:\.\d+)?)F?,\s*(-?\d+(?:\.\d+)?)F?'
        mirror_pattern = r'\.mirror\(\s*(true|false)\s*\)'
        
        tex_match = re.search(tex_pattern, cube_text)
        box_match = re.search(box_pattern, cube_text)
        mirror_match = re.search(mirror_pattern, cube_text)
        
        if not (tex_match and box_match):
            return None
            
        # Extract values
        uv_x, uv_y = float(tex_match.group(1)), float(tex_match.group(2))
        x, y, z = float(box_match.group(1)), float(box_match.group(2)), float(box_match.group(3))
        w, h, d = float(box_match.group(4)), float(box_match.group(5)), float(box_match.group(6))
        
        # Check for mirror flag
        is_mirrored = mirror_match and mirror_match.group(1) == "false"  # mirror(false) = mirrored
        
        # Convert from Java coordinates to Blockbench coordinates
        # Java uses Y-down with 24.0F root offset, Blockbench uses Y-up from 0
        # For Minecraft models: BB_Y = -(Java_Y + Java_height) because Y is inverted
        bb_from = [x, -(y + h), z]  
        bb_to = [x + w, -y, z + d]
        
        # Generate cube faces with UV mapping
        faces = {
            "north": {"uv": [uv_x + d, uv_y + d, uv_x + d + w, uv_y + d + h], "texture": 0},
            "east": {"uv": [uv_x, uv_y + d, uv_x + d, uv_y + d + h], "texture": 0},
            "south": {"uv": [uv_x + d + w, uv_y + d, uv_x + d + w + d, uv_y + d + h], "texture": 0},
            "west": {"uv": [uv_x + d + w, uv_y + d, uv_x + d + w + d, uv_y + d + h], "texture": 0},
            "up": {"uv": [uv_x + d, uv_y, uv_x + d + w, uv_y + d], "texture": 0},
            "down": {"uv": [uv_x + d + w, uv_y, uv_x + d + w + w, uv_y + d], "texture": 0}
        }
        
        return {
            "from": bb_from,
            "to": bb_to,
            "uv_offset": [uv_x, uv_y],
            "faces": faces,
            "mirrored": is_mirrored
        }
    
    def extract_part_definitions(self) -> Dict[str, Any]:
        """Extract part definitions and their hierarchy"""
        parts = {}
        
        # Enhanced pattern to match complex part definitions with multi-line cube builders
        # This pattern handles nested parentheses and multi-line definitions better
        content_no_whitespace = re.sub(r'\s+', ' ', self.java_content)
        
        # Pattern to match part definitions with better multi-line support
        pattern = r'PartDefinition\s+(\w+)\s*=\s*(\w+)\.addOrReplaceChild\("([^"]+)",\s*CubeListBuilder\.create\(\)([^;]*?)PartPose\.(\w+)\(([^)]+)\)\s*\)\s*;'
        
        matches = re.finditer(pattern, content_no_whitespace)
        
        for match in matches:
            var_name = match.group(1)
            parent = match.group(2)
            name = match.group(3)
            cube_definitions = match.group(4)
            pose_type = match.group(5)
            pose_params = match.group(6)
            
            # Skip rotation helper parts (they're just for transform calculations)
            if '_r' in var_name and var_name.endswith(('_r1', '_r2', '_r3', '_r4', '_r5', '_r6', '_r7', '_r8', '_r9', '_r10', '_r11', '_r12')):
                continue
                
            # Parse cube definitions in this part - handle multiple cubes per part
            cubes = []
            # Find all texOffs().addBox() sequences, including chained ones with mirrors
            cube_pattern = r'\.texOffs\([^)]+\)\.(?:mirror\(\)\.|)addBox\([^)]+\)[^.]*(?:\.mirror\([^)]*\))?'
            cube_matches = re.findall(cube_pattern, cube_definitions)
            
            for cube_match in cube_matches:
                cube_data = self.parse_cube_definition(cube_match)
                if cube_data:
                    cubes.append(cube_data)
            
            # Parse pose parameters with rotation support
            local_origin = [0.0, 0.0, 0.0]
            rotation = [0.0, 0.0, 0.0]
            
            # Handle different pose types
            if pose_type == "offset":
                pose_match = re.search(r'(-?\d+(?:\.\d+)?)F?,\s*(-?\d+(?:\.\d+)?)F?,\s*(-?\d+(?:\.\d+)?)F?', pose_params)
                if pose_match:
                    local_origin = [float(pose_match.group(1)), float(pose_match.group(2)), float(pose_match.group(3))]
                    
            elif pose_type == "offsetAndRotation":
                pose_match = re.search(r'(-?\d+(?:\.\d+)?)F?,\s*(-?\d+(?:\.\d+)?)F?,\s*(-?\d+(?:\.\d+)?)F?,\s*(-?\d+(?:\.\d+)?)F?,\s*(-?\d+(?:\.\d+)?)F?,\s*(-?\d+(?:\.\d+)?)F?', pose_params)
                if pose_match:
                    local_origin = [float(pose_match.group(1)), float(pose_match.group(2)), float(pose_match.group(3))]
                    rotation = [float(pose_match.group(4)), float(pose_match.group(5)), float(pose_match.group(6))]
            
            # Store local origin (will calculate world position later)
            parts[var_name] = {
                "name": name,
                "parent": parent,
                "cubes": cubes,
                "local_origin": local_origin,  # Store the Java local offset
                "world_origin": [0.0, 0.0, 0.0],  # Will be calculated with cumulative transforms
                "rotation": rotation
            }
        
        return parts
    
    def calculate_cumulative_transforms(self, parts: Dict[str, Any]) -> None:
        """Calculate cumulative world positions for all parts"""
        
        def calculate_world_position(part_name: str, accumulated_transform: List[float] = None) -> None:
            if accumulated_transform is None:
                accumulated_transform = [0.0, 0.0, 0.0]
            
            if part_name not in parts:
                return
                
            part = parts[part_name]
            local_origin = part["local_origin"]
            
            # Add this part's local offset to accumulated transform
            world_x = accumulated_transform[0] + local_origin[0]
            world_y = accumulated_transform[1] + local_origin[1]  
            world_z = accumulated_transform[2] + local_origin[2]
            
            # Convert Y coordinate: Java Y-axis is inverted relative to Blockbench
            # Apply Y inversion here at the world level
            blockbench_y = -world_y
            
            # Store world position in Blockbench coordinates
            part["world_origin"] = [world_x, blockbench_y, world_z]
            
            # Also update cubes to use world position for correct placement
            # The cubes need to be offset by the cumulative world position
            for cube in part["cubes"]:
                # Adjust cube positions by the world offset
                # Note: cube coordinates were already converted from Java to Blockbench in parse_cube_definition
                # Now we just need to offset them by the world origin
                cube["world_from"] = [
                    cube["from"][0] + world_x,
                    cube["from"][1] + blockbench_y,
                    cube["from"][2] + world_z
                ]
                cube["world_to"] = [
                    cube["to"][0] + world_x,
                    cube["to"][1] + blockbench_y,
                    cube["to"][2] + world_z
                ]
            
            # Pass accumulated transform to children
            new_accumulated = [world_x, world_y, world_z]  # Keep Java Y for child calculations
            
            # Find and process children
            for child_name, child_data in parts.items():
                if child_data["parent"] == part_name:
                    calculate_world_position(child_name, new_accumulated)
        
        # Find root parts and start calculation
        root_parts = [name for name, data in parts.items() if data["parent"] == "partdefinition"]
        
        for root_part in root_parts:
            calculate_world_position(root_part)
    
    def build_blockbench_structure(self, parts: Dict[str, Any]) -> Dict[str, Any]:
        """Build the Blockbench JSON structure"""
        self.texture_width, self.texture_height = self.extract_texture_size()
        
        # Calculate cumulative world positions for all parts
        self.calculate_cumulative_transforms(parts)
        
        elements = []
        outliner_map = {}
        
        # Create elements from cubes
        element_id = 0
        for part_name, part_data in parts.items():
            for i, cube in enumerate(part_data["cubes"]):
                element = {
                    "name": f"{part_data['name']}_{i}" if len(part_data["cubes"]) > 1 else part_data['name'],
                    "box_uv": True,
                    "rescale": False,
                    "locked": False,
                    "light_emission": 0,
                    "render_order": "default",
                    "allow_mirror_modeling": True,
                    "from": cube.get("world_from", cube["from"]),  # Use world coordinates if available
                    "to": cube.get("world_to", cube["to"]),      # Use world coordinates if available
                    "autouv": 0,
                    "color": 0,
                    "origin": part_data["world_origin"],  # Use world origin instead of local
                    "rotation": part_data.get("rotation", [0.0, 0.0, 0.0]),
                    "uv_offset": cube["uv_offset"],
                    "faces": cube["faces"],
                    "type": "cube",
                    "uuid": f"element_{element_id}",
                    "mirror_uv": cube.get("mirrored", False)
                }
                elements.append(element)
                
                # Track which group this element belongs to
                if part_name not in outliner_map:
                    outliner_map[part_name] = {
                        "name": part_data['name'],
                        "origin": part_data['world_origin'],  # Use world origin
                        "color": 0,
                        "uuid": f"group_{part_name}",
                        "export": True,
                        "mirror_uv": False,
                        "isOpen": True,
                        "locked": False,
                        "visibility": True,
                        "autouv": 0,
                        "selected": False,
                        "children": []
                    }
                
                outliner_map[part_name]["children"].append(f"element_{element_id}")
                element_id += 1
        
        # Build hierarchy properly with rotation support
        def build_hierarchy(part_name: str, parts: Dict[str, Any], outliner_map: Dict[str, Any]) -> Any:
            if part_name not in parts:
                return None
                
            part_data = parts[part_name]
            
            # Create group structure with rotation support
            group = {
                "name": part_data["name"],
                "origin": part_data["world_origin"],  # Use world origin
                "rotation": part_data.get("rotation", [0.0, 0.0, 0.0]),
                "color": 0,
                "uuid": f"group_{part_name}",
                "export": True,
                "mirror_uv": False,
                "isOpen": True,
                "locked": False,
                "visibility": True,
                "autouv": 0,
                "selected": False,
                "children": []
            }
            
            # Add cube elements for this part
            if part_name in outliner_map:
                group["children"].extend(outliner_map[part_name]["children"])
            
            # Find and add child parts - sort by name for consistent ordering
            child_parts = sorted([p for p, data in parts.items() if data["parent"] == part_name and p != part_name])
            for child_part in child_parts:
                child_group = build_hierarchy(child_part, parts, outliner_map)
                if child_group:
                    group["children"].append(child_group)
            
            return group
        
        # Find root part
        root_parts = [name for name, data in parts.items() if data["parent"] == "partdefinition" or data["name"] == "root"]
        
        outliner = []
        for root_part in root_parts:
            root_group = build_hierarchy(root_part, parts, outliner_map)
            if root_group:
                outliner.append(root_group)
        
        return {
            "meta": {
                "format_version": "4.10",
                "model_format": "modded_entity",
                "box_uv": True
            },
            "name": "Netherite_Monstrosity",
            "model_identifier": "netherite_monstrosity",
            "modded_entity_entity_class": "Netherite_Monstrosity_Entity",
            "modded_entity_version": "1.17",
            "modded_entity_flip_y": True,
            "visible_box": [1, 1.5, 0],
            "variable_placeholders": "",
            "variable_placeholder_buttons": [],
            "timeline_setups": [],
            "unhandled_root_fields": {},
            "resolution": {
                "width": self.texture_width,
                "height": self.texture_height
            },
            "elements": elements,
            "outliner": outliner,
            "textures": []
        }
    
    def convert(self) -> str:
        """Convert Java model to Blockbench format"""
        parts = self.extract_part_definitions()
        bbmodel = self.build_blockbench_structure(parts)
        return json.dumps(bbmodel, indent=2)

def convert_java_model_file(java_file_path: str, output_path: str):
    """Convert a Java model file to Blockbench format"""
    with open(java_file_path, 'r') as f:
        java_content = f.read()
    
    converter = JavaToBlockbenchConverter(java_content)
    bbmodel_json = converter.convert()
    
    with open(output_path, 'w') as f:
        f.write(bbmodel_json)
    
    print(f"Conversion complete: {output_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python java_to_blockbench_converter.py <input.java> <output.bbmodel>")
        sys.exit(1)
    
    convert_java_model_file(sys.argv[1], sys.argv[2])