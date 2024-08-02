class Config:
    BASE_URL = "http://120.26.59.7:23262"
    UPLOAD_FILE_URL = f"{BASE_URL}/docxFile2rule"  # 上传文件
    CHECK_ATOM_RULE_URL = f"{BASE_URL}/checkAtomRule"  # 判断原子条例
    SPLIT_ATOMIC_RULES_URL = f"{BASE_URL}/splitAtomRule"  # 分割原子规则
    IDENTIFY_RULES_URL = f"{BASE_URL}/identifyRule"  # 识别规则
    CLASSIFY_RULES_URL = f"{BASE_URL}/classifyRule"  # 分类规则
    EXTRACT_COMMON_RULES_URL = f"{BASE_URL}/extractCommonElement"  # 提取通用规则
    GENERATE_CDSRL_URL = f"{BASE_URL}/generateCDSRL"  # 输出条例对应的监管语⾔
