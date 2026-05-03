import json, os, re
from pathlib import Path
from rapidfuzz import fuzz
from unidecode import unidecode
from tqdm import tqdm
import arxiv
import bibtexparser
import requests
from bs4 import BeautifulSoup
import hashlib
from datetime import datetime
import urllib.parse
import time

DATA = Path("data")
DATA.mkdir(exist_ok=True)

CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)

# Keywords
APR_TERMS = [
    "program repair", "automatic program repair", "APR",
    "bug fixing", "patch generation", "patch synthesis",
    "code repair", "vulnerability repair", "automated repair",
    "vulnerability fixing", "vulnerability patching", "security patch",
    "CVE repair", "vulnerability mitigation"
]
LLM_TERMS = [
    "large language model", "LLM", "GPT", "CodeX", "CodeT5",
    "StarCoder", "LLaMA", "Llama", "transformer", "neural network", 
    "generative model", "deep learning", "DeepSeek", "Claude",
    "Incoder", "CodeGen", "BERT"
]
BENCH_TERMS = [
    # 通用 APR benchmarks
    "Defects4J", "SWE-bench", "SWE-bench Lite", "SWE-bench Verified", "SWE-bench Multimodal",
    "QuixBugs", "Bugs.jar", "HumanEvalFix", "HumanEval-Java", "HumanEval-Perl",
    "IntroClass", "ManySStuBs4J", "CodeFLAWS", "Bears", "d4j", "humaneval",
    # 漏洞相关 benchmarks
    "CVEFixes", "Big-Vul", "VulnLoc", "ExtractFix", "InstructVul",
    # 其他 benchmarks
    "BugsInPy", "RepoBugs", "LMDefects", "TutorCode", "MBPP", "APPS",
    "CodeNet", "CodeNet4Repair", "ACPR", "InferredBugs", "PyTyDefects",
    "LeetCode", "MODIT", "ATLAS", "DS-1000", "Zero-Day", "xCodeEval",
    "ARVO", "APR Competition", "LoopInv", "BFP"
]
TOOL_TERMS = [
    # Agentic
    "RepairAgent", "AutoCodeRover", "Autocoderover",  # AutoCodeRover 的变体
    "SWE-agent", "SWE-Agent", "Swe-agent",  # SWE-agent 的变体
    "OpenHands", "Openhands",  # OpenHands 的变体
    "LANTERN", "VulDebugger", "Magis", "MAGIS",  # Magis 的变体
    "SWE-Search", "Learn-by-Interact", "Learn-by-interact",  # 大小写变体
    # Procedural
    "ChatRepair", "ThinkRepair", "Thinkrepair",  # ThinkRepair 的变体
    "ContrastRepair", "Contrastrepair",  # ContrastRepair 的变体
    "Agentless", "REx",
    "CREF", "Cref",  # CREF 的变体
    "HULA", "DRCodePilot", "PATCH", "KGCompass",
    "Repilot", "SAN2PATCH", "PredicateFix", "LLM4CVE",
    # Prompting
    "AlphaRepair", "CEDAR", "RLCE", "DSrepair", "D4C", 
    "Appatch", "APPATCH",  # Appatch 的变体
    "TracePrompt",
    # Fine-tuning
    "VulMaster", "RepairCAT", "RepairLLaMA", "Repairllama",  # RepairLLaMA 的变体
    "MORepair", "KNOD", "Knod",  # KNOD 的变体
    "DistiLRR", "NARRepair", "Narrepair",  # NARRepair 的变体
    "RePair", "SecRepair",
    "Swe-rl", "SWE-RL", "Swe-agent",  # SWE-RL 的变体
    "AdaPatcher", "Vul-R2", "VulR2",  # Vul-R2 的变体 
    "Tracefixer", "TraceFixer",  # TraceFixer 的变体
    "InferFix", "Inferfix",  # InferFix 的变体
    "PyTy", "Pyty",  # PyTy 的变体
    "NTR",
    # LLM-as-Judges
    "TSAPR", "SpecRover", "Abstain and Validate",
    # Legacy/Other
    "CURE", "CoCoNut", "Recoder", "FitRepair"
]

MANDATORY_ARXIV_IDS = [
    # 保留此机制用于特殊情况（如已知arXiv API搜索不到的论文）
    # 但正常情况下应该为空，让搜索策略自己找到论文
]

# ========== 通用数据源配置 ==========
SOURCE_CONFIG = [
    # ICSE (2022-2026)
    {"id": "icse-2022", "venue": "ICSE", "year": 2022, "type": "conference", "parser": "researchr_track",
     "url": "https://conf.researchr.org/track/icse-2022/icse-2022-papers", "track_keyword": "Technical Track"},
    {"id": "icse-2023", "venue": "ICSE", "year": 2023, "type": "conference", "parser": "researchr_track",
     "url": "https://conf.researchr.org/track/icse-2023/icse-2023-technical-track", "track_keyword": "Technical Track"},
    {"id": "icse-2024", "venue": "ICSE", "year": 2024, "type": "conference", "parser": "researchr_track",
     "url": "https://conf.researchr.org/track/icse-2024/icse-2024-research-track", "track_keyword": "Research Track"},
    {"id": "icse-2025", "venue": "ICSE", "year": 2025, "type": "conference", "parser": "researchr_track",
     "url": "https://conf.researchr.org/track/icse-2025/icse-2025-research-track", "track_keyword": "Research Track"},
    {"id": "icse-2026", "venue": "ICSE", "year": 2026, "type": "conference", "parser": "researchr_track",
     "url": "https://conf.researchr.org/track/icse-2026/icse-2026-research-track", "track_keyword": "Research Track"},
    
    # FSE (2022-2026)
    {"id": "fse-2022", "venue": "FSE", "year": 2022, "type": "conference", "parser": "researchr_track",
     "url": "https://conf.researchr.org/track/fse-2022/fse-2022-research-papers", "track_keyword": "Research Papers"},
    {"id": "fse-2023", "venue": "FSE", "year": 2023, "type": "conference", "parser": "researchr_track",
     "url": "https://conf.researchr.org/track/fse-2023/fse-2023-research-papers", "track_keyword": "Research Papers"},
    {"id": "fse-2024", "venue": "FSE", "year": 2024, "type": "conference", "parser": "researchr_track",
     "url": "https://conf.researchr.org/track/fse-2024/fse-2024-research-papers", "track_keyword": "Research Papers"},
    {"id": "fse-2025", "venue": "FSE", "year": 2025, "type": "conference", "parser": "researchr_track",
     "url": "https://conf.researchr.org/track/fse-2025/fse-2025-research-papers", "track_keyword": "Research Papers"},
    {"id": "fse-2026", "venue": "FSE", "year": 2026, "type": "conference", "parser": "researchr_track",
     "url": "https://conf.researchr.org/track/fse-2026/fse-2026-research-papers", "track_keyword": "Research Papers"},
    
    # ASE (2022-2025)
    {"id": "ase-2022", "venue": "ASE", "year": 2022, "type": "conference", "parser": "researchr_track",
     "url": "https://conf.researchr.org/track/ase-2022/ase-2022-research-papers", "track_keyword": "Research Papers"},
    {"id": "ase-2023", "venue": "ASE", "year": 2023, "type": "conference", "parser": "researchr_track",
     "url": "https://conf.researchr.org/track/ase-2023/ase-2023-papers", "track_keyword": "Research Papers"},
    {"id": "ase-2024", "venue": "ASE", "year": 2024, "type": "conference", "parser": "researchr_track",
     "url": "https://conf.researchr.org/track/ase-2024/ase-2024-papers", "track_keyword": "Research Papers"},
    {"id": "ase-2025", "venue": "ASE", "year": 2025, "type": "conference", "parser": "researchr_track",
     "url": "https://conf.researchr.org/track/ase-2025/ase-2025-papers", "track_keyword": "Research Papers"},
    
    # ISSTA (2022-2026)
    {"id": "issta-2022", "venue": "ISSTA", "year": 2022, "type": "conference", "parser": "researchr_track",
     "url": "https://conf.researchr.org/track/issta-2022/issta-2022-technical-papers", "track_keyword": "Technical Papers"},
    {"id": "issta-2023", "venue": "ISSTA", "year": 2023, "type": "conference", "parser": "researchr_track",
     "url": "https://conf.researchr.org/track/issta-2023/issta-2023-technical-papers", "track_keyword": "Technical Papers"},
    {"id": "issta-2024", "venue": "ISSTA", "year": 2024, "type": "conference", "parser": "researchr_track",
     "url": "https://2024.issta.org/track/issta-2024-papers#event-overview", "track_keyword": "Technical Papers"},
    {"id": "issta-2025", "venue": "ISSTA", "year": 2025, "type": "conference", "parser": "researchr_track",
     "url": "https://conf.researchr.org/track/issta-2025/issta-2025-papers", "track_keyword": "Papers"},
    {"id": "issta-2026", "venue": "ISSTA", "year": 2026, "type": "conference", "parser": "researchr_track",
     "url": "https://conf.researchr.org/track/issta-2026/issta-2026-research-papers", "track_keyword": "Research papers"},
    
    # USENIX Security (2022-2025) - Summer and Fall cycles
    {"id": "usenix-sec-2022-summer", "venue": "USENIX Security", "year": 2022, "type": "conference", "parser": "usenix_accepted",
     "url": "https://www.usenix.org/conference/usenixsecurity22/summer-accepted-papers"},
    {"id": "usenix-sec-2022-fall", "venue": "USENIX Security", "year": 2022, "type": "conference", "parser": "usenix_accepted",
     "url": "https://www.usenix.org/conference/usenixsecurity22/fall-accepted-papers"},
    {"id": "usenix-sec-2023-summer", "venue": "USENIX Security", "year": 2023, "type": "conference", "parser": "usenix_accepted",
     "url": "https://www.usenix.org/conference/usenixsecurity23/summer-accepted-papers"},
    {"id": "usenix-sec-2023-fall", "venue": "USENIX Security", "year": 2023, "type": "conference", "parser": "usenix_accepted",
     "url": "https://www.usenix.org/conference/usenixsecurity23/fall-accepted-papers"},
    {"id": "usenix-sec-2024-summer", "venue": "USENIX Security", "year": 2024, "type": "conference", "parser": "usenix_accepted",
     "url": "https://www.usenix.org/conference/usenixsecurity24/summer-accepted-papers"},
    {"id": "usenix-sec-2024-fall", "venue": "USENIX Security", "year": 2024, "type": "conference", "parser": "usenix_accepted",
     "url": "https://www.usenix.org/conference/usenixsecurity24/fall-accepted-papers"},
    {"id": "usenix-sec-2025-c1", "venue": "USENIX Security", "year": 2025, "type": "conference", "parser": "usenix_accepted",
     "url": "https://www.usenix.org/conference/usenixsecurity25/cycle1-accepted-papers"},
    {"id": "usenix-sec-2025-main", "venue": "USENIX Security", "year": 2025, "type": "conference", "parser": "usenix_accepted",
     "url": "https://www.usenix.org/conference/usenixsecurity25/technical-sessions"},
    
    # APR Workshop (ICSE co-located)
    {"id": "apr-2023", "venue": "APR", "year": 2023, "type": "workshop", "parser": "apr_workshop",
     "url": "https://program-repair.org/workshop-2023/"},
    {"id": "apr-2024", "venue": "APR", "year": 2024, "type": "workshop", "parser": "apr_workshop",
     "url": "https://conf.researchr.org/program/icse-2024/program-icse-2024/?track=APR"},
    {"id": "apr-2025", "venue": "APR", "year": 2025, "type": "workshop", "parser": "apr_workshop",
     "url": "https://program-repair.org/workshop-2025/"},
    
    # TOSEM (Journal) - 使用OpenAlex API
    {"id": "tosem-openalex", "venue": "TOSEM", "type": "journal", "parser": "openalex_journal",
     "openalex_id": "S142627899", "years": [2022, 2023, 2024, 2025, 2026]},
    
    # TSE (Journal) - 使用OpenAlex API
    {"id": "tse-openalex", "venue": "TSE", "type": "journal", "parser": "openalex_journal",
     "openalex_id": "S8351582", "years": [2022, 2023, 2024, 2025, 2026]},

    # AAAI (Conference 2022-2026) - 使用OpenReview accepted venue
    {"id": "aaai-2022", "venue": "AAAI", "year": 2022, "type": "conference", "parser": "openreview_venue",
     "venue_name": "AAAI 2022", "venue_patterns": ["AAAI 2022"]},
    {"id": "aaai-2023", "venue": "AAAI", "year": 2023, "type": "conference", "parser": "openreview_venue",
     "venue_name": "AAAI 2023", "venue_patterns": ["AAAI 2023"]},
    {"id": "aaai-2024", "venue": "AAAI", "year": 2024, "type": "conference", "parser": "openreview_venue",
     "venue_name": "AAAI 2024", "venue_patterns": ["AAAI 2024"]},
    {"id": "aaai-2025", "venue": "AAAI", "year": 2025, "type": "conference", "parser": "openreview_venue",
     "venue_name": "AAAI 2025", "venue_patterns": ["AAAI 2025"]},
    {"id": "aaai-2026", "venue": "AAAI", "year": 2026, "type": "conference", "parser": "openreview_venue",
     "venue_name": "AAAI 2026", "venue_patterns": ["AAAI 2026"]},
    
    # NeurIPS (Conference 2022-2024) - 使用网页爬虫
    {"id": "neurips-2022", "venue": "NeurIPS", "year": 2022, "type": "conference", "parser": "nips_web",
     "url": "https://papers.nips.cc/paper_files/paper/2022"},
    {"id": "neurips-2023", "venue": "NeurIPS", "year": 2023, "type": "conference", "parser": "nips_web",
     "url": "https://papers.nips.cc/paper_files/paper/2023"},
    {"id": "neurips-2024", "venue": "NeurIPS", "year": 2024, "type": "conference", "parser": "nips_web",
     "url": "https://papers.nips.cc/paper_files/paper/2024"},
    
    # ACL (Conference 2023-2025) - 使用网页爬虫
    # Main Conference Papers
    {"id": "acl-2023-main", "venue": "ACL", "year": 2023, "type": "conference", "parser": "acl_web",
     "url": "https://2023.aclweb.org/program/accepted_main_conference/", "paper_type": "main"},
    {"id": "acl-2024-main", "venue": "ACL", "year": 2024, "type": "conference", "parser": "acl_web",
     "url": "https://2024.aclweb.org/program/main_conference_papers/", "paper_type": "main"},
    {"id": "acl-2025-main", "venue": "ACL", "year": 2025, "type": "conference", "parser": "acl_web",
     "url": "https://2025.aclweb.org/program/main_papers/", "paper_type": "main"},
    # Findings Papers
    {"id": "acl-2023-findings", "venue": "ACL", "year": 2023, "type": "conference", "parser": "acl_web",
     "url": "https://2023.aclweb.org/program/accepted_findings/", "paper_type": "findings"},
    {"id": "acl-2024-findings", "venue": "ACL", "year": 2024, "type": "conference", "parser": "acl_web",
     "url": "https://2024.aclweb.org/program/finding_papers/", "paper_type": "findings"},
    {"id": "acl-2025-findings", "venue": "ACL", "year": 2025, "type": "conference", "parser": "acl_web",
     "url": "https://2025.aclweb.org/program/find_papers/", "paper_type": "findings"},
    {"id": "acl-2026-openreview", "venue": "ACL", "year": 2026, "type": "conference", "parser": "openreview_venue",
     "venue_name": "ACL 2026",
     "venue_patterns": ["ACL 2026 Main", "ACL 2026 Findings", "Findings of ACL 2026"]},
    
    # ICLR (Conference 2022-2026)
    # 2022-2024使用GitHub精选列表，2025使用OpenReview完整列表
    {"id": "iclr-2022", "venue": "ICLR", "year": 2022, "type": "conference", "parser": "iclr_github",
     "url": "https://raw.githubusercontent.com/yinizhilian/ICLR2025-Papers-with-Code/main/ICLR2022-Papers-with-Code.md"},
    {"id": "iclr-2023", "venue": "ICLR", "year": 2023, "type": "conference", "parser": "iclr_github",
     "url": "https://raw.githubusercontent.com/yinizhilian/ICLR2025-Papers-with-Code/main/ICLR2023-Papers-with-Code.md"},
    {"id": "iclr-2024", "venue": "ICLR", "year": 2024, "type": "conference", "parser": "iclr_github",
     "url": "https://raw.githubusercontent.com/yinizhilian/ICLR2025-Papers-with-Code/main/ICLR2024-Papers-with-Code.md"},
    {"id": "iclr-2025", "venue": "ICLR", "year": 2025, "type": "conference", "parser": "openreview_venue",
     "venue_name": "ICLR 2025"},
    {"id": "iclr-2026", "venue": "ICLR", "year": 2026, "type": "conference", "parser": "openreview_venue",
     "venue_name": "ICLR 2026", "venue_patterns": ["ICLR 2026 Oral", "ICLR 2026 Poster"]},

    # ICML (Conference 2022-2026) - 使用OpenReview accepted venue
    {"id": "icml-2022", "venue": "ICML", "year": 2022, "type": "conference", "parser": "openreview_venue",
     "venue_name": "ICML 2022", "venue_patterns": ["ICML 2022"]},
    {"id": "icml-2023", "venue": "ICML", "year": 2023, "type": "conference", "parser": "openreview_venue",
     "venue_name": "ICML 2023", "venue_patterns": ["ICML 2023"]},
    {"id": "icml-2024", "venue": "ICML", "year": 2024, "type": "conference", "parser": "openreview_venue",
     "venue_name": "ICML 2024", "venue_patterns": ["ICML 2024", "ICML 2024 Oral", "ICML 2024 Spotlight", "ICML 2024 Poster"]},
    {"id": "icml-2025", "venue": "ICML", "year": 2025, "type": "conference", "parser": "openreview_venue",
     "venue_name": "ICML 2025", "venue_patterns": ["ICML 2025"]},
    {"id": "icml-2026", "venue": "ICML", "year": 2026, "type": "conference", "parser": "openreview_venue",
     "venue_name": "ICML 2026", "venue_patterns": ["ICML 2026"]},
    
    # # SANER (2022-2025)
    # {"id": "saner-2022", "venue": "SANER", "year": 2022, "type": "conference", "parser": "researchr_track",
    #  "url": "https://conf.researchr.org/track/saner-2022/saner-2022-papers", "track_keyword": "Research Track"},
    # {"id": "saner-2023", "venue": "SANER", "year": 2023, "type": "conference", "parser": "researchr_track",
    #  "url": "https://conf.researchr.org/track/saner-2023/saner-2023-papers", "track_keyword": "Research Track"},
    # {"id": "saner-2024", "venue": "SANER", "year": 2024, "type": "conference", "parser": "researchr_track",
    #  "url": "https://conf.researchr.org/track/saner-2024/saner-2024-papers", "track_keyword": "Research Track"},
    # {"id": "saner-2025", "venue": "SANER", "year": 2025, "type": "conference", "parser": "researchr_track",
    #  "url": "https://conf.researchr.org/track/saner-2025/saner-2025-papers", "track_keyword": "Research Track"},
    
    # # MSR (2022-2025)
    # {"id": "msr-2022", "venue": "MSR", "year": 2022, "type": "conference", "parser": "researchr_track",
    #  "url": "https://conf.researchr.org/track/msr-2022/msr-2022-technical-papers", "track_keyword": "Technical Papers"},
    # {"id": "msr-2023", "venue": "MSR", "year": 2023, "type": "conference", "parser": "researchr_track",
    #  "url": "https://conf.researchr.org/track/msr-2023/msr-2023-technical-papers", "track_keyword": "Technical Papers"},
    # {"id": "msr-2024", "venue": "MSR", "year": 2024, "type": "conference", "parser": "researchr_track",
    #  "url": "https://conf.researchr.org/track/msr-2024/msr-2024-technical-papers", "track_keyword": "Technical Papers"},
    # {"id": "msr-2025", "venue": "MSR", "year": 2025, "type": "conference", "parser": "researchr_track",
    #  "url": "https://conf.researchr.org/track/msr-2025/msr-2025-technical-papers", "track_keyword": "Technical Papers"},
]

