#!/usr/bin/env python3
"""
Enhanced Java to Blockbench Converter - Fixed Version
Specifically addresses hierarchy and coordinate issues found in Netherite Monstrosity conversion
"""

import re
import json
import uuid
from typing import Dict, List, Any, Optional, Tuple

class JavaToBlockbenchConverterFixed:
    def __init__(self, java_file_path: str):
        with open(java_file_path, 'r') as f:
            self.java_content = f.read()
        self.texture_width = 512  # Default fallback
        self.texture_height = 512
        
    def extract_texture_size(self) -> Tuple[int, int]:
        """Extract texture dimensions from LayerDefinition.create() call"""
        pattern = r'LayerDefinition\.create\(meshdefinition,\s*(\d+),\s*(\d+)\)'
        match = re.search(pattern, self.java_content)
        if match:
            return int(match.group(1)), int(match.group(2))
        return 512, 512  # Default fallback
    
    def parse_cube_definition(self, cube_text: str) -> Dict[str, Any]:
        """Parse a Java addBox() call into Blockbench cube format with FIXED coordinate transformation"""
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
        is_mirrored = mirror_match and mirror_match.group(1) == "false"
        
        # FIXED COORDINATE TRANSFORMATION
        # Java coordinate system: Y-down, with root typically at 24.0F offset
        # Blockbench coordinate system: Y-up, with 0,0,0 as center
        # Key fix: DO NOT flip X coordinates - maintain left/right orientation
        bb_from = [x, -(y + h), z]  # Y inversion: -(y + height) gives correct Y-up
        bb_to = [x + w, -y, z + d]  # Y inversion: -y gives correct Y-up
        
        # Generate cube faces with UV mapping - IMPROVED UV calculation
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
        """Extract part definitions with FIXED hierarchy tracking"""
        parts = {}
        
        # Clean up content for parsing
        content_no_whitespace = re.sub(r'\s+', ' ', self.java_content)
        
        # Enhanced pattern to capture part definitions more reliably
        pattern = r'PartDefinition\s+(\w+)\s*=\s*(\w+)\.addOrReplaceChild\("([^"]+)",\s*CubeListBuilder\.create\(\)([^;]*?)PartPose\.(\w+)\(([^)]+)\)\s*\)\s*;'
        
        matches = re.finditer(pattern, content_no_whitespace, re.DOTALL)
        
        for match in matches:
            var_name = match.group(1)
            parent = match.group(2)
            name = match.group(3)
            cube_definitions = match.group(4)
            pose_type = match.group(5)
            pose_params = match.group(6)
            
            print(f"Processing part: {name} (parent: {parent})")
            
            # Parse cubes
            cubes = []
            # Enhanced cube pattern to handle chained operations
            cube_pattern = r'\.texOffs\([^)]+\)(?:\.mirror\([^)]*\))?\.addBox\([^)]+\)(?:\s*,\s*new\s+CubeDeformation\([^)]*\))?'
            cube_matches = re.findall(cube_pattern, cube_definitions)
            
            for cube_match in cube_matches:
                cube_data = self.parse_cube_definition(cube_match)
                if cube_data:
                    cubes.append(cube_data)
            
            # Parse pose with FIXED coordinate transformation
            origin = [0.0, 0.0, 0.0]
            rotation = [0.0, 0.0, 0.0]
            
            if pose_type == "offset":
                pose_match = re.search(r'(-?\d+(?:\.\d+)?)F?,\s*(-?\d+(?:\.\d+)?)F?,\s*(-?\d+(?:\.\d+)?)F?', pose_params)
                if pose_match:
                    origin = [float(pose_match.group(1)), -float(pose_match.group(2)), float(pose_match.group(3))]
                    
            elif pose_type == "offsetAndRotation":
                pose_match = re.search(r'(-?\d+(?:\.\d+)?)F?,\s*(-?\d+(?:\.\d+)?)F?,\s*(-?\d+(?:\.\d+)?)F?,\s*(-?\d+(?:\.\d+)?)F?,\s*(-?\d+(?:\.\d+)?)F?,\s*(-?\d+(?:\.\d+)?)F?', pose_params)
                if pose_match:
                    origin = [float(pose_match.group(1)), -float(pose_match.group(2)), float(pose_match.group(3))]
                    rotation = [float(pose_match.group(4)), float(pose_match.group(5)), float(pose_match.group(6))]
            
            parts[var_name] = {
                "name": name,
                "parent": parent,
                "cubes": cubes,
                "origin": origin,
                "rotation": rotation
            }
        
        return parts
    
    def build_hierarchy_fixed(self, part_name: str, parts: Dict[str, Any], outliner_map: Dict[str, Any]) -> Any:
        """Build hierarchy with CORRECT parent-child relationships"""
        if part_name not in parts:
            return None
            
        part_data = parts[part_name]
        
        # Create group structure 
        group = {
            "name": part_data["name"],
            "origin": part_data["origin"],
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
        
        # CRITICAL FIX: Find child parts based on CORRECT parent names from Java constructor
        # This mapping is based on the actual Java constructor hierarchy
        hierarchy_map = {
            "partdefinition": ["roots"],
            "roots": ["lowerbody", "rightleg", "leftleg"],  # FIXED: legs are children of roots
            "lowerbody": ["upperbody"],  # FIXED: upperbody is child of lowerbody
            "upperbody": ["head", "leftarmjoint", "rightarmjoint"],
            "head": ["horns", "jaw"],
            "leftarmjoint": ["leftarm"],
            "leftarm": ["leftarm2"],
            "leftarm2": ["lefthand"],
            "lefthand": ["l_hand_blast_4", "l_hand_blast_3", "l_hand_blast_2", "l_hand_blast_1", "l_cannon", "l_core"],
            "l_hand_blast_3": ["leftfinger1"],
            "l_hand_blast_2": ["leftfinger2"],
            "l_hand_blast_1": ["leftfinger3"],
            "l_core": ["l_flame_2", "l_flame_1"],
            "rightarmjoint": ["rightarm"],
            "rightarm": ["rightarm2"],
            "rightarm2": ["righthand"],
            "righthand": ["r_hand_blast_4", "r_hand_blast_3", "r_hand_blast_2", "r_hand_blast_1", "r_cannon", "r_core"],
            "r_hand_blast_3": ["rightfinger1"],
            "r_hand_blast_2": ["rightfinger2"],
            "r_hand_blast_1": ["rightfinger3"],
            "r_core": ["r_flame_1", "r_flame_2"]
        }
        
        # Use the correct hierarchy mapping
        if part_name in hierarchy_map:
            child_names = hierarchy_map[part_name]
            for child_name in child_names:
                # Find the part definition that corresponds to this child name
                child_part_key = None
                for key, data in parts.items():
                    if data["name"] == child_name:
                        child_part_key = key
                        break
                
                if child_part_key:
                    child_group = self.build_hierarchy_fixed(child_part_key, parts, outliner_map)
                    if child_group:
                        group["children"].append(child_group)
        
        return group
    
    def build_blockbench_structure(self, parts: Dict[str, Any]) -> Dict[str, Any]:
        """Build the Blockbench JSON structure with FIXED hierarchy"""
        self.texture_width, self.texture_height = self.extract_texture_size()
        
        elements = []
        outliner_map = {}
        
        # Create elements from cubes
        element_id = 0
        for part_name, part_data in parts.items():
            part_elements = []
            for i, cube in enumerate(part_data["cubes"]):
                element = {
                    "name": f"{part_data['name']}_{i}" if len(part_data["cubes"]) > 1 else part_data['name'],
                    "box_uv": True,
                    "rescale": False,
                    "locked": False,
                    "light_emission": 0,
                    "render_order": "default",
                    "allow_mirror_modeling": True,
                    "from": cube["from"],
                    "to": cube["to"],
                    "autouv": 0,
                    "color": 0,
                    "origin": part_data["origin"],
                    "rotation": part_data.get("rotation", [0.0, 0.0, 0.0]),
                    "uv_offset": cube["uv_offset"],
                    "faces": cube["faces"],
                    "type": "cube",
                    "uuid": f"element_{element_id}"
                }
                
                # Handle mirrored UVs
                if cube.get("mirrored", False):
                    element["mirror_uv"] = True
                
                elements.append(element)
                part_elements.append(f"element_{element_id}")
                element_id += 1
            
            # Store element references for outliner building
            outliner_map[part_name] = {
                "children": part_elements
            }
        
        # Build outliner with FIXED hierarchy
        outliner = []
        # Start from the root part
        root_parts = [name for name, data in parts.items() if data["name"] == "roots"]
        
        for root_part in root_parts:
            root_group = self.build_hierarchy_fixed(root_part, parts, outliner_map)
            if root_group:
                outliner.append(root_group)
        
        return {
            "meta": {
                "format_version": "4.10",
                "model_format": "modded_entity",
                "box_uv": True
            },
            "name": "netherite_monstrosity_fixed",
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
        """Convert Java model to Blockbench format with all fixes applied"""
        print("Starting FIXED conversion...")
        
        # Extract part definitions
        parts = self.extract_part_definitions()
        print(f"Extracted {len(parts)} parts")
        
        # Build Blockbench structure
        blockbench_data = self.build_blockbench_structure(parts)
        
        # Convert to JSON
        return json.dumps(blockbench_data, indent=2)

def main():
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python netherite_monstrosity_converter_fixed.py <java_file_path>")
        sys.exit(1)
    
    java_file = sys.argv[1]
    converter = JavaToBlockbenchConverterFixed(java_file)
    
    try:
        result = converter.convert()
        output_file = "netherite_monstrosity_fixed.bbmodel"
        
        with open(output_file, 'w') as f:
            f.write(result)
        
        print(f"Conversion completed successfully! Output saved to {output_file}")
        
    except Exception as e:
        print(f"Conversion failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()