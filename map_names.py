def map_name_to_LATASSOC1(name):
    """map common names of a subset of objects to 3FGL ASSOC1 name"""

    n=name.upper().replace(" ","")

    # Markarian 421
    if n in ["MRK421", "MARKARIAN421", "MKN421"]:
        return "Mkn421"
    
    # Markarian 501
    if n in ["MRK501", "MARKARIAN501", "MKN501"]:
        return "Mkn501"
        

    # W Comae                                                                                            
    if n in ["W Comae", "W Com"]:
        return "WComae"

    # Bl Lacertae                                                                                        
    if n in ["BLLAC", "BLLACERTAE"]:
        return "BLLac"

    return name




def map_name_to_SwiftLC(name):
    """map common names to what is on the Swift LightCurves page for a selection of objects"""

    name=name.replace(" ","")  # all whitespace needs to be removed.
    n=name.upper()            # just for matching.

    # Markarian 421
    if n in ["MRK421", "MARKARIAN421", "MKN421"]:
        return "Mrk421"

    # Markarian 501
    if n in ["MRK501", "MARKARIAN501", "MKN501"]:
        return "Mrk501"

    # W Comae
    if n in ["WCOMAE", "WCOM"]:
        return "WCom"


    # Bl Lacertae
    if n in ["BLLAC", "BLLACERTAE"]:
        return "BLLacertae"
        
    return name 




def map_name_to_LATLC(name):
    """map common names to what is on the LAT LightCurves page for a selection of objects"""
    
    name=name.replace(" ","")  # all whitespace needs to be removed.
    n=name.upper()            # just for matching.

    # Markarian 421
    if n in ["MRK421", "MARKARIAN421", "MKN421"]:
        return "Mrk421"

    # Markarian 501
    if n in ["MRK501", "MARKARIAN501", "MKN501"]:
        return "Mrk501"

    # W Comae
    if n in ["W Comae", "W Com"]:
        return "WComae"

    # Bl Lacertae
    if n in ["BLLAC", "BLLACERTAE"]:
        return "BLLac"
        
    return name 