TIER1_VENUES = {
    "ICSE", "FSE", "ASE", "ISSTA", "TSE", "TOSEM",
    "NeurIPS", "ICML", "ICLR", "AAAI", "ACL",
    "USENIX Security", "APR"  # APR Workshop (ICSE co-located)
}

# Heuristics
ABSTRACT_POSITIVE_HINTS = [
    # Bug/Code repair - 核心关键词
    r"\bpatch(es)?\b", r"\brepair(s|ed|ing)?\b", r"\bfix(es|ed|ing)?\b",
    r"\bcorrect(ing|ion|ed)?\s+bug(s)?\b",
    r"\bgenerate(d|s|ing)?\s+(correct\s+)?code\b",
    # Vulnerability repair
    r"\bvulnerabilit(y|ies)\s+(repair|fix|patch|mitigation)\b",
    r"\bsecurity\s+(patch|fix)\b", r"\bCVE\s+(repair|fix)\b",
    r"\bpatch(ing)?\s+vulnerabilit(y|ies)\b",
    # Issue/Problem resolution - 扩展表达
    r"\bresolv(e|ed|ing)\s+(issue|bug|problem)s?\b",
    r"\bsolv(e|ed|ing)\s+(issue|bug|problem)s?\b",
    r"\bGitHub\s+issue(s)?\b",  # GitHub issue本身就是APR相关
    # Software agents (APR领域的重要方向)
    r"\bsoftware\s+(engineering|development)\s+agent(s)?\b",
    r"\b(autonomous|agentic)\s+(program|software|code)\b",
    r"\bautomated\s+(debugging|repair|fixing)\b",
    r"\bprogram\s+improvement\b",
    # LLM应用于代码任务
    r"\b(llm|language\s+model).{0,50}(code|program|software)\b",
    r"\b(code|program|software).{0,50}(llm|language\s+model)\b",
    # Bug定位/识别（APR的上游任务）
    r"\bbug(gy)?\s+(identif|detect|locat|find)\b",
    r"\bfault\s+localization\b",
    r"\bbugginess\b"
]

# Expanded evaluation hints
EVAL_HINTS = [
    r"\bevaluat(e|ion|ed|ing)\b", r"\bbenchmark(s)?\b", 
    r"\bempirical\b", r"\bdataset(s)?\b", r"\bstudy\b", 
    r"\bexperiment(s|al)?\b", r"\bresult(s)?\b", r"\bperformance\b",
    r"\baccura(cy|te)\b", r"\bcomparison\b", r"\bcompare(d)?\b",
    r"\boutperform(s|ed)?\b", r"\bstate-of-the-art\b", r"\bsota\b",
    # Metrics
    r"\bpass@\d+\b", r"\bF1\b", r"\bprecision\b", r"\brecall\b",
    r"\bCodeBLEU\b", r"\bexact\s+match\b"
]

# Explicit exclusion for non-repair topics (unless seed)
EXCLUDE_TITLE_TERMS = [
    "detection", "localization", "prediction", "classification",
    "generating tests", "test generation"
]
# Only exclude if these are NOT present in title
RETAIN_TITLE_TERMS = [
    # 直接修复相关
    "repair", "fix", "patch", "correct", "fixing",
    "vulnerability", "CVE", "security",
    # APR相关的同义表达（不是trick，而是领域通用术语）
    "agent", "autonomous",  # software agents是APR的重要方向
    "improvement",          # program improvement
    "debug",                # debugging
]

# APR技术特征词（用于辅助判断）
APR_TECH_INDICATORS = [
    "llm", "language model", "gpt", "codex", "chatgpt",
    "automated", "automatic", "autonomous",
    "agent", "agentic",
    "issue resolution", "github issue", "bug fixing"
]

def norm_title(s: str) -> str:
    """标准化标题用于比较
    
    处理流程：
    1. 清除LaTeX/BibTeX格式（如$\{$text$\}$, {text}, etc.）
    2. Unicode标准化
    3. 转小写
    4. 只保留字母数字和空格
    5. 合并多余空格
    """
    s = s or ""
    
    # 1. 清除LaTeX/BibTeX格式
    # 移除各种LaTeX包装：$\{$, $\}$, {, }, $, \
    s = re.sub(r'\$\\{?\$', '', s)  # 移除 $\{$, $$
    s = re.sub(r'\$\\}?\$', '', s)  # 移除 $\}$, $$
    s = re.sub(r'[{}\\$]', '', s)   # 移除剩余的 {, }, \, $
    
    # 2-5. 标准化处理
    s = unidecode(s).lower().strip()
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()

def has_tool_name_in_title(title: str) -> bool:
    """检查标题是否包含代表性工具名（严格匹配，避免误判）
    
    匹配策略：
    1. 只做精确匹配（单词边界）
    2. 不做词干变化匹配（避免"patch"误判为"PATCH工具"）
    3. 特殊处理：一些工具名需要额外验证APR上下文
    """
    title_lower = title.lower()
    
    # 通用工具（可能造成误判的）需要配合APR上下文
    # 例如：PATCH, REx 这些通用词
    ambiguous_tools = ['patch', 'rex', 'repair', 'cure']
    
    # APR上下文关键词
    apr_context = ['program', 'code', 'bug', 'software', 'automated', 'llm', 'agent']
    has_apr_context = any(kw in title_lower for kw in apr_context)
    
    for tool in TOOL_TERMS:
        tool_lower = tool.lower()
        
        # 精确匹配（单词边界）
        pattern = r'\b' + re.escape(tool_lower) + r'\b'
        if re.search(pattern, title_lower):
            # 如果是通用词，需要APR上下文验证
            if tool_lower in ambiguous_tools:
                if has_apr_context:
                    return True
                else:
                    continue  # 跳过，不认为是工具名
            else:
                return True
    
    return False

def token_diff_leq3(a: str, b: str) -> bool:
    ta = set(norm_title(a).split())
    tb = set(norm_title(b).split())
    return len(ta.symmetric_difference(tb)) <= 3

def title_sim(a: str, b: str) -> int:
    return max(
        fuzz.token_set_ratio(a, b),
        fuzz.token_sort_ratio(a, b),
        fuzz.QRatio(a, b)
    )

def is_tier1(venue: str) -> bool:
    if not venue: return False
    v = venue.replace(".", "").strip()
    return any(t.lower() in v.lower() for t in TIER1_VENUES)

def from_arxiv(rec):
    short_id = rec.get_short_id()
    base_id = short_id.split("v")[0] if short_id and "v" in short_id else short_id
    return {
        "source": "arxiv",
        "title": rec.title,
        "year": rec.published.year if rec.published else None,
        "doi": (rec.doi or "").lower(),
        "venue": "arXiv",
        "type": "preprint",
        "authors": [a.name for a in rec.authors],
        "abstract": rec.summary,
        "url": rec.entry_id,
        "openalex_id": None,
        "arxiv_id": base_id.lower() if base_id else "",
        "citation_count": 0  # 初始值，后续通过 OpenAlex 查询
    }

