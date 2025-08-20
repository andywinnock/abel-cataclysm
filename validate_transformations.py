#!/usr/bin/env python3
"""
Validation script to verify cumulative transformations are calculated correctly
"""

def manual_calculation():
    """Manual calculation of expected positions"""
    print("=== MANUAL TRANSFORMATION CALCULATIONS ===")
    
    # roots position
    roots = [0.0, 24.0, 0.0]
    print(f"roots: {roots}")
    
    # lowerbody (relative to roots)
    lowerbody_local = [0.0, -24.0, 2.0]
    lowerbody_world = [roots[0] + lowerbody_local[0], 
                      roots[1] + lowerbody_local[1], 
                      roots[2] + lowerbody_local[2]]
    print(f"lowerbody: {lowerbody_local} → world: {lowerbody_world}")
    
    # upperbody (relative to lowerbody) 
    upperbody_local = [0.0, -11.0, 0.0]
    upperbody_world = [lowerbody_world[0] + upperbody_local[0],
                      lowerbody_world[1] + upperbody_local[1],
                      lowerbody_world[2] + upperbody_local[2]]
    print(f"upperbody: {upperbody_local} → world: {upperbody_world}")
    
    # leftarmjoint (relative to upperbody)
    leftarmjoint_local = [37.0, -38.5, -2.5]
    leftarmjoint_world = [upperbody_world[0] + leftarmjoint_local[0],
                         upperbody_world[1] + leftarmjoint_local[1],
                         upperbody_world[2] + leftarmjoint_local[2]]
    print(f"leftarmjoint: {leftarmjoint_local} → world: {leftarmjoint_world}")
    
    # Convert to Blockbench coordinates (Y inverted)
    leftarmjoint_bb = [leftarmjoint_world[0], -leftarmjoint_world[1], leftarmjoint_world[2]]
    print(f"leftarmjoint Blockbench: {leftarmjoint_bb}")
    
    # rightleg (relative to roots)
    rightleg_local = [-14.0, -27.0, 0.0]
    rightleg_world = [roots[0] + rightleg_local[0],
                     roots[1] + rightleg_local[1],
                     roots[2] + rightleg_local[2]]
    rightleg_bb = [rightleg_world[0], -rightleg_world[1], rightleg_world[2]]
    print(f"rightleg: {rightleg_local} → world: {rightleg_world} → BB: {rightleg_bb}")
    
    # leftleg (relative to roots)
    leftleg_local = [14.0, -27.0, 0.0]
    leftleg_world = [roots[0] + leftleg_local[0],
                    roots[1] + leftleg_local[1],
                    roots[2] + leftleg_local[2]]
    leftleg_bb = [leftleg_world[0], -leftleg_world[1], leftleg_world[2]]
    print(f"leftleg: {leftleg_local} → world: {leftleg_world} → BB: {leftleg_bb}")

def check_generated_model():
    """Check the generated model positions"""
    import json
    
    print("\n=== GENERATED MODEL POSITIONS ===")
    with open('netherite_monstrosity_cumulative_fixed.bbmodel', 'r') as f:
        model = json.load(f)
    
    # Find key parts in outliner
    def find_part_origin(outliner, target_name):
        for item in outliner:
            if isinstance(item, dict) and item['name'] == target_name:
                return item['origin']
            elif isinstance(item, dict) and 'children' in item:
                result = find_part_origin(item['children'], target_name)
                if result:
                    return result
        return None
    
    parts_to_check = ['roots', 'lowerbody', 'upperbody', 'leftarmjoint', 'rightarmjoint', 'leftleg', 'rightleg']
    
    for part_name in parts_to_check:
        origin = find_part_origin(model['outliner'], part_name)
        if origin:
            print(f"{part_name}: {origin}")

if __name__ == "__main__":
    manual_calculation()
    check_generated_model()