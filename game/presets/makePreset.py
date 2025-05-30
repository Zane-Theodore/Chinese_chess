import os

DIR = os.path.dirname(__file__)
SEPERATOR = " ******** "

positions = {
    "chariot": [(0, 0), (0, 8)],  
    "horse": [(0, 1), (0, 7)],      
    "elephant": [(0, 2), (0, 6)],  
    "advisor": [(0, 3), (0, 5)],  
    "lord": [(0, 4)],              
    "cannon": [(2, 1), (2, 7)],    
    "soldier": [(3, 0), (3, 2), (3, 4), (3, 6), (3, 8)] 
}

def validate_position(row, col):
    """
    Check if location is valid
    """
    if not (0 <= row <= 9) or not (0 <= col <= 8):
        raise ValueError(f"Invalid chess position: ({row}, {col})")

final = []

for side in ["blue", "red"]:
    row_offset = 0 if side == "blue" else 9
    is_red = (side == "red")
    
    # Main pieces
    for piece in ["chariot", "horse", "elephant", "advisor", "lord"]:
        for (r_rel, c) in positions[piece]:
            r_abs = row_offset + (r_rel if not is_red else -r_rel)
            validate_position(r_abs, c)
            final.append([piece, r_abs, c, side])
    
    # Cannons
    for (r_rel, c) in positions["cannon"]:
        r_abs = (9 - r_rel) if is_red else r_rel
        validate_position(r_abs, c)
        final.append(["cannon", r_abs, c, side])
    
    # Soldiers
    for (r_rel, c) in positions["soldier"]:
        r_abs = 6 if is_red else 3 
        validate_position(r_abs, c)
        final.append(["soldier", r_abs, c, side])

# Write to file
with open(os.path.join(DIR, "standard.cfg"), "w") as f:
    for item in final:
        f.write(f"{SEPERATOR.join(map(str, item))}\n")