def get_arxiv_citation_count(arxiv_id, use_cache=True):
    """通过 OpenAlex API 获取 arXiv 论文的引用次数
    
    Args:
        arxiv_id: arXiv ID (例如: "2401.12345")
        use_cache: 是否使用缓存
    
    Returns:
        引用次数（整数），失败时返回 0
    """
    if not arxiv_id:
        return 0
    
    # 缓存键：使用 arxiv_id 作为缓存标识
    cache_id = f"citation_{arxiv_id}"
    
    # 尝试从缓存加载
    if use_cache:
        cached = load_from_cache(cache_id)
        if cached is not None:
            # 缓存格式：{"citation_count": N}
            return cached.get("citation_count", 0)
    
    # 构建 OpenAlex API URL
    # OpenAlex 通过 DOI 查询 arXiv 论文：10.48550/arxiv.XXXX.XXXXX
    arxiv_doi = f"10.48550/arxiv.{arxiv_id}"
    url = f"https://api.openalex.org/works?filter=doi:{arxiv_doi}"
    
    try:
        resp = requests.get(url, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            results = data.get("results", [])
            
            if results:
                # 取第一个结果的引用数
                citation_count = results[0].get("cited_by_count", 0)
                
                # 保存到缓存
                if use_cache:
                    save_to_cache(cache_id, {"citation_count": citation_count})
                
                return citation_count
            else:
                # OpenAlex 没有找到该论文
                return 0
        else:
            # API 请求失败
            return 0
    
    except Exception as exc:
        # 网络错误或解析错误，返回 0
        # print(f"[WARN] Failed to fetch citation count for arXiv:{arxiv_id}: {exc}")
        return 0

def normalize_doi(url_or_doi: str) -> str:
    if not url_or_doi:
        return ""
    doi = url_or_doi.strip()
    doi = doi.replace("https://doi.org/", "").replace("http://doi.org/", "")
    doi = doi.replace("https://dx.doi.org/", "").replace("http://dx.doi.org/", "")
    return doi.strip()

def acm_pdf_url_for_doi(doi: str) -> str:
    """Return ACM's deterministic PDF endpoint for ACM DOI records."""
    doi = normalize_doi(doi).lower()
    if doi.startswith("10.1145/"):
        return f"https://dl.acm.org/doi/pdf/{doi}"
    return ""

def extract_openalex_access_fields(work: dict) -> dict:
    """Extract OA/PDF metadata from an OpenAlex work without dropping closed records."""
    open_access = work.get("open_access") or {}
    primary_location = work.get("primary_location") or {}
    best_oa_location = work.get("best_oa_location") or {}
    locations = [primary_location, best_oa_location]
    locations.extend(work.get("locations") or [])

    pdf_url = ""
    landing_page_url = ""
    license_value = ""
    for location in locations:
        if not isinstance(location, dict):
            continue
        pdf_url = pdf_url or (location.get("pdf_url") or "")
        landing_page_url = landing_page_url or (location.get("landing_page_url") or "")
        license_value = license_value or (location.get("license") or location.get("license_id") or "")

    doi = work.get("doi") or ""
    pdf_url = pdf_url or acm_pdf_url_for_doi(doi)
    return {
        "pdf_url": pdf_url,
        "oa_url": open_access.get("oa_url") or pdf_url or "",
        "open_access_status": open_access.get("oa_status") or "",
        "is_oa": bool(open_access.get("is_oa")),
        "landing_page_url": landing_page_url or doi or work.get("id") or "",
        "license": license_value,
    }

# ========== 缓存机制 ==========

def get_cache_key(source_id):
    """生成缓存键"""
    return hashlib.md5(source_id.encode()).hexdigest()

def get_cache_path(source_id):
    """获取缓存文件路径"""
    cache_key = get_cache_key(source_id)
    return CACHE_DIR / f"{cache_key}_{source_id}.json"

def load_from_cache(source_id):
    """从缓存加载数据"""
    cache_path = get_cache_path(source_id)
    if cache_path.exists():
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            # 检查缓存是否过期（默认7天）
            cache_time = cache_data.get('timestamp', 0)
            cache_age_days = (datetime.now().timestamp() - cache_time) / 86400
            if cache_age_days < 7:  # 7天内的缓存有效
                records = cache_data.get('records', [])
                if source_id.endswith("-openalex") and records and "pdf_url" not in records[0]:
                    print(f"[CACHE] 缓存缺少 OA/PDF 字段，重新抓取 {source_id}")
                    return None
                print(f"[CACHE] 从缓存加载 {source_id} ({cache_data.get('count', 0)} 条记录, {cache_age_days:.1f} 天前)")
                return records
            else:
                print(f"[CACHE] 缓存已过期 {source_id} ({cache_age_days:.1f} 天前)")
        except Exception as exc:
            print(f"[CACHE] 缓存加载失败 {source_id}: {exc}")
    return None

def save_to_cache(source_id, records):
    """保存数据到缓存"""
    cache_path = get_cache_path(source_id)
    try:
        cache_data = {
            'source_id': source_id,
            'timestamp': datetime.now().timestamp(),
            'count': len(records),
            'records': records
        }
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
        print(f"[CACHE] 已缓存 {source_id} ({len(records)} 条记录)")
    except Exception as exc:
        print(f"[CACHE] 缓存保存失败 {source_id}: {exc}")

def clear_cache(source_id=None):
    """清除缓存"""
    if source_id:
        cache_path = get_cache_path(source_id)
        if cache_path.exists():
            cache_path.unlink()
            print(f"[CACHE] 已清除缓存: {source_id}")
    else:
        # 清除所有缓存
        for cache_file in CACHE_DIR.glob("*.json"):
            cache_file.unlink()
        print(f"[CACHE] 已清除所有缓存")

# ========== 解析器实现 ==========

def parse_researchr_track(source_meta):
    """解析 conf.researchr.org 的会议 track 页面 (ICSE/FSE/ASE/ISSTA 等)"""
    records = []
    try:
        resp = requests.get(source_meta["url"], timeout=30)
        resp.raise_for_status()
    except Exception as exc:
        print(f"[WARN] Failed to fetch {source_meta['id']}: {exc}")
        return records

    soup = BeautifulSoup(resp.text, "html.parser")
    track_keyword = source_meta.get("track_keyword", "")
    
    # 尝试三种常见的结构
    # 结构1: table.session-table (程序表格)
    rows = soup.select("table.session-table tr")
    for row in rows:
        tds = row.find_all("td")
        if len(tds) < 4:
            continue
        detail_cell = tds[-1]
        title_anchor = detail_cell.find("a", attrs={"data-event-modal": True})
        if not title_anchor:
            continue
        
        # 过滤 track
        if track_keyword:
            track_div = detail_cell.find("div", class_="prog-track")
            if track_div and track_keyword not in track_div.get_text(strip=True):
                continue
        
        title = title_anchor.get_text(strip=True)
        if not title:
            continue
        
        performer_anchors = detail_cell.select("div.performers a")
        authors = [a.get_text(strip=True) for a in performer_anchors if a.get_text(strip=True)]
        
        doi_link = detail_cell.find("a", class_="publication-link")
        doi_url = doi_link["href"].strip() if doi_link and doi_link.get("href") else ""
        doi = normalize_doi(doi_url)

        records.append({
            "source": f"conf:{source_meta['venue']}:{source_meta['year']}",
            "title": title,
            "year": source_meta.get("year"),
            "doi": doi,
            "venue": f"{source_meta['venue']} {source_meta['year']}",
            "type": "conference",
            "authors": authors,
            "abstract": "",
            "url": doi_url or source_meta["url"],
            "openalex_id": None,
            "arxiv_id": None
        })
    
    # 结构2: div.event-item (事件列表)
    if not records:
        events = soup.select("div.event-item, div.program-event")
        for event in events:
            title_elem = event.find("a", class_="event-title") or event.find("h4")
            if not title_elem:
                continue
            title = title_elem.get_text(strip=True)
            if not title:
                continue
            
            authors_elem = event.find("div", class_="authors") or event.find("span", class_="authors")
            authors = []
            if authors_elem:
                author_links = authors_elem.find_all("a")
                authors = [a.get_text(strip=True) for a in author_links if a.get_text(strip=True)]
            
            doi_link = event.find("a", href=re.compile(r"doi\.org"))
            doi_url = doi_link["href"].strip() if doi_link else ""
            doi = normalize_doi(doi_url)
            
            records.append({
                "source": f"conf:{source_meta['venue']}:{source_meta['year']}",
                "title": title,
                "year": source_meta.get("year"),
                "doi": doi,
                "venue": f"{source_meta['venue']} {source_meta['year']}",
                "type": "conference",
                "authors": authors,
                "abstract": "",
                "url": doi_url or source_meta["url"],
                "openalex_id": None,
                "arxiv_id": None
            })
    
    # 结构3: 简单的两列表格 (ICSE 2026 风格)
    # 第一列为空，第二列包含标题链接、作者和track信息
    if not records:
        tables = soup.find_all("table")
        for table in tables:
            table_rows = table.find_all("tr")
            if len(table_rows) < 10:  # 跳过小表格（如日期表）
                continue
            
            for row in table_rows[1:]:  # 跳过标题行
                cells = row.find_all("td")
                if len(cells) < 2:
                    continue
                
                title_cell = cells[1]
                # 查找标题链接
                title_link = title_cell.find("a")
                if not title_link:
                    continue
                
                title = title_link.get_text(strip=True)
                if not title or len(title) < 10:  # 过滤太短的标题
                    continue
                
                # 从完整文本中提取信息
                full_text = title_cell.get_text(strip=True)
                
                # 检查 track 关键词（如果指定）
                if track_keyword and track_keyword not in full_text:
                    continue
                
                # 尝试提取作者（标题后面的文本，通常以逗号分隔）
                # 格式: "Title...Research TrackAuthor1,Author2,Author3..."
                authors = []
                if track_keyword:
                    # 移除标题和track关键词，剩下的是作者
                    author_text = full_text.replace(title, "").replace(track_keyword, "")
                    # 分割作者（以逗号分隔）
                    author_parts = [a.strip() for a in author_text.split(",") if a.strip()]
                    # 过滤掉太长的部分（可能是其他信息）
                    authors = [a for a in author_parts if len(a) < 50 and len(a) > 2]
                
                records.append({
                    "source": f"conf:{source_meta['venue']}:{source_meta['year']}",
                    "title": title,
                    "year": source_meta.get("year"),
                    "doi": "",
                    "venue": f"{source_meta['venue']} {source_meta['year']}",
                    "type": "conference",
                    "authors": authors,
                    "abstract": "",
                    "url": source_meta["url"],
                    "openalex_id": None,
                    "arxiv_id": None
                })
            
            # 如果找到了论文，就不再检查其他表格
            if records:
                break
    
    print(f"[INFO] Parsed {len(records)} entries from {source_meta['id']}")
    return records


def parse_usenix_accepted(source_meta):
    """解析 USENIX Security 的 accepted papers 页面"""
    records = []
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        resp = requests.get(source_meta["url"], timeout=30, headers=headers)
        resp.raise_for_status()
    except Exception as exc:
        print(f"[WARN] Failed to fetch {source_meta['id']}: {exc}")
        return records

    soup = BeautifulSoup(resp.text, "html.parser")
    
    # 尝试多种结构
    # 结构1: article.node-paper (最新版，2024+)
    paper_divs = soup.select("article.node-paper")
    if not paper_divs:
        # 结构2: div.views-row (旧版)
        paper_divs = soup.select("div.views-row")
    if not paper_divs:
        # 结构3: div.node--paper (中间版本)
        paper_divs = soup.select("div.node--paper")
    if not paper_divs:
        # 结构4: 简单的列表项
        paper_divs = soup.select("div.field--name-field-paper-title")
    
    for div in paper_divs:
        # 标题提取 - 多种方式
        title = None
        title_elem = (div.find("h2") or div.find("h3") or 
                     div.find("div", class_="title") or
                     div.find("span", class_="field--name-field-paper-title"))
        
        if title_elem:
            title_link = title_elem.find("a")
            title = title_link.get_text(strip=True) if title_link else title_elem.get_text(strip=True)
        
        if not title:
            continue
        
        # 作者信息 - 多种方式
        authors = []
        author_elem = (div.find("div", class_="authors") or 
                      div.find("p", class_="authors") or
                      div.find("div", class_="field--name-field-paper-people-text"))
        
        if author_elem:
            author_text = author_elem.get_text(strip=True)
            # 清理格式
            author_text = re.sub(r'\s+', ' ', author_text)
            # 分割作者 "Author1, Author2, and Author3" 或 "Author1; Author2"
            authors = [a.strip() for a in re.split(r'[,;]\s*(?:and\s+)?', author_text) if a.strip()]
        
        # PDF/DOI 链接
        url = source_meta["url"]
        pdf_link = div.find("a", href=re.compile(r'\.pdf$', re.I))
        if pdf_link and pdf_link.get("href"):
            url = pdf_link["href"]
            if not url.startswith("http"):
                url = "https://www.usenix.org" + url
        
        records.append({
            "source": f"conf:{source_meta['venue']}:{source_meta['year']}",
            "title": title,
            "year": source_meta.get("year"),
            "doi": "",
            "venue": f"{source_meta['venue']} {source_meta['year']}",
            "type": "conference",
            "authors": authors,
            "abstract": "",
            "url": url,
            "openalex_id": None,
            "arxiv_id": None
        })
    
    print(f"[INFO] Parsed {len(records)} entries from {source_meta['id']}")
    return records


def parse_apr_workshop(source_meta):
    """解析 ICSE APR Workshop accepted papers"""
    records = []
    
    url = source_meta.get('url')
    year = source_meta.get('year')
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        resp = requests.get(url, headers=headers, timeout=30)
        
        if resp.status_code != 200:
            print(f"[WARN] Failed to fetch {source_meta['id']}: status {resp.status_code}")
            return records
        
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # 查找 Accepted Papers 部分
        accepted_section = soup.find('h2', string=re.compile(r'Accepted Papers', re.I))
        
        if not accepted_section:
            print(f"[INFO] No 'Accepted Papers' section found for APR {year}")
            return records
        
        # 查找该部分后的表格
        table = accepted_section.find_next('table')
        if table:
            rows = table.find_all('tr')
            
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if not cells:
                    continue
                
                # 提取论文信息
                cell_text = cells[0].get_text(strip=True)
                
                # 分离标题和作者（通常标题是粗体）
                bold = cells[0].find('strong')
                if bold:
                    title = bold.get_text(strip=True)
                    # 作者在粗体后面
                    authors_text = cell_text.replace(title, '').strip()
                else:
                    # 如果没有粗体，整个当作标题
                    title = cell_text
                    authors_text = ""
                
                if not title or len(title) < 10:
                    continue
                
                # 解析作者
                authors = []
                if authors_text:
                    # 通常以逗号分隔
                    author_names = [a.strip() for a in authors_text.split(',')]
                    authors = [a for a in author_names if len(a) > 2]
                
                records.append({
                    "source": f"workshop:APR:{year}",
                    "title": title,
                    "year": year,
                    "doi": "",
                    "venue": "APR",  # APR Workshop视为ICSE的一部分
                    "type": "workshop",
                    "authors": authors,
                    "abstract": "",
                    "url": url,
                    "openalex_id": None,
                    "arxiv_id": None
                })
        
    except Exception as exc:
        print(f"[WARN] Failed to parse APR {year}: {exc}")
    
    print(f"[INFO] Parsed {len(records)} entries from {source_meta['id']}")
    return records


def parse_openalex_journal(source_meta):
    """使用OpenAlex API解析期刊数据"""
    records = []
    
    openalex_id = source_meta.get('openalex_id')
    years = source_meta.get('years', [2022, 2023, 2024, 2025])
    venue_name = source_meta.get('venue')
    
    if not openalex_id:
        print(f"[WARN] No OpenAlex ID specified for {source_meta['id']}")
        return records
    
    for year in years:
        url = f"https://api.openalex.org/works?filter=primary_location.source.id:{openalex_id},publication_year:{year}&per-page=200"
        
        try:
            headers = {'User-Agent': 'ProgramRepair-SLR/1.0'}
            params = {"api_key": os.environ["OPENALEX_API_KEY"]} if os.environ.get("OPENALEX_API_KEY") else None
            resp = requests.get(url, headers=headers, params=params, timeout=30)
            
            if resp.status_code != 200:
                print(f"[WARN] OpenAlex API returned {resp.status_code} for {venue_name} {year}")
                continue
            
            data = resp.json()
            results = data.get('results', [])
            
            print(f"[INFO] Fetched {len(results)} articles from {venue_name} {year}")
            
            for work in results:
                title = work.get('title', '')
                if not title:
                    continue
                
                # 安全处理DOI（可能为None）
                doi_raw = work.get('doi')
                doi = doi_raw.replace('https://doi.org/', '') if doi_raw else ''
                
                # 提取作者
                authors = []
                for authorship in work.get('authorships', []):
                    author_info = authorship.get('author', {})
                    author_name = author_info.get('display_name', '')
                    if author_name:
                        authors.append(author_name)
                
                # 重建摘要
                abstract = ""
                inverted_abstract = work.get('abstract_inverted_index', {})
                if inverted_abstract:
                    words = []
                    for word, positions in inverted_abstract.items():
                        for pos in positions:
                            words.append((pos, word))
                    words.sort()
                    abstract = ' '.join([w[1] for w in words])
                
                access_fields = extract_openalex_access_fields(work)
                url_value = access_fields.get("landing_page_url") or work.get('doi') or work.get('id')
                
                records.append({
                    "source": f"openalex:{venue_name}",
                    "title": title,
                    "year": year,
                    "doi": doi.lower() if doi else "",
                    "venue": venue_name,
                    "type": "journal",
                    "authors": authors,
                    "abstract": abstract if abstract else "",  # 不再截断摘要
                    "url": url_value,
                    "pdf_url": access_fields["pdf_url"],
                    "oa_url": access_fields["oa_url"],
                    "open_access_status": access_fields["open_access_status"],
                    "is_oa": access_fields["is_oa"],
                    "license": access_fields["license"],
                    "openalex_id": work.get('id'),
                    "arxiv_id": None
                })
        
        except Exception as exc:
            print(f"[ERROR] OpenAlex API failed for {venue_name} {year}: {exc}")
            continue
    
    print(f"[INFO] Parsed {len(records)} entries from {source_meta['id']}")
    return records


def parse_acl_web(source_meta):
    """解析 ACL 会议的网页论文列表
    支持 main papers 和 findings papers
    """
    records = []
    year = source_meta.get('year')
    url = source_meta.get('url')
    paper_type = source_meta.get('paper_type', 'main')  # 'main' or 'findings'
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
    except Exception as exc:
        print(f"[WARN] Failed to fetch {source_meta['id']}: {exc}")
        return records
    
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    # ACL网页通常在<ul>或<li>中列出论文
    # 格式：<li><strong>Title</strong> <i>Authors</i></li>
    paper_items = soup.find_all('li')
    
    for item in paper_items:
        # 提取标题（通常是加粗的文本或链接）
        title_elem = item.find('strong') or item.find('b')
        if not title_elem:
            # 如果没有加粗，尝试查找链接
            title_elem = item.find('a')
        
        if not title_elem:
            continue
            
        title = title_elem.get_text(strip=True)
        if not title or len(title) < 10:  # 过滤太短的标题
            continue
        
        # 提取作者（通常在斜体标签中）
        authors = []
        author_elem = item.find('i') or item.find('em')
        if author_elem:
            authors_text = author_elem.get_text(strip=True)
            authors = [a.strip() for a in authors_text.split(',') if a.strip()]
        
        # 提取链接
        paper_url = url
        link_elem = item.find('a', href=True)
        if link_elem:
            href = link_elem['href']
            if href.startswith('http'):
                paper_url = href
            elif href.startswith('/'):
                # 相对路径，补全域名
                from urllib.parse import urljoin
                paper_url = urljoin(url, href)
        
        records.append({
            "source": f"conf:ACL:{year}:{paper_type}",
            "title": title,
            "year": year,
            "doi": None,
            "venue": f"ACL {year}",
            "type": "conference",
            "authors": authors,
            "abstract": "",
            "url": paper_url,
            "openalex_id": None,
            "arxiv_id": None
        })
    
    print(f"[INFO] Parsed {len(records)} entries from {source_meta['id']}")
    return records


def parse_nips_web(source_meta):
    """解析 NeurIPS 论文网页
    URL格式: https://papers.nips.cc/paper_files/paper/YYYY
    """
    records = []
    year = source_meta.get('year')
    url = source_meta.get('url')
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
    except Exception as exc:
        print(f"[WARN] Failed to fetch {source_meta['id']}: {exc}")
        return records
    
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    # NeurIPS论文在<li class="conference">或<li class="datasets_and_benchmarks_track">中
    paper_items = soup.find_all('li', class_=['conference', 'datasets_and_benchmarks_track'])
    
    for item in paper_items:
        # 提取标题和链接
        title_link = item.find('a', title='paper title')
        if not title_link:
            continue
        
        title = title_link.get_text(strip=True)
        paper_url = title_link.get('href', '')
        if paper_url and not paper_url.startswith('http'):
            paper_url = f"https://papers.nips.cc{paper_url}"
        
        # 提取作者（在<i>标签中）
        authors = []
        author_elem = item.find('i')
        if author_elem:
            authors_text = author_elem.get_text(strip=True)
            authors = [a.strip() for a in authors_text.split(',') if a.strip()]
        
        records.append({
            "source": f"conf:NeurIPS:{year}",
            "title": title,
            "year": year,
            "doi": None,
            "venue": f"NeurIPS {year}",
            "type": "conference",
            "authors": authors,
            "abstract": "",
            "url": paper_url or url,
            "openalex_id": None,
            "arxiv_id": None
        })
    
    print(f"[INFO] Parsed {len(records)} entries from {source_meta['id']}")
    return records

def parse_iclr_github(source_meta):
    """解析GitHub上的ICLR论文列表
    
    来源: https://github.com/yinizhilian/ICLR2025-Papers-with-Code
    """
    year = source_meta.get("year")
    url = source_meta.get("url")
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        content = response.text
    except Exception as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return []
    
    records = []
    lines = content.split('\n')
    
    current_title = None
    for line in lines:
        # 匹配论文标题（格式：1、Title）
        title_match = re.match(r'^\d+、(.+)$', line.strip())
        if title_match:
            current_title = title_match.group(1).strip()
            # 清理可能的截断符号
            if current_title.endswith('...'):
                current_title = current_title[:-3]
            continue
        
        # 如果有标题，查找Paper链接
        if current_title and '- Paper:' in line:
            # 提取OpenReview链接（如果有）
            paper_url_match = re.search(r'https://openreview\.net/\S+', line)
            paper_url = paper_url_match.group(0) if paper_url_match else ""
            
            # 创建记录
            record = {
                "source": f"conf:ICLR:{year}",
                "title": current_title,
                "year": year,
                "doi": paper_url,
                "venue": f"ICLR {year}",
                "type": "conference",
                "authors": [],
                "abstract": "",
                "url": paper_url
            }
            records.append(record)
            current_title = None  # 重置
    
    print(f"[INFO] Parsed {len(records)} ICLR {year} papers from GitHub")
    return records

def parse_openreview_venue(source_meta):
    """解析OpenReview上的accepted papers
    
    使用OpenReview API获取某个venue的所有accepted papers
    支持分页获取完整列表，包括自定义venue标签（如ACL Findings、AAAI、ICML regular等）
    """
    year = source_meta.get("year")
    venue_name = source_meta.get("venue_name", "ICLR")  # e.g., "ICLR 2025"
    venue_short = source_meta.get("venue", venue_name.split()[0])
    
    # OpenReview的venue标签由会议自行配置。ICLR常见为 Oral/Poster，
    # 但ACL/AAAI/ICML等会议使用不同标签，因此允许SOURCE_CONFIG显式覆盖。
    venue_patterns = source_meta.get("venue_patterns")
    if not venue_patterns:
        venue_patterns = [
            venue_name,
            f"{venue_name} Poster",
            f"{venue_name} Spotlight",
            f"{venue_name} Oral"
        ]
    
    all_notes = []
    seen_notes = set()
    
    for venue_pattern in venue_patterns:
        offset = 0
        limit = 1000
        
        print(f"[INFO] Fetching '{venue_pattern}' papers from OpenReview API...")
        
        while True:
            # 构建API URL
            encoded_venue = urllib.parse.quote(venue_pattern)
            api_url = f'https://api2.openreview.net/notes?content.venue={encoded_venue}&select=id,content&limit={limit}&offset={offset}'
            
            try:
                response = requests.get(api_url, timeout=60)
                response.raise_for_status()
                data = response.json()
            except Exception as e:
                print(f"[ERROR] Failed to fetch '{venue_pattern}' from OpenReview: {e}")
                break
            
            notes = data.get('notes', [])
            if not notes:
                break
            
            for note in notes:
                note_key = note.get("id") or norm_title(extract_openreview_value(note.get("content", {}).get("title", "")))
                if note_key and note_key not in seen_notes:
                    all_notes.append(note)
                    seen_notes.add(note_key)
            print(f"[INFO] Fetched {len(notes)} papers from '{venue_pattern}' (total: {len(all_notes)})")
            
            # 如果返回的论文数少于limit，说明已经获取完所有论文
            if len(notes) < limit:
                break
            
            offset += limit
    
    notes = all_notes
    records = []
    
    for note in notes:
        content = note.get('content', {})
        
        # 提取标题
        title = extract_openreview_value(content.get('title', {}))
        
        if not title or not isinstance(title, str):
            continue
        
        # 提取摘要
        abstract = extract_openreview_value(content.get('abstract', {}))
        if not isinstance(abstract, str):
            abstract = ""
        
        # 提取作者
        authors = normalize_openreview_authors(extract_openreview_value(content.get('authors', {})))
        
        # 构建OpenReview URL
        note_id = note.get('id', '')
        paper_url = f'https://openreview.net/forum?id={note_id}' if note_id else ""
        
        record = {
            "source": f"conf:{venue_short}:{year}",
            "title": title.strip(),
            "year": year,
            "doi": paper_url,
            "venue": f"{venue_short} {year}",
            "type": "conference",
            "authors": authors,
            "abstract": abstract.strip(),
            "url": paper_url,
            "openalex_id": None,
            "arxiv_id": None
        }
        records.append(record)
    
    print(f"[INFO] Parsed {len(records)} papers from {venue_name} via OpenReview API")
    return records

def extract_openreview_value(value):
    """Return the OpenReview content value regardless of API schema variant."""
    if isinstance(value, dict) and "value" in value:
        return value["value"]
    return value

def normalize_openreview_authors(authors):
    """Normalize OpenReview authors to a list of display names."""
    if not isinstance(authors, list):
        return []
    normalized = []
    for author in authors:
        if isinstance(author, str):
            normalized.append(author)
        elif isinstance(author, dict):
            name = author.get("fullname") or author.get("name") or author.get("value") or author.get("username")
            if name:
                normalized.append(name)
    return normalized


# 解析器注册表
PARSER_REGISTRY = {
    "researchr_track": parse_researchr_track,
    "usenix_accepted": parse_usenix_accepted,
    "apr_workshop": parse_apr_workshop,
    "openalex_journal": parse_openalex_journal,
    "acl_web": parse_acl_web,
    "nips_web": parse_nips_web,
    "iclr_github": parse_iclr_github,
    "openreview_venue": parse_openreview_venue
}

def load_seeds_from_bib():
    """加载62个代表系统作为种子论文
    
    只加载 representative_62.bib 中的论文（从表格中提取的代表作）
    如果文件不存在，回退到 sample-base.bib
    """
    # 优先使用62个代表系统的文件
    bib_path = Path("representative_62.bib")
    if not bib_path.exists():
        # 回退到完整列表
        bib_path = Path("sample-base.bib")
        if not bib_path.exists():
            return []
    
    with open(bib_path) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    
    seeds = []
    for entry in bib_database.entries:
        year = entry.get("year")
        # 【修改】如果没有年份，尝试从 journal/booktitle 推断，或使用 2024 作为默认值
        if not year or not year.isdigit():
            # 对于缺少年份的条目，假设是最近的（2024）
            year = "2024"
            print(f"[WARN] Missing year for '{entry.get('title', 'Unknown')}', assuming 2024")
        
        # 只加载 2022+ 的代表系统
        if int(year) >= 2022:
            seeds.append({
                "title": entry.get("title", "").strip("{}"),
                "year": int(year),
                "doi": entry.get("doi", "").lower(),
                "arxiv_id": entry.get("eprint", "").lower().replace("arxiv:", ""),
                "venue": entry.get("journal") or entry.get("booktitle") or "Unknown"
            })
    
    print(f"[INFO] Loaded {len(seeds)} representative systems from {bib_path.name}")
    return seeds

def search_related_papers_via_semantic_scholar(paper_id, paper_type="arxiv", top_k=3):
    """通过 Semantic Scholar API 搜索相关论文
    
    Args:
        paper_id: 论文ID（arXiv ID, DOI 或 S2 Paper ID）
        paper_type: ID类型 ("arxiv", "doi", "s2")
        top_k: 返回前K篇相关论文（默认3）
    
    Returns:
        相关论文列表
    """
    # 构建 Semantic Scholar API URL
    if paper_type == "arxiv":
        # arXiv ID 格式：ARXIV:2304.12743
        api_url = f"https://api.semanticscholar.org/graph/v1/paper/ARXIV:{paper_id}"
    elif paper_type == "doi":
        # DOI 格式需要 URL 编码
        encoded_doi = urllib.parse.quote(paper_id, safe='')
        api_url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{encoded_doi}"
    else:
        api_url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}"
    
    # 请求相关论文（recommendations）
    params = {
        "fields": "paperId,title,year,authors,venue,publicationTypes,citationCount,abstract,externalIds"
    }
    
    try:
        # 获取论文基本信息
        resp = requests.get(api_url, params=params, timeout=10)
        time.sleep(0.5)  # 避免请求过快
        
        if resp.status_code != 200:
            return []
        
        paper_data = resp.json()
        paper_s2_id = paper_data.get("paperId")
        
        if not paper_s2_id:
            return []
        
        # 获取相关论文推荐
        recommendations_url = f"https://api.semanticscholar.org/recommendations/v1/papers/forpaper/{paper_s2_id}"
        rec_params = {
            "fields": "paperId,title,year,authors,venue,publicationTypes,citationCount,abstract,externalIds",
            "limit": top_k * 3  # 多取一些，过滤后可能不足top_k
        }
        
        resp = requests.get(recommendations_url, params=rec_params, timeout=10)
        time.sleep(0.5)
        
        if resp.status_code != 200:
            return []
        
        rec_data = resp.json()
        recommendations = rec_data.get("recommendedPapers", [])
        
        # 转换为标准格式，并筛选
        results = []
        for rec in recommendations[:top_k * 2]:  # 取前2*top_k，避免过滤后不足
            # 只保留2022年及之后的论文
            year = rec.get("year")
            if not year or int(year) < 2022:
                continue
            
            # 提取 arXiv ID 和 DOI
            external_ids = rec.get("externalIds", {})
            arxiv_id = external_ids.get("ArXiv", "").lower()
            doi = external_ids.get("DOI", "").lower()
            
            # 构建标准格式
            paper = {
                "source": "semantic_scholar:related",
                "title": rec.get("title", "").strip(),
                "year": int(year),
                "authors": [a.get("name", "") for a in rec.get("authors", [])],
                "venue": rec.get("venue", ""),
                "abstract": rec.get("abstract", ""),
                "doi": doi,
                "arxiv_id": arxiv_id,
                "citation_count": rec.get("citationCount", 0),
                "related_to": paper_data.get("title", "")  # 标记是从哪篇论文找到的
            }
            
            results.append(paper)
            
            if len(results) >= top_k:
                break
        
        return results
    
    except Exception as exc:
        # print(f"[WARN] Failed to fetch related papers for {paper_id}: {exc}")
        return []

