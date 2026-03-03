def correct_name(name: str) -> str:
    """
    Corrects a name by only keeping the first and last name (in titlecse)
    
    :param name: the name to correct
    :type name: str
    :return: the corrected name
    :rtype: str
    """
    parts = [x.title() for x in name.split() if x]
    if len(parts) <= 2:
        return name.title()
    return f"{parts[0]} {parts[-1]}"