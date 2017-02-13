def map_name(name, format="3FGL_ASSOC1"):
    """map common names of a subset of objects to associated catalogue/web site
    Allowed formats are "3FGL_ASSOC1", "Swift_LC", "LAT_LC" """

    if format not in ["3FGL_ASSOC1", "Swift_LC", "LAT_LC"]:
        print("Format must be one of", "3FGL_ASSOC1", "Swift_LC", "LAT_LC") 

    objects=[]

    objects.append({"accepted":["MRK421", "MKN421", "MARKARIAN421"],
                    "3FGL_ASSOC1":"Mkn421",
                    "Swift_LC":"Mrk421",
                    "LAT_LC":"Mrk421"})

    objects.append({"accepted":["MRK501", "MARKARIAN501", "MKN501"],
                    "3FGL_ASSOC1":"Mkn501",
                    "Swift_LC":"Mrk501",
                    "LAT_LC":"Mrk501"})

    objects.append({"accepted":["WCOMAE", "WCOM"],
                    "3FGL_ASSOC1":"WComae",
                    "Swift_LC":"WCom",
                    "LAT_LC":"WComae"})

    objects.append({"accepted":["WCOMAE", "WCOM"],
                    "3FGL_ASSOC1":"WComae",
                    "Swift_LC":"WCom",
                    "LAT_LC":"WComae"})

    objects.append({"accepted":["BLLAC", "BLLACERTAE"],
                    "3FGL_ASSOC1":"BLLac",
                    "Swift_LC":"BLLacertae",
                    "LAT_LC":"BLLac"})

    objects.append({"accepted":["NGC1275", "3C84"],
                    "3FGL_ASSOC1":"NGC 1275",
                    "Swift_LC":"3C84",
                    "LAT_LC":"NGC1275"})


    n=name.upper().replace(" ","")

    
    for object in objects:
        if n in object["accepted"]:
            return object[format]
    
    return name