def search_papers_by_tool_names(use_cache=True, top_k=3):
    """基于代表性工具名称搜索相关论文
    
    策略：
    1. 使用 TOOL_TERMS 列表中的工具名称
    2. 对每个工具，通过 Semantic Scholar 搜索相关论文
    3. 取前top_k篇相关论文加入候选
    
    这样可以确保代码完全独立，不依赖外部 .bib 文件，适合开源
    
    Args:
        use_cache: 是否使用缓存
        top_k: 每个工具名取多少相关论文（默认3）
    
    Returns:
        相关论文列表
    """
    cache_id = f"tool_based_papers_top{top_k}"
    
    # 检查缓存
    if use_cache:
        cached = load_from_cache(cache_id)
        if cached is not None:
            return cached
    
    # 选择最重要的工具名称（去重和标准化）
    # 优先选择代表性强的工具
    priority_tools = [
        # Agentic
        "RepairAgent", "AutoCodeRover", "SWE-agent", "OpenHands", 
        "LANTERN", "Magis", "SWE-Search",
        # Procedural
        "ChatRepair", "ThinkRepair", "ContrastRepair", "Agentless",
        "CREF", "PATCH", "Repilot", "PredicateFix", "LLM4CVE",
        # Prompting
        "AlphaRepair", "CEDAR", "APPATCH", "TracePrompt",
        # Fine-tuning
        "RepairLLaMA", "MORepair", "KNOD", "DistiLRR", "NARRepair",
        "InferFix", "PyTy", "TraceFixer", "Swe-rl", "Vul-R2",
        # LLM-as-Judges
        "TSAPR", "SpecRover",
        # Other
        "VulMaster", "CoCoNut"
    ]
    
    print(f"\n[INFO] Searching for papers by {len(priority_tools)} representative tool names...")
    print(f"[INFO] Will collect top-{top_k} papers for each tool")
    
    all_related = []
    seen = set()
    success_count = 0
    
    for tool_name in tqdm(priority_tools, desc="Searching by Tool Names"):
        # 构建搜索查询：工具名 + program repair
        query = f"{tool_name} program repair"
        
        try:
            # 使用 Semantic Scholar 搜索
            search_url = "https://api.semanticscholar.org/graph/v1/paper/search"
            params = {
                "query": query,
                "fields": "paperId,title,year,authors,venue,publicationTypes,citationCount,abstract,externalIds",
                "limit": 20,  # 增加limit，因为很多会被过滤
                "year": "2022-"  # 只要2022年及之后
            }
            
            resp = requests.get(search_url, params=params, timeout=10)
            time.sleep(0.5)  # 避免请求过快
            
            if resp.status_code != 200:
                continue
            
            data = resp.json()
            papers = data.get("data", [])
            
            found_count = 0
            for paper in papers:
                if found_count >= top_k:
                    break
                
                # 基本信息验证
                title = paper.get("title", "").strip()
                year = paper.get("year")
                
                if not title or not year or int(year) < 2022:
                    continue
                
                # 【修复Bug】放宽标题验证：
                # 1. 标题包含工具名（不区分大小写）→ 直接通过
                # 2. 或者标题包含 APR 关键词 → 通过
                title_lower = title.lower()
                tool_name_lower = tool_name.lower()
                
                # 检查标题是否包含工具名（支持部分匹配）
                has_tool_name = tool_name_lower in title_lower
                
                # 扩展的 APR 关键词列表
                apr_keywords = [
                    "repair", "fix", "patch", "debug", "vulnerability", "bug",
                    "automated", "automatic", "generation", "synthesis", "agent"
                ]
                has_apr_keyword = any(kw in title_lower for kw in apr_keywords)
                
                # 宽松的验证：有工具名或有APR关键词即可
                if not (has_tool_name or has_apr_keyword):
                    continue
                
                # 去重
                title_norm = norm_title(title)
                if title_norm in seen:
                    continue
                
                # 提取信息
                external_ids = paper.get("externalIds", {})
                arxiv_id = external_ids.get("ArXiv", "").lower()
                doi = external_ids.get("DOI", "").lower()
                
                # 构建标准格式
                paper_obj = {
                    "source": f"tool_search:{tool_name}",
                    "title": title,
                    "year": int(year),
                    "authors": [a.get("name", "") for a in paper.get("authors", [])],
                    "venue": paper.get("venue", ""),
                    "abstract": paper.get("abstract", ""),
                    "doi": doi,
                    "arxiv_id": arxiv_id,
                    "citation_count": paper.get("citationCount", 0),
                    "tool_keyword": tool_name
                }
                
                all_related.append(paper_obj)
                seen.add(title_norm)
                found_count += 1
            
            if found_count > 0:
                success_count += 1
                
        except Exception as exc:
            # print(f"[WARN] Failed to search for {tool_name}: {exc}")
            continue
    
    print(f"[INFO] Successfully found papers for {success_count}/{len(priority_tools)} tools")
    print(f"[INFO] Collected {len(all_related)} unique papers (year >= 2022)")
    
    # 保存到缓存
    if use_cache:
        save_to_cache(cache_id, all_related)
    
    return all_related

