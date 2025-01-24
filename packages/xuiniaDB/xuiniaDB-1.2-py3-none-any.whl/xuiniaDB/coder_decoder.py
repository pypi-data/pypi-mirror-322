import random
#...........



letters = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '_', '1', '2', '3',
    '4', '5', '6', '7', '8', '9', '0', ',',  '-', '*', '/', '+', '!', '@', '#',
    '%', ':', ';', '&', '?', '(', ')', '.', '`', 'A', 'B', 'C', 'D', 'E', 'F',
    'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
    'V', 'W', 'X', 'Y', 'Z', '<', '>', '|', '~', '$', '[', ']', '{', '}','=',
    
    'А', 'Б', 'В', 'Г', 'Ґ', 'Д', 'Е', 'Є', 'Ж', 'З', 'И', 'І', 'Ї', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 
    'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ь', 'Ю', 'Я', 
    'Ё', 'Ъ', 'Ы', 'Э', 
    'а', 'б', 'в', 'г', 'ґ', 'д', 'е', 'є', 'ж', 'з', 'и', 'і', 'ї', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 
    'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ь', 'ю', 'я',
    'ё', 'ъ', 'ы', 'э', ' '
    ]
  

codes1 = [
    ['ZPH', 'NYI', 'NXQ', 'COQ', 'JHE', 'RDG', 'HUI', 'XJV', 'IAH', 'ALV', 'CNM', 'UPS', 'KPQ', 'GNC', 'EUX', 'HIJ', 'GLD', 'FBU', 'SXK', 'OXA'],# 'a', 
    ['OJU', 'RIP', 'VTF', 'NXM', 'AQI', 'WTW', 'FHP', 'FGN', 'OQK', 'QZA', 'EHK', 'OAB', 'XWV', 'BPT', 'TEA', 'NZK', 'TAK', 'KYP', 'MKE', 'DRT'],# 'b', 
    ['NRC', 'LKB', 'QAX', 'DRS', 'NMG', 'GWG', 'XGJ', 'CBF', 'SNA', 'VSV', 'WII', 'BMD', 'EZF', 'GMD', 'PGG', 'PKG', 'HQE', 'MON', 'HHQ', 'NFB'],# 'c', 
    ['QVO', 'LHF', 'SNE', 'KSV', 'FAD', 'NFC', 'TUF', 'KOW', 'PPM', 'EXD', 'IOC', 'AQM', 'QYJ', 'KEF', 'TJE', 'LRQ', 'SWH', 'ROU', 'KVW', 'PKK'],# 'd', 
    ['ZKF', 'GUN', 'BTW', 'CGA', 'FBH', 'FBR', 'HPN', 'MYB', 'XCR', 'SOY', 'JFS', 'LSH', 'DFA', 'HGY', 'HPD', 'ZKI', 'XGI', 'NXV', 'IQX', 'DTI'],# 'e', 
    ['PSS', 'NSB', 'PPP', 'HXI', 'NMF', 'PCL', 'MDR', 'YGI', 'AWY', 'LPF', 'AQT', 'POM', 'MDU', 'OXW', 'EVZ', 'MFY', 'SSF', 'ZRE', 'MEE', 'OSB'],# 'f', 
    ['XJN', 'WWP', 'XCA', 'LTE', 'UTF', 'WBN', 'OEV', 'EJW', 'OQR', 'NCI', 'TRE', 'NFZ', 'OCI', 'VGN', 'ADI', 'EGZ', 'BGD', 'PUX', 'TOM', 'QMP'],# 'g', 
    ['DVM', 'RCL', 'OHO', 'WWH', 'XZE', 'DBZ', 'YQC', 'XFP', 'MCN', 'MIK', 'MUL', 'DNB', 'QWH', 'AKG', 'ISV', 'SKA', 'XBL', 'IIR', 'SID', 'XSX'],# 'h', 
    ['FHK', 'AVJ', 'MNW', 'TLN', 'ASQ', 'PTJ', 'TVV', 'DXF', 'JJS', 'HFF', 'UKQ', 'NAF', 'JNO', 'JVR', 'XEQ', 'OXR', 'IAZ', 'WAU', 'YPN', 'NOO'],# 'i', 
    ['OZV', 'LLQ', 'HQA', 'YHF', 'MNR', 'KRR', 'ZAP', 'HOZ', 'UJL', 'BDC', 'NCQ', 'PLF', 'SDO', 'ENG', 'BMQ', 'EDO', 'VSK', 'HCN', 'IIV', 'GNB'],# 'j', 
    ['KUE', 'OVJ', 'CVP', 'WJG', 'UIM', 'KHV', 'ZCA', 'VQA', 'EMK', 'AKL', 'NWE', 'UKG', 'DMU', 'XQK', 'TOH', 'ZII', 'MOS', 'VNZ', 'IFT', 'ZOZ'],# 'k', 
    ['BAF', 'HBV', 'JUD', 'UPC', 'FAF', 'RSC', 'YEW', 'UTJ', 'JMZ', 'LYA', 'CNG', 'CIR', 'UFJ', 'FEL', 'GMJ', 'DPE', 'JOZ', 'ZJK', 'YNW', 'UKV'],# 'l', 
    ['HPX', 'QJH', 'WLT', 'NNN', 'NKW', 'ENA', 'QPW', 'KIH', 'LLP', 'EKR', 'EBI', 'XHG', 'PNO', 'SHK', 'DBX', 'GOY', 'IPI', 'YKP', 'TIG', 'FSA'],# 'm', 
    ['WIY', 'JHG', 'DWF', 'JII', 'JQH', 'VHK', 'OXD', 'LMW', 'ICI', 'TIR', 'BGI', 'WMT', 'OIS', 'MVQ', 'WGS', 'UQP', 'KQH', 'DPI', 'AWZ', 'MFD'],# 'n', 
    ['JCL', 'AIB', 'QGQ', 'QHR', 'JJF', 'WUJ', 'NHS', 'KHR', 'TJQ', 'ORP', 'YSS', 'NPJ', 'KRE', 'HOU', 'YGU', 'FRU', 'TVS', 'GUF', 'SRF', 'DOQ'],# 'o',
    ['YRP', 'TXO', 'ZXA', 'FIH', 'BEU', 'RIK', 'AFL', 'ZDR', 'NHD', 'ACN', 'XRK', 'FZK', 'ENP', 'QRF', 'MMM', 'YTI', 'PHJ', 'KHJ', 'PMF', 'IZG'],# 'p', 
    ['RBD', 'ZZX', 'ZXW', 'NVR', 'UGJ', 'UWX', 'RSG', 'HGE', 'ZAE', 'HVC', 'ENH', 'LEI', 'MEU', 'ZIK', 'FMH', 'MRW', 'JQV', 'UXM', 'LTP', 'QVU'],# 'q', 
    ['JPF', 'CLU', 'OUD', 'RTV', 'OLK', 'YCM', 'UGP', 'RIB', 'QPR', 'ZFV', 'KPJ', 'GPN', 'YWS', 'UHT', 'CQY', 'ZQD', 'LCY', 'CJG', 'YKV', 'KVH'],# 'r', 
    ['ILE', 'MWM', 'WFF', 'ASP', 'UMI', 'SLR', 'TCH', 'BNH', 'SPT', 'FKD', 'XDY', 'ZXL', 'KHQ', 'ZDW', 'BNY', 'BPK', 'VWO', 'IOZ', 'AUD', 'FHT'],# 's', 
    ['FOW', 'GEB', 'AZP', 'GMR', 'RVL', 'WOQ', 'BVN', 'EEM', 'EFP', 'KFJ', 'SGL', 'XEF', 'YEF', 'QVY', 'FYK', 'FVO', 'LLU', 'COS', 'EXO', 'ZMW'],# 't', 
    ['NNY', 'ZVE', 'SLU', 'ZYD', 'OHE', 'FCB', 'AGX', 'HKA', 'IXZ', 'MBH', 'NXD', 'VTY', 'QHM', 'XPX', 'DGS', 'HLC', 'EOQ', 'KKM', 'NTR', 'CGT'],# 'u', 
    ['CUU', 'UVB', 'LMU', 'XVY', 'YCU', 'PUK', 'NOX', 'XVP', 'TWB', 'WEL', 'HYO', 'DKU', 'WXM', 'DDT', 'GQV', 'OPM', 'UAA', 'RFU', 'ZFN', 'XJQ'],# 'v', 
    ['ALZ', 'YOO', 'LIF', 'VCX', 'UXN', 'KFB', 'LWI', 'FBS', 'VCK', 'BQQ', 'UBN', 'CWU', 'TPZ', 'DEA', 'XTB', 'JBC', 'PMM', 'DSG', 'OWD', 'XGP'],# 'w', 
    ['TGK', 'SUB', 'VOQ', 'BLM', 'JCA', 'CAV', 'WZB', 'GVP', 'SLN', 'ZGE', 'QTB', 'SLL', 'SJB', 'ZRN', 'FJZ', 'ULM', 'BPA', 'RAH', 'XEZ', 'FOJ'],# 'x', 
    ['FUG', 'XJC', 'EDU', 'MAG', 'VGR', 'CCZ', 'MTN', 'FRT', 'EXK', 'SKW', 'VFW', 'RNI', 'VRG', 'AGP', 'LZL', 'UCT', 'RCT', 'OHC', 'ERT', 'IQS'],# 'y', 
    ['XAV', 'KHZ', 'JSL', 'BZJ', 'HTC', 'MVZ', 'UWA', 'VFM', 'DBQ', 'QBD', 'RWJ', 'VXR', 'ZRA', 'HBH', 'JBZ', 'MYU', 'ELH', 'FMZ', 'SVA', 'RXC'],# 'z', 
    ['GBW', 'FTG', 'FEB', 'VGM', 'SBN', 'XZX', 'SXU', 'WJE', 'WLO', 'QIW', 'ACD', 'BIP', 'MSQ', 'PPU', 'AQO', 'JYI', 'KMO', 'PLG', 'IAG', 'TMS'],# '_', 
    ['PAE', 'KIF', 'HZL', 'PSH', 'YQQ', 'PKC', 'SRV', 'YQJ', 'YFK', 'LRM', 'OGG', 'JGU', 'DOW', 'FZG', 'GFR', 'MUJ', 'UOV', 'GIN', 'XVG', 'JXB'],# '1',
    ['KGQ', 'GDP', 'SIM', 'KGH', 'WQQ', 'ZXX', 'HSJ', 'SME', 'IDB', 'EWL', 'SOT', 'NMB', 'NFK', 'GQD', 'KZH', 'VJI', 'RID', 'SOF', 'EYG', 'KNA'],# '2', 
    ['PKQ', 'RGL', 'HFB', 'EVP', 'GFL', 'DNL', 'ZEP', 'FZX', 'ADS', 'BAD', 'HJJ', 'LPG', 'VTO', 'KGS', 'UQL', 'HKD', 'HIH', 'PCI', 'DMC', 'FTL'],# '3',
    ['JWY', 'VKF', 'KCV', 'IWF', 'OLF', 'MXT', 'CXY', 'GQJ', 'YGE', 'VLP', 'KDV', 'UWN', 'BAY', 'MKW', 'FXH', 'AEU', 'UVO', 'SRE', 'XZU', 'RYB'],# '4', 
    ['BCF', 'BHH', 'JVV', 'ZAR', 'ZHD', 'WQM', 'UWY', 'ALQ', 'ZKU', 'BZK', 'ZCI', 'DMI', 'JAP', 'XAR', 'QHD', 'FRK', 'HLI', 'RKO', 'GET', 'ISZ'],# '5', 
    ['OWG', 'GJS', 'WXF', 'RBQ', 'XTP', 'NXT', 'IMY', 'BWR', 'YFG', 'YSM', 'DIZ', 'IJQ', 'BLK', 'DTA', 'SDL', 'ZJU', 'FEE', 'OJA', 'XMQ', 'AMI'],# '6', 
    ['XBO', 'SAI', 'RQT', 'XUR', 'LUO', 'WHE', 'IXD', 'TLJ', 'YCD', 'ILA', 'AZT', 'OZU', 'QJX', 'CIP', 'GMI', 'WQB', 'LPA', 'WRQ', 'RGU', 'AQU'],# '7', 
    ['CQK', 'UAZ', 'AYH', 'PXZ', 'XQQ', 'YQN', 'IZP', 'XPR', 'EDA', 'QHC', 'LEL', 'IVZ', 'YQL', 'FLF', 'HXK', 'XTE', 'LFS', 'UJZ', 'QUI', 'AVQ'],# '8', 
    ['RXH', 'WSN', 'FWL', 'TEV', 'JVI', 'QJT', 'HDT', 'UGO', 'HGW', 'MWA', 'QCE', 'ING', 'QQV', 'MGP', 'SJX', 'NNW', 'MBN', 'BHL', 'UIY', 'UEN'],# '9', 
    ['XZY', 'SPV', 'MMC', 'YIN', 'RJL', 'VZX', 'SBM', 'WUI', 'FAN', 'JIN', 'ABH', 'YXT', 'MLC', 'HAR', 'PWZ', 'MEP', 'CSH', 'SLG', 'LAZ', 'OEK'],# '0', 
    ['DGL', 'QFB', 'QRW', 'SUM', 'CIO', 'FWK', 'FUV', 'TSD', 'KQQ', 'CEW', 'QNX', 'BGK', 'XRQ', 'UHW', 'MJQ', 'MEH', 'FWW', 'JVS', 'GVR', 'MLW'],# ',', 
    ['HMS', 'RXV', 'RXX', 'FHQ', 'HBX', 'EPB', 'UPF', 'PKO', 'SYC', 'WKM', 'XHH', 'EVN', 'BOA', 'KNM', 'RJR', 'YZS', 'OBR', 'CBE', 'FUH', 'CSA'],# '-', 
    ['YAA', 'SMY', 'WGN', 'OGF', 'YGR', 'HJD', 'GCV', 'PCE', 'JKL', 'HQX', 'OGD', 'MGH', 'CCK', 'THZ', 'ZML', 'TIZ', 'BPS', 'IPW', 'ZQL', 'OCG'],# '*', 
    ['DRE', 'YRK', 'MXH', 'JTZ', 'QAP', 'NGY', 'GWI', 'QDD', 'VYA', 'OMG', 'MBD', 'RSI', 'LCT', 'NNF', 'TBM', 'CSE', 'VTD', 'PCO', 'GYP', 'KTH'],# '/', 
    ['IFG', 'YEM', 'XRH', 'EGQ', 'ZQS', 'WTB', 'IUF', 'EPL', 'DCD', 'XIL', 'EOR', 'ZOB', 'APP', 'PZR', 'VTK', 'WDA', 'BJX', 'CQL', 'IDS', 'JAO'],# '+', 
    ['KEM', 'QRJ', 'TFQ', 'YUY', 'NAV', 'XFH', 'GYW', 'YIT', 'OFH', 'PTY', 'IGL', 'WNF', 'BIT', 'ZKH', 'AHU', 'CGW', 'WNN', 'EXF', 'GLC', 'CJN'],# '!', 
    ['JBU', 'NWT', 'PQI', 'YYU', 'ELO', 'MOD', 'QNN', 'ZRS', 'ACF', 'TZS', 'WRU', 'SQG', 'AXO', 'YNX', 'IXV', 'ONI', 'HJI', 'YJQ', 'QPN', 'JYY'],# '@', 
    ['DXX', 'WFV', 'FPY', 'KNG', 'ILQ', 'IXB', 'VUZ', 'MTI', 'YMJ', 'MMV', 'ZMK', 'GMH', 'PUD', 'ODQ', 'BDE', 'AYJ', 'RPH', 'RFT', 'YVA', 'QLI'],# '#',
    ['YAU', 'RBJ', 'KIK', 'MJG', 'GIL', 'ZTY', 'GFH', 'IEL', 'XTO', 'DPA', 'LYG', 'TLI', 'SGX', 'CYC', 'ZZL', 'IUN', 'CPV', 'VVE', 'SMF', 'CCR'],# '%', 
    ['EMU', 'TDJ', 'BRY', 'NEW', 'DNA', 'MMD', 'PDU', 'RUA', 'GHG', 'UZB', 'NBK', 'WEM', 'HJP', 'RJX', 'NXO', 'ZJF', 'MVA', 'FAT', 'CIQ', 'DRG'],# ':', 
    ['UDO', 'FQI', 'SCR', 'EVB', 'DGD', 'WJS', 'WTR', 'EBL', 'ZGY', 'ZCH', 'GIC', 'VXK', 'NSY', 'KLD', 'YDL', 'RGQ', 'USD', 'UOK', 'HTV', 'CEE'],# ';', 
    ['CQC', 'JMC', 'VCS', 'UNL', 'VRH', 'ZLA', 'PYM', 'INL', 'NSM', 'SXJ', 'GOS', 'YSL', 'AJP', 'OLZ', 'XLL', 'MER', 'OKJ', 'ZQJ', 'VHP', 'JRZ'],# '&', 
    ['DIU', 'WWL', 'VQU', 'RPE', 'CYD', 'BMV', 'CLS', 'IBP', 'KGX', 'CRI', 'IEF', 'RNT', 'RHC', 'TCY', 'BDG', 'JEZ', 'ZEX', 'TBK', 'IGX', 'OPS'],# '?', 
    ['NPE', 'DIB', 'ELV', 'OEI', 'ZBQ', 'MGZ', 'ULA', 'NKJ', 'YPS', 'JKN', 'AWW', 'KAF', 'LRK', 'PNP', 'KRY', 'BKH', 'USJ', 'PTQ', 'BVM', 'GIZ'],# '(', 
    ['HFK', 'IOI', 'COB', 'XPC', 'MEV', 'BQM', 'XTY', 'JMI', 'JIB', 'YLD', 'RRK', 'ZXN', 'JGX', 'RQK', 'YHM', 'PAZ', 'ZXM', 'AEO', 'WPH', 'BPQ'],# ')', 
    ['REN', 'SCB', 'UGQ', 'ZBU', 'QUC', 'JRB', 'XOV', 'TMU', 'IZZ', 'LJE', 'BLS', 'VCA', 'XPK', 'DCV', 'CZZ', 'VUU', 'HTN', 'HEL', 'DIH', 'YZD'],# '.', 
    ['RPL', 'FEK', 'NKU', 'JJL', 'MXZ', 'KGJ', 'TPG', 'CJE', 'BHA', 'DFB', 'UOR', 'NUX', 'AAB', 'JCF', 'FHC', 'LYE', 'DZT', 'JZK', 'QOV', 'WNJ'],# '`', 
    ['OYK', 'EKA', 'FAU', 'NQG', 'QYP', 'HNF', 'CXT', 'BUY', 'LGS', 'KGF', 'FBM', 'ELQ', 'FJR', 'VUG', 'RYP', 'NBE', 'EHV', 'QSJ', 'WTL', 'NMP'],# 'A', 
    ['PSZ', 'OXI', 'JGE', 'XOO', 'JOC', 'ARE', 'UNZ', 'PZZ', 'ANK', 'HXD', 'HLK', 'KHA', 'IRN', 'QUQ', 'CCW', 'EBZ', 'VVI', 'KWC', 'RXN', 'DPZ'],# 'B', 
    ['NPN', 'AYP', 'WEX', 'DPM', 'CID', 'JGM', 'QAK', 'AJQ', 'ZQH', 'CBI', 'FMV', 'WIR', 'KRD', 'CKR', 'JOR', 'EIB', 'WVL', 'DSW', 'XFI', 'DTW'],# 'C', 
    ['JHP', 'NPU', 'SMA', 'QAC', 'KPR', 'MDE', 'MOV', 'BVC', 'LSZ', 'HWQ', 'MED', 'UAI', 'ERW', 'MHG', 'RNE', 'DDP', 'SLD', 'HHU', 'QHA', 'SJN'],# 'D', 
    ['UFD', 'ZLJ', 'XBU', 'LIL', 'LDT', 'HHJ', 'ZBJ', 'JVK', 'UNB', 'OPF', 'ETV', 'CGM', 'DXE', 'QAD', 'KPT', 'GKK', 'NFI', 'KRC', 'AJX', 'IXL'],# 'E', 
    ['EMS', 'VJQ', 'IKY', 'SQN', 'GRG', 'MBZ', 'NXJ', 'GCZ', 'ZOK', 'XCO', 'OJQ', 'EYB', 'KVE', 'HCZ', 'LTI', 'OQC', 'MXD', 'NVX', 'TGA', 'IRK'],# 'F',
    ['RIQ', 'HXV', 'UIU', 'ZXH', 'AZI', 'UNP', 'IRF', 'LHG', 'YNE', 'QMK', 'CJS', 'WXT', 'PWV', 'ZKB', 'PKZ', 'NFT', 'KOX', 'HWL', 'XKL', 'IGD'],# 'G', 
    ['YBP', 'KXR', 'XWX', 'UND', 'HVP', 'WAA', 'UVE', 'WQX', 'NBZ', 'HII', 'XGA', 'GPA', 'SOP', 'JHM', 'NGJ', 'OOK', 'PVU', 'YUA', 'THI', 'BHK'],# 'H', 
    ['WIP', 'NLO', 'UOU', 'TKF', 'HVS', 'BQY', 'HNE', 'FLO', 'SHG', 'QBL', 'KBQ', 'EJP', 'HUF', 'FJK', 'JFX', 'DMT', 'TFO', 'RGR', 'TOU', 'JWD'],# 'I',
    ['JGL', 'BIM', 'PPR', 'CSG', 'RCG', 'XLH', 'HGH', 'NDL', 'TYI', 'AOS', 'UQG', 'KRI', 'HYC', 'PHV', 'AHH', 'UYL', 'HEI', 'KOF', 'ESC', 'BAJ'],# 'J', 
    ['GOM', 'MPI', 'HOG', 'SQY', 'JAT', 'UYV', 'FRZ', 'NOI', 'HIA', 'XTW', 'RHV', 'VBQ', 'AYB', 'PBS', 'VVD', 'RCU', 'RRO', 'SNT', 'VST', 'MIQ'],# 'K', 
    ['CLR', 'FQS', 'CDR', 'UHG', 'MLS', 'KBP', 'FGR', 'NAM', 'VSN', 'EKL', 'ULE', 'UYX', 'RKD', 'HEQ', 'CYY', 'JNU', 'CPL', 'QNH', 'LEG', 'CLW'],# 'L',
    ['VCG', 'JQK', 'QZU', 'PFU', 'BQP', 'SGG', 'MWZ', 'IIJ', 'DHJ', 'BEN', 'QWP', 'UCQ', 'OQT', 'YRE', 'VLS', 'IDP', 'YOS', 'BYG', 'ZZP', 'AQD'],# 'M', 
    ['RNG', 'BXR', 'UPQ', 'OEZ', 'IND', 'DIX', 'GNV', 'MBA', 'XTS', 'TOT', 'WPF', 'GPZ', 'VBX', 'OVX', 'LQQ', 'USV', 'GUM', 'UZI', 'WGZ', 'GGB'],# 'N', 
    ['EKS', 'SBI', 'LAP', 'LHJ', 'VMT', 'EOL', 'WSY', 'NPO', 'OJP', 'RUZ', 'MIZ', 'NJC', 'EHF', 'VZO', 'IEW', 'VHQ', 'ASK', 'NMD', 'VTI', 'MQT'],# 'O', 
    ['WGF', 'NEY', 'YFZ', 'MGF', 'GVV', 'MUI', 'AOY', 'THQ', 'WNC', 'YWC', 'OLT', 'MXC', 'OAR', 'YGL', 'YUI', 'BCT', 'FHD', 'ISY', 'ZXY', 'MNE'],# 'P', 
    ['WUX', 'TKJ', 'RFR', 'GQZ', 'VRU', 'ZAY', 'VBU', 'POT', 'CVM', 'WNM', 'OFX', 'HES', 'NVM', 'DNH', 'WDQ', 'JGJ', 'VHO', 'GQX', 'BBA', 'SBW'],# 'Q', 
    ['DMB', 'MYL', 'SJQ', 'VUR', 'QAO', 'LCX', 'LRW', 'KWW', 'ABD', 'RQN', 'MCS', 'TGR', 'XGY', 'PWU', 'UIA', 'FIF', 'JXN', 'BXL', 'DDW', 'QLK'],# 'R', 
    ['YFV', 'XER', 'XXT', 'ZGM', 'ONH', 'KFZ', 'CSR', 'TIC', 'OAA', 'FNN', 'BZX', 'QTY', 'FOE', 'IAB', 'LFT', 'RSW', 'JHU', 'VLA', 'OMQ', 'EMO'],# 'S', 
    ['MBS', 'UDU', 'CGL', 'BHU', 'AHQ', 'HXZ', 'BDW', 'DKA', 'EVL', 'XCT', 'QWX', 'VGX', 'AAQ', 'VRL', 'AVY', 'TYX', 'LIJ', 'HIR', 'LPS', 'JQQ'],# 'T', 
    ['IFV', 'TNG', 'EIM', 'EWU', 'ANG', 'OKY', 'OKH', 'LOE', 'NCY', 'WMF', 'WBU', 'UDP', 'XIJ', 'HBT', 'JPA', 'DGE', 'ABU', 'REM', 'HVT', 'LYZ'],# 'U',
    ['TFJ', 'NYL', 'CQZ', 'VEI', 'YWX', 'JJT', 'IRW', 'KTR', 'NDX', 'DLE', 'FYJ', 'DCF', 'WGU', 'OEW', 'MUE', 'CZX', 'MZF', 'GCR', 'RPC', 'SNH'],# 'V', 
    ['XAE', 'EFX', 'PZP', 'BJQ', 'ISM', 'DMA', 'SRU', 'ZOQ', 'CFW', 'EZX', 'CPC', 'ZYH', 'QCB', 'EQP', 'UKT', 'OKP', 'UVV', 'RDK', 'OCD', 'VMJ'],# 'W', 
    ['FIB', 'JXX', 'WOI', 'VDC', 'TGD', 'IPS', 'MGX', 'BWT', 'ZQA', 'FYB', 'ABF', 'GAU', 'HDV', 'ZDD', 'BMW', 'CDL', 'IMJ', 'KVJ', 'MHU', 'CNP'],# 'X',
    ['BTK', 'AXL', 'DYP', 'ROZ', 'LFB', 'NJP', 'QHY', 'SMS', 'SJR', 'REF', 'OJD', 'RHU', 'GXZ', 'EUI', 'NFL', 'JDF', 'YTV', 'OTR', 'FOO', 'GWB'],# 'Y', 
    ['HKQ', 'BUA', 'BSO', 'UTC', 'MRE', 'GST', 'RIH', 'DUS', 'TRR', 'HMT', 'HYU', 'ANQ', 'DIE', 'KQM', 'QUM', 'IQO', 'OHM', 'OCQ', 'TQF', 'JOI'],# 'Z', 
    ['HFW', 'MXN', 'YFS', 'SYG', 'RRR', 'IKB', 'VBE', 'MZO', 'HQR', 'CZV', 'ESZ', 'NXC', 'PSE', 'MGS', 'URX', 'XOR', 'POH', 'BYW', 'HTT', 'RTI'],# '<', 
    ['QKL', 'HMQ', 'WLG', 'YJH', 'QNE', 'JFH', 'NVL', 'TRS', 'QWY', 'SNS', 'AIF', 'UAS', 'TXT', 'HEZ', 'ZOU', 'JGY', 'LDL', 'WCN', 'CFA', 'SXI'],# '>', 
    ['QGL', 'KZE', 'ZKN', 'KKG', 'YCH', 'NZI', 'XQY', 'AAX', 'YCR', 'PJG', 'AVX', 'DFM', 'TNM', 'SHC', 'SVG', 'PNI', 'QEB', 'WCV', 'DOD', 'LAT'],# '|', 
    ['QMU', 'EWT', 'VDK', 'OTZ', 'IPB', 'TXS', 'PKS', 'VYH', 'OWQ', 'YLM', 'ZJM', 'VSD', 'ZWH', 'YKS', 'AUX', 'LWF', 'UVC', 'GJF', 'COP', 'CZM'],# '~', 
    ['MSY', 'KNC', 'HWN', 'ILF', 'IYG', 'TFH', 'HAV', 'VBG', 'YTO', 'FWM', 'PAT', 'GLU', 'GPK', 'NJX', 'EMD', 'DLB', 'HRV', 'DFX', 'PAR', 'CYF'],# '$', 
    ['ILY', 'UHY', 'PDC', 'MSZ', 'IOJ', 'YKE', 'CFG', 'LIT', 'DMR', 'QUB', 'VID', 'BRO', 'GMG', 'DCZ', 'AUQ', 'FVY', 'UTO', 'NXX', 'MKC', 'OIY'],# '[', 
    ['IUO', 'UAU', 'VPA', 'SGH', 'FMD', 'SNF', 'OUX', 'EAF', 'AIR', 'KIQ', 'DWG', 'LFO', 'BIR', 'ESW', 'DIA', 'ZGA', 'ERB', 'LOY', 'FAX', 'CWZ'],# ']', 
    ['ZNY', 'TFV', 'OAZ', 'XJK', 'KPE', 'KDI', 'BIB', 'CGQ', 'ZTG', 'SCH', 'YHO', 'UGC', 'OCU', 'ZZZ', 'WTZ', 'VFO', 'DEO', 'DME', 'PBE', 'AVB'],# '{', 
    ['DWU', 'XTX', 'KAW', 'ZCF', 'LGC', 'DUD', 'LXP', 'IIN', 'MYV', 'VVN', 'HLR', 'SDQ', 'QPZ', 'PLX', 'WYR', 'PFL', 'KPI', 'EKW', 'SKF', 'HBR'],# '}',
    ['KSQ', 'BSD', 'TJR', 'LMN', 'QTX', 'ONV', 'PJO', 'RWC', 'ZEB', 'ZQG', 'MAH', 'GZW', 'BDP', 'FUW', 'YCQ', 'RCB', 'APR', 'FXO', 'LVQ', 'ZMB'],# '=',
    ['EZJ', 'SKP', 'SDN', 'GJO', 'NTZ', 'TWS', 'QOX', 'KKL', 'NNR', 'LFI', 'MIR', 'CLT', 'GZB', 'IWB', 'IDT', 'VIX', 'OIM', 'OEY', 'IWC', 'HXA'],# 'А', 
    ['ZOY', 'QYW', 'HVF', 'IJJ', 'ATM', 'GOP', 'AWK', 'VWP', 'OGC', 'MHP', 'ZHB', 'DAJ', 'LUJ', 'NWP', 'VVX', 'LWP', 'ECH', 'VNL', 'PVZ', 'XUC'],# 'Б', 
    ['EHQ', 'HCE', 'TQU', 'FBI', 'ENU', 'QKR', 'BUP', 'LXY', 'LTY', 'OOB', 'ZVC', 'WXH', 'ZBH', 'ORR', 'MRV', 'EAJ', 'KTK', 'ASY', 'JJJ', 'DII'],# 'В',
    ['UDI', 'FJA', 'NAU', 'HRU', 'SFR', 'JLY', 'VQD', 'HVH', 'KXX', 'TEM', 'GJJ', 'REV', 'PEB', 'OLQ', 'TLM', 'KRH', 'ONT', 'QVZ', 'ASW', 'TPW'],# 'Г', 
    ['QEM', 'QYX', 'VSI', 'NZM', 'NAJ', 'KYV', 'ZRQ', 'OSQ', 'IKH', 'IVV', 'HOC', 'BZE', 'PAI', 'VZK', 'ICT', 'DTK', 'PUE', 'DAY', 'QXS', 'VZM'],# 'Ґ', 
    ['MVR', 'DEH', 'AKO', 'VIB', 'ZRO', 'DSI', 'CFD', 'JKP', 'CLH', 'SYU', 'IUK', 'AIN', 'LPX', 'MJZ', 'TUV', 'QNW', 'ILH', 'YAF', 'HBJ', 'QQL'],# 'Д', 
    ['XYR', 'OUI', 'VKO', 'RFL', 'BIE', 'QJV', 'GWS', 'JZA', 'FIC', 'NQQ', 'HDF', 'JRP', 'JMU', 'YAB', 'QEK', 'LBX', 'ZTA', 'PBB', 'GAW', 'ZRM'],# 'Е', 
    ['PIE', 'ULX', 'RCJ', 'EGR', 'QMJ', 'MGA', 'STM', 'NZL', 'CXH', 'TEI', 'RQO', 'BNE', 'EIT', 'HAH', 'RUY', 'OTK', 'EYN', 'XIA', 'GMY', 'FQD'],# 'Є',
    ['IVA', 'YJU', 'ROL', 'WLR', 'JAQ', 'UGX', 'TME', 'NDI', 'SGC', 'QZQ', 'TIM', 'EEZ', 'KBM', 'SAW', 'CMD', 'QLH', 'QKQ', 'LVT', 'XBB', 'FIK'],# 'Ж', 
    ['UOJ', 'SUU', 'OVY', 'ANF', 'WWA', 'EWZ', 'ZIR', 'ACL', 'NUR', 'EWW', 'HXU', 'GCI', 'MTF', 'LGL', 'HPW', 'ZBK', 'XOM', 'JEE', 'ICB', 'IYK'],# 'З', 
    ['LPR', 'MWI', 'MZX', 'PGB', 'EYH', 'KCZ', 'AXT', 'TJH', 'DVF', 'BKD', 'KLW', 'QQO', 'FHN', 'GNI', 'NLR', 'PJV', 'PKI', 'FIZ', 'VBB', 'HBC'],# 'И', 
    ['CAQ', 'WVI', 'PQX', 'JEA', 'KYA', 'TOZ', 'KFL', 'CMP', 'YOA', 'OQO', 'UTA', 'EWN', 'TNF', 'UQA', 'KQJ', 'UHS', 'FTN', 'DUF', 'JDR', 'COM'],# 'І',
    ['ELR', 'GRT', 'CDI', 'MIX', 'FAB', 'ABI', 'YCW', 'THY', 'QSS', 'GXM', 'XTL', 'FOQ', 'EMW', 'EKM', 'VXH', 'BPO', 'IWM', 'QAV', 'XPT', 'IGT'],# 'Ї', 
    ['WKB', 'RAD', 'QAN', 'DUX', 'QGP', 'TSV', 'OGI', 'SNN', 'QDT', 'ULN', 'ULO', 'MKI', 'VQO', 'MSW', 'IYD', 'EAQ', 'VKM', 'PKV', 'GWN', 'EQZ'],# 'Й', 
    ['VZH', 'DAM', 'GJY', 'ICU', 'PIS', 'QVJ', 'YYL', 'BCN', 'QJI', 'ETZ', 'HBE', 'ZHT', 'TPY', 'CWY', 'VAO', 'DUC', 'OUL', 'IPC', 'ZZC', 'HUG'],# 'К', 
    ['IKR', 'GAO', 'GDU', 'CIM', 'XIU', 'RVQ', 'MNH', 'RFH', 'DQK', 'BRM', 'FAG', 'MUD', 'DHW', 'OUJ', 'QQM', 'KXU', 'NCE', 'FVX', 'DIQ', 'TQN'],# 'Л', 
    ['YVK', 'FLN', 'SRK', 'GRU', 'NYZ', 'CFN', 'QHU', 'GWD', 'UVL', 'QIV', 'QCQ', 'EKX', 'FHR', 'OFM', 'IBK', 'VMV', 'QNV', 'GFP', 'EKP', 'XMR'],# 'М', 
    ['STH', 'GHV', 'JPY', 'WCD', 'OVP', 'FQR', 'TGS', 'FWN', 'ABT', 'ODN', 'SSB', 'HVD', 'GNF', 'XOW', 'JND', 'VQS', 'QSZ', 'NRX', 'JNH', 'AYR'],# 'Н', 
    ['AOP', 'VKJ', 'VLH', 'UJF', 'YUT', 'VAV', 'YIQ', 'ZVZ', 'MQN', 'ECP', 'XMK', 'BCV', 'BYO', 'NVI', 'YWO', 'ECT', 'FNA', 'CHR', 'JSX', 'JRU'],# 'О', 
    ['IBC', 'XQP', 'QSV', 'FFL', 'JLA', 'VNW', 'EXI', 'HZA', 'WTY', 'WIQ', 'FTE', 'UBH', 'GEE', 'GSN', 'AKJ', 'TRX', 'WKX', 'ZQW', 'VNM', 'FPF'],# 'П', 
    ['ZHR', 'WIV', 'YTD', 'BOY', 'FVQ', 'SJY', 'THC', 'IJA', 'XZL', 'HDQ', 'FRI', 'TPV', 'BYA', 'CYT', 'UGU', 'YNL', 'CPD', 'RKA', 'NJU', 'IBD'],# 'Р', 
    ['NTN', 'CIV', 'NFF', 'YBA', 'JMD', 'BCY', 'NJS', 'XNX', 'TUM', 'JPJ', 'DWO', 'XUA', 'BWN', 'AOT', 'OQF', 'CRJ', 'WCP', 'YDK', 'MTR', 'BKG'],# 'С', 
    ['DBS', 'QTE', 'TVX', 'VPZ', 'SVF', 'DES', 'OWL', 'MQX', 'PSX', 'EQB', 'SYD', 'PGE', 'IZE', 'ZLF', 'AOL', 'WOB', 'JRC', 'JHA', 'IJX', 'WWO'],# 'Т', 
    ['CMB', 'AJE', 'JFN', 'WVH', 'WKF', 'NQK', 'KGR', 'HGZ', 'DQT', 'YQM', 'WHO', 'NRI', 'KCC', 'EUG', 'CQA', 'WHG', 'TRZ', 'OEN', 'PKE', 'ROB'],# 'У', 
    ['PRN', 'PXE', 'BUR', 'UDZ', 'VEN', 'DLS', 'FSN', 'WLW', 'ALX', 'LHZ', 'ZPD', 'GTJ', 'BLV', 'FGH', 'AVW', 'LFU', 'MWK', 'WAX', 'NXE', 'PSV'],# 'Ф', 
    ['GJG', 'OMR', 'TMX', 'MVG', 'FFF', 'XQS', 'EPM', 'PTV', 'IDQ', 'WUG', 'RXU', 'LSK', 'OYR', 'ERE', 'HKR', 'OYY', 'TWJ', 'SNZ', 'CGD', 'LUE'],# 'Х', 
    ['PPC', 'PYW', 'FJL', 'ROQ', 'UJR', 'YFX', 'HSO', 'PHZ', 'GJR', 'DGM', 'BZV', 'ZNB', 'CHJ', 'XEK', 'VLO', 'RDU', 'EBY', 'ITD', 'WRL', 'POV'],# 'Ц', 
    ['ZPZ', 'LVA', 'HLM', 'AUZ', 'FFG', 'PQD', 'ZSH', 'GCO', 'COC', 'RKU', 'GZE', 'BDO', 'JWX', 'LYR', 'ZVG', 'ZEL', 'NIJ', 'OKW', 'AXD', 'TLH'],# 'Ч', 
    ['UMS', 'EEC', 'GAZ', 'VLD', 'RWO', 'MXE', 'MPM', 'ZHI', 'SBV', 'HBA', 'EBE', 'QZD', 'NAE', 'QMQ', 'MEB', 'OAI', 'ETH', 'JGK', 'OMU', 'PMN'],# 'Ш', 
    ['KBJ', 'IBS', 'DDO', 'EVY', 'PJY', 'RDC', 'QEC', 'XMM', 'ARK', 'GFV', 'CJK', 'HSQ', 'RYS', 'ZNQ', 'DCR', 'PXF', 'RGH', 'UTY', 'STW', 'ZZN'],# 'Щ', 
    ['NHH', 'KMP', 'CLX', 'PID', 'DLI', 'XAJ', 'NAK', 'WHY', 'VIK', 'MVM', 'HKE', 'PXM', 'OLC', 'EZR', 'VWT', 'UVG', 'ZME', 'DCC', 'NMY', 'ZHE'],# 'Ь', 
    ['ZKS', 'JXD', 'JKE', 'UHF', 'VJD', 'ACJ', 'QKG', 'MSV', 'UJX', 'LRI', 'JPG', 'RBH', 'MSK', 'QUD', 'HNU', 'IHX', 'UMN', 'TXF', 'QNY', 'JRD'],# 'Ю', 
    ['XHO', 'INC', 'IIW', 'YTM', 'QAF', 'OJB', 'PRV', 'VEU', 'TXP', 'QMV', 'WYK', 'SIS', 'MGC', 'KWB', 'TGZ', 'IXM', 'UYQ', 'UJO', 'INW', 'VII'],# 'Я',
    ['ESA', 'THJ', 'CKX', 'IMD', 'GYU', 'LGP', 'QOF', 'OPJ', 'YNO', 'WDN', 'BFG', 'TBE', 'IUP', 'SNW', 'WJZ', 'HTM', 'XOC', 'MZT', 'BDS', 'TIA'],# 'Ё', 
    ['PDG', 'UTR', 'HQT', 'FOX', 'ZTO', 'EDQ', 'OUN', 'GSP', 'ZXQ', 'TMO', 'MFM', 'OVW', 'IMP', 'NBB', 'CLA', 'MJU', 'UBK', 'LIW', 'ECJ', 'JET'],# 'Ъ', 
    ['TFN', 'GQY', 'OBG', 'XPQ', 'BMN', 'VHE', 'PZC', 'PCH', 'WEQ', 'CVG', 'CMI', 'ACP', 'GBO', 'YCC', 'IKM', 'ZYG', 'QWZ', 'BDH', 'RZC', 'MUF'],# 'Ы', 
    ['HON', 'WXU', 'HVV', 'SAT', 'QGR', 'WES', 'YRX', 'CEI', 'IHH', 'CXA', 'FLR', 'CPT', 'ENO', 'PRX', 'YVQ', 'HDU', 'HUY', 'HLN', 'ZON', 'XBC'],# 'Э', 
    ['TZA', 'DDD', 'DHY', 'YUM', 'XLC', 'ERQ', 'BXU', 'WPM', 'AYM', 'QGZ', 'VSY', 'YAR', 'ZKX', 'QZL', 'LJB', 'CJM', 'OGA', 'IZN', 'JYQ', 'WNQ'],# 'а', 
    ['TTF', 'DTM', 'NSE', 'LJX', 'ROF', 'ACA', 'ABL', 'PAL', 'ZUX', 'GQG', 'VIO', 'AJH', 'BWJ', 'CCA', 'SLW', 'YYS', 'FNV', 'XKF', 'BNX', 'ZTK'],# 'б', 
    ['YAO', 'TPO', 'GUE', 'EJF', 'FAM', 'EVF', 'UIH', 'EGU', 'SRW', 'UKS', 'VDW', 'QTT', 'IXQ', 'PLO', 'JST', 'GBX', 'ARL', 'COR', 'TOG', 'HGJ'],# 'в', 
    ['WKJ', 'ELB', 'PEZ', 'PTX', 'GHS', 'IYE', 'TCX', 'RBY', 'IOM', 'UFT', 'XYF', 'LEJ', 'YIB', 'ETP', 'QFO', 'GLR', 'MDS', 'BYH', 'CME', 'LDP'],# 'г', 
    ['WTC', 'JLG', 'FAR', 'KHW', 'KRA', 'WEB', 'IGZ', 'OWS', 'OUK', 'UEY', 'RMU', 'QGO', 'BXV', 'LUG', 'TVK', 'JZG', 'DUI', 'IUR', 'RWA', 'DBY'],# 'ґ', 
    ['WCR', 'QGB', 'BTG', 'EFS', 'WKY', 'MDP', 'NCK', 'CKK', 'GTL', 'RRL', 'SUR', 'PVX', 'KZO', 'HGX', 'HZM', 'NIL', 'EUM', 'FMS', 'HER', 'WMI'],# 'д', 
    ['VLV', 'FAW', 'WGB', 'RSH', 'VWG', 'BXA', 'KIC', 'CMC', 'RON', 'DSV', 'MIU', 'DBT', 'AGG', 'HEV', 'ANY', 'UGF', 'KMQ', 'TTB', 'WYP', 'UIP'],# 'е', 
    ['OZX', 'UJM', 'CSW', 'KFD', 'QSX', 'HCJ', 'JCG', 'VNA', 'NET', 'ILW', 'UTI', 'TYK', 'UBW', 'SYK', 'HIS', 'FMB', 'TGO', 'LMJ', 'GKS', 'PBN'],# 'є', 
    ['VHM', 'YGS', 'EUO', 'DAN', 'QSQ', 'VKQ', 'TFP', 'JFD', 'DPB', 'WSR', 'ROG', 'XPP', 'VTR', 'GOX', 'RQU', 'XXX', 'ELT', 'HJX', 'OSN', 'LYY'],# 'ж', 
    ['QAR', 'TAW', 'WZK', 'IUU', 'OUV', 'BXM', 'PRT', 'KTC', 'ZHX', 'JIP', 'XQI', 'IZT', 'KZC', 'KPZ', 'KAM', 'TDG', 'UBJ', 'CJJ', 'JOB', 'ALF'],# 'з', 
    ['FYU', 'UIK', 'WJO', 'UMA', 'IMA', 'AYK', 'DDF', 'TAQ', 'QHW', 'VZU', 'KWT', 'SFP', 'GDV', 'RTR', 'TTA', 'JNL', 'XVL', 'KDT', 'OZB', 'MEC'],# 'и', 
    ['BZS', 'LEW', 'OOM', 'CPA', 'TST', 'CWP', 'BVQ', 'XNI', 'WBP', 'LFW', 'YZC', 'KMF', 'NJT', 'FJW', 'PEI', 'FOM', 'QDX', 'GUI', 'VAL', 'KSP'],# 'і', 
    ['WBV', 'UIJ', 'ZSV', 'CRQ', 'OKE', 'PYY', 'YIK', 'PKW', 'YDB', 'OIP', 'VEQ', 'PQP', 'HMG', 'PTC', 'SKZ', 'ZTS', 'NSQ', 'VLM', 'KBH', 'UOD'],# 'ї', 
    ['GOF', 'QWK', 'XKD', 'OXH', 'GHT', 'SXS', 'KKO', 'XLE', 'ZYM', 'KBX', 'DHZ', 'NWY', 'YFT', 'RLX', 'HLF', 'ETO', 'LFA', 'KCA', 'MZD', 'YLA'],# 'й', 
    ['ACO', 'TIV', 'HPP', 'RUB', 'BPI', 'VEX', 'UDW', 'XZQ', 'FRN', 'KIW', 'QKA', 'APX', 'ZUV', 'GBF', 'KQD', 'KSU', 'DSH', 'WFG', 'GTO', 'NGV'],# 'к', 
    ['PYP', 'MCR', 'BKX', 'SUF', 'WPI', 'ETL', 'XMP', 'WTE', 'HSM', 'DOE', 'UCA', 'HAE', 'GEP', 'ONA', 'ULD', 'UTU', 'THE', 'WNX', 'PWC', 'TOB'],# 'л', 
    ['BYJ', 'CMR', 'YZU', 'NIG', 'JIX', 'ASI', 'WCJ', 'EOK', 'TCW', 'AOR', 'QWB', 'ZBI', 'EVK', 'JCD', 'JLW', 'NYQ', 'BWI', 'HRN', 'LJU', 'PNM'],# 'м', 
    ['FDQ', 'KQN', 'QBB', 'EWE', 'WAI', 'IXK', 'PLY', 'DOM', 'FJQ', 'GCT', 'AHX', 'HKL', 'PER', 'TFU', 'CXS', 'JSH', 'LZF', 'SAU', 'GDB', 'RNV'],# 'н', 
    ['DLM', 'AVP', 'ZIY', 'WAL', 'UCM', 'HUT', 'QBX', 'TNA', 'BPU', 'AXX', 'QWR', 'ZTE', 'JAJ', 'YFY', 'FWF', 'GHB', 'SAF', 'LTG', 'SMN', 'VZN'],# 'о', 
    ['OIL', 'CHE', 'WVV', 'EDZ', 'TBP', 'WFK', 'JXW', 'WLH', 'WRG', 'TZU', 'ZNS', 'XZM', 'SRD', 'UJS', 'TWR', 'QIZ', 'NCU', 'NZD', 'YJR', 'FLM'],# 'п', 
    ['MZC', 'GGR', 'LZA', 'ONW', 'WAH', 'IAS', 'JDQ', 'ORZ', 'QCP', 'SJD', 'ERR', 'LUZ', 'UQM', 'YWZ', 'VZD', 'AMP', 'AQZ', 'BIA', 'NMM', 'QVX'],# 'р', 
    ['OEM', 'YAN', 'XQF', 'YXR', 'TDW', 'HUE', 'HFJ', 'IKC', 'NGP', 'QIA', 'WCA', 'ULR', 'QXC', 'RLB', 'EJV', 'NUN', 'KZI', 'JFP', 'KRX', 'AAL'],# 'с', 
    ['MWR', 'CPJ', 'QVB', 'YQD', 'IYF', 'OCL', 'PHM', 'GOJ', 'RSO', 'TZE', 'GEH', 'WFY', 'IIA', 'JVL', 'VYT', 'PYH', 'THA', 'SXH', 'CUK', 'FGP'],# 'т', 
    ['CBY', 'PYZ', 'FMK', 'FEQ', 'WUC', 'XWE', 'AML', 'YNQ', 'FUA', 'TCO', 'YYJ', 'BVU', 'BRW', 'PWW', 'YQT', 'QZW', 'KVI', 'NRN', 'JBF', 'WXJ'],# 'у',
    ['GPG', 'DQG', 'YKB', 'LGF', 'QOA', 'NNP', 'BJH', 'JAA', 'EQH', 'DNI', 'FOL', 'NDB', 'XDS', 'MCT', 'ZED', 'VDN', 'DNR', 'PMP', 'KTL', 'MZH'],# 'ф', 
    ['IXP', 'OLE', 'IHJ', 'CLK', 'BCC', 'JEC', 'QFQ', 'GWZ', 'SEN', 'BPD', 'VOC', 'JRT', 'KJV', 'ICS', 'IIK', 'CUJ', 'GVF', 'OSD', 'RPO', 'VIV'],# 'х', 
    ['YIY', 'QAW', 'HNR', 'KSJ', 'CXP', 'WHD', 'UBV', 'HTX', 'YPC', 'QHH', 'VVM', 'CON', 'HKX', 'DYB', 'RZW', 'VDV', 'SOZ', 'YFQ', 'RAN', 'IMN'],# 'ц', 
    ['JDL', 'EOI', 'YPJ', 'BDN', 'FDD', 'KIV', 'FZE', 'NJW', 'NRA', 'UDV', 'TLE', 'RSZ', 'WEA', 'RUT', 'AHA', 'BWS', 'RZY', 'JMN', 'RVW', 'OZW'],# 'ч', 
    ['WCO', 'NLT', 'OJS', 'PJC', 'OMD', 'ODM', 'ZNI', 'MFN', 'GPP', 'JIZ', 'FAZ', 'PGA', 'KUK', 'IPM', 'ALI', 'AIP', 'NGZ', 'FQY', 'YSZ', 'FMC'],# 'ш', 
    ['FWZ', 'FUS', 'EEE', 'DZL', 'XBX', 'DWD', 'BOD', 'QIU', 'AFH', 'RAW', 'NMW', 'AJS', 'UWM', 'CWE', 'NMJ', 'SHZ', 'WYB', 'YCE', 'WHJ', 'LJW'],# 'щ', 
    ['BOV', 'JKT', 'HSG', 'ZMU', 'VSC', 'ZBZ', 'ILO', 'LIU', 'RYQ', 'VAF', 'BGO', 'NTQ', 'WZT', 'EMA', 'AEA', 'QRS', 'XYS', 'XWL', 'WJF', 'DXI'],# 'ь', 
    ['RZN', 'TQM', 'VCP', 'RJB', 'NCH', 'FZT', 'TXM', 'TFW', 'DKS', 'SUT', 'VRJ', 'GSW', 'NSZ', 'JBJ', 'USY', 'SRL', 'IMW', 'VIH', 'QAE', 'GXN'],# 'ю',
    ['WYM', 'JFC', 'KTS', 'YKJ', 'DCY', 'TYW', 'PVG', 'NAQ', 'GOD', 'JVE', 'HAU', 'GNM', 'QCS', 'QQI', 'VMW', 'NUE', 'PHD', 'ZKT', 'MXF', 'QHI'],# 'я',
    ['AOV', 'GKO', 'MUQ', 'OJJ', 'NQU', 'XAA', 'HHT', 'GRJ', 'YON', 'YJI', 'SNP', 'KFQ', 'ETJ', 'KNX', 'SXM', 'VYO', 'DBM', 'GUR', 'TEB', 'PHU'],# 'ё', 
    ['LAK', 'ADP', 'KCW', 'PKT', 'VXO', 'UIF', 'QXJ', 'RKV', 'AZC', 'NOE', 'HJG', 'MQM', 'USK', 'ZCE', 'FJM', 'XAZ', 'ZWA', 'TZO', 'HWT', 'JGG'],# 'ъ', 
    ['MIP', 'CPZ', 'LGX', 'VND', 'MWO', 'AQE', 'JEQ', 'RRF', 'RLA', 'ERN', 'CKC', 'REG', 'WAV', 'LWK', 'BUW', 'SGV', 'BDT', 'MGN', 'BSW', 'TXV'],# 'ы', 
    ['YHC', 'PIU', 'QFM', 'BZN', 'PYB', 'VEC', 'IOR', 'OJX', 'VFC', 'GVH', 'FLK', 'CGI', 'XHU', 'CTK', 'LQC', 'INI', 'ZTX', 'VPK', 'ZKZ', 'PPL'],# 'э'
    ['KLK', 'XMH', 'JTA', 'DHR', 'VRI', 'TKA', 'GHL', 'FUU', 'GCK', 'EFK', 'BVW', 'QZC', 'GJB', 'NQC', 'EXG', 'WCY', 'EHI', 'XYB', 'RUS', 'APT'] # ' '
    ]
    




def code(text):
    output = ""
    letters_list = list(text)

    for l in range(len(letters_list)):
        for i in range(len(letters)):
            if letters_list[l] == letters[i]:
                output += codes1[i][random.randint(0,19)]
                break  
    return output

##################################################
def decode(text1):
    output = ""
    letters_list1 = list(text1)

    for i in range(0, len(letters_list1), 3):
        three = "".join(letters_list1[i:i+3])
        for u in range(165):
            for j in range(20):
                if three == codes1[u][j]:
                    output += letters[u]
    return output
#################################################







