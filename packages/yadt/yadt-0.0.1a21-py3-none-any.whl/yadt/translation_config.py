from yadt.const import (
    CACHE_FOLDER,
)
import os


class TranslationConfig:
    def __init__(
        self,
        input_file: str,
        translator,
        lang_in: str,
        lang_out: str,
        font: str | None = None,
        pages: str | None = None,
        output_dir: str | None = None,
        debug: bool = False,
        working_dir: str | None = None,
        no_dual: bool = False,
        no_mono: bool = False,
        formular_font_pattern: str | None = None,
        formular_char_pattern: str | None = None,
        qps: int = 1,
    ):
        self.input_file = input_file
        self.translator = translator
        self.font = font
        self.pages = pages
        self.page_ranges = self._parse_pages(pages) if pages else None
        self.debug = debug
        self.lang_in = lang_in
        self.lang_out = lang_out
        self.no_dual = no_dual
        self.no_mono = no_mono
        self.formular_font_pattern = formular_font_pattern
        self.formular_char_pattern = formular_char_pattern
        self.qps = qps

        if working_dir is None:
            working_dir = os.path.join(
                CACHE_FOLDER, "working", os.path.basename(input_file).split(".")[0]
            )
        self.working_dir = working_dir

        os.makedirs(working_dir, exist_ok=True)

        if output_dir is None:
            output_dir = os.path.dirname(input_file)
        self.output_dir = output_dir

        os.makedirs(output_dir, exist_ok=True)

    def get_output_file_path(self, filename):
        return os.path.join(self.output_dir, filename)

    def get_working_file_path(self, filename):
        return os.path.join(self.working_dir, filename)

    def _parse_pages(self, pages_str: str | None) -> list[tuple[int, int]] | None:
        """解析页码字符串，返回页码范围列表

        Args:
            pages_str: 形如 "1-,2,-3,4" 的页码字符串

        Returns:
            包含(start, end)元组的列表，其中-1表示无限制
        """
        if not pages_str:
            return None

        ranges = []
        for part in pages_str.split(","):
            part = part.strip()
            if "-" in part:
                start, end = part.split("-")
                start = int(start) if start else 1
                end = int(end) if end else -1
                ranges.append((start, end))
            else:
                page = int(part)
                ranges.append((page, page))
        return ranges

    def should_translate_page(self, page_number: int) -> bool:
        """判断指定页码是否需要翻译

        Args:
            page_number: 页码

        Returns:
            是否需要翻译该页
        """
        if not self.page_ranges:
            return True

        for start, end in self.page_ranges:
            if start <= page_number and (end == -1 or page_number <= end):
                return True
        return False