def harvest_arxiv_sources(use_cache=True, force_refresh=False):
    """爬取arXiv数据源，支持缓存和引用数筛选
    
    筛选标准：
    1. 年份 >= 2022
    2. 内容相关性过滤（APR相关）
    3. 引用数筛选：(最近一年 且 引用数>=1) 或 (引用数>=30)
    
    Args:
        use_cache: 是否使用缓存（默认True）
        force_refresh: 是否强制刷新，忽略缓存（默认False）
    """
    cache_id = "arxiv_all"
    
    # 尝试从缓存加载
    if use_cache and not force_refresh:
        cached = load_from_cache(cache_id)
        if cached is not None:
            print(f"[CACHE] 从缓存加载 arXiv 数据: {len(cached)} 条记录")
            return cached
    
    results = []
    seen = set()

    print("Searching arXiv (No Year Filter)...")
    arxiv_queries = []
    
    # 查询1: 核心APR术语 + 编程/软件上下文（更精确）
    core_apr_terms = [
        "automated program repair", "automatic program repair", "APR",
        "program repair", "patch generation", "code repair",
        "vulnerability repair", "bug fixing", "patch synthesis"
    ]
    code_context = ["code", "program", "software", "bug", "patch", "vulnerability"]
    
    for apr_term in core_apr_terms:
        # 核心术语本身就很精确，直接搜索
        arxiv_queries.append(f'all:"{apr_term}"')
    
    # 查询2: 所有工具名称（在标题中搜索，确保不遗漏）
    # 标题包含工具名的论文是代表性系统，必须全部覆盖
    for tool in TOOL_TERMS:
        # 使用灵活匹配（不加引号），可以匹配词干变化
        # 例如：PATCH可以匹配patching, patches, patched
        arxiv_queries.append(f'ti:{tool}')  # 标题包含（灵活匹配）
    
    # 查询3: LLM + 修复（但必须有代码/程序上下文）
    llm_terms = ["large language model", "LLM", "GPT", "ChatGPT", "language model"]
    repair_terms = ["bug fix", "patch", "program repair", "code repair", "vulnerability fix"]
    for llm in llm_terms:
        for repair in repair_terms:
            arxiv_queries.append(f'all:"{llm}" AND all:"{repair}"')
    
    # 查询4: Benchmark驱动的查询（提高精确度）
    key_benchmarks = ["Defects4J", "SWE-bench", "QuixBugs", "CVEFixes"]
    for bench in key_benchmarks:
        arxiv_queries.append(f'all:"{bench}"')

    # 初步相关性过滤：过滤明显不相关的论文
    def is_relevant_arxiv_paper(obj):
        """初步判断arXiv论文是否与APR相关"""
        title = (obj.get("title") or "").lower()
        abstract = (obj.get("abstract") or "").lower()
        text = title + " " + abstract

        # 标题包含已知APR工具名，直接保留
        if has_tool_name_in_title(obj.get("title") or ""):
            return True
        
        # 黑名单：明显不相关的领域关键词（扩展）
        blacklist = [
            # 自然科学
            "coconut", "astronomy", "astrophys", "telescope", "photometry",
            "medical imaging", "disease", "agriculture", "plant", "crop",
            "climate", "weather", "ocean", "marine", "biology", "genetic",
            "chemistry", "physics", "quantum", "particle", "cosmology",
            # 对话/语音
            "dialogue repair", "conversation repair", "speech repair",
            # 图像/视频/音频
            "image repair", "video repair", "audio repair", "image patch",
            "video patch", "rendering", "diffusion model",
            # 时间序列/机器学习（非代码）
            "time series", "time-series", "forecasting", "prediction",
            # 硬件
            "fpga", "hardware", "circuit", "chip",
            # 其他
            "block world", "robot", "reinforcement learning environment",
            "neural rendering", "image generation"
        ]
        
        # 如果包含黑名单关键词，排除
        if any(kw in text for kw in blacklist):
            return False
        
        # 强制要求：标题或摘要必须包含核心APR关键词
        # 更严格：不仅要有"patch"，还要有代码/软件上下文
        core_keywords = [
            "program repair", "automated program repair", "automatic program repair", 
            "code repair", "bug fix", "patch generation", "vulnerability repair",
            "software repair", "defect repair", "program patch", "code patch",
            "bug patch", "vulnerability patch", "software patch",
            "program debugging", "code debugging", "software debugging",
            "program fixing", "code fixing"
        ]
        
        # 必须包含至少一个核心APR关键词
        has_core_keyword = any(kw in text for kw in core_keywords)
        
        # 或者：包含"patch"/"repair"/"fix" + 代码相关词
        code_keywords = ["code", "program", "software", "bug", "defect", "vulnerability"]
        action_keywords = ["patch", "repair", "fix"]
        
        has_action = any(kw in text for kw in action_keywords)
        has_code_context = any(kw in text for kw in code_keywords)
        
        # 如果有核心关键词，或者有动作词+代码上下文，则通过
        if has_core_keyword or (has_action and has_code_context):
            return True
        
        return False
    
    client = arxiv.Client(num_retries=2, page_size=200, delay_seconds=1)
    arxiv_queries = list(set(arxiv_queries))
    filtered_count = 0
    
    for q in tqdm(arxiv_queries, desc="arXiv Queries"):
        try:
            search = arxiv.Search(
                query=q,
                max_results=2000,
                sort_by=arxiv.SortCriterion.Relevance
            )
            for rec in client.results(search):
                obj = from_arxiv(rec)
                key = ("arxiv", obj["arxiv_id"])
                year = obj.get("year")
                
                # 年份过滤 + 相关性过滤
                if obj["title"] and key not in seen and year and int(year) >= 2022:
                    if is_relevant_arxiv_paper(obj):
                        results.append(obj)
                        seen.add(key)
                    else:
                        filtered_count += 1
        except Exception:
            continue

    # 强制拉取特定的 arXiv 论文（仅用于特殊情况，如已知arXiv API搜索不到的论文）
    if MANDATORY_ARXIV_IDS:
        print(f"[INFO] Force-fetching {len(MANDATORY_ARXIV_IDS)} mandatory arXiv papers...")
        mandatory_added = 0
        for arxiv_id in MANDATORY_ARXIV_IDS:
            base_id = arxiv_id.lower()
            key = ("arxiv", base_id)
            if key in seen:
                continue
            try:
                search = arxiv.Search(id_list=[arxiv_id])
                recs = list(client.results(search))
                for rec in recs:
                    obj = from_arxiv(rec)
                    year = obj.get("year")
                    if obj["title"] and year and int(year) >= 2022:
                        results.append(obj)
                        seen.add(key)
                        mandatory_added += 1
                        print(f"  [✓] {obj['title'][:60]}...")
            except Exception as exc:
                print(f"  [✗] Failed to fetch arXiv:{arxiv_id}: {exc}")
        
        print(f"[INFO] Successfully added {mandatory_added}/{len(MANDATORY_ARXIV_IDS)} mandatory papers")
    
    print(f"[INFO] Harvested {len(results)} arXiv records (year >= 2022).")
    print(f"[INFO] Filtered out {filtered_count} irrelevant papers at Stage 1.")
    
    # 【新增】批量查询引用数并应用筛选逻辑
    print(f"[INFO] Querying citation counts from OpenAlex for {len(results)} papers...")
    current_year = datetime.now().year
    
    for obj in tqdm(results, desc="Fetching Citations"):
        arxiv_id = obj.get("arxiv_id")
        if arxiv_id:
            citation_count = get_arxiv_citation_count(arxiv_id, use_cache=use_cache)
            obj["citation_count"] = citation_count
    
    # 应用新的筛选标准（放宽条件以提高覆盖率）：
    # 1. 2024-2025年的论文：无引用数要求（新论文还没被引用）
    # 2. 2023年的论文：至少有 1 个引用
    # 3. 2022年的论文：至少有 5 个引用
    # 4. 或者有 15 个及以上引用（不限年份）
    filtered_results = []
    citation_filtered_count = 0
    
    for obj in results:
        year = obj.get("year")
        citation_count = obj.get("citation_count", 0)
        
        if not year:
            filtered_results.append(obj)
            continue
        
        year_int = int(year)
        
        # 筛选规则（按优先级，放宽到10）
        if citation_count >= 10:  # 规则1：引用数≥10直接通过
            filtered_results.append(obj)
        elif year_int >= 2024:  # 规则2：2024-2025年新论文无引用要求
            filtered_results.append(obj)
        elif year_int == 2023 and citation_count >= 1:  # 规则3：2023年至少1引用
            filtered_results.append(obj)
        elif year_int == 2022 and citation_count >= 3:  # 规则4：2022年至少3引用
            filtered_results.append(obj)
        else:
            citation_filtered_count += 1
    
    print(f"[INFO] After citation filtering: {len(filtered_results)} papers kept, {citation_filtered_count} filtered out.")
    print(f"[INFO] Filtering criteria: (2024-2025: no limit) OR (2023: ≥1) OR (2022: ≥3) OR (≥10 citations)")
    
    # 保存到缓存
    save_to_cache(cache_id, filtered_results)
    
    return filtered_results

