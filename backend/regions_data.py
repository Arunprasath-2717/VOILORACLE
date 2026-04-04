"""
Kronaxis — Hierarchical Region Data (30 Countries)
"""

HIERARCHICAL_REGION_MAP = [
    {
        "id": "ind", "name": "India", "code": "IN",
        "keywords": ["india", "new delhi", "bharat", "modi", "indian", "niti aayog", "lok sabha", "rajya sabha", "supreme court of india", "rbi", "sensex", "nifty", "isro", "drdo"],
        "states": [
            {"id": "in_tn", "name": "Tamil Nadu", "keywords": ["tamil nadu", "tamilnadu", "chennai", "madras", "stalin", "dravidian", "dmk", "aiadmk", "tn govt", "tamil", "kollywood"],
             "districts": [
                 {"id": "in_tn_che", "name": "Chennai", "keywords": ["chennai", "madras", "tambaram", "t nagar", "marina beach", "chennai port", "adyar", "anna nagar"]},
                 {"id": "in_tn_mdu", "name": "Madurai", "keywords": ["madurai", "meenakshi amman", "vaigai"]},
                 {"id": "in_tn_cbe", "name": "Coimbatore", "keywords": ["coimbatore", "kovai", "tiruppur", "pollachi"]},
                 {"id": "in_tn_try", "name": "Trichy", "keywords": ["trichy", "tiruchirappalli", "srirangam", "rockfort"]},
                 {"id": "in_tn_slm", "name": "Salem", "keywords": ["salem", "yercaud", "mettur"]},
                 {"id": "in_tn_tnj", "name": "Thanjavur", "keywords": ["thanjavur", "tanjore", "big temple", "cauvery delta"]},
                 {"id": "in_tn_tvl", "name": "Tirunelveli", "keywords": ["tirunelveli", "nellai", "tenkasi"]},
                 {"id": "in_tn_vlr", "name": "Vellore", "keywords": ["vellore", "cmi hospital", "ranipet"]},
                 {"id": "in_tn_erd", "name": "Erode", "keywords": ["erode", "bhavani", "gobichettipalayam"]},
                 {"id": "in_tn_knc", "name": "Kancheepuram", "keywords": ["kancheepuram", "kanchipuram", "mahabalipuram", "sriperumbudur"]}
             ]},
            {"id": "in_mh", "name": "Maharashtra", "keywords": ["maharashtra", "mumbai", "bombay", "pune", "nagpur"],
             "districts": [{"id": "in_mh_mum", "name": "Mumbai", "keywords": ["mumbai", "bombay", "bse", "nse"]},
                           {"id": "in_mh_pun", "name": "Pune", "keywords": ["pune"]},
                           {"id": "in_mh_nag", "name": "Nagpur", "keywords": ["nagpur"]}]},
            {"id": "in_ka", "name": "Karnataka", "keywords": ["karnataka", "bengaluru", "bangalore", "mysuru"],
             "districts": [{"id": "in_ka_blr", "name": "Bengaluru", "keywords": ["bengaluru", "bangalore", "whitefield", "electronic city"]},
                           {"id": "in_ka_mys", "name": "Mysuru", "keywords": ["mysuru", "mysore"]}]},
            {"id": "in_dl", "name": "Delhi", "keywords": ["delhi", "new delhi", "parliament", "india gate"],
             "districts": [{"id": "in_dl_nd", "name": "New Delhi", "keywords": ["new delhi", "connaught place", "rashtrapati bhavan"]}]},
            {"id": "in_up", "name": "Uttar Pradesh", "keywords": ["uttar pradesh", "lucknow", "varanasi", "noida"],
             "districts": [{"id": "in_up_lko", "name": "Lucknow", "keywords": ["lucknow"]},
                           {"id": "in_up_vrn", "name": "Varanasi", "keywords": ["varanasi", "kashi"]},
                           {"id": "in_up_nda", "name": "Noida", "keywords": ["noida", "greater noida"]}]},
            {"id": "in_ts", "name": "Telangana", "keywords": ["telangana", "hyderabad", "secunderabad"],
             "districts": [{"id": "in_ts_hyd", "name": "Hyderabad", "keywords": ["hyderabad", "hitec city", "cyberabad"]}]},
            {"id": "in_ap", "name": "Andhra Pradesh", "keywords": ["andhra pradesh", "amaravati", "visakhapatnam"],
             "districts": [{"id": "in_ap_viz", "name": "Visakhapatnam", "keywords": ["visakhapatnam", "vizag"]},
                           {"id": "in_ap_tpt", "name": "Tirupati", "keywords": ["tirupati", "tirumala"]}]},
            {"id": "in_gj", "name": "Gujarat", "keywords": ["gujarat", "ahmedabad", "gandhinagar", "surat"],
             "districts": [{"id": "in_gj_ahm", "name": "Ahmedabad", "keywords": ["ahmedabad"]},
                           {"id": "in_gj_sur", "name": "Surat", "keywords": ["surat"]}]},
            {"id": "in_kl", "name": "Kerala", "keywords": ["kerala", "kochi", "thiruvananthapuram", "kozhikode"],
             "districts": [{"id": "in_kl_kch", "name": "Kochi", "keywords": ["kochi", "cochin"]},
                           {"id": "in_kl_tvm", "name": "Thiruvananthapuram", "keywords": ["thiruvananthapuram", "trivandrum"]}]},
            {"id": "in_wb", "name": "West Bengal", "keywords": ["west bengal", "kolkata", "calcutta"],
             "districts": [{"id": "in_wb_kol", "name": "Kolkata", "keywords": ["kolkata", "calcutta"]}]},
            {"id": "in_rj", "name": "Rajasthan", "keywords": ["rajasthan", "jaipur", "jodhpur", "udaipur"],
             "districts": [{"id": "in_rj_jpr", "name": "Jaipur", "keywords": ["jaipur"]}]},
            {"id": "in_pb", "name": "Punjab", "keywords": ["punjab", "chandigarh", "amritsar", "ludhiana"],
             "districts": [{"id": "in_pb_asr", "name": "Amritsar", "keywords": ["amritsar", "golden temple"]}]},
            {"id": "in_br", "name": "Bihar", "keywords": ["bihar", "patna", "gaya"],
             "districts": [{"id": "in_br_pat", "name": "Patna", "keywords": ["patna"]}]},
            {"id": "in_mp", "name": "Madhya Pradesh", "keywords": ["madhya pradesh", "bhopal", "indore"],
             "districts": [{"id": "in_mp_bho", "name": "Bhopal", "keywords": ["bhopal"]}]},
            {"id": "in_od", "name": "Odisha", "keywords": ["odisha", "orissa", "bhubaneswar"],
             "districts": [{"id": "in_od_bbs", "name": "Bhubaneswar", "keywords": ["bhubaneswar"]}]},
        ]
    },
    {
        "id": "usa", "name": "United States", "code": "US",
        "keywords": ["united states", "usa", "america", "washington dc", "white house", "pentagon"],
        "states": [
            {"id": "us_ca", "name": "California", "keywords": ["california", "los angeles", "silicon valley", "sacramento"],
             "districts": [{"id": "us_ca_sf", "name": "San Francisco", "keywords": ["san francisco", "bay area"]},
                           {"id": "us_ca_la", "name": "Los Angeles", "keywords": ["los angeles", "hollywood"]}]},
            {"id": "us_ny", "name": "New York", "keywords": ["new york", "nyc", "manhattan"],
             "districts": [{"id": "us_ny_nyc", "name": "New York City", "keywords": ["nyc", "manhattan", "wall street"]},
                           {"id": "us_ny_buf", "name": "Buffalo", "keywords": ["buffalo"]}]},
            {"id": "us_tx", "name": "Texas", "keywords": ["texas", "houston", "dallas", "austin"],
             "districts": [{"id": "us_tx_hou", "name": "Houston", "keywords": ["houston"]},
                           {"id": "us_tx_dal", "name": "Dallas", "keywords": ["dallas", "fort worth"]}]},
            {"id": "us_fl", "name": "Florida", "keywords": ["florida", "miami", "orlando", "tampa"],
             "districts": [{"id": "us_fl_mia", "name": "Miami", "keywords": ["miami"]},
                           {"id": "us_fl_orl", "name": "Orlando", "keywords": ["orlando"]}]},
            {"id": "us_il", "name": "Illinois", "keywords": ["illinois", "chicago"],
             "districts": [{"id": "us_il_chi", "name": "Chicago", "keywords": ["chicago"]}]},
            {"id": "us_wa", "name": "Washington", "keywords": ["washington state", "seattle"],
             "districts": [{"id": "us_wa_sea", "name": "Seattle", "keywords": ["seattle"]}]},
            {"id": "us_ma", "name": "Massachusetts", "keywords": ["massachusetts", "boston"],
             "districts": [{"id": "us_ma_bos", "name": "Boston", "keywords": ["boston"]}]},
        ]
    },
    {
        "id": "chn", "name": "China", "code": "CN",
        "keywords": ["china", "prc", "chinese", "xi jinping"],
        "states": [
            {"id": "cn_gd", "name": "Guangdong", "keywords": ["guangdong", "shenzhen", "guangzhou"],
             "districts": [{"id": "cn_gd_sz", "name": "Shenzhen", "keywords": ["shenzhen"]},
                           {"id": "cn_gd_gz", "name": "Guangzhou", "keywords": ["guangzhou"]}]},
            {"id": "cn_bj", "name": "Beijing", "keywords": ["beijing"],
             "districts": [{"id": "cn_bj_cy", "name": "Chaoyang", "keywords": ["chaoyang"]}]},
            {"id": "cn_sh", "name": "Shanghai", "keywords": ["shanghai"],
             "districts": [{"id": "cn_sh_pd", "name": "Pudong", "keywords": ["pudong"]}]},
            {"id": "cn_zj", "name": "Zhejiang", "keywords": ["zhejiang", "hangzhou"],
             "districts": [{"id": "cn_zj_hz", "name": "Hangzhou", "keywords": ["hangzhou"]}]},
            {"id": "cn_js", "name": "Jiangsu", "keywords": ["jiangsu", "nanjing"],
             "districts": [{"id": "cn_js_nj", "name": "Nanjing", "keywords": ["nanjing"]}]},
            {"id": "cn_sc", "name": "Sichuan", "keywords": ["sichuan", "chengdu"],
             "districts": [{"id": "cn_sc_cd", "name": "Chengdu", "keywords": ["chengdu"]}]},
            {"id": "cn_hk", "name": "Hong Kong", "keywords": ["hong kong"],
             "districts": [{"id": "cn_hk_ct", "name": "Central", "keywords": ["hong kong central"]}]},
        ]
    },
    {
        "id": "jpn", "name": "Japan", "code": "JP",
        "keywords": ["japan", "japanese", "tokyo"],
        "states": [
            {"id": "jp_tk", "name": "Tokyo", "keywords": ["tokyo"],
             "districts": [{"id": "jp_tk_shb", "name": "Shibuya", "keywords": ["shibuya"]}]},
            {"id": "jp_os", "name": "Osaka", "keywords": ["osaka"],
             "districts": [{"id": "jp_os_ct", "name": "Osaka City", "keywords": ["osaka city"]}]},
            {"id": "jp_ky", "name": "Kyoto", "keywords": ["kyoto"],
             "districts": [{"id": "jp_ky_ct", "name": "Kyoto City", "keywords": ["kyoto city"]}]},
            {"id": "jp_kn", "name": "Kanagawa", "keywords": ["kanagawa", "yokohama"],
             "districts": [{"id": "jp_kn_yh", "name": "Yokohama", "keywords": ["yokohama"]}]},
            {"id": "jp_hk", "name": "Hokkaido", "keywords": ["hokkaido", "sapporo"],
             "districts": [{"id": "jp_hk_sp", "name": "Sapporo", "keywords": ["sapporo"]}]},
            {"id": "jp_ai", "name": "Aichi", "keywords": ["aichi", "nagoya"],
             "districts": [{"id": "jp_ai_ng", "name": "Nagoya", "keywords": ["nagoya"]}]},
        ]
    },
    {
        "id": "gbr", "name": "United Kingdom", "code": "GB",
        "keywords": ["united kingdom", "uk ", "britain", "british"],
        "states": [
            {"id": "gb_en", "name": "England", "keywords": ["england", "london", "manchester", "birmingham"],
             "districts": [{"id": "gb_en_ldn", "name": "London", "keywords": ["london"]},
                           {"id": "gb_en_man", "name": "Manchester", "keywords": ["manchester"]}]},
            {"id": "gb_sc", "name": "Scotland", "keywords": ["scotland", "edinburgh", "glasgow"],
             "districts": [{"id": "gb_sc_edi", "name": "Edinburgh", "keywords": ["edinburgh"]}]},
            {"id": "gb_wa", "name": "Wales", "keywords": ["wales", "cardiff"],
             "districts": [{"id": "gb_wa_car", "name": "Cardiff", "keywords": ["cardiff"]}]},
            {"id": "gb_ni", "name": "Northern Ireland", "keywords": ["northern ireland", "belfast"],
             "districts": [{"id": "gb_ni_bel", "name": "Belfast", "keywords": ["belfast"]}]},
        ]
    },
    {
        "id": "deu", "name": "Germany", "code": "DE",
        "keywords": ["germany", "german", "berlin", "bundeswehr"],
        "states": [
            {"id": "de_by", "name": "Bavaria", "keywords": ["bavaria", "munich", "bayern"],
             "districts": [{"id": "de_by_muc", "name": "Munich", "keywords": ["munich"]}]},
            {"id": "de_nw", "name": "North Rhine-Westphalia", "keywords": ["north rhine-westphalia", "cologne", "dusseldorf"],
             "districts": [{"id": "de_nw_col", "name": "Cologne", "keywords": ["cologne"]}]},
            {"id": "de_bw", "name": "Baden-Württemberg", "keywords": ["baden-württemberg", "stuttgart"],
             "districts": [{"id": "de_bw_stg", "name": "Stuttgart", "keywords": ["stuttgart"]}]},
            {"id": "de_he", "name": "Hesse", "keywords": ["hesse", "frankfurt"],
             "districts": [{"id": "de_he_fra", "name": "Frankfurt", "keywords": ["frankfurt"]}]},
            {"id": "de_be", "name": "Berlin", "keywords": ["berlin"],
             "districts": [{"id": "de_be_ct", "name": "Berlin Central", "keywords": ["berlin central"]}]},
        ]
    },
    {
        "id": "can", "name": "Canada", "code": "CA",
        "keywords": ["canada", "canadian", "ottawa"],
        "states": [
            {"id": "ca_on", "name": "Ontario", "keywords": ["ontario", "toronto"],
             "districts": [{"id": "ca_on_tor", "name": "Toronto", "keywords": ["toronto"]}]},
            {"id": "ca_qc", "name": "Quebec", "keywords": ["quebec", "montreal"],
             "districts": [{"id": "ca_qc_mtl", "name": "Montreal", "keywords": ["montreal"]}]},
            {"id": "ca_bc", "name": "British Columbia", "keywords": ["british columbia", "vancouver"],
             "districts": [{"id": "ca_bc_van", "name": "Vancouver", "keywords": ["vancouver"]}]},
            {"id": "ca_ab", "name": "Alberta", "keywords": ["alberta", "calgary", "edmonton"],
             "districts": [{"id": "ca_ab_cal", "name": "Calgary", "keywords": ["calgary"]}]},
            {"id": "ca_mb", "name": "Manitoba", "keywords": ["manitoba", "winnipeg"],
             "districts": [{"id": "ca_mb_win", "name": "Winnipeg", "keywords": ["winnipeg"]}]},
        ]
    },
    {
        "id": "aus", "name": "Australia", "code": "AU",
        "keywords": ["australia", "australian", "canberra"],
        "states": [
            {"id": "au_nsw", "name": "New South Wales", "keywords": ["new south wales", "sydney"],
             "districts": [{"id": "au_nsw_syd", "name": "Sydney", "keywords": ["sydney"]}]},
            {"id": "au_vic", "name": "Victoria", "keywords": ["victoria", "melbourne"],
             "districts": [{"id": "au_vic_mel", "name": "Melbourne", "keywords": ["melbourne"]}]},
            {"id": "au_qld", "name": "Queensland", "keywords": ["queensland", "brisbane"],
             "districts": [{"id": "au_qld_bri", "name": "Brisbane", "keywords": ["brisbane"]}]},
            {"id": "au_wa", "name": "Western Australia", "keywords": ["western australia", "perth"],
             "districts": [{"id": "au_wa_per", "name": "Perth", "keywords": ["perth"]}]},
            {"id": "au_sa", "name": "South Australia", "keywords": ["south australia", "adelaide"],
             "districts": [{"id": "au_sa_ade", "name": "Adelaide", "keywords": ["adelaide"]}]},
        ]
    },
    {
        "id": "fra", "name": "France", "code": "FR",
        "keywords": ["france", "french", "paris", "macron"],
        "states": [
            {"id": "fr_idf", "name": "Île-de-France", "keywords": ["ile-de-france", "paris"],
             "districts": [{"id": "fr_idf_par", "name": "Paris", "keywords": ["paris"]}]},
            {"id": "fr_pac", "name": "Provence-Alpes-Côte d'Azur", "keywords": ["provence", "marseille", "nice", "cote d'azur"],
             "districts": [{"id": "fr_pac_mar", "name": "Marseille", "keywords": ["marseille"]}]},
            {"id": "fr_nor", "name": "Normandy", "keywords": ["normandy", "rouen"],
             "districts": [{"id": "fr_nor_rou", "name": "Rouen", "keywords": ["rouen"]}]},
            {"id": "fr_occ", "name": "Occitanie", "keywords": ["occitanie", "toulouse"],
             "districts": [{"id": "fr_occ_tou", "name": "Toulouse", "keywords": ["toulouse"]}]},
            {"id": "fr_ara", "name": "Auvergne-Rhône-Alpes", "keywords": ["auvergne", "rhone-alpes", "lyon"],
             "districts": [{"id": "fr_ara_lyo", "name": "Lyon", "keywords": ["lyon"]}]},
        ]
    },
    {
        "id": "bra", "name": "Brazil", "code": "BR",
        "keywords": ["brazil", "brazilian", "brasilia"],
        "states": [
            {"id": "br_sp", "name": "São Paulo", "keywords": ["sao paulo", "são paulo"],
             "districts": [{"id": "br_sp_ct", "name": "São Paulo City", "keywords": ["sao paulo city"]}]},
            {"id": "br_rj", "name": "Rio de Janeiro", "keywords": ["rio de janeiro", "rio"],
             "districts": [{"id": "br_rj_ct", "name": "Rio City", "keywords": ["rio city", "copacabana"]}]},
            {"id": "br_mg", "name": "Minas Gerais", "keywords": ["minas gerais", "belo horizonte"],
             "districts": [{"id": "br_mg_bh", "name": "Belo Horizonte", "keywords": ["belo horizonte"]}]},
            {"id": "br_ba", "name": "Bahia", "keywords": ["bahia", "salvador"],
             "districts": [{"id": "br_ba_sal", "name": "Salvador", "keywords": ["salvador"]}]},
            {"id": "br_pr", "name": "Paraná", "keywords": ["parana", "paraná", "curitiba"],
             "districts": [{"id": "br_pr_cur", "name": "Curitiba", "keywords": ["curitiba"]}]},
        ]
    },
    {
        "id": "rus", "name": "Russia", "code": "RU",
        "keywords": ["russia", "russian", "kremlin", "moscow", "putin"],
        "states": [
            {"id": "ru_mos", "name": "Moscow", "keywords": ["moscow", "kremlin"],
             "districts": [{"id": "ru_mos_ct", "name": "Central Moscow", "keywords": ["moscow central"]}]},
            {"id": "ru_spb", "name": "Saint Petersburg", "keywords": ["saint petersburg", "st petersburg"],
             "districts": [{"id": "ru_spb_ct", "name": "St Petersburg City", "keywords": ["st petersburg city"]}]},
            {"id": "ru_tat", "name": "Tatarstan", "keywords": ["tatarstan", "kazan"],
             "districts": [{"id": "ru_tat_kaz", "name": "Kazan", "keywords": ["kazan"]}]},
            {"id": "ru_kra", "name": "Krasnodar Krai", "keywords": ["krasnodar", "sochi"],
             "districts": [{"id": "ru_kra_soc", "name": "Sochi", "keywords": ["sochi"]}]},
            {"id": "ru_sib", "name": "Siberia", "keywords": ["siberia", "novosibirsk"],
             "districts": [{"id": "ru_sib_nov", "name": "Novosibirsk", "keywords": ["novosibirsk"]}]},
        ]
    },
    {
        "id": "kor", "name": "South Korea", "code": "KR",
        "keywords": ["south korea", "korean", "seoul"],
        "states": [
            {"id": "kr_sel", "name": "Seoul", "keywords": ["seoul"],
             "districts": [{"id": "kr_sel_gn", "name": "Gangnam", "keywords": ["gangnam"]}]},
            {"id": "kr_bus", "name": "Busan", "keywords": ["busan"],
             "districts": [{"id": "kr_bus_ct", "name": "Busan City", "keywords": ["busan city"]}]},
            {"id": "kr_icn", "name": "Incheon", "keywords": ["incheon"],
             "districts": [{"id": "kr_icn_ct", "name": "Incheon City", "keywords": ["incheon city"]}]},
            {"id": "kr_ggp", "name": "Gyeonggi Province", "keywords": ["gyeonggi", "suwon"],
             "districts": [{"id": "kr_ggp_swn", "name": "Suwon", "keywords": ["suwon"]}]},
            {"id": "kr_dae", "name": "Daegu", "keywords": ["daegu"],
             "districts": [{"id": "kr_dae_ct", "name": "Daegu City", "keywords": ["daegu city"]}]},
        ]
    },
    {
        "id": "ita", "name": "Italy", "code": "IT",
        "keywords": ["italy", "italian", "rome", "roma"],
        "states": [
            {"id": "it_lom", "name": "Lombardy", "keywords": ["lombardy", "milan", "milano"],
             "districts": [{"id": "it_lom_mil", "name": "Milan", "keywords": ["milan", "milano"]}]},
            {"id": "it_laz", "name": "Lazio", "keywords": ["lazio", "rome", "roma"],
             "districts": [{"id": "it_laz_rom", "name": "Rome", "keywords": ["rome", "roma"]}]},
            {"id": "it_ven", "name": "Veneto", "keywords": ["veneto", "venice", "venezia"],
             "districts": [{"id": "it_ven_ven", "name": "Venice", "keywords": ["venice", "venezia"]}]},
            {"id": "it_tos", "name": "Tuscany", "keywords": ["tuscany", "florence", "firenze"],
             "districts": [{"id": "it_tos_flo", "name": "Florence", "keywords": ["florence", "firenze"]}]},
            {"id": "it_sic", "name": "Sicily", "keywords": ["sicily", "palermo"],
             "districts": [{"id": "it_sic_pal", "name": "Palermo", "keywords": ["palermo"]}]},
        ]
    },
    {
        "id": "uae", "name": "United Arab Emirates", "code": "AE",
        "keywords": ["uae", "emirates", "united arab emirates"],
        "states": [
            {"id": "ae_dxb", "name": "Dubai", "keywords": ["dubai"],
             "districts": [{"id": "ae_dxb_ct", "name": "Dubai City", "keywords": ["dubai city", "burj"]}]},
            {"id": "ae_auh", "name": "Abu Dhabi", "keywords": ["abu dhabi"],
             "districts": [{"id": "ae_auh_ct", "name": "Abu Dhabi City", "keywords": ["abu dhabi city"]}]},
            {"id": "ae_shj", "name": "Sharjah", "keywords": ["sharjah"],
             "districts": [{"id": "ae_shj_ct", "name": "Sharjah City", "keywords": ["sharjah city"]}]},
            {"id": "ae_ajm", "name": "Ajman", "keywords": ["ajman"],
             "districts": [{"id": "ae_ajm_ct", "name": "Ajman City", "keywords": ["ajman city"]}]},
            {"id": "ae_rak", "name": "Ras Al Khaimah", "keywords": ["ras al khaimah"],
             "districts": [{"id": "ae_rak_ct", "name": "RAK City", "keywords": ["ras al khaimah city"]}]},
        ]
    },
    {
        "id": "zaf", "name": "South Africa", "code": "ZA",
        "keywords": ["south africa", "south african", "pretoria", "johannesburg"],
        "states": [
            {"id": "za_gau", "name": "Gauteng", "keywords": ["gauteng", "johannesburg", "pretoria"],
             "districts": [{"id": "za_gau_jhb", "name": "Johannesburg", "keywords": ["johannesburg"]}]},
            {"id": "za_wc", "name": "Western Cape", "keywords": ["western cape", "cape town"],
             "districts": [{"id": "za_wc_cpt", "name": "Cape Town", "keywords": ["cape town"]}]},
            {"id": "za_kzn", "name": "KwaZulu-Natal", "keywords": ["kwazulu-natal", "durban"],
             "districts": [{"id": "za_kzn_dur", "name": "Durban", "keywords": ["durban"]}]},
            {"id": "za_ec", "name": "Eastern Cape", "keywords": ["eastern cape", "port elizabeth"],
             "districts": [{"id": "za_ec_pe", "name": "Port Elizabeth", "keywords": ["port elizabeth"]}]},
            {"id": "za_fs", "name": "Free State", "keywords": ["free state", "bloemfontein"],
             "districts": [{"id": "za_fs_blm", "name": "Bloemfontein", "keywords": ["bloemfontein"]}]},
        ]
    },
    {
        "id": "mex", "name": "Mexico", "code": "MX",
        "keywords": ["mexico", "mexican"],
        "states": [
            {"id": "mx_cdmx", "name": "Mexico City", "keywords": ["mexico city", "cdmx"],
             "districts": [{"id": "mx_cdmx_ct", "name": "CDMX Central", "keywords": ["cdmx central"]}]},
            {"id": "mx_jal", "name": "Jalisco", "keywords": ["jalisco", "guadalajara"],
             "districts": [{"id": "mx_jal_gdl", "name": "Guadalajara", "keywords": ["guadalajara"]}]},
            {"id": "mx_nl", "name": "Nuevo León", "keywords": ["nuevo leon", "monterrey"],
             "districts": [{"id": "mx_nl_mty", "name": "Monterrey", "keywords": ["monterrey"]}]},
            {"id": "mx_bc", "name": "Baja California", "keywords": ["baja california", "tijuana"],
             "districts": [{"id": "mx_bc_tij", "name": "Tijuana", "keywords": ["tijuana"]}]},
            {"id": "mx_yuc", "name": "Yucatán", "keywords": ["yucatan", "merida"],
             "districts": [{"id": "mx_yuc_mer", "name": "Merida", "keywords": ["merida"]}]},
        ]
    },
    {
        "id": "esp", "name": "Spain", "code": "ES",
        "keywords": ["spain", "spanish", "madrid"],
        "states": [
            {"id": "es_cat", "name": "Catalonia", "keywords": ["catalonia", "barcelona", "catalunya"],
             "districts": [{"id": "es_cat_bcn", "name": "Barcelona", "keywords": ["barcelona"]}]},
            {"id": "es_mad", "name": "Madrid", "keywords": ["madrid"],
             "districts": [{"id": "es_mad_ct", "name": "Madrid City", "keywords": ["madrid city"]}]},
            {"id": "es_and", "name": "Andalusia", "keywords": ["andalusia", "seville", "malaga"],
             "districts": [{"id": "es_and_sev", "name": "Seville", "keywords": ["seville"]}]},
            {"id": "es_val", "name": "Valencia", "keywords": ["valencia"],
             "districts": [{"id": "es_val_ct", "name": "Valencia City", "keywords": ["valencia city"]}]},
            {"id": "es_bas", "name": "Basque Country", "keywords": ["basque", "bilbao"],
             "districts": [{"id": "es_bas_bil", "name": "Bilbao", "keywords": ["bilbao"]}]},
        ]
    },
    {
        "id": "idn", "name": "Indonesia", "code": "ID",
        "keywords": ["indonesia", "indonesian", "jakarta"],
        "states": [
            {"id": "id_jav", "name": "Java", "keywords": ["java", "jakarta", "surabaya"],
             "districts": [{"id": "id_jav_jkt", "name": "Jakarta", "keywords": ["jakarta"]}]},
            {"id": "id_bal", "name": "Bali", "keywords": ["bali", "denpasar"],
             "districts": [{"id": "id_bal_den", "name": "Denpasar", "keywords": ["denpasar"]}]},
            {"id": "id_sum", "name": "Sumatra", "keywords": ["sumatra", "medan"],
             "districts": [{"id": "id_sum_med", "name": "Medan", "keywords": ["medan"]}]},
            {"id": "id_kal", "name": "Kalimantan", "keywords": ["kalimantan", "borneo"],
             "districts": [{"id": "id_kal_ct", "name": "Balikpapan", "keywords": ["balikpapan"]}]},
            {"id": "id_sul", "name": "Sulawesi", "keywords": ["sulawesi", "makassar"],
             "districts": [{"id": "id_sul_mak", "name": "Makassar", "keywords": ["makassar"]}]},
        ]
    },
    {
        "id": "sau", "name": "Saudi Arabia", "code": "SA",
        "keywords": ["saudi arabia", "saudi", "riyadh"],
        "states": [
            {"id": "sa_riy", "name": "Riyadh", "keywords": ["riyadh"],
             "districts": [{"id": "sa_riy_ct", "name": "Riyadh City", "keywords": ["riyadh city"]}]},
            {"id": "sa_mec", "name": "Mecca", "keywords": ["mecca", "makkah"],
             "districts": [{"id": "sa_mec_ct", "name": "Makkah City", "keywords": ["makkah city"]}]},
            {"id": "sa_med", "name": "Medina", "keywords": ["medina", "madinah"],
             "districts": [{"id": "sa_med_ct", "name": "Madinah City", "keywords": ["madinah city"]}]},
            {"id": "sa_ep", "name": "Eastern Province", "keywords": ["eastern province", "dammam", "dhahran"],
             "districts": [{"id": "sa_ep_dam", "name": "Dammam", "keywords": ["dammam"]}]},
            {"id": "sa_jed", "name": "Jeddah", "keywords": ["jeddah", "jidda"],
             "districts": [{"id": "sa_jed_ct", "name": "Jeddah City", "keywords": ["jeddah city"]}]},
        ]
    },
    {
        "id": "tur", "name": "Turkey", "code": "TR",
        "keywords": ["turkey", "turkish", "turkiye", "ankara", "erdogan"],
        "states": [
            {"id": "tr_ist", "name": "Istanbul", "keywords": ["istanbul"],
             "districts": [{"id": "tr_ist_ct", "name": "Istanbul City", "keywords": ["istanbul city"]}]},
            {"id": "tr_ank", "name": "Ankara", "keywords": ["ankara"],
             "districts": [{"id": "tr_ank_ct", "name": "Ankara City", "keywords": ["ankara city"]}]},
            {"id": "tr_izm", "name": "Izmir", "keywords": ["izmir"],
             "districts": [{"id": "tr_izm_ct", "name": "Izmir City", "keywords": ["izmir city"]}]},
            {"id": "tr_ant", "name": "Antalya", "keywords": ["antalya"],
             "districts": [{"id": "tr_ant_ct", "name": "Antalya City", "keywords": ["antalya city"]}]},
            {"id": "tr_bur", "name": "Bursa", "keywords": ["bursa"],
             "districts": [{"id": "tr_bur_ct", "name": "Bursa City", "keywords": ["bursa city"]}]},
        ]
    },
    {
        "id": "nld", "name": "Netherlands", "code": "NL",
        "keywords": ["netherlands", "dutch", "holland", "amsterdam"],
        "states": [
            {"id": "nl_nh", "name": "North Holland", "keywords": ["north holland", "amsterdam"],
             "districts": [{"id": "nl_nh_ams", "name": "Amsterdam", "keywords": ["amsterdam"]}]},
            {"id": "nl_sh", "name": "South Holland", "keywords": ["south holland", "rotterdam", "the hague"],
             "districts": [{"id": "nl_sh_rot", "name": "Rotterdam", "keywords": ["rotterdam"]}]},
            {"id": "nl_ut", "name": "Utrecht", "keywords": ["utrecht"],
             "districts": [{"id": "nl_ut_ct", "name": "Utrecht City", "keywords": ["utrecht city"]}]},
            {"id": "nl_ge", "name": "Gelderland", "keywords": ["gelderland", "arnhem"],
             "districts": [{"id": "nl_ge_arn", "name": "Arnhem", "keywords": ["arnhem"]}]},
            {"id": "nl_li", "name": "Limburg", "keywords": ["limburg", "maastricht"],
             "districts": [{"id": "nl_li_maa", "name": "Maastricht", "keywords": ["maastricht"]}]},
        ]
    },
    {
        "id": "che", "name": "Switzerland", "code": "CH",
        "keywords": ["switzerland", "swiss"],
        "states": [
            {"id": "ch_zh", "name": "Zurich", "keywords": ["zurich", "zürich"],
             "districts": [{"id": "ch_zh_ct", "name": "Zurich City", "keywords": ["zurich city"]}]},
            {"id": "ch_ge", "name": "Geneva", "keywords": ["geneva", "geneve"],
             "districts": [{"id": "ch_ge_ct", "name": "Geneva City", "keywords": ["geneva city"]}]},
            {"id": "ch_be", "name": "Bern", "keywords": ["bern", "berne"],
             "districts": [{"id": "ch_be_ct", "name": "Bern City", "keywords": ["bern city"]}]},
            {"id": "ch_bs", "name": "Basel", "keywords": ["basel"],
             "districts": [{"id": "ch_bs_ct", "name": "Basel City", "keywords": ["basel city"]}]},
            {"id": "ch_vd", "name": "Vaud", "keywords": ["vaud", "lausanne"],
             "districts": [{"id": "ch_vd_lau", "name": "Lausanne", "keywords": ["lausanne"]}]},
        ]
    },
    {
        "id": "swe", "name": "Sweden", "code": "SE",
        "keywords": ["sweden", "swedish", "stockholm"],
        "states": [
            {"id": "se_stk", "name": "Stockholm", "keywords": ["stockholm"],
             "districts": [{"id": "se_stk_ct", "name": "Stockholm City", "keywords": ["stockholm city"]}]},
            {"id": "se_vg", "name": "Västra Götaland", "keywords": ["vastra gotaland", "gothenburg"],
             "districts": [{"id": "se_vg_got", "name": "Gothenburg", "keywords": ["gothenburg"]}]},
            {"id": "se_sk", "name": "Skåne", "keywords": ["skane", "malmo"],
             "districts": [{"id": "se_sk_mal", "name": "Malmö", "keywords": ["malmo"]}]},
            {"id": "se_up", "name": "Uppsala", "keywords": ["uppsala"],
             "districts": [{"id": "se_up_ct", "name": "Uppsala City", "keywords": ["uppsala city"]}]},
            {"id": "se_or", "name": "Örebro", "keywords": ["orebro"],
             "districts": [{"id": "se_or_ct", "name": "Örebro City", "keywords": ["orebro city"]}]},
        ]
    },
    {
        "id": "nor", "name": "Norway", "code": "NO",
        "keywords": ["norway", "norwegian", "oslo"],
        "states": [
            {"id": "no_osl", "name": "Oslo", "keywords": ["oslo"],
             "districts": [{"id": "no_osl_ct", "name": "Oslo City", "keywords": ["oslo city"]}]},
            {"id": "no_ber", "name": "Bergen", "keywords": ["bergen"],
             "districts": [{"id": "no_ber_ct", "name": "Bergen City", "keywords": ["bergen city"]}]},
            {"id": "no_trd", "name": "Trondheim", "keywords": ["trondheim"],
             "districts": [{"id": "no_trd_ct", "name": "Trondheim City", "keywords": ["trondheim city"]}]},
            {"id": "no_stv", "name": "Stavanger", "keywords": ["stavanger"],
             "districts": [{"id": "no_stv_ct", "name": "Stavanger City", "keywords": ["stavanger city"]}]},
            {"id": "no_tms", "name": "Tromsø", "keywords": ["tromso", "tromsø"],
             "districts": [{"id": "no_tms_ct", "name": "Tromsø City", "keywords": ["tromso city"]}]},
        ]
    },
    {
        "id": "arg", "name": "Argentina", "code": "AR",
        "keywords": ["argentina", "argentine", "buenos aires"],
        "states": [
            {"id": "ar_ba", "name": "Buenos Aires", "keywords": ["buenos aires"],
             "districts": [{"id": "ar_ba_ct", "name": "Buenos Aires City", "keywords": ["buenos aires city"]}]},
            {"id": "ar_cor", "name": "Córdoba", "keywords": ["cordoba", "córdoba"],
             "districts": [{"id": "ar_cor_ct", "name": "Córdoba City", "keywords": ["cordoba city"]}]},
            {"id": "ar_sf", "name": "Santa Fe", "keywords": ["santa fe", "rosario"],
             "districts": [{"id": "ar_sf_ros", "name": "Rosario", "keywords": ["rosario"]}]},
            {"id": "ar_men", "name": "Mendoza", "keywords": ["mendoza"],
             "districts": [{"id": "ar_men_ct", "name": "Mendoza City", "keywords": ["mendoza city"]}]},
            {"id": "ar_tuc", "name": "Tucumán", "keywords": ["tucuman", "tucumán"],
             "districts": [{"id": "ar_tuc_ct", "name": "Tucumán City", "keywords": ["tucuman city"]}]},
        ]
    },
    {
        "id": "egy", "name": "Egypt", "code": "EG",
        "keywords": ["egypt", "egyptian", "cairo"],
        "states": [
            {"id": "eg_cai", "name": "Cairo", "keywords": ["cairo"],
             "districts": [{"id": "eg_cai_ct", "name": "Cairo City", "keywords": ["cairo city"]}]},
            {"id": "eg_ale", "name": "Alexandria", "keywords": ["alexandria"],
             "districts": [{"id": "eg_ale_ct", "name": "Alexandria City", "keywords": ["alexandria city"]}]},
            {"id": "eg_giz", "name": "Giza", "keywords": ["giza", "pyramids"],
             "districts": [{"id": "eg_giz_ct", "name": "Giza City", "keywords": ["giza city"]}]},
            {"id": "eg_lux", "name": "Luxor", "keywords": ["luxor"],
             "districts": [{"id": "eg_lux_ct", "name": "Luxor City", "keywords": ["luxor city"]}]},
            {"id": "eg_asw", "name": "Aswan", "keywords": ["aswan"],
             "districts": [{"id": "eg_asw_ct", "name": "Aswan City", "keywords": ["aswan city"]}]},
        ]
    },
    {
        "id": "tha", "name": "Thailand", "code": "TH",
        "keywords": ["thailand", "thai", "bangkok"],
        "states": [
            {"id": "th_bkk", "name": "Bangkok", "keywords": ["bangkok"],
             "districts": [{"id": "th_bkk_ct", "name": "Bangkok City", "keywords": ["bangkok city"]}]},
            {"id": "th_cnx", "name": "Chiang Mai", "keywords": ["chiang mai"],
             "districts": [{"id": "th_cnx_ct", "name": "Chiang Mai City", "keywords": ["chiang mai city"]}]},
            {"id": "th_pkt", "name": "Phuket", "keywords": ["phuket"],
             "districts": [{"id": "th_pkt_ct", "name": "Phuket City", "keywords": ["phuket city"]}]},
            {"id": "th_cbi", "name": "Chonburi", "keywords": ["chonburi", "pattaya"],
             "districts": [{"id": "th_cbi_pat", "name": "Pattaya", "keywords": ["pattaya"]}]},
            {"id": "th_krb", "name": "Krabi", "keywords": ["krabi"],
             "districts": [{"id": "th_krb_ct", "name": "Krabi Town", "keywords": ["krabi town"]}]},
        ]
    },
    {
        "id": "mys", "name": "Malaysia", "code": "MY",
        "keywords": ["malaysia", "malaysian", "kuala lumpur"],
        "states": [
            {"id": "my_kl", "name": "Kuala Lumpur", "keywords": ["kuala lumpur"],
             "districts": [{"id": "my_kl_ct", "name": "KL City", "keywords": ["kl city"]}]},
            {"id": "my_sel", "name": "Selangor", "keywords": ["selangor", "shah alam"],
             "districts": [{"id": "my_sel_ct", "name": "Shah Alam", "keywords": ["shah alam"]}]},
            {"id": "my_pen", "name": "Penang", "keywords": ["penang", "george town"],
             "districts": [{"id": "my_pen_gt", "name": "George Town", "keywords": ["george town"]}]},
            {"id": "my_jhr", "name": "Johor", "keywords": ["johor", "johor bahru"],
             "districts": [{"id": "my_jhr_jb", "name": "Johor Bahru", "keywords": ["johor bahru"]}]},
            {"id": "my_sab", "name": "Sabah", "keywords": ["sabah", "kota kinabalu"],
             "districts": [{"id": "my_sab_kk", "name": "Kota Kinabalu", "keywords": ["kota kinabalu"]}]},
        ]
    },
    {
        "id": "sgp", "name": "Singapore", "code": "SG",
        "keywords": ["singapore", "singaporean"],
        "states": [
            {"id": "sg_cen", "name": "Central Region", "keywords": ["singapore central", "orchard", "marina bay"],
             "districts": [{"id": "sg_cen_mb", "name": "Marina Bay", "keywords": ["marina bay"]}]},
            {"id": "sg_eas", "name": "East Region", "keywords": ["singapore east", "changi", "tampines"],
             "districts": [{"id": "sg_eas_ch", "name": "Changi", "keywords": ["changi"]}]},
            {"id": "sg_wes", "name": "West Region", "keywords": ["singapore west", "jurong"],
             "districts": [{"id": "sg_wes_ju", "name": "Jurong", "keywords": ["jurong"]}]},
            {"id": "sg_nor", "name": "North Region", "keywords": ["singapore north", "woodlands"],
             "districts": [{"id": "sg_nor_wl", "name": "Woodlands", "keywords": ["woodlands"]}]},
            {"id": "sg_ne", "name": "North-East Region", "keywords": ["singapore north-east", "sengkang"],
             "districts": [{"id": "sg_ne_sk", "name": "Sengkang", "keywords": ["sengkang"]}]},
        ]
    },
    {
        "id": "nzl", "name": "New Zealand", "code": "NZ",
        "keywords": ["new zealand", "kiwi", "wellington"],
        "states": [
            {"id": "nz_akl", "name": "Auckland", "keywords": ["auckland"],
             "districts": [{"id": "nz_akl_ct", "name": "Auckland City", "keywords": ["auckland city"]}]},
            {"id": "nz_wlg", "name": "Wellington", "keywords": ["wellington"],
             "districts": [{"id": "nz_wlg_ct", "name": "Wellington City", "keywords": ["wellington city"]}]},
            {"id": "nz_can", "name": "Canterbury", "keywords": ["canterbury", "christchurch"],
             "districts": [{"id": "nz_can_chc", "name": "Christchurch", "keywords": ["christchurch"]}]},
            {"id": "nz_wkt", "name": "Waikato", "keywords": ["waikato", "hamilton"],
             "districts": [{"id": "nz_wkt_ham", "name": "Hamilton", "keywords": ["hamilton"]}]},
            {"id": "nz_ota", "name": "Otago", "keywords": ["otago", "dunedin"],
             "districts": [{"id": "nz_ota_dun", "name": "Dunedin", "keywords": ["dunedin"]}]},
        ]
    },
    {
        "id": "pak", "name": "Pakistan", "code": "PK",
        "keywords": ["pakistan", "pakistani", "islamabad", "karachi"],
        "states": [
            {"id": "pk_sd", "name": "Sindh", "keywords": ["sindh", "karachi"],
             "districts": [{"id": "pk_sd_khi", "name": "Karachi", "keywords": ["karachi"]}]},
            {"id": "pk_pb", "name": "Punjab", "keywords": ["punjab pakistan", "lahore"],
             "districts": [{"id": "pk_pb_lhe", "name": "Lahore", "keywords": ["lahore"]}]},
            {"id": "pk_isl", "name": "Islamabad", "keywords": ["islamabad"],
             "districts": [{"id": "pk_isl_ct", "name": "Islamabad City", "keywords": ["islamabad city"]}]},
        ]
    },
    {
        "id": "bgd", "name": "Bangladesh", "code": "BD",
        "keywords": ["bangladesh", "bangladeshi", "dhaka"],
        "states": [
            {"id": "bd_dhk", "name": "Dhaka", "keywords": ["dhaka"],
             "districts": [{"id": "bd_dhk_ct", "name": "Dhaka City", "keywords": ["dhaka city"]}]},
            {"id": "bd_ctg", "name": "Chittagong", "keywords": ["chittagong", "chattogram"],
             "districts": [{"id": "bd_ctg_ct", "name": "Chittagong City", "keywords": ["chittagong city"]}]},
        ]
    },
    {
        "id": "lka", "name": "Sri Lanka", "code": "LK",
        "keywords": ["sri lanka", "sri lankan", "colombo"],
        "states": [
            {"id": "lk_wp", "name": "Western Province", "keywords": ["colombo", "western province"],
             "districts": [{"id": "lk_wp_cmb", "name": "Colombo", "keywords": ["colombo"]}]},
            {"id": "lk_cp", "name": "Central Province", "keywords": ["kandy", "central province"],
             "districts": [{"id": "lk_cp_kdy", "name": "Kandy", "keywords": ["kandy"]}]},
        ]
    },
    {
        "id": "nga", "name": "Nigeria", "code": "NG",
        "keywords": ["nigeria", "nigerian", "abuja", "lagos"],
        "states": [
            {"id": "ng_lag", "name": "Lagos", "keywords": ["lagos"],
             "districts": [{"id": "ng_lag_ct", "name": "Lagos City", "keywords": ["lagos city"]}]},
            {"id": "ng_abj", "name": "Abuja", "keywords": ["abuja"],
             "districts": [{"id": "ng_abj_ct", "name": "Abuja City", "keywords": ["abuja city"]}]},
        ]
    },
    {
        "id": "ken", "name": "Kenya", "code": "KE",
        "keywords": ["kenya", "kenyan", "nairobi"],
        "states": [
            {"id": "ke_nrb", "name": "Nairobi", "keywords": ["nairobi"],
             "districts": [{"id": "ke_nrb_ct", "name": "Nairobi City", "keywords": ["nairobi city"]}]},
            {"id": "ke_mbs", "name": "Mombasa", "keywords": ["mombasa"],
             "districts": [{"id": "ke_mbs_ct", "name": "Mombasa City", "keywords": ["mombasa city"]}]},
        ]
    },
    {
        "id": "isr", "name": "Israel", "code": "IL",
        "keywords": ["israel", "israeli", "tel aviv", "jerusalem", "netanyahu"],
        "states": [
            {"id": "il_tlv", "name": "Tel Aviv", "keywords": ["tel aviv"],
             "districts": [{"id": "il_tlv_ct", "name": "Tel Aviv City", "keywords": ["tel aviv city"]}]},
            {"id": "il_jrs", "name": "Jerusalem", "keywords": ["jerusalem"],
             "districts": [{"id": "il_jrs_ct", "name": "Jerusalem City", "keywords": ["jerusalem city"]}]},
        ]
    },
    {
        "id": "irn", "name": "Iran", "code": "IR",
        "keywords": ["iran", "iranian", "tehran", "persian"],
        "states": [
            {"id": "ir_thr", "name": "Tehran", "keywords": ["tehran"],
             "districts": [{"id": "ir_thr_ct", "name": "Tehran City", "keywords": ["tehran city"]}]},
            {"id": "ir_isf", "name": "Isfahan", "keywords": ["isfahan", "esfahan"],
             "districts": [{"id": "ir_isf_ct", "name": "Isfahan City", "keywords": ["isfahan city"]}]},
        ]
    },
    {
        "id": "pol", "name": "Poland", "code": "PL",
        "keywords": ["poland", "polish", "warsaw"],
        "states": [
            {"id": "pl_maz", "name": "Masovia", "keywords": ["warsaw", "masovia"],
             "districts": [{"id": "pl_maz_war", "name": "Warsaw", "keywords": ["warsaw"]}]},
            {"id": "pl_mlp", "name": "Lesser Poland", "keywords": ["krakow", "lesser poland"],
             "districts": [{"id": "pl_mlp_krk", "name": "Krakow", "keywords": ["krakow"]}]},
        ]
    },
    {
        "id": "ukr", "name": "Ukraine", "code": "UA",
        "keywords": ["ukraine", "ukrainian", "kyiv", "zelenskyy"],
        "states": [
            {"id": "ua_kyv", "name": "Kyiv", "keywords": ["kyiv", "kiev"],
             "districts": [{"id": "ua_kyv_ct", "name": "Kyiv City", "keywords": ["kyiv city"]}]},
            {"id": "ua_odsa", "name": "Odesa", "keywords": ["odesa", "odessa"],
             "districts": [{"id": "ua_odsa_ct", "name": "Odesa City", "keywords": ["odesa city"]}]},
        ]
    },
    {
        "id": "vnm", "name": "Vietnam", "code": "VN",
        "keywords": ["vietnam", "vietnamese", "hanoi", "ho chi minh"],
        "states": [
            {"id": "vn_hcm", "name": "Ho Chi Minh City", "keywords": ["ho chi minh", "saigon"],
             "districts": [{"id": "vn_hcm_ct", "name": "HCMC Center", "keywords": ["ho chi minh city"]}]},
            {"id": "vn_hn", "name": "Hanoi", "keywords": ["hanoi"],
             "districts": [{"id": "vn_hn_ct", "name": "Hanoi City", "keywords": ["hanoi city"]}]},
        ]
    },
    {
        "id": "phl", "name": "Philippines", "code": "PH",
        "keywords": ["philippines", "filipino", "manila"],
        "states": [
            {"id": "ph_mnl", "name": "Metro Manila", "keywords": ["manila", "metro manila"],
             "districts": [{"id": "ph_mnl_ct", "name": "Manila City", "keywords": ["manila city"]}]},
            {"id": "ph_ceb", "name": "Cebu", "keywords": ["cebu"],
             "districts": [{"id": "ph_ceb_ct", "name": "Cebu City", "keywords": ["cebu city"]}]},
        ]
    },
    {
        "id": "col", "name": "Colombia", "code": "CO",
        "keywords": ["colombia", "colombian", "bogota"],
        "states": [
            {"id": "co_bog", "name": "Bogotá", "keywords": ["bogota"],
             "districts": [{"id": "co_bog_ct", "name": "Bogotá City", "keywords": ["bogota city"]}]},
            {"id": "co_med", "name": "Medellín", "keywords": ["medellin"],
             "districts": [{"id": "co_med_ct", "name": "Medellín City", "keywords": ["medellin city"]}]},
        ]
    },
    {
        "id": "chl", "name": "Chile", "code": "CL",
        "keywords": ["chile", "chilean", "santiago"],
        "states": [
            {"id": "cl_rm", "name": "Santiago Metropolitan", "keywords": ["santiago"],
             "districts": [{"id": "cl_rm_stg", "name": "Santiago City", "keywords": ["santiago city"]}]},
            {"id": "cl_vlp", "name": "Valparaíso", "keywords": ["valparaiso"],
             "districts": [{"id": "cl_vlp_ct", "name": "Valparaíso City", "keywords": ["valparaiso city"]}]},
        ]
    },
    {
        "id": "gha", "name": "Ghana", "code": "GH",
        "keywords": ["ghana", "ghanaian", "accra"],
        "states": [
            {"id": "gh_acc", "name": "Greater Accra", "keywords": ["accra"],
             "districts": [{"id": "gh_acc_ct", "name": "Accra City", "keywords": ["accra city"]}]},
            {"id": "gh_kum", "name": "Kumasi", "keywords": ["kumasi"],
             "districts": [{"id": "gh_kum_ct", "name": "Kumasi City", "keywords": ["kumasi city"]}]},
        ]
    },
    {
        "id": "eth", "name": "Ethiopia", "code": "ET",
        "keywords": ["ethiopia", "ethiopian", "addis ababa"],
        "states": [
            {"id": "et_aa", "name": "Addis Ababa", "keywords": ["addis ababa"],
             "districts": [{"id": "et_aa_ct", "name": "Addis Ababa City", "keywords": ["addis ababa city"]}]},
            {"id": "et_oro", "name": "Oromia", "keywords": ["oromia"],
             "districts": [{"id": "et_oro_ct", "name": "Oromia Region", "keywords": ["oromia region"]}]},
        ]
    },
    {
        "id": "grc", "name": "Greece", "code": "GR",
        "keywords": ["greece", "greek", "athens"],
        "states": [
            {"id": "gr_att", "name": "Attica", "keywords": ["attica", "athens"],
             "districts": [{"id": "gr_att_ath", "name": "Athens", "keywords": ["athens"]}]}
        ]
    },
    {
        "id": "prt", "name": "Portugal", "code": "PT",
        "keywords": ["portugal", "portuguese", "lisbon", "porto"],
        "states": [
            {"id": "pt_lis", "name": "Lisbon", "keywords": ["lisbon"],
             "districts": [{"id": "pt_lis_ct", "name": "Lisbon City", "keywords": ["lisbon city"]}]}
        ]
    },
    {
        "id": "per", "name": "Peru", "code": "PE",
        "keywords": ["peru", "peruvian", "lima"],
        "states": [
            {"id": "pe_lim", "name": "Lima", "keywords": ["lima"],
             "districts": [{"id": "pe_lim_ct", "name": "Lima City", "keywords": ["lima city"]}]}
        ]
    },
    {
        "id": "mar", "name": "Morocco", "code": "MA",
        "keywords": ["morocco", "moroccan", "rabat", "casablanca"],
        "states": [
            {"id": "ma_cas", "name": "Casablanca-Settat", "keywords": ["casablanca"],
             "districts": [{"id": "ma_cas_ct", "name": "Casablanca City", "keywords": ["casablanca city"]}]}
        ]
    },
    {
        "id": "npl", "name": "Nepal", "code": "NP",
        "keywords": ["nepal", "nepalese", "kathmandu"],
        "states": [
            {"id": "np_bag", "name": "Bagmati", "keywords": ["bagmati", "kathmandu"],
             "districts": [{"id": "np_bag_kat", "name": "Kathmandu City", "keywords": ["kathmandu"]}]}
        ]
    },
    {
        "id": "twn", "name": "Taiwan", "code": "TW",
        "keywords": ["taiwan", "taiwanese", "taipei", "tsmc"],
        "states": [
            {"id": "tw_tpe", "name": "Taipei", "keywords": ["taipei"],
             "districts": [{"id": "tw_tpe_ct", "name": "Taipei City", "keywords": ["taipei city", "xinyi"]}]},
            {"id": "tw_khh", "name": "Kaohsiung", "keywords": ["kaohsiung"],
             "districts": [{"id": "tw_khh_ct", "name": "Kaohsiung City", "keywords": ["kaohsiung city"]}]},
            {"id": "tw_txg", "name": "Taichung", "keywords": ["taichung"],
             "districts": [{"id": "tw_txg_ct", "name": "Taichung City", "keywords": ["taichung city"]}]},
            {"id": "tw_hsc", "name": "Hsinchu", "keywords": ["hsinchu", "hsinchu science park"],
             "districts": [{"id": "tw_hsc_ct", "name": "Hsinchu City", "keywords": ["hsinchu city"]}]},
        ]
    },
    {
        "id": "irq", "name": "Iraq", "code": "IQ",
        "keywords": ["iraq", "iraqi", "baghdad"],
        "states": [
            {"id": "iq_bgw", "name": "Baghdad", "keywords": ["baghdad"],
             "districts": [{"id": "iq_bgw_ct", "name": "Baghdad City", "keywords": ["baghdad city"]}]},
            {"id": "iq_bsr", "name": "Basra", "keywords": ["basra"],
             "districts": [{"id": "iq_bsr_ct", "name": "Basra City", "keywords": ["basra city"]}]},
            {"id": "iq_ebl", "name": "Erbil", "keywords": ["erbil", "arbil", "kurdistan"],
             "districts": [{"id": "iq_ebl_ct", "name": "Erbil City", "keywords": ["erbil city"]}]},
        ]
    },
    {
        "id": "cod", "name": "DR Congo", "code": "CD",
        "keywords": ["congo", "drc", "democratic republic of congo", "kinshasa"],
        "states": [
            {"id": "cd_kin", "name": "Kinshasa", "keywords": ["kinshasa"],
             "districts": [{"id": "cd_kin_ct", "name": "Kinshasa City", "keywords": ["kinshasa city"]}]},
            {"id": "cd_lub", "name": "Lubumbashi", "keywords": ["lubumbashi"],
             "districts": [{"id": "cd_lub_ct", "name": "Lubumbashi City", "keywords": ["lubumbashi city"]}]},
        ]
    },
    {
        "id": "tza", "name": "Tanzania", "code": "TZ",
        "keywords": ["tanzania", "tanzanian", "dar es salaam", "dodoma"],
        "states": [
            {"id": "tz_dar", "name": "Dar es Salaam", "keywords": ["dar es salaam"],
             "districts": [{"id": "tz_dar_ct", "name": "Dar es Salaam City", "keywords": ["dar es salaam city"]}]},
            {"id": "tz_dod", "name": "Dodoma", "keywords": ["dodoma"],
             "districts": [{"id": "tz_dod_ct", "name": "Dodoma City", "keywords": ["dodoma city"]}]},
        ]
    },
    {
        "id": "cub", "name": "Cuba", "code": "CU",
        "keywords": ["cuba", "cuban", "havana"],
        "states": [
            {"id": "cu_hav", "name": "Havana", "keywords": ["havana", "la habana"],
             "districts": [{"id": "cu_hav_ct", "name": "Havana City", "keywords": ["havana city"]}]},
            {"id": "cu_stg", "name": "Santiago de Cuba", "keywords": ["santiago de cuba"],
             "districts": [{"id": "cu_stg_ct", "name": "Santiago de Cuba City", "keywords": ["santiago de cuba city"]}]},
        ]
    },
    {
        "id": "ven", "name": "Venezuela", "code": "VE",
        "keywords": ["venezuela", "venezuelan", "caracas", "maduro"],
        "states": [
            {"id": "ve_car", "name": "Caracas", "keywords": ["caracas"],
             "districts": [{"id": "ve_car_ct", "name": "Caracas City", "keywords": ["caracas city"]}]},
            {"id": "ve_zul", "name": "Zulia", "keywords": ["zulia", "maracaibo"],
             "districts": [{"id": "ve_zul_mar", "name": "Maracaibo", "keywords": ["maracaibo"]}]},
        ]
    },
    {
        "id": "afg", "name": "Afghanistan", "code": "AF",
        "keywords": ["afghanistan", "afghan", "kabul", "taliban"],
        "states": [
            {"id": "af_kbl", "name": "Kabul", "keywords": ["kabul"],
             "districts": [{"id": "af_kbl_ct", "name": "Kabul City", "keywords": ["kabul city"]}]},
            {"id": "af_kdr", "name": "Kandahar", "keywords": ["kandahar"],
             "districts": [{"id": "af_kdr_ct", "name": "Kandahar City", "keywords": ["kandahar city"]}]},
            {"id": "af_hrt", "name": "Herat", "keywords": ["herat"],
             "districts": [{"id": "af_hrt_ct", "name": "Herat City", "keywords": ["herat city"]}]},
        ]
    },
    {
        "id": "mmr", "name": "Myanmar", "code": "MM",
        "keywords": ["myanmar", "burma", "burmese", "yangon", "naypyidaw"],
        "states": [
            {"id": "mm_ygn", "name": "Yangon", "keywords": ["yangon", "rangoon"],
             "districts": [{"id": "mm_ygn_ct", "name": "Yangon City", "keywords": ["yangon city"]}]},
            {"id": "mm_npt", "name": "Naypyidaw", "keywords": ["naypyidaw"],
             "districts": [{"id": "mm_npt_ct", "name": "Naypyidaw City", "keywords": ["naypyidaw city"]}]},
            {"id": "mm_mdy", "name": "Mandalay", "keywords": ["mandalay"],
             "districts": [{"id": "mm_mdy_ct", "name": "Mandalay City", "keywords": ["mandalay city"]}]},
        ]
    },
    {
        "id": "fin", "name": "Finland", "code": "FI",
        "keywords": ["finland", "finnish", "helsinki"],
        "states": [
            {"id": "fi_hel", "name": "Helsinki", "keywords": ["helsinki"],
             "districts": [{"id": "fi_hel_ct", "name": "Helsinki City", "keywords": ["helsinki city"]}]},
            {"id": "fi_tmp", "name": "Tampere", "keywords": ["tampere"],
             "districts": [{"id": "fi_tmp_ct", "name": "Tampere City", "keywords": ["tampere city"]}]},
            {"id": "fi_tur", "name": "Turku", "keywords": ["turku"],
             "districts": [{"id": "fi_tur_ct", "name": "Turku City", "keywords": ["turku city"]}]},
        ]
    },
    {
        "id": "dnk", "name": "Denmark", "code": "DK",
        "keywords": ["denmark", "danish", "copenhagen"],
        "states": [
            {"id": "dk_cph", "name": "Copenhagen", "keywords": ["copenhagen"],
             "districts": [{"id": "dk_cph_ct", "name": "Copenhagen City", "keywords": ["copenhagen city"]}]},
            {"id": "dk_aar", "name": "Aarhus", "keywords": ["aarhus"],
             "districts": [{"id": "dk_aar_ct", "name": "Aarhus City", "keywords": ["aarhus city"]}]},
            {"id": "dk_ode", "name": "Odense", "keywords": ["odense"],
             "districts": [{"id": "dk_ode_ct", "name": "Odense City", "keywords": ["odense city"]}]},
        ]
    },
    {
        "id": "aut", "name": "Austria", "code": "AT",
        "keywords": ["austria", "austrian", "vienna", "wien"],
        "states": [
            {"id": "at_vie", "name": "Vienna", "keywords": ["vienna", "wien"],
             "districts": [{"id": "at_vie_ct", "name": "Vienna City", "keywords": ["vienna city"]}]},
            {"id": "at_sbg", "name": "Salzburg", "keywords": ["salzburg"],
             "districts": [{"id": "at_sbg_ct", "name": "Salzburg City", "keywords": ["salzburg city"]}]},
            {"id": "at_grz", "name": "Graz", "keywords": ["graz"],
             "districts": [{"id": "at_grz_ct", "name": "Graz City", "keywords": ["graz city"]}]},
        ]
    },
    {
        "id": "hun", "name": "Hungary", "code": "HU",
        "keywords": ["hungary", "hungarian", "budapest", "orban"],
        "states": [
            {"id": "hu_bud", "name": "Budapest", "keywords": ["budapest"],
             "districts": [{"id": "hu_bud_ct", "name": "Budapest City", "keywords": ["budapest city"]}]},
            {"id": "hu_deb", "name": "Debrecen", "keywords": ["debrecen"],
             "districts": [{"id": "hu_deb_ct", "name": "Debrecen City", "keywords": ["debrecen city"]}]},
        ]
    },
]
