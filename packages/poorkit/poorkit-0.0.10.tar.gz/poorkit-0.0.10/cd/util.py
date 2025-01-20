import os
import re
from typing import Set, Tuple

# 为不同的语言定义正注释行检测正则表达式
REGS_FOR_LANGS = {
    "python": r"^\s*#",
    "py": r"^\s*#",
    "javascript": r"^\s*//",
    "js": r"^\s*//",
    "jsx": r"^\s*//",
    "typescript": r"^\s*//",
    "ts": r"^\s*//",
    "tsx": r"^\s*//",
    "java": r"^\s*//",
    "c": r"^\s*//",
    "cpp": r"^\s*//",
    "go": r"^\s*//",
    "golang": r"^\s*//",
    "rust": r"^\s*//",
    "rs": r"^\s*//",
    "shell": r"^\s*#",
    "sh": r"^\s*#",
    "ruby": r"^\s*#",
    "perl": r"^\s*#",
    "php": r"^\s*//",
    "swift": r"^\s*//",
    "kotlin": r"^\s*//",
    "scala": r"^\s*//",
    "groovy": r"^\s*//",
    "lua": r"^\s*--",
    "r": r"^\s*#",
    "matlab": r"^\s*%",
    "julia": r"^\s*#",
    "haskell": r"^\s*--",
    "erlang": r"^\s*%",
    "elixir": r"^\s*#",
    "clojure": r"^\s*;",
}

# 空白行正则表达式
REG_BLANK_LINE = r"^\s*$"

# 扩展名到语言名映射
EXT_LANG_MAPPING = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".java": "java",
    ".c": "c",
    ".cpp": "cpp",
    ".go": "go",
    ".rs": "rust",
    ".sh": "shell",
    ".rb": "ruby",
    ".pl": "perl",
    ".php": "php",
    ".swift": "swift",
    ".kt": "kotlin",
    ".scala": "scala",
    ".groovy": "groovy",
    ".lua": "lua",
    ".r": "r",
    ".m": "matlab",
    ".jl": "julia",
    ".hs": "haskell",
    ".erl": "erlang",
    ".ex": "elixir",
    ".clj": "clojure",
}


def get_supported_lang(lang_ext: str) -> str:
    """
    获取支持的语言名称

    :param lang_ext: 语言扩展名, 以 "." 开头
    :type lang_ext: str
    :return: 对应的语言名称
    :rtype: str
    """
    return lang_ext[1:] if lang_ext in EXT_LANG_MAPPING else ""


def is_comment_or_blank(lang: str, line: str):
    comment_reg = REGS_FOR_LANGS.get(lang, r"^\s*//")
    # 检查是否为空白行或注释行
    return re.match(comment_reg, line) or re.match(REG_BLANK_LINE, line)


def mapping_input_langs_to_supported(langs: Tuple[str]) -> Set[str]:
    return set(lang for lang in langs if lang in REGS_FOR_LANGS)


def extract_code_from_directory(dirs, langs, output_file):
    support_langs = mapping_input_langs_to_supported(langs)
    print(f"support langs: {support_langs}")
    with open(output_file, "w", encoding="utf-8") as outfile:
        for directory in dirs:
            for root, _, files in os.walk(directory):
                for file in files:
                    # get file extend name
                    _, ext = os.path.splitext(file)
                    lang = get_supported_lang(ext)
                    if lang not in REGS_FOR_LANGS or lang not in support_langs:
                        continue
                    print(f"extract code from {root} {file}")
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as reader:
                        lines = reader.readlines()
                        filtered_lines = [
                            line
                            for line in lines
                            if not is_comment_or_blank(lang, line)
                        ]
                        if filtered_lines:
                            outfile.writelines(filtered_lines)
                            if not filtered_lines[-1].endswith("\n"):
                                outfile.write("\n")