def harvest_conf_sources(use_cache=True, force_refresh=False):
    """使用通用解析器架构爬取所有配置的数据源
    
    Args:
        use_cache: 是否使用缓存（默认True）
        force_refresh: 是否强制刷新，忽略缓存（默认False）
    """
    records = []
    cache_hits = 0
    cache_misses = 0
    
    for source_meta in tqdm(SOURCE_CONFIG, desc="Harvesting Conference/Journal Sources"):
        source_id = source_meta.get('id')
        parser_key = source_meta.get("parser")
        
        if not parser_key:
            print(f"[WARN] No parser specified for {source_id}")
            continue
        
        parser_func = PARSER_REGISTRY.get(parser_key)
        if not parser_func:
            print(f"[WARN] Unknown parser '{parser_key}' for {source_id}")
            continue
        
        # 尝试从缓存加载
        parsed_records = None
        if use_cache and not force_refresh:
            parsed_records = load_from_cache(source_id)
            if parsed_records is not None:
                cache_hits += 1
                records.extend(parsed_records)
                continue
        
        # 缓存未命中，执行爬取
        cache_misses += 1
        try:
            parsed_records = parser_func(source_meta)
            # 【改进】直接在收集时过滤年份 >= 2022
            filtered_records = []
            for r in parsed_records:
                year = r.get("year")
                if year and int(year) >= 2022:
                    filtered_records.append(r)
            records.extend(filtered_records)
            
            # 保存到缓存
            if use_cache and filtered_records:
                save_to_cache(source_id, filtered_records)
                
        except Exception as exc:
            print(f"[ERROR] Parser '{parser_key}' failed for {source_id}: {exc}")
            continue
    
    print(f"\n[INFO] 缓存统计: 命中 {cache_hits}, 未命中 {cache_misses}")
    print(f"[INFO] 总共收集 {len(records)} 条记录 (year >= 2022)，来自 {len(SOURCE_CONFIG)} 个数据源")
    return records

def stage1_harvest():
    """Stage 1: 从各数据源收集论文（已过滤年份 >= 2022）"""
    arxiv_records = harvest_arxiv_sources()
    conf_records = harvest_conf_sources()
    
    # 【新增】基于工具名称搜索相关论文（每个工具取前3篇）
    tool_based_records = search_papers_by_tool_names(use_cache=True, top_k=3)
    
    combined = arxiv_records + conf_records + tool_based_records

    with open(DATA / "stage1_filtered.jsonl", "w") as f:
        for r in combined:
            json.dump(r, f, ensure_ascii=False)
            f.write("\n")
    
    print(f"\n[INFO] Stage1 数据源统计:")
    print(f"  - 会议/期刊论文: {len(conf_records)} 篇")
    print(f"  - arXiv 论文: {len(arxiv_records)} 篇")
    print(f"  - 工具定向搜索: {len(tool_based_records)} 篇")
    print(f"  - 总计: {len(combined)} 篇（已过滤年份 >= 2022）")
    return len(combined)

def is_same_paper(a, b):
    # Normalized title exact match
    ta, tb = norm_title(a["title"]), norm_title(b["title"])
    if ta == tb: return True
    
    # ID match
    if a.get("doi") and b.get("doi") and a["doi"] == b["doi"]: return True
    if a.get("arxiv_id") and b.get("arxiv_id") and a["arxiv_id"] == b["arxiv_id"]: return True
    
    # Fuzzy title match
    if title_sim(ta, tb) >= 95: return True
    
    # 【新增】作者序列完全一致 + 摘要高度相似 → 同一篇论文
    authors_a = a.get("authors", [])
    authors_b = b.get("authors", [])
    abstract_a = (a.get("abstract") or "").lower()
    abstract_b = (b.get("abstract") or "").lower()
    
    # 作者序列完全一致（至少3个作者，避免误判）
    if (len(authors_a) >= 3 and len(authors_b) >= 3 and 
        authors_a == authors_b):
        # 检查摘要相似度
        if abstract_a and abstract_b and len(abstract_a) > 100 and len(abstract_b) > 100:
            # 使用 token set ratio（忽略顺序）
            abstract_sim = fuzz.token_set_ratio(abstract_a, abstract_b)
            if abstract_sim >= 90:  # 摘要90%相似
                return True
    
    # 【新增】作者序列完全一致 + 标题高度相似（80%） → 同一篇论文
    if (len(authors_a) >= 2 and len(authors_b) >= 2 and 
        authors_a == authors_b):
        if title_sim(ta, tb) >= 80:  # 标题80%相似
            return True
    
    return False

def better_version(a, b):
    # Prefer non-arXiv, Tier 1, DOI present
    score_a = 0
    score_b = 0
    
    va = (a.get("venue") or "").lower()
    vb = (b.get("venue") or "").lower()
    
    if "arxiv" not in va and va != "unknown": score_a += 3
    if "arxiv" not in vb and vb != "unknown": score_b += 3
    
    if is_tier1(a.get("venue")): score_a += 2
    if is_tier1(b.get("venue")): score_b += 2
    
    if a.get("doi"): score_a += 1
    if b.get("doi"): score_b += 1
    
    better = a if score_a >= score_b else b
    worse = b if score_a >= score_b else a
    
    # 【关键】如果更好的版本没有摘要，从另一个版本复制摘要
    if not better.get("abstract") and worse.get("abstract"):
        better["abstract"] = worse["abstract"]
    
    # 同样处理 arxiv_id（保留 arXiv 信息）
    if not better.get("arxiv_id") and worse.get("arxiv_id"):
        better["arxiv_id"] = worse["arxiv_id"]
    
    return better

def stage2_dedup():
    """Stage 2: 去除重复论文"""
    crawled = []
    if (DATA / "stage1_filtered.jsonl").exists():
        with open(DATA / "stage1_filtered.jsonl") as f:
            crawled = [json.loads(line) for line in f]

    if not crawled:
        print("[WARN] No records to deduplicate at stage 2.")
        return 0

    groups = {}
    for item in crawled:
        nt = norm_title(item["title"])
        groups.setdefault(nt, []).append(item)

    deduped_list = []
    exact_dupes = 0

    for nt, cluster in groups.items():
        if len(cluster) > 1:
            exact_dupes += (len(cluster) - 1)
        best = cluster[0]
        for x in cluster[1:]:
            best = better_version(best, x)
        deduped_list.append(best)

    print(f"  Removed {exact_dupes} exact title duplicates.")
    print(f"  开始模糊去重 (共 {len(deduped_list)} 条记录)...")

    final_list = []
    skip_indices = set()
    fuzzy_dupes = 0
    
    # 按标题排序，相似标题会聚集在一起
    deduped_list.sort(key=lambda x: norm_title(x["title"]))

    # 构建 DOI 和 arXiv ID 的快速索引
    print("  构建 DOI/arXiv 索引...")
    doi_map = {}
    arxiv_map = {}
    for idx, item in enumerate(deduped_list):
        if item.get("doi"):
            doi_map[item["doi"]] = idx
        if item.get("arxiv_id"):
            arxiv_map[item["arxiv_id"]] = idx

    # 快速预检查函数：避免不必要的昂贵模糊匹配
    def quick_check_similar(a, b):
        """快速判断两篇论文是否可能相似"""
        ta = norm_title(a["title"])
        tb = norm_title(b["title"])
        
        # 长度差异过大
        if abs(len(ta) - len(tb)) > max(len(ta), len(tb)) * 0.3:
            return False
        
        # 首字母不同
        if ta and tb and ta[0] != tb[0]:
            return False
            
        return True

    # 使用滑动窗口 + tqdm 进度条
    from tqdm import tqdm
    WINDOW_SIZE = 100  # 只比较后续的100条记录
    
    for i in tqdm(range(len(deduped_list)), desc="  模糊去重", unit="条"):
        if i in skip_indices:
            continue
        current = deduped_list[i]
        
        # 计算滑动窗口范围
        window_end = min(i + 1 + WINDOW_SIZE, len(deduped_list))
        
        for j in range(i + 1, window_end):
            if j in skip_indices:
                continue
                
            candidate = deduped_list[j]
            
            # 1. 快速检查：DOI 匹配
            if (current.get("doi") and candidate.get("doi") and 
                current["doi"] == candidate["doi"]):
                fuzzy_dupes += 1
                current = better_version(current, candidate)
                skip_indices.add(j)
                continue
            
            # 2. 快速检查：arXiv ID 匹配
            if (current.get("arxiv_id") and candidate.get("arxiv_id") and 
                current["arxiv_id"] == candidate["arxiv_id"]):
                fuzzy_dupes += 1
                current = better_version(current, candidate)
                skip_indices.add(j)
                continue
            
            # 3. 快速预检查：是否值得做模糊匹配
            if not quick_check_similar(current, candidate):
                continue
            
            # 4. 昂贵的模糊匹配（只有通过预检查才执行）
            if is_same_paper(current, candidate):
                fuzzy_dupes += 1
                current = better_version(current, candidate)
                skip_indices.add(j)
        
        final_list.append(current)

    print(f"  Removed {fuzzy_dupes} fuzzy/ID duplicates.")
    print(f"  Total duplicates removed: {exact_dupes + fuzzy_dupes}")

    with open(DATA / "stage2_dedup.jsonl", "w") as f:
        for r in final_list:
            json.dump(r, f, ensure_ascii=False)
            f.write("\n")
    
    print(f"[INFO] Stage2 完成: 去重后保留 {len(final_list)} 条记录")
    return len(final_list)

