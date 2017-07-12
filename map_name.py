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
                    "LAT_LC":"NGC 1275"})

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


    objects.append({"accepted":["4C31.03", "4C+31.03"],
                    "3FGL_ASSOC1":"4C +31.03",
                    "Swift_LC":"4C31.03",
                    "LAT_LC":"4C 31.03"})

    objects.append({"accepted":["MG1 J021114+1051", "CGRABSJ0211+1051"],
                    "3FGL_ASSOC1":"MG1 J021114+1051",
                    "Swift_LC":"CGRaBS J0211+1051",
                    "LAT_LC":"CGRaBS J0211+1051"})


    objects.append({"accepted":["B0218+357", "S30218+35"],
                    "3FGL_ASSOC1":"B0218+357",
                    "Swift_LC":"S30218+35",
                    "LAT_LC":"S30218+35"})


    objects.append({"accepted":["S3 0458-02", "NRAO190"],
                    "3FGL_ASSOC1":"S3 0458-02",
                    "Swift_LC":"PKS0458-02",
                    "LAT_LC":"PKS0458-02"})


    objects.append({"accepted":["TXS 0518+211", "VER0521+211", "VER J0521+211"],
                    "3FGL_ASSOC1":"TXS 0518+211",
                    "Swift_LC":"VER J0521+211",
                    "LAT_LC":"VER0521+211"})


    objects.append({"accepted":["CRATESJ0531-4827","PMN J0531-4827"],
                    "3FGL_ASSOC1":"PMN J0531-4827",
                    "Swift_LC":"PMN J0531-4827",
                    "LAT_LC":"CRATESJ0531-4827"})


    objects.append({"accepted":["0716+714","S5 0716+714"],
                    "3FGL_ASSOC1":"S5 0716+714",
                    "Swift_LC":"S5 0716+714",
                    "LAT_LC":"0716+714"})


    objects.append({"accepted":["4C14.23","4C +14.23"],
                    "3FGL_ASSOC1":"4C +14.23",
                    "Swift_LC":"",
                    "LAT_LC":"4C14.23"})


    objects.append({"accepted":["GB6 J0742+5444","BZUJ0742+5444"],
                    "3FGL_ASSOC1":"GB6 J0742+5444",
                    "Swift_LC":"",
                    "LAT_LC":"BZUJ0742+5444"})


    objects.append({"accepted":["OJ 248","0827+243", "QSO B0827+243"],
                    "3FGL_ASSOC1":"OJ 248",
                    "Swift_LC":"QSO B0827+243",
                    "LAT_LC":"0827+243"})


    objects.append({"accepted":["NVSS J090442-351423","3EGJ0903-3531"],
                    "3FGL_ASSOC1":"NVSS J090442-3514233",
                    "Swift_LC":"",
                    "LAT_LC":"3EGJ0903-3531"})


    objects.append({"accepted":["PKS 0906+01","PKSB0906+015"],
                    "3FGL_ASSOC1":"PKS 0906+01",
                    "Swift_LC":"PKS B0906+015",
                    "LAT_LC":"PKSB0906+015"})


    objects.append({"accepted":["PMNJ1038-5311","MRC 1036-529"],
                    "3FGL_ASSOC1":"MRC 1036-529",
                    "Swift_LC":"",
                    "LAT_LC":"PMNJ1038-5311"})


    objects.append({"accepted":["4C +21.35","PKSB1222+216","PKS 1222+216"],
                    "3FGL_ASSOC1":"4C +21.35",
                    "Swift_LC":"PKS 1222_216",
                    "LAT_LC":"PKSB1222+216"})


    objects.append({"accepted":["PKS B1424-418","PKS1424-41","PKS 1424-418"],
                    "3FGL_ASSOC1":"PKS B1424-418",
                    "Swift_LC":"PKS 1424-418",
                    "LAT_LC":"PKS1424-41"})


    objects.append({"accepted":["PKS 1510-08","PKS 1510-089","1510-089"],
                    "3FGL_ASSOC1":"PKS 1510-08",
                    "Swift_LC":"PKS 1510-089",
                    "LAT_LC":"1510-089"})


    objects.append({"accepted":["PKS 1622-29","PKS 1622-297","PKSB1622-297"],
                    "3FGL_ASSOC1":"PKS 1622-29",
                    "Swift_LC":"PKS 1622-297",
                    "LAT_LC":"PKSB1622-297"})

    objects.append({"accepted":["PMN J1626-2426"],
                    "3FGL_Source_Name":"3FGL J1626.2-2428c",
                    "3FGL_ASSOC1":"",
                    "Swift_LC":"PMN J1626-2426",
                    "LAT_LC":"PMN J1626-2426"})


    objects.append({"accepted":["4C +38.41","1JY 1633+38","1633+382"],
                    "3FGL_ASSOC1":"4C +38.41",
                    "Swift_LC":"1Jy 1633+38",
                    "LAT_LC":"1633+382"})


    objects.append({"accepted":["3C 345","0FGLJ1641.4+3939"],
                    "3FGL_ASSOC1":"3C 345",
                    "Swift_LC":"",
                    "LAT_LC":"0FGLJ1641.4+3939"})


    objects.append({"accepted":["TXS 1700+685","GB6 J1700+6830"],
                    "3FGL_ASSOC1":"TXS 1700+685",
                    "Swift_LC":"GB6 J1700+6830",
                    "LAT_LC":"GB6 J1700+6830"})


    objects.append({"accepted":["PMN J1717-5155","FERMIJ1717-5156"],
                    "3FGL_ASSOC1":"PMN J1717-5155",
                    "Swift_LC":"PMN J1717-5155",
                    "LAT_LC":"FermiJ1717-5156"})


    objects.append({"accepted":["PKS 1730-13","PKS 1730-130", "1730-130"],
                    "3FGL_ASSOC1":"PKS 1730-13",
                    "Swift_LC":"PKS 1730-130",
                    "LAT_LC":"1730-130"})


    objects.append({"accepted":["B2 1846+32A","CGRaBS J1848+3219"],
                    "3FGL_ASSOC1":"B2 1846+32A",
                    "Swift_LC":"CGRaBS J1848+3219",
                    "LAT_LC":"CGRaBS J1848+3219"})


    objects.append({"accepted":["S4 1849+67","CGRaBS J1849+6705"],
                    "3FGL_ASSOC1":"S4 1849+67",
                    "Swift_LC":"CGRaBS J1849+6705",
                    "LAT_LC":"CGRaBS J1849+6705"})

    objects.append({"accepted":["0235+164","PKS 0235+164","AO 0235+164"],
                    "3FGL_ASSOC1":"AO 0235+164",
                    "Swift_LC":"PKS 0235+164",
                    "LAT_LC":"0235+164"})

    objects.append({"accepted":["PKS0336-01","0336-019"],
                    "3FGL_ASSOC1":"PKS 0336-01",
                    "Swift_LC":"0336-019",
                    "LAT_LC":"PKS 0336-01"})


    objects.append({"accepted":["VER J0521+212","VER 0521+211","TXS 0518+211"],
                    "3FGL_ASSOC1":"TXS 0518+211",
                    "Swift_LC":"VER J0521+212",
                    "LAT_LC":"VER 0521+211"})

    objects.append({"accepted":["PKS 0727-115"," PKS 0727-11"],
                    "3FGL_ASSOC1":"PKS 0727-11",
                    "Swift_LC":"PKS 0727-115",
                    "LAT_LC":"PKS 0727-11"})

    objects.append({"accepted":["BZUJ0742+5444","GB6 J0742+5444"],
                    "3FGL_ASSOC1":"GB6 J0742+5444",
                    "Swift_LC":"",
                    "LAT_LC":"BZUJ0742+5444"})


    objects.append({"accepted":["S5 0836+71","0836+710"],
                    "3FGL_ASSOC1":"S5 0836+71",
                    "Swift_LC":"0836+710",
                    "LAT_LC":"S5 0836+71"})


    objects.append({"accepted":["3EG J0903-3531","NVSS J090442-351423"],
                    "3FGL_ASSOC1":"NVSS J090442-351423",
                    "Swift_LC":"",
                    "LAT_LC":"3EG J0903-3531"})


    objects.append({"accepted":["0FGL J0910.2-5044","J0910-5041"],
                    "3FGL_ASSOC1":"",
                    "Swift_LC":"J0910-5041",
                    "LAT_LC":"0FGL J0910.2-5044"})


    objects.append({"accepted":["S4 0954+65","0954+658"],
                    "3FGL_ASSOC1":"S4 0954+65",
                    "Swift_LC":"0954+658",
                    "LAT_LC":"S4 0954+65"})


    objects.append({"accepted":["S4 0954+65","0954+658"],
                    "3FGL_ASSOC1":"S4 0954+65",
                    "Swift_LC":"0954+658",
                    "LAT_LC":"S4 0954+65"})


    objects.append({"accepted":["PMN J1038-5311","MRC 1036-529"],
                    "3FGL_ASSOC1":"MRC 1036-529",
                    "Swift_LC":"",
                    "LAT_LC":"PMN J1038-5311"})


    objects.append({"accepted":["Ton 599","1156+295"],
                    "3FGL_ASSOC1":"Ton 599",
                    "Swift_LC":"1156+295",
                    "LAT_LC":"Ton 599"})


    objects.append({"accepted":["PKS B1222+216","4C +21.35", "PKS 1222+216"],
                    "3FGL_ASSOC1":"4C +21.35",
                    "Swift_LC":"PKS 1222+216",
                    "LAT_LC":"PKS B1222+216 "})


    objects.append({"accepted":["OP 313","1308+326"],
                    "3FGL_ASSOC1":"OP 313",
                    "Swift_LC":"1308+326",
                    "LAT_LC":"OP 313"})


    objects.append({"accepted":["1406-076","1Jy 1406-076","PKS B1406-076"],
                    "3FGL_ASSOC1":"PKS B1406-076",
                    "Swift_LC":"1Jy 1406-076",
                    "LAT_LC":"1406-076"})


    objects.append({"accepted":["AP Librae","AP Lib"],
                    "3FGL_ASSOC1":"AP Librae",
                    "Swift_LC":"",
                    "LAT_LC":"AP Lib"})


    objects.append({"accepted":["0FGLJ1641.4+3939","3C 345"],
                    "3FGL_ASSOC1":"3C 345",
                    "Swift_LC":"3C 345",
                    "LAT_LC":"0FGLJ1641.4+3939"})


    objects.append({"accepted":["PKS 1830-211","PKS 1830-21"],
                    "3FGL_ASSOC1":"PKS 1830-211",
                    "Swift_LC":"PKS 1830-21",
                    "LAT_LC":"PKS 1830-211"})

    objects.append({"accepted":["PKS B1908-201","PKS 1908-201"],
                    "3FGL_ASSOC1":"PKS B1908-201",
                    "Swift_LC":"PKS 1908-201",
                    "LAT_LC":"PKS B1908-201"})


    objects.append({"accepted":["S5 2007+77"],
                    "3FGL_ASSOC1":"S5 2007+77",
                    "Swift_LC":"s5 2007+77",
                    "LAT_LC":"S5 2007+77"})

    objects.append({"accepted":["OX 169","S3 2141+17"],
                    "3FGL_ASSOC1":"OX 169",
                    "Swift_LC":"S3 2141+17",
                    "LAT_LC":"OX 169"})

    objects.append({"accepted":["3C 345","0FGL J1641.4+3939"],
                    "3FGL_ASSOC1":"3C345",
                    "Swift_LC":"3C345",
                    "LAT_LC":"0FGL J1641.4+3939"})








# 4C+50.11 not in 3FGL!
# 3C120 not in 3FGL!
# PKS0438-43 not in 3FGL!
# B20748+33 not in 3FGL!
# 0FGLJ0910.2-5044 not in 3FGL!
# PKS1824-582 not in 3FGL!
# B21846+32B not in 3FGL! but same as B2 1846+32A/CGRaBS J1848+3219 ?
# PKS2136-642 not in 3FGL!
# PKS0438-43 not in 3FGL!
# 0FGLJ0910.2-5044 not in 3FGL!
# PKS1824-582 not in 3FGL!
# PKS2136-642 not in 3FGL!
# PKSB2258-022 not in 3FGL!



    n=name.upper().replace(" ","")

    
    for object in objects:
        if n in object["accepted"]:
            return object[format].replace(" ","")
    
    return name.replace(" ","")



