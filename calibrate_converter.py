#!/usr/bin/env python3
"""
Calibration Tool for Java to Blockbench Converter
Uses OBJ reference model to calibrate coordinate transformations
"""

import json
import re
from typing import Dict, Tuple

class ConverterCalibrator:
    def __init__(self):
        # OBJ reference positions (from analysis)
        self.obj_positions = {
            'right_leg': {'x': 1.083, 'y': 0.604, 'z': 0.021},
            'left_leg': {'x': -1.083, 'y': 0.604, 'z': 0.021},
            'left_arm_upper': {'x': 2.313, 'y': 3.500, 'z': 0.000},
            'right_arm_upper': {'x': -2.313, 'y': 3.500, 'z': 0.000},
            'body_center': {'x': 0.000, 'y': 2.458, 'z': -0.167}
        }
        
        # Java model expected positions (from Netherite_Monstrosity_Model.java)
        # These are the PartPose.offset values from the Java code
        self.java_positions = {
            # rightleg: offset(-14.0F, -27.0F, 0.0F) relative to roots at (0, 24, 0)
            'right_leg': {'x': -14.0, 'y': -3.0, 'z': 0.0},  # 24-27 = -3
            # leftleg: offset(14.0F, -27.0F, 0.0F)
            'left_leg': {'x': 14.0, 'y': -3.0, 'z': 0.0},
            # leftarmjoint: offset(37.0F, -38.5F, -2.5F) relative to upperbody
            'left_arm': {'x': 37.0, 'y': 14.5, 'z': -2.5},  # Needs cumulative calc
            # rightarmjoint: offset(-37.0F, -38.5F, -2.5F)
            'right_arm': {'x': -37.0, 'y': 14.5, 'z': -2.5}
        }
        
    def calculate_scale_factor(self):
        """Calculate scale factor between OBJ and Java models"""
        # Use leg positions as reference (simpler hierarchy)
        obj_leg_spread = abs(self.obj_positions['right_leg']['x'] - self.obj_positions['left_leg']['x'])
        java_leg_spread = abs(self.java_positions['right_leg']['x'] - self.java_positions['left_leg']['x'])
        
        scale = java_leg_spread / obj_leg_spread if obj_leg_spread > 0 else 1.0
        print(f"Scale factor: {scale:.3f}")
        print(f"  OBJ leg spread: {obj_leg_spread:.3f}")
        print(f"  Java leg spread: {java_leg_spread:.3f}")
        
        return scale
    
    def analyze_coordinate_mapping(self):
        """Analyze how coordinates should be mapped"""
        print("\n=== Coordinate Mapping Analysis ===\n")
        
        scale = self.calculate_scale_factor()
        
        print("\nCoordinate System Differences:")
        print("1. OBJ uses +X for LEFT, -X for RIGHT")
        print("2. Java uses +X for LEFT, -X for RIGHT (standard)")
        print("3. OBJ is ground-based (Y starts at 0)")
        print("4. Java uses Y=24 as ground reference")
        
        print("\nProposed Transformation:")
        print("1. Scale OBJ coordinates by factor of", f"{scale:.3f}")
        print("2. For Y-axis: Java_Y = 24 - (OBJ_Y * scale)")
        print("3. For X-axis: Java_X = OBJ_X * scale (keep same)")
        print("4. For Z-axis: Java_Z = OBJ_Z * scale")
        
        return scale
    
    def generate_fixed_converter_code(self):
        """Generate improved converter code with proper transformations"""
        scale = self.calculate_scale_factor()
        
        converter_fix = f'''
# Fixed coordinate transformation for Java to Blockbench
def convert_java_to_blockbench_coords(x, y, z, parent_offset=None):
    """
    Convert Java model coordinates to Blockbench coordinates
    
    Key insights from OBJ calibration:
    - Scale factor: {scale:.3f}
    - Java uses Y=24 as ground, Blockbench uses Y=0
    - Need to accumulate parent offsets through hierarchy
    """
    
    # If there's a parent offset, we need to add it
    if parent_offset:
        x += parent_offset[0]
        y += parent_offset[1]  
        z += parent_offset[2]
    
    # Convert Y coordinate (Java Y-down to Blockbench Y-up)
    # For Blockbench: Y position should be relative to ground (Y=0)
    bb_y = 24 + y  # Since Java Y is negative from 24
    
    return [x, bb_y, z]

def parse_part_with_hierarchy(java_line, parent_transform=None):
    """Parse Java part definition with proper hierarchy transformation"""
    # Extract offset values
    offset_pattern = r'PartPose\\.offset\\(([^,]+)F?,\\s*([^,]+)F?,\\s*([^)]+)F?\\)'
    offset_match = re.search(offset_pattern, java_line)
    
    if offset_match:
        x = float(offset_match.group(1))
        y = float(offset_match.group(2))
        z = float(offset_match.group(3))
        
        # Apply parent transformation if exists
        if parent_transform:
            x += parent_transform['x']
            y += parent_transform['y']
            z += parent_transform['z']
        
        # Convert to Blockbench coordinates
        bb_coords = convert_java_to_blockbench_coords(x, y, z)
        
        return {{
            'x': x,
            'y': y,
            'z': z,
            'bb_x': bb_coords[0],
            'bb_y': bb_coords[1],
            'bb_z': bb_coords[2]
        }}
    
    return None
'''
        
        print("\n=== Generated Converter Fix ===")
        print(converter_fix)
        
        return converter_fix
    
    def test_calibration(self):
        """Test the calibration with known positions"""
        print("\n=== Testing Calibration ===\n")
        
        scale = self.calculate_scale_factor()
        
        # Test with leg positions
        print("Testing leg positions:")
        
        # Right leg OBJ position
        obj_right_x = self.obj_positions['right_leg']['x']
        obj_right_y = self.obj_positions['right_leg']['y']
        
        # Scale and transform
        scaled_x = obj_right_x * scale
        scaled_y = 24 - (obj_right_y * scale)  # Invert for Java coordinates
        
        print(f"Right Leg:")
        print(f"  OBJ: X={obj_right_x:.3f}, Y={obj_right_y:.3f}")
        print(f"  Scaled: X={scaled_x:.3f}, Y={scaled_y:.3f}")
        print(f"  Expected Java: X={self.java_positions['right_leg']['x']:.3f}, Y={self.java_positions['right_leg']['y']:.3f}")
        print(f"  Match: {'YES' if abs(scaled_x - self.java_positions['right_leg']['x']) < 2 else 'NO'}")

def main():
    print("=== Java to Blockbench Converter Calibration ===\n")
    
    calibrator = ConverterCalibrator()
    calibrator.analyze_coordinate_mapping()
    calibrator.generate_fixed_converter_code()
    calibrator.test_calibration()
    
    print("\n=== Calibration Complete ===")
    print("\nKey findings:")
    print("1. The OBJ model shows limbs ARE properly positioned outside the body")
    print("2. Our converter needs proper cumulative transformation through hierarchy")
    print("3. Scale factor between OBJ and Java coordinates is significant")
    print("4. Y-axis transformation needs to account for ground-based vs centered models")

if __name__ == "__main__":
    main()