def stage3_screen():
    """Stage3: 多步筛选，逐步缩减到约 400 篇
    
    策略：
    - Step 3a: 基础筛选（has_positive_abstract）
    - Step 3b: 要求包含量化指标和成功率关键词
    - Step 3c: 要求提到 LLM 或经典模型
    - Step 3d: 要求提到已知 benchmark
    - Step 3e: 高质量论文筛选（顶会/近期/代表性系统）
    - 目标：保留高置信度论文，同时覆盖大部分代表性系统
    
    Returns:
        包含各阶段统计数据的字典
    """
    input_file = DATA / "stage2_dedup.jsonl"
    if not input_file.exists():
        print("[WARN] stage2_dedup.jsonl missing; skipping stage3.")
        return {"stage3a_basic": 0, "stage3b_quant": 0, "stage3c_llm": 0, "stage3d_bench": 0, "stage3e_quality": 0, "final": 0}

    with open(input_file) as f:
        items = [json.loads(line) for line in f]
    
    print("\n" + "="*80)
    print("Stage 3: 多步筛选流程")
    print("="*80)
    
    def run_filter(records, filter_func, step_name, out_filename):
        filtered = [r for r in records if filter_func(r)]
        if out_filename:
            with open(DATA / out_filename, "w") as f:
                for r in filtered:
                    json.dump(r, f, ensure_ascii=False)
                    f.write("\n")
        
        reduction_rate = (1 - len(filtered) / len(records)) * 100 if records else 0
        print(f"[{step_name}] {len(records)} -> {len(filtered)} "
              f"(缩减 {reduction_rate:.1f}%)")
        return filtered
    
    # Step 3a: 基础筛选
    print("\n[Step 3a] 基础筛选（APR 相关性 + Tier1/评估信号）")
    keep_3a = run_filter(items, has_positive_abstract, "Step 3a", "stage3a_basic.jsonl")
    
    # Step 3b: 量化指标 + 成功率关键词
    print("\n[Step 3b] 要求包含数值指标（%或小数点）+ 修复成功率关键词")
    keep_3b = run_filter(keep_3a, has_quantitative_success_signals, "Step 3b", "stage3b_quant.jsonl")
    
    # Step 3c: 提到 LLM
    print("\n[Step 3c] 要求提到 LLM 或经典模型（GPT/Llama/DeepSeek等）")
    keep_3c = run_filter(keep_3b, mentions_llm, "Step 3c", "stage3c_llm.jsonl")
    
    # Step 3d: 提到 benchmark
    print("\n[Step 3d] 要求摘要提到已知 benchmark")
    keep_3d = run_filter(keep_3c, mentions_known_benchmark, "Step 3d", "stage3d_bench.jsonl")
    
    # Step 3e: Venue/Recency 门槛筛选（对标论文方法论）
    print("\n[Step 3e] Venue/Recency 门槛筛选")
    print("  参照论文 Inclusion Criteria (iii):")
    print("  - Tier-1 SE/AI/Security venue, OR")
    print("  - Recent arXiv preprint with practitioner signals")
    
    def meets_venue_threshold(r):
        """对标论文方法论的venue门槛
        
        Inclusion: Tier-1 venue OR recent arXiv with signals
        Tier-1 venues (论文中定义):
        - SE: ICSE, FSE, ASE, ISSTA, TSE, TOSEM
        - AI/NLP: NeurIPS, ICML, ICLR, AAAI, ACL
        - Security: USENIX Security
        
        重要：完全没有引用的arXiv论文全部排除（除非是代表性工具）
        """
        title = (r.get("title") or "")
        venue = (r.get("venue") or "").upper()
        year = r.get("year", 2022)
        citation = r.get("citation_count", 0)
        source = r.get("source", "")
        
        # 检查是否是arXiv论文
        is_arxiv = "arxiv" in source.lower() or "arxiv" in venue.lower()
        
        # 标题包含工具名的代表性系统必须保留（即使没有引用）
        if has_tool_name_in_title(title):
            return True
        
        # 【关键规则】arXiv论文如果完全没有引用，直接排除
        if is_arxiv and citation == 0:
            return False
        
        # Tier-1 venues（严格列表，来自论文方法论）
        tier1_se = ["ICSE", "FSE", "ASE", "ISSTA", "TSE", "TOSEM"]
        tier1_ai = ["NEURIPS", "ICML", "ICLR", "AAAI", "ACL"]
        tier1_security = ["USENIX SECURITY", "USENIX"]
        
        all_tier1 = tier1_se + tier1_ai + tier1_security
        
        # 检查是否是Tier-1 venue
        is_tier1 = any(v in venue for v in all_tier1)
        
        if is_tier1:
            return True
        
        # Recent arXiv with practitioner signals
        # "Recent" = 2024-2025, "signals" = citation ≥ 15
        if is_arxiv and year >= 2024 and citation >= 15:
            return True
        
        # 高引用论文（任何来源，说明有影响力）
        if citation >= 50:
            return True
        
        return False
    
    keep_3e = [r for r in keep_3d if meets_venue_threshold(r)]
    
    reduction_rate = (1 - len(keep_3e) / len(keep_3d)) * 100 if keep_3d else 0
    print(f"[Step 3e] {len(keep_3d)} -> {len(keep_3e)} (缩减 {reduction_rate:.1f}%)")
    
    # 保存到文件
    with open(DATA / "stage3e_quality.jsonl", "w") as f:
        for r in keep_3e:
            json.dump(r, f, ensure_ascii=False)
            f.write("\n")
    
    # 最终输出
    final_output = DATA / "stage3_final_candidates.jsonl"
    with open(final_output, "w") as f:
        for r in keep_3e:
            json.dump(r, f, ensure_ascii=False)
            f.write("\n")
    
    # 检查对代表性论文的覆盖情况（仅供参考，不在此补充）
    print("\n" + "="*80)
    print("检查代表性论文的覆盖情况（仅供参考）")
    print("="*80)
    
    representative_papers = load_seeds_from_bib()
    if not representative_papers:
        print("[WARN] 未找到 representative_62.bib 文件，跳过覆盖率检查")
    else:
        # 构建已保留论文的索引（用于快速查找）
        kept_titles = {norm_title(r["title"]) for r in keep_3e}
        kept_dois = {r.get("doi", "").lower() for r in keep_3e if r.get("doi")}
        kept_arxiv = {r.get("arxiv_id", "").lower() for r in keep_3e if r.get("arxiv_id")}
        
        found_count = 0
        missing_papers = []
        
        for seed in representative_papers:
            found = False
            seed_title_norm = norm_title(seed["title"])
            seed_doi = seed.get("doi", "").lower()
            seed_arxiv = seed.get("arxiv_id", "").lower()
            
            # 检查是否在最终保留的论文中
            if seed_title_norm in kept_titles:
                found = True
            elif seed_doi and seed_doi in kept_dois:
                found = True
            elif seed_arxiv and seed_arxiv in kept_arxiv:
                found = True
            
            if found:
                found_count += 1
            else:
                missing_papers.append(seed)
        
        coverage_rate = found_count * 100.0 / len(representative_papers) if representative_papers else 0
        
        print(f"[INFO] 代表性论文自动筛选覆盖情况:")
        print(f"  - 总数: {len(representative_papers)} 篇")
        print(f"  - Stage3 保留: {found_count} 篇 ({coverage_rate:.1f}%)")
        print(f"  - 将在 Stage4 补充: {len(missing_papers)} 篇 ({100-coverage_rate:.1f}%)")
    
    print("="*80)
    print(f"[INFO] Stage3 完成: 自动筛选保留 {len(keep_3e)} 篇候选论文")
    print(f"[INFO] 下一步：Stage4 将补充遗漏的代表性论文")
    print("="*80)
    
    return {
        "stage3a_basic": len(keep_3a),
        "stage3b_quant": len(keep_3b),
        "stage3c_llm": len(keep_3c),
        "stage3d_bench": len(keep_3d),
        "stage3e_quality": len(keep_3e),
        "final": len(keep_3e)
    }

# ========== Stage 3e Venue门槛筛选已内联到 stage3_screen() 中 ==========

# ========== Stage 4 多步筛选辅助函数 ==========

# 量化指标正则
NUMERIC_PATTERN = re.compile(r"(\d+\.\d+|\d+%)")

# 修复成功率关键词（扩展）
SUCCESS_RATE_KEYWORDS = [
    "pass@", "full match", "accuracy", "f1", "success rate", "fix rate",
    "resolved", "bugs fixed", "plausible", "correct", "precision", "recall",
    "pass rate", "repair rate", "fixed bugs", "resolved issues", "top-", "top@", "resolved",
    # 扩展：评估相关
    "outperform", "performance", "effective", "successfully", "improvement",
    "better than", "compared to", "baseline", "state-of-the-art", "sota",
    # 扩展：修复相关
    "patches", "fixes", "repairs", "bug fix", "fixed", "repaired",
    "generate patch", "patch generation", "repair tool", "repair system"
]

# LLM 关键词（扩展列表）
LLM_KEYWORDS = [
    "llm", "large language model", "gpt", "gpt-4", "gpt-3.5", "gpt-3", "gpt-4o",
    "llama", "codellama", "deepseek", "qwen", "claude", "starcoder", "codet5",
    "codegen", "incoder", "codex", "bert", "codebert", "transformer",
    "neural network", "deep learning", "generative model", "grok"
]

# Benchmark 关键词（从表格中提取）
BENCHMARK_KEYWORDS = [
    "defects4j", "swe-bench", "swe-bench lite", "swe-bench verified",
    "swe-bench multimodal", "quixbugs", "bugs.jar", "lmdefects",
    "humaneval", "humaneval-java", "humaneval-perl", "leetcode",
    "modit", "atlas", "repobugs", "ds-1000", "bfp", "loopinv",
    "cve", "cvefixes", "big-vul", "cleanvul", "vulnloc", "extractfix",
    "arvo", "apr competition", "acpr", "codenet4repair", "codenet",
    "pytydefects", "inferredbugs", "tutorcode", "apps", "mbpp",
    "codeflaws", "zero-day", "xcodeeval", "flink", "bugsinpy",
    "introsclass", "manysstubs4j", "bears", "transfer", "b2f",
    "recoder dataset", "megadiff", "tutorllmcode", "selfapr",
    "instructvul", "seed rl"
]

def has_quantitative_success_signals(r):
    """Step 3b: 检查摘要是否包含数值指标和修复成功率关键词"""
    # 【优先级最高】标题包含工具名 → 直接通过
    title = (r.get("title") or "")
    if has_tool_name_in_title(title):
        return True
    
    title = title.lower()
    
    abstract = (r.get("abstract") or "").lower()
    venue = r.get("venue", "")
    is_tier1_venue = is_tier1(venue)
    
    # 核心APR词汇
    core_terms = ["repair", "fix", "patch", "fixing", "repairing"]
    has_core_term = any(term in title for term in core_terms)
    
    # 如果没有摘要，放宽条件
    if not abstract or len(abstract) < 50:
        # 【宽松策略】顶会 + 核心APR词 → 通过
        if is_tier1_venue and has_core_term:
            return True
        return False
    
    # 检查是否包含数字（百分比或小数点）
    has_numeric = bool(NUMERIC_PATTERN.search(abstract))
    
    # 检查是否包含成功率相关关键词
    has_success_keyword = any(kw in abstract for kw in SUCCESS_RATE_KEYWORDS)
    
    # 【策略1】Tier1 venue + 核心APR词 + 有数字 → 通过
    if is_tier1_venue and has_core_term and has_numeric:
        return True
    
    # 【策略2】Tier1 venue + 有数字 + 有成功率关键词 → 通过
    if is_tier1_venue and has_numeric and has_success_keyword:
        return True
    
    # 【策略3】核心APR词 + 有数字 + 有成功率关键词 → 通过
    if has_core_term and has_numeric and has_success_keyword:
        return True
    
    return False

def mentions_llm(r):
    """Step 3c: 检查标题或摘要是否提到 LLM 或经典模型"""
    # 【优先级最高】标题包含工具名 → 直接通过
    title = (r.get("title") or "")
    if has_tool_name_in_title(title):
        return True
    
    text = ((r.get("title") or "") + " " + (r.get("abstract") or "")).lower()
    text = unidecode(text)
    
    # 检查是否提到 LLM
    mentions_llm_keyword = any(llm in text for llm in LLM_KEYWORDS)
    
    return mentions_llm_keyword

