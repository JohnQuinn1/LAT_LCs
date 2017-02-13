def map_name(name, format="3FGL_ASSOC1"):
    """map common names of a subset of objects to associated catalogue/web site
    Allowed formats are "3FGL_ASSOC1", "Swift_LC", "LAT_LC" """

    # NED does not give 3FGL names but can use a NED query in the 3FGL Browse Table online!

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

    objects.append({"accepted":["S41144+40", "B21144+40"],
                    "3FGL_ASSOC1":"S4 1144+40",
                    "Swift_LC":"B2 1144+40",
                    "LAT_LC":"B2 1144+40"})

    objects.append({"accepted":["AT20GJ112319-641735", "PMNJ1123-6417"],
                    "3FGL_ASSOC1":"AT20GJ112319-641735",
                    "Swift_LC":"PMNJ1123-6417",
                    "LAT_LC":"PMNJ1123-6417"})


    objects.append({"accepted":["1150+497", "SBS 1150+497", "OM 484"],
                    "3FGL_ASSOC1":"OM 484",
                    "Swift_LC":"SBS 1150+497",
                    "LAT_LC":"1150+497"})




    n=name.upper().replace(" ","")

    
    for object in objects:
        if n in object["accepted"]:
            return object[format].replace(" ","")
    
    return name.replace(" ","")



