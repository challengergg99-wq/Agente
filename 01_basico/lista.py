test_settings = {
    'theme': 'light',
    'font': 'monospace'
}


def add_setting(settings_dict, setting_tuple):
    key = setting_tuple[0].lower()
    value = setting_tuple[1].lower()
    
    if key in settings_dict:
        return f"Setting '{key}' already exists! Cannot add a new setting with this name."
    
    settings_dict[key] = value
    
    return f"Setting '{key}' added with value '{value}' successfully!"


def update_setting(settings_dict, setting_tuple):
    key = setting_tuple[0].lower()
    value = setting_tuple[1].lower()
    
    if key not in settings_dict:  
        return f"Setting '{key}' does not exist! Cannot update a non-existing setting."
    
    settings_dict[key] = value
    
    return f"Setting '{key}' updated to '{value}' successfully!"



def delete_setting(settings_dict, key_to_delete):
    key = key_to_delete.lower()
    
    if key not in settings_dict:
        return "Setting not found!"
    
    del settings_dict[key]
    
    return f"Setting '{key}' deleted successfully!"



def view_settings(settings_dict):
    if not settings_dict:
        return "No settings available."
    
    settings_list = [f"{key}: {value}" for key, value in settings_dict.items()]
    return "\n".join(settings_list)