def mentions_known_benchmark(r):
    """Step 3d: 检查摘要是否提到已知的 benchmark（极严格版本）
    
    要求：
    - 标题包含工具名，或
    - 提到至少3个benchmark（评估非常充分的论文）
    """
    # 【优先级最高】标题包含工具名 → 直接通过
    title = (r.get("title") or "")
    if has_tool_name_in_title(title):
        return True
    
    text = ((r.get("title") or "") + " " + (r.get("abstract") or "")).lower()
    if not text or len(text) < 20:
        return False
    
    text = unidecode(text)
    
    # 统计提到的 benchmark 数量
    bench_count = sum(1 for bench in BENCHMARK_KEYWORDS if bench in text)
    
    # 要求：提到至少3个benchmark（评估非常充分）
    if bench_count >= 3:
        return True
    
    return False

def has_positive_abstract(r):
    """高门槛筛选：只自动保留高置信度的 APR/vulnerability-repair 论文
    
    目标：自动保留高质量的APR论文
    
    策略：放宽顶会论文的筛选条件，严格控制其他来源
    """
    
    abs_ = (r.get("abstract") or "") + " " + (r.get("title") or "")
    t = unidecode(abs_.lower())
    title_norm = unidecode((r.get("title") or "").lower())
    has_abstract = bool(r.get("abstract") and len(r.get("abstract", "")) > 50)
    
    # 【优先级最高】检查是否包含具体的APR方法名/系统名
    # 如果标题包含方法名，说明这是介绍该APR工具的论文，应直接保留
    if has_tool_name_in_title(r.get("title") or ""):
        return True  # 直接通过！
    
    # 检查标题是否包含APR核心词汇
    core_repair_terms = ["repair", "fix", "patch", "fixing", "repairing"]
    is_core_repair_title = any(x in title_norm for x in core_repair_terms)
    
    # 检查标题是否包含APR相关词汇（包括扩展词汇）
    is_repair_title = any(x in title_norm for x in RETAIN_TITLE_TERMS)
    
    # 检查标题是否包含APR技术特征（LLM, automated, agent等）
    has_tech_indicator = any(x in title_norm for x in APR_TECH_INDICATORS)
    
    # 检查是否是 program/code/software + repair/fix 的组合
    is_program_repair = (
        any(prog in title_norm for prog in ["program", "code", "software", "bug", "vulnerability", "cve"]) and
        any(rep in title_norm for rep in ["repair", "fix", "patch", "correct"])
    )
    
    # 负面过滤：纯检测/定位，且不包含修复关键词
    is_detect_title = any(x in title_norm for x in EXCLUDE_TITLE_TERMS)
    
    if is_detect_title and not is_repair_title:
        # 检查摘要是否提到生成补丁
        if not re.search(r"\b(generate|synthesize|produce)\s+(patch|fix)", t):
            return False
    
    # 正向信号：包含 repair/patch/fix 等核心关键词
    pos = any(re.search(p, t) for p in ABSTRACT_POSITIVE_HINTS)
    
    # 评估信号：包含评估词或 benchmark 名称
    eval_signal = any(re.search(p, t) for p in EVAL_HINTS)
    bench_signal = any(b.lower() in t for b in BENCH_TERMS)
    
    # Venue 和其他属性
    is_tier1_venue = is_tier1(r.get("venue"))
    has_explicit_bench = bench_signal
    has_arxiv_id = bool(r.get("arxiv_id"))
    
    # ============================================
    # 高优先级：Tier1 会议论文（放宽条件，确保覆盖）
    # ============================================
    
    if is_tier1_venue:
        # 1. Tier1 + 核心repair标题 → 直接通过
        if is_core_repair_title:
            return True
        
        # 2. Tier1 + program/code repair组合 → 直接通过
        if is_program_repair:
            return True
        
        # 3. Tier1 + repair相关标题 + 正向词 → 通过
        if is_repair_title and pos:
            return True
        
        # 4. Tier1 + 正向词 + benchmark → 通过
        if pos and has_explicit_bench:
            return True
        
        # 5. Tier1 + 正向词 + 评估信号 + 有摘要 → 通过
        if pos and eval_signal and has_abstract:
            return True
    
    # ============================================
    # 中优先级：arXiv 预印本（适度放宽）
    # ============================================
    
    if has_arxiv_id:
        # 6. arXiv + 核心repair标题 + 正向词 → 通过
        if is_core_repair_title and pos:
            return True
        
        # 7. arXiv + program repair + benchmark → 通过
        if is_program_repair and has_explicit_bench:
            return True
        
        # 8. arXiv + repair标题 + benchmark + 评估 → 通过
        if is_repair_title and has_explicit_bench and eval_signal:
            return True
    
    # ============================================
    # 其他来源：严格要求（控制总数）
    # ============================================
    
    # 9. 任何venue + 核心repair标题 + benchmark + 评估
    if is_core_repair_title and has_explicit_bench and eval_signal:
        return True
    
    # 10. 任何venue + program repair + benchmark + 正向词
    if is_program_repair and has_explicit_bench and pos:
        return True
    
    # 默认拒绝
    return False

# stage4_screen函数已删除，其功能合并到 stage3_screen

def stage4_manual_supplement():
    """Stage 4: 补充经过人工验证的代表性论文
    
    对于在自动搜索（Stage1-2）和筛选（Stage3）中被遗漏或过滤掉的代表性工作，
    在此阶段统一补充。这是文献综述中常见的做法，确保不遗漏重要工作。
    
    Returns:
        补充的论文数量
    """
    # 读取 Stage2 和 Stage3 的结果
    stage2_path = DATA / "stage2_dedup.jsonl"
    stage3_path = DATA / "stage3_final_candidates.jsonl"
    
    if not stage2_path.exists() or not stage3_path.exists():
        print("[WARN] Required files missing; skipping stage4.")
        return 0
    
    with open(stage2_path) as f:
        stage2_papers = [json.loads(line) for line in f]
    
    with open(stage3_path) as f:
        stage3_papers = [json.loads(line) for line in f]
    
    # 加载代表性论文列表
    seeds = load_seeds_from_bib()
    if not seeds:
        print("[INFO] No representative papers to check.")
        return 0
    
    # 构建 Stage2 的索引（检查哪些没被搜索到）
    stage2_titles = {norm_title(p["title"]) for p in stage2_papers}
    stage2_dois = {normalize_doi(p.get("doi", "")) for p in stage2_papers if p.get("doi")}
    stage2_arxiv = {p.get("arxiv_id", "").lower() for p in stage2_papers if p.get("arxiv_id")}
    
    # 构建 Stage3 的索引（检查哪些被过滤掉）
    stage3_titles = {norm_title(p["title"]) for p in stage3_papers}
    stage3_dois = {normalize_doi(p.get("doi", "")) for p in stage3_papers if p.get("doi")}
    stage3_arxiv = {p.get("arxiv_id", "").lower() for p in stage3_papers if p.get("arxiv_id")}
    
    # 找出需要补充的代表性论文（在Stage2中没有 OR 在Stage3中被过滤）
    missing_seeds = []
    search_missed = []  # 自动搜索遗漏的
    filter_missed = []  # 自动筛选过滤的
    
    for seed in seeds:
        title_norm = norm_title(seed["title"])
        doi = normalize_doi(seed.get("doi", ""))
        arxiv_id = seed.get("arxiv_id", "").lower()
        
        # 检查是否在 Stage3 最终结果中
        found_in_stage3 = False
        if title_norm in stage3_titles:
            found_in_stage3 = True
        elif doi and doi in stage3_dois:
            found_in_stage3 = True
        elif arxiv_id and arxiv_id in stage3_arxiv:
            found_in_stage3 = True
        
        if found_in_stage3:
            continue  # 已经在最终结果中，无需补充
        
        # 检查是否在 Stage2 中（判断是搜索遗漏还是筛选过滤）
        found_in_stage2 = False
        if title_norm in stage2_titles:
            found_in_stage2 = True
        elif doi and doi in stage2_dois:
            found_in_stage2 = True
        elif arxiv_id and arxiv_id in stage2_arxiv:
            found_in_stage2 = True
        
        missing_seeds.append(seed)
        if not found_in_stage2:
            search_missed.append(seed)
        else:
            filter_missed.append(seed)
    
    if not missing_seeds:
        print("\n" + "="*80)
        print("Stage 4: 补充代表性论文")
        print("="*80)
        print("[SUCCESS] ✅ 所有代表性论文都通过了自动流程，无需补充！")
        print("="*80)
        
        # 直接复制 stage3 结果作为最终结果
        import shutil
        shutil.copy(stage3_path, DATA / "stage4_final.jsonl")
        return 0, 0
    
    print("\n" + "="*80)
    print("Stage 4: 补充代表性论文")
    print("="*80)
    print(f"[INFO] 发现 {len(missing_seeds)} 篇代表性论文需要补充:")
    print(f"  - 自动搜索遗漏: {len(search_missed)} 篇")
    print(f"  - 自动筛选过滤: {len(filter_missed)} 篇")
    print()
    
    # 保存补充列表（用于透明度）
    with open(DATA / "stage4_manual_supplement.jsonl", "w") as f:
        for seed in missing_seeds:
            # 添加标记说明补充原因
            seed_copy = seed.copy()
            if seed in search_missed:
                seed_copy["supplement_reason"] = "search_missed"
            else:
                seed_copy["supplement_reason"] = "filter_missed"
            json.dump(seed_copy, f, ensure_ascii=False)
            f.write("\n")
    
    print("[INFO] 补充的论文列表:")
    for i, seed in enumerate(missing_seeds, 1):
        reason = "自动搜索遗漏" if seed in search_missed else "自动筛选过滤"
        print(f"  {i}. {seed['title']}")
        print(f"     Venue: {seed.get('venue', 'Unknown')}, Year: {seed.get('year', 'Unknown')}")
        print(f"     原因: {reason}")
    
    # 合并到最终结果
    final_papers = stage3_papers + missing_seeds
    with open(DATA / "stage4_final.jsonl", "w") as f:
        for p in final_papers:
            json.dump(p, f, ensure_ascii=False)
            f.write("\n")
    
    print(f"\n[INFO] Stage4 完成: 最终保留 {len(final_papers)} 篇论文")
    print(f"  - Stage3 自动筛选: {len(stage3_papers)} 篇")
    print(f"  - Stage4 手动补充: {len(missing_seeds)} 篇 (搜索遗漏 {len(search_missed)}, 筛选过滤 {len(filter_missed)})")
    print("="*80)
    
    return len(search_missed), len(filter_missed)

def main():
    """运行完整的文献搜索和筛选流程"""
    print("\n" + "="*80)
    print("程序修复 (APR) 文献搜索与筛选流程")
    print("="*80)
    
    # Stage 1: 收集论文（已过滤年份 >= 2022）
    n1 = stage1_harvest()
    
    # Stage 2: 去重
    n2 = stage2_dedup()
    
    # Stage 3: 多步筛选
    stage3_stats = stage3_screen()
    
    # Stage 4: 补充被遗漏或过滤的代表性论文
    search_missed, filter_missed = stage4_manual_supplement()
    
    # 读取最终结果
    final_path = DATA / "stage4_final.jsonl"
    if final_path.exists():
        with open(final_path) as f:
            n4_final = sum(1 for _ in f)
    else:
        n4_final = stage3_stats["final"]
    
    # 统计Stage1的数据源分布（用于透明度）
    stage1_path = DATA / "stage1_filtered.jsonl"
    conf_count = arxiv_count = tool_count = 0
    if stage1_path.exists():
        with open(stage1_path) as f:
            for line in f:
                r = json.loads(line)
                source = r.get("source", "")
                if source.startswith("conf:"):
                    conf_count += 1
                elif source.startswith("arxiv"):
                    arxiv_count += 1
                elif source.startswith("tool_search:"):
                    tool_count += 1
    
    stats = {
        "stage1_filtered": n1,
        "stage1_conf": conf_count,
        "stage1_arxiv": arxiv_count,
        "stage1_tool_based": tool_count,
        "stage2_dedup": n2,
        "stage3a_basic": stage3_stats["stage3a_basic"],
        "stage3b_quant": stage3_stats["stage3b_quant"],
        "stage3c_llm": stage3_stats["stage3c_llm"],
        "stage3d_bench": stage3_stats["stage3d_bench"],
        "stage3e_quality": stage3_stats["stage3e_quality"],
        "stage3_final": stage3_stats["final"],
        "stage4_search_missed": search_missed,
        "stage4_filter_missed": filter_missed,
        "stage4_supplement_total": search_missed + filter_missed,
        "stage4_final": n4_final
    }
    
    print("\n" + "="*80)
    print("文献搜索流程完成")
    print("="*80)
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    print("\n流程说明:")
    print("  Stage 1: 从各数据源收集论文（已过滤 year >= 2022）")
    print("    - 会议/期刊: 爬取顶会论文")
    print("    - arXiv: 关键词搜索 + 引用数筛选")
    print("    - 工具定向搜索: 基于代表性工具名称搜索（每个工具取前3篇）")
    print("  Stage 2: 去除重复论文")
    print("  Stage 3: 多步筛选（APR相关性、量化指标、LLM、Benchmark、质量优先）")
    print("  Stage 4: 补充遗漏的代表性论文（搜索遗漏 + 筛选过滤）")
    print(f"\n最终结果: stage4_final.jsonl ({n4_final} 篇论文)")
    print(f"  其中手动补充: {search_missed + filter_missed} 篇 (详见 stage4_manual_supplement.jsonl)")
    print("="*80)
    
    with open(DATA / "pipeline_stats.json", "w") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
