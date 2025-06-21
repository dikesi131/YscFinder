from typing import Any
from .statistics import Statistics  # type: ignore
from typing import List, Dict
from collections import Counter
import math


class CliOutput(Statistics):
    def __init__(self, keys: List[str]) -> None:
        super().__init__(keys)
        self.print_format = "{name}\t->\t{value}\t(Line: {line_num})"
        # self.standard_pass_shannon = 3.42
        # self.standard_phone_shannon = 2.63
        # self.standard_idcard_shannon = 2.91
        # self.standard_bankcard_shannon = 2.79
        # min shannon for pass, phone, id_card, generic_card_regex
        self.min_shannon_lst = [1.30, 1.24, 1.88, 1.28]
        # max shannon for pass, phone, id_card, generic_card_regex
        self.max_shannon_lst = [4.73, 3.28, 3.39, 3.30]
        self.regex_keys = ["Possible_Creds", "phone", "id_card", "generic_card_regex"]  # noqa
        self.min_shannon_map = {**{key: min_shannon for key,
                                   min_shannon in zip(self.regex_keys,
                                                      self.min_shannon_lst)}}
        self.max_shannon_map = {**{key: max_shannon for key,
                                   max_shannon in zip(self.regex_keys,
                                                      self.max_shannon_lst)}}

    def calculate_shannon_entropy(self, text: str) -> float:
        """
        calculate the Shannon entropy of a string (in bits/char)
        Args:
            text (str): The input string to calculate entropy for.
        Returns:
            float: The Shannon entropy value (0~8).
        """
        if not text:
            return 0

        # 统计字符频率
        char_counts = Counter(text)
        text_length = len(text)

        # 计算熵值
        entropy = 0.0
        for count in char_counts.values():
            probability = count / text_length
            entropy += probability * math.log(probability, 2)

        return -entropy

    def check_shannon_entropy(self, name: str, text: str) -> bool:
        """
        Check if the Shannon entropy of a given text exceeds the standard threshold.
        Args:
            text (str): The input string to check.
        Returns:
            bool: True if the entropy exceeds the standard threshold, False otherwise.
        """  # noqa
        if name not in self.regex_keys:
            return True
        entropy = self.calculate_shannon_entropy(text)
        min_shannon = self.min_shannon_map.get(name, 0)
        max_shannon = self.max_shannon_map.get(name, 8)
        return min_shannon <= entropy <= max_shannon

    def cli_print(self, matched: List[Dict[str, Any]]) -> None:
        '''Print the matched results in a CLI-friendly format.

        Args:
            matched (list[Any]): A list of dictionaries containing matched results.
        '''  # noqa
        for match in matched:
            name = match.get('name', 'Unknown')
            value = match.get('matched', '').strip()
            num = match.get('line', '-')
            line = self.print_format.format(
                name=name,
                value=value,
                line_num=num
            )
            self.count_keys(name)
            print(line)
