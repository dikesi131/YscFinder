from typing import List, Dict


class Statistics:
    def __init__(self, keys: List[str]):
        self.keys = keys
        self.counts = {k: 0 for k in keys}

    def count_keys(self, name: str):
        """count the occurrences of each key in the result"""
        if name.strip() in self.keys:
            self.counts[name] += 1

    def get_positive_counts(self) -> Dict[str, int]:
        """return the counts of each key if count > 0
        Returns:
            dict[str, int]: A dictionary with keys and their counts greater than 0.
        """  # noqa
        return {k: v for k, v in self.counts.items() if v > 0}
