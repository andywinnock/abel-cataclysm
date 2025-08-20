#!/usr/bin/env python3
"""
Manual Netherite Monstrosity Conversion - Targeted Fix
Creates a properly structured .bbmodel with correct hierarchy and coordinates
"""

import json
import uuid

def create_netherite_monstrosity_fixed():
    """Create a properly structured Netherite Monstrosity model"""
    
    # Define the main structural parts based on the Java model
    # Using the actual coordinates from the createBodyLayer method
    
    elements = []
    element_id = 0
    
    # Helper function to create cube element
    def create_cube(name, from_coords, to_coords, origin, rotation, uv_offset, faces):
        nonlocal element_id
        element = {
            "name": name,
            "box_uv": True,
            "rescale": False,
            "locked": False,
            "light_emission": 0,
            "render_order": "default",
            "allow_mirror_modeling": True,
            "from": from_coords,
            "to": to_coords,
            "autouv": 0,
            "color": 0,
            "origin": origin,
            "rotation": rotation,
            "uv_offset": uv_offset,
            "faces": faces,
            "type": "cube",
            "uuid": f"element_{element_id}"
        }
        elements.append(element)
        result_id = f"element_{element_id}"
        element_id += 1
        return result_id
    
    # Helper function to generate cube faces
    def generate_faces(uv_x, uv_y, w, h, d):
        return {
            "north": {"uv": [uv_x + d, uv_y + d, uv_x + d + w, uv_y + d + h], "texture": 0},
            "east": {"uv": [uv_x, uv_y + d, uv_x + d, uv_y + d + h], "texture": 0},
            "south": {"uv": [uv_x + d + w, uv_y + d, uv_x + d + w + d, uv_y + d + h], "texture": 0},
            "west": {"uv": [uv_x + d + w, uv_y + d, uv_x + d + w + d, uv_y + d + h], "texture": 0},
            "up": {"uv": [uv_x + d, uv_y, uv_x + d + w, uv_y + d], "texture": 0},
            "down": {"uv": [uv_x + d + w, uv_y, uv_x + d + w + w, uv_y + d], "texture": 0}
        }
    
    # Create main body parts
    
    # LOWERBODY - Java: addBox(-14.0F, -11.0F, -10.5F, 28.0F, 11.0F, 21.0F)
    # Converted: from = [-14, -(-11+11) = 0, -10.5] = [-14, 0, -10.5], to = [14, 11, 10.5]
    lowerbody_id = create_cube(
        "lowerbody",
        [-14.0, 0.0, -10.5],        # from
        [14.0, 11.0, 10.5],         # to  
        [0.0, 24.0, 2.0],           # origin (from Java PartPose)
        [0.0, 0.0, 0.0],            # rotation
        [175, 193],                 # UV offset
        generate_faces(175, 193, 28, 11, 21)
    )
    
    # UPPERBODY - Multiple cubes
    # Main cube: addBox(-37.0F, -57.0F, -15.0F, 74.0F, 57.0F, 30.0F)
    upperbody_main_id = create_cube(
        "upperbody_main",
        [-37.0, 0.0, -15.0],        # from  
        [37.0, 57.0, 15.0],         # to
        [0.0, 11.0, 0.0],           # origin 
        [0.0873, 0.0, 0.0],         # rotation (5 degrees in radians)
        [0, 0],                     # UV offset
        generate_faces(0, 0, 74, 57, 30)
    )
    
    # Second upperbody cube: addBox(-14.0F, -50.0F, 15.0F, 28.0F, 16.0F, 11.0F)
    upperbody_back_id = create_cube(
        "upperbody_back",
        [-14.0, 7.0, 15.0],         # from (50-57 = -7, inverted = 7)
        [14.0, 23.0, 26.0],         # to
        [0.0, 11.0, 0.0],           # origin
        [0.0873, 0.0, 0.0],         # rotation
        [209, 226],                 # UV offset
        generate_faces(209, 226, 28, 16, 11)
    )
    
    # HEAD - Main cube: addBox(-14.0F, -18.0F, -20.5F, 28.0F, 31.0F, 22.0F)
    head_main_id = create_cube(
        "head_main", 
        [-14.0, -13.0, -20.5],      # from
        [14.0, 18.0, 1.5],          # to
        [0.0, 33.0, -16.5],         # origin
        [0.0, 0.0, 0.0],            # rotation
        [0, 139],                   # UV offset
        generate_faces(0, 139, 28, 31, 22)
    )
    
    # HEAD - Left horn: addBox(-34.0F, -12.5F, -16.0F, 20.0F, 13.0F, 13.0F)
    head_left_horn_id = create_cube(
        "head_left_horn",
        [-34.0, -0.5, -16.0],       # from
        [-14.0, 12.5, -3.0],        # to
        [0.0, 33.0, -16.5],         # origin
        [0.0, 0.0, 0.0],            # rotation
        [246, 112],                 # UV offset
        generate_faces(246, 112, 20, 13, 13)
    )
    
    # HEAD - Right horn: mirror().addBox(14.0F, -12.5F, -16.0F, 20.0F, 13.0F, 13.0F)
    head_right_horn_id = create_cube(
        "head_right_horn", 
        [14.0, -0.5, -16.0],        # from
        [34.0, 12.5, -3.0],         # to
        [0.0, 33.0, -16.5],         # origin
        [0.0, 0.0, 0.0],            # rotation
        [246, 112],                 # UV offset - same as left but mirrored
        generate_faces(246, 112, 20, 13, 13)
    )
    
    # JAW - Main part
    jaw_main_id = create_cube(
        "jaw_main",
        [-13.5, -6.0, -21.9],       # from
        [13.5, 10.0, -0.9],         # to
        [0.0, -11.0, 1.5],          # origin
        [0.1309, 0.0, 0.0],         # rotation
        [209, 2],                   # UV offset
        generate_faces(209, 2, 27, 16, 21)
    )
    
    # LEFT ARM CHAIN
    # leftarmjoint has no cubes, just a pivot point
    
    # leftarm - Two cubes
    leftarm_upper_id = create_cube(
        "leftarm_upper",
        [0.0, -33.5, -13.5],        # from - NOTE: this is relative to leftarm origin
        [20.0, -10.5, 13.5],        # to
        [37.0, 38.5, -2.5],         # origin from leftarmjoint
        [0.0, 0.0, 0.0],            # rotation
        [101, 163],                 # UV offset
        generate_faces(101, 163, 20, 23, 27)
    )
    
    leftarm_lower_id = create_cube(
        "leftarm_lower",
        [0.0, -10.5, -13.5],        # from
        [37.0, 12.5, 13.5],         # to
        [37.0, 38.5, -2.5],         # origin
        [0.0, 0.0, 0.0],            # rotation
        [0, 88],                    # UV offset
        generate_faces(0, 88, 37, 23, 27)
    )
    
    # leftarm2
    leftarm2_id = create_cube(
        "leftarm2",
        [-11.0, -4.5, -8.0],        # from
        [11.0, 15.5, 8.0],          # to  
        [55.0, 50.5, -2.5],         # origin (leftarmjoint + leftarm offset + leftarm2 offset)
        [-0.1309, 0.0, 0.0],        # rotation
        [132, 226],                 # UV offset
        generate_faces(132, 226, 22, 20, 16)
    )
    
    # lefthand 
    lefthand_id = create_cube(
        "lefthand",
        [-12.0, -5.0, -12.0],       # from
        [12.0, 0.0, 12.0],          # to
        [55.0, 67.5, -2.5],         # origin (full chain + offsets)
        [-0.0873, 0.0, 0.0],        # rotation
        [136, 264],                 # UV offset
        generate_faces(136, 264, 24, 5, 24)
    )
    
    # RIGHT ARM CHAIN - Mirrored positions
    # rightarm - Two cubes
    rightarm_upper_id = create_cube(
        "rightarm_upper",
        [-20.0, -33.5, -13.5],      # from - mirrored X
        [0.0, -10.5, 13.5],         # to
        [-37.0, 38.5, -2.5],        # origin - mirrored X
        [0.0, 0.0, 0.0],            # rotation
        [101, 163],                 # UV offset
        generate_faces(101, 163, 20, 23, 27)
    )
    
    rightarm_lower_id = create_cube(
        "rightarm_lower", 
        [-37.0, -10.5, -13.5],      # from - mirrored X
        [0.0, 12.5, 13.5],          # to
        [-37.0, 38.5, -2.5],        # origin - mirrored X
        [0.0, 0.0, 0.0],            # rotation
        [0, 88],                    # UV offset
        generate_faces(0, 88, 37, 23, 27)
    )
    
    # rightarm2
    rightarm2_id = create_cube(
        "rightarm2",
        [-11.0, -4.5, -8.0],        # from
        [11.0, 15.5, 8.0],          # to
        [-55.0, 50.5, -2.5],        # origin - mirrored X
        [-0.1309, 0.0, 0.0],        # rotation
        [132, 226],                 # UV offset
        generate_faces(132, 226, 22, 20, 16)
    )
    
    # righthand
    righthand_id = create_cube(
        "righthand",
        [-12.0, -5.0, -12.0],       # from
        [12.0, 0.0, 12.0],          # to
        [-55.0, 67.5, -2.5],        # origin - mirrored X
        [-0.0873, 0.0, 0.0],        # rotation
        [136, 264],                 # UV offset
        generate_faces(136, 264, 24, 5, 24)
    )
    
    # LEGS
    # rightleg: PartPose.offsetAndRotation(0.0F, -24.0F, 0.0F, 0.0F, 0.0873F, 0.0F) - but this is under roots
    # From context, rightleg should be at positive X
    rightleg_id = create_cube(
        "rightleg",
        [-12.0, -29.0, -9.5],       # from
        [12.0, 0.0, 9.5],           # to
        [19.0, 13.0, -2.0],         # origin
        [0.0, 0.0873, 0.0],         # rotation
        [0, 193],                   # UV offset
        generate_faces(0, 193, 24, 29, 19)
    )
    
    # leftleg: mirror version
    leftleg_id = create_cube(
        "leftleg", 
        [-12.0, -29.0, -9.5],       # from
        [12.0, 0.0, 9.5],           # to
        [-19.0, 13.0, -2.0],        # origin - mirrored X
        [0.0, -0.0873, 0.0],        # rotation - mirrored Y rotation
        [0, 193],                   # UV offset
        generate_faces(0, 193, 24, 29, 19)
    )
    
    # Build the correct outliner structure
    outliner = [{
        "name": "roots",
        "origin": [0.0, -24.0, 0.0],
        "rotation": [0.0, 0.0, 0.0],
        "color": 0,
        "uuid": "group_roots",
        "export": True,
        "mirror_uv": False,
        "isOpen": True,
        "locked": False,
        "visibility": True,
        "autouv": 0,
        "selected": False,
        "children": [
            # lowerbody group
            {
                "name": "lowerbody",
                "origin": [0.0, 24.0, 2.0],
                "rotation": [0.0, 0.0, 0.0],
                "color": 0,
                "uuid": "group_lowerbody",
                "export": True,
                "mirror_uv": False,
                "isOpen": True,
                "locked": False,
                "visibility": True,
                "autouv": 0,
                "selected": False,
                "children": [
                    lowerbody_id,
                    # upperbody group
                    {
                        "name": "upperbody",
                        "origin": [0.0, 11.0, 0.0],
                        "rotation": [0.0873, 0.0, 0.0],
                        "color": 0,
                        "uuid": "group_upperbody",
                        "export": True,
                        "mirror_uv": False,
                        "isOpen": True,
                        "locked": False,
                        "visibility": True,
                        "autouv": 0,
                        "selected": False,
                        "children": [
                            upperbody_main_id,
                            upperbody_back_id,
                            # head group
                            {
                                "name": "head",
                                "origin": [0.0, 33.0, -16.5],
                                "rotation": [0.0, 0.0, 0.0],
                                "color": 0,
                                "uuid": "group_head",
                                "export": True,
                                "mirror_uv": False,
                                "isOpen": True,
                                "locked": False,
                                "visibility": True,
                                "autouv": 0,
                                "selected": False,
                                "children": [
                                    head_main_id,
                                    head_left_horn_id,
                                    head_right_horn_id,
                                    # jaw group
                                    {
                                        "name": "jaw",
                                        "origin": [0.0, -11.0, 1.5],
                                        "rotation": [0.1309, 0.0, 0.0],
                                        "color": 0,
                                        "uuid": "group_jaw",
                                        "export": True,
                                        "mirror_uv": False,
                                        "isOpen": True,
                                        "locked": False,
                                        "visibility": True,
                                        "autouv": 0,
                                        "selected": False,
                                        "children": [jaw_main_id]
                                    }
                                ]
                            },
                            # leftarmjoint group
                            {
                                "name": "leftarmjoint",
                                "origin": [37.0, 38.5, -2.5],
                                "rotation": [0.0, 0.0, 0.0],
                                "color": 0,
                                "uuid": "group_leftarmjoint",
                                "export": True,
                                "mirror_uv": False,
                                "isOpen": True,
                                "locked": False,
                                "visibility": True,
                                "autouv": 0,
                                "selected": False,
                                "children": [
                                    # leftarm group
                                    {
                                        "name": "leftarm",
                                        "origin": [0.0, 0.0, 0.0],
                                        "rotation": [0.0, 0.0, 0.0],
                                        "color": 0,
                                        "uuid": "group_leftarm",
                                        "export": True,
                                        "mirror_uv": False,
                                        "isOpen": True,
                                        "locked": False,
                                        "visibility": True,
                                        "autouv": 0,
                                        "selected": False,
                                        "children": [
                                            leftarm_upper_id,
                                            leftarm_lower_id,
                                            # leftarm2 group
                                            {
                                                "name": "leftarm2",
                                                "origin": [18.0, 12.0, 0.0],
                                                "rotation": [-0.1309, 0.0, 0.0],
                                                "color": 0,
                                                "uuid": "group_leftarm2",
                                                "export": True,
                                                "mirror_uv": False,
                                                "isOpen": True,
                                                "locked": False,
                                                "visibility": True,
                                                "autouv": 0,
                                                "selected": False,
                                                "children": [
                                                    leftarm2_id,
                                                    # lefthand group
                                                    {
                                                        "name": "lefthand",
                                                        "origin": [0.0, 17.0, 0.0],
                                                        "rotation": [-0.0873, 0.0, 0.0],
                                                        "color": 0,
                                                        "uuid": "group_lefthand",
                                                        "export": True,
                                                        "mirror_uv": False,
                                                        "isOpen": True,
                                                        "locked": False,
                                                        "visibility": True,
                                                        "autouv": 0,
                                                        "selected": False,
                                                        "children": [lefthand_id]
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            },
                            # rightarmjoint group
                            {
                                "name": "rightarmjoint",
                                "origin": [-37.0, 38.5, -2.5],
                                "rotation": [0.0, 0.0, 0.0],
                                "color": 0,
                                "uuid": "group_rightarmjoint",
                                "export": True,
                                "mirror_uv": False,
                                "isOpen": True,
                                "locked": False,
                                "visibility": True,
                                "autouv": 0,
                                "selected": False,
                                "children": [
                                    # rightarm group
                                    {
                                        "name": "rightarm",
                                        "origin": [0.0, 0.0, 0.0],
                                        "rotation": [0.0, 0.0, 0.0],
                                        "color": 0,
                                        "uuid": "group_rightarm",
                                        "export": True,
                                        "mirror_uv": False,
                                        "isOpen": True,
                                        "locked": False,
                                        "visibility": True,
                                        "autouv": 0,
                                        "selected": False,
                                        "children": [
                                            rightarm_upper_id,
                                            rightarm_lower_id,
                                            # rightarm2 group
                                            {
                                                "name": "rightarm2",
                                                "origin": [-18.0, 12.0, 0.0],
                                                "rotation": [-0.1309, 0.0, 0.0],
                                                "color": 0,
                                                "uuid": "group_rightarm2",
                                                "export": True,
                                                "mirror_uv": False,
                                                "isOpen": True,
                                                "locked": False,
                                                "visibility": True,
                                                "autouv": 0,
                                                "selected": False,
                                                "children": [
                                                    rightarm2_id,
                                                    # righthand group
                                                    {
                                                        "name": "righthand",
                                                        "origin": [0.0, 17.0, 0.0],
                                                        "rotation": [-0.0873, 0.0, 0.0],
                                                        "color": 0,
                                                        "uuid": "group_righthand",
                                                        "export": True,
                                                        "mirror_uv": False,
                                                        "isOpen": True,
                                                        "locked": False,
                                                        "visibility": True,
                                                        "autouv": 0,
                                                        "selected": False,
                                                        "children": [righthand_id]
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            # rightleg group
            {
                "name": "rightleg",
                "origin": [19.0, 13.0, -2.0],
                "rotation": [0.0, 0.0873, 0.0],
                "color": 0,
                "uuid": "group_rightleg",
                "export": True,
                "mirror_uv": False,
                "isOpen": True,
                "locked": False,
                "visibility": True,
                "autouv": 0,
                "selected": False,
                "children": [rightleg_id]
            },
            # leftleg group
            {
                "name": "leftleg",
                "origin": [-19.0, 13.0, -2.0],
                "rotation": [0.0, -0.0873, 0.0],
                "color": 0,
                "uuid": "group_leftleg",
                "export": True,
                "mirror_uv": False,
                "isOpen": True,
                "locked": False,
                "visibility": True,
                "autouv": 0,
                "selected": False,
                "children": [leftleg_id]
            }
        ]
    }]
    
    return {
        "meta": {
            "format_version": "4.10",
            "model_format": "modded_entity",
            "box_uv": True
        },
        "name": "netherite_monstrosity_manual_fixed",
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
            "width": 512,
            "height": 512
        },
        "elements": elements,
        "outliner": outliner,
        "textures": []
    }

def main():
    model_data = create_netherite_monstrosity_fixed()
    
    with open("netherite_monstrosity_manual_fixed.bbmodel", "w") as f:
        json.dump(model_data, f, indent=2)
    
    print("Manual fixed conversion completed! Output: netherite_monstrosity_manual_fixed.bbmodel")
    print("\nStructural fixes applied:")
    print("✅ Correct hierarchy: roots -> lowerbody -> upperbody")
    print("✅ Legs properly positioned as children of roots")
    print("✅ Left/right arms correctly positioned")
    print("✅ Y-coordinate system properly converted")
    print("✅ Proper origins and rotations applied")

if __name__ == "__main__":
    main()