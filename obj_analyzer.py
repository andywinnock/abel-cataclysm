#!/usr/bin/env python3
"""
OBJ File Analyzer for Model Calibration
Analyzes OBJ files to extract vertex positions and bounding boxes for calibrating model converters
"""

import re
from typing import Dict, List, Tuple

class OBJAnalyzer:
    def __init__(self, obj_file: str):
        self.obj_file = obj_file
        self.vertices = []
        self.objects = {}
        self.current_object = None
        
    def parse(self):
        """Parse the OBJ file and extract vertices and objects"""
        with open(self.obj_file, 'r') as f:
            current_vertices = []
            for line in f:
                line = line.strip()
                
                if line.startswith('v '):  # Vertex
                    parts = line.split()
                    x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                    self.vertices.append((x, y, z))
                    if self.current_object:
                        current_vertices.append((x, y, z))
                        
                elif line.startswith('o '):  # New object
                    # Save previous object's vertices
                    if self.current_object and current_vertices:
                        self.objects[self.current_object] = current_vertices
                    
                    # Start new object
                    self.current_object = line.split()[1]
                    current_vertices = []
            
            # Save last object
            if self.current_object and current_vertices:
                self.objects[self.current_object] = current_vertices
    
    def get_bounding_box(self, vertices: List[Tuple[float, float, float]]) -> Dict:
        """Calculate bounding box for a set of vertices"""
        if not vertices:
            return None
            
        # Calculate min/max for each axis
        xs = [v[0] for v in vertices]
        ys = [v[1] for v in vertices]
        zs = [v[2] for v in vertices]
        
        min_coords = [min(xs), min(ys), min(zs)]
        max_coords = [max(xs), max(ys), max(zs)]
        center = [(min_coords[i] + max_coords[i]) / 2 for i in range(3)]
        size = [max_coords[i] - min_coords[i] for i in range(3)]
        
        return {
            'min': min_coords,
            'max': max_coords,
            'center': center,
            'size': size
        }
    
    def analyze_model_structure(self):
        """Analyze the overall model structure"""
        print(f"Total vertices: {len(self.vertices)}")
        print(f"Total objects: {len(self.objects)}")
        print()
        
        # Get overall bounding box
        overall_bb = self.get_bounding_box(self.vertices)
        print("Overall Model Bounding Box:")
        print(f"  Min: {overall_bb['min']}")
        print(f"  Max: {overall_bb['max']}")
        print(f"  Center: {overall_bb['center']}")
        print(f"  Size: {overall_bb['size']}")
        print()
        
        # Analyze each object
        print("Object Analysis:")
        for obj_name, vertices in self.objects.items():
            bb = self.get_bounding_box(vertices)
            if bb:
                print(f"\n{obj_name}: ({len(vertices)} vertices)")
                print(f"  Center: [{bb['center'][0]:.3f}, {bb['center'][1]:.3f}, {bb['center'][2]:.3f}]")
                print(f"  Size: [{bb['size'][0]:.3f}, {bb['size'][1]:.3f}, {bb['size'][2]:.3f}]")
    
    def find_limb_positions(self):
        """Try to identify limb positions based on object positions"""
        print("\nAttempting to identify limbs based on positions:")
        
        limb_candidates = {}
        for obj_name, vertices in self.objects.items():
            bb = self.get_bounding_box(vertices)
            if bb:
                x_center = bb['center'][0]
                y_center = bb['center'][1]
                z_center = bb['center'][2]
                
                # Classify based on position
                if abs(x_center) > 1.5:  # Far from center X - likely arms
                    if x_center > 0:
                        limb_type = "Left Arm/Hand part"
                    else:
                        limb_type = "Right Arm/Hand part"
                elif y_center > 2.0:  # High Y - likely head/upper body
                    limb_type = "Head/Upper body part"
                elif y_center < 1.0:  # Low Y - likely legs/lower body
                    if abs(x_center) > 0.5:
                        limb_type = "Leg part"
                    else:
                        limb_type = "Lower body part"
                else:
                    limb_type = "Body/Core part"
                
                limb_candidates[obj_name] = {
                    'type': limb_type,
                    'center': bb['center'],
                    'size': bb['size']
                }
        
        # Sort by type for organized output
        sorted_limbs = sorted(limb_candidates.items(), key=lambda x: x[1]['type'])
        for obj_name, info in sorted_limbs:
            print(f"{obj_name}: {info['type']}")
            print(f"  Position: [{info['center'][0]:.3f}, {info['center'][1]:.3f}, {info['center'][2]:.3f}]")
    
    def get_coordinate_system_info(self):
        """Analyze the coordinate system being used"""
        print("\nCoordinate System Analysis:")
        
        overall_bb = self.get_bounding_box(self.vertices)
        
        # Check if model is centered at origin or elevated
        y_min = overall_bb['min'][1]
        y_max = overall_bb['max'][1]
        y_center = overall_bb['center'][1]
        
        print(f"Y range: {y_min:.3f} to {y_max:.3f}")
        print(f"Y center: {y_center:.3f}")
        
        if y_min >= 0:
            print("Model appears to be positioned above Y=0 (ground-based)")
        elif abs(y_center) < 0.5:
            print("Model appears to be centered around Y=0")
        else:
            print("Model uses custom Y positioning")
        
        # Check X symmetry (left/right)
        x_min = overall_bb['min'][0]
        x_max = overall_bb['max'][0]
        x_center = overall_bb['center'][0]
        
        print(f"\nX range: {x_min:.3f} to {x_max:.3f}")
        print(f"X center: {x_center:.3f}")
        
        if abs(x_center) < 0.1:
            print("Model appears to be X-centered (symmetric left/right)")
        else:
            print(f"Model is offset in X by {x_center:.3f}")

def main():
    print("=== OBJ Model Analyzer for Netherite/Redstone Monstrosity ===\n")
    
    analyzer = OBJAnalyzer("/home/andy/Developer/abel-cataclysm/redstone_monstrosity.obj")
    analyzer.parse()
    
    analyzer.analyze_model_structure()
    analyzer.find_limb_positions()
    analyzer.get_coordinate_system_info()

if __name__ == "__main__":
    main()