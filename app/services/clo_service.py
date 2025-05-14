import os
import yaml
from typing import List, Dict, Tuple, Any, Optional
from app.schemas.clothing import ClothingAnalysis

def load_clo_values(yaml_file: str = 'clo_values.yaml') -> Dict[str, Any]:
    """
    Load CLO values from a YAML file.
    
    Args:
        yaml_file: Path to the YAML file containing CLO values
        
    Returns:
        Dictionary containing CLO values and base CLO
    """
    if not os.path.exists(yaml_file):
        raise FileNotFoundError(f"CLO values file not found: {yaml_file}")
    
    with open(yaml_file, 'r') as f:
        clo_data = yaml.safe_load(f)
    
    return clo_data

def get_clothing_clo_values(yaml_file: str = 'clo_values.yaml') -> Dict[str, float]:
    """
    Returns a dictionary mapping clothing items to their CLO values.
    
    Args:
        yaml_file: Path to the YAML file containing CLO values
        
    Returns:
        Dictionary mapping clothing items to their CLO values
    """
    clo_data = load_clo_values(yaml_file)
    return clo_data.get('clo_values', {})

def get_base_clo_value(yaml_file: str = 'clo_values.yaml') -> float:
    """
    Returns the base CLO value for a nude person.
    
    Args:
        yaml_file: Path to the YAML file containing CLO values
        
    Returns:
        Base CLO value
    """
    clo_data = load_clo_values(yaml_file)
    return clo_data.get('base_clo', 0.0)

def calculate_clo_value(analysis: ClothingAnalysis, yaml_file: str = 'clo_values.yaml') -> float:
    """
    Calculates the total CLO value based on detected clothing items.
    
    Args:
        analysis: ClothingAnalysis object containing detected clothing items
        yaml_file: Path to the YAML file containing CLO values
        
    Returns:
        Total CLO value
    """
    clo_mapping = get_clothing_clo_values(yaml_file)
    base_clo = get_base_clo_value(yaml_file)
    total_clo = base_clo
    
    # Define lower body items for detection
    lower_body_items = ["pants", "dress pants", "jeans", "trousers", "shorts", "skirt", "leggings", "joggers"]
    
    # Check if any lower body item is detected
    has_lower_body = any(item.lower() in lower_body_items for item in analysis.clothing_type)
    
    # Track if t-shirt or shirt has been processed to avoid double counting
    processed_shirt = False
    
    # Add CLO values for each clothing type
    for item in analysis.clothing_type:
        item_lower = item.lower()
        
        # Special handling for t-shirt, polo t-shirt, and shirt based on sleeve length
        if (item_lower == "t-shirt" or item_lower == "polo t-shirt") and analysis.sleeve_length == 'long' and not processed_shirt:
            # If t-shirt or polo t-shirt with long sleeves, use shirt CLO value
            if "shirt" in clo_mapping:
                total_clo += clo_mapping["shirt"]
                processed_shirt = True
        elif item_lower == "shirt" and analysis.sleeve_length == 'short' and not processed_shirt:
            # If shirt with short sleeves, use t-shirt CLO value
            if "t-shirt" in clo_mapping:
                total_clo += clo_mapping["t-shirt"]
                processed_shirt = True
        elif item_lower in clo_mapping and not (processed_shirt and (item_lower == "t-shirt" or item_lower == "shirt" or item_lower == "polo t-shirt")):
            # Normal case for other items, or if t-shirt/shirt/polo t-shirt hasn't been processed yet
            total_clo += clo_mapping[item_lower]
            if item_lower == "t-shirt" or item_lower == "shirt" or item_lower == "polo t-shirt":
                processed_shirt = True
    
    # If no lower body item detected, add jeans as default
    if not has_lower_body and "jeans" in clo_mapping:
        total_clo += clo_mapping["jeans"]
        # Optionally, you could add jeans to the clothing_type list for reference
        #analysis.clothing_type.append("jeans")
    
    # Add CLO values for accessories
    for accessory in analysis.accessories:
        if accessory.lower() in clo_mapping and accessory.lower() != "none":
            total_clo += clo_mapping[accessory.lower()]
    
    # Add CLO value for headwear if present
    if analysis.headwear and "headwear" in clo_mapping:
        total_clo += clo_mapping["headwear"]
    
    # Add CLO value for glasses if present
    if analysis.glasses and "glasses" in clo_mapping:
        total_clo += clo_mapping["glasses"]
    
    # Round to 2 decimal places for readability
    return round(total_clo, 2)
