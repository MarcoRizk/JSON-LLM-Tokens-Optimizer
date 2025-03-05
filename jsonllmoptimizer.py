import json
import re
from datetime import datetime


class JsonTokenOptimizerBase:
    def __init__(self, json_data):
        self._json_data: str = self.minify_json(json_data)

    @staticmethod
    def minify_json(data):
        """
        Minifies JSON by removing spaces and unnecessary quotation marks where possible.

        :param data: The input JSON (dict or list).
        :return: A compact JSON string.
        """
        return json.dumps(data, separators=(",", ":"), ensure_ascii=False)

    @staticmethod
    def _truncate_iso_timestamps(text, level="minute"):
        """
        Finds ISO 8601 date-time stamps in a string and truncates them
        to the specified level (minute, hour, date, or month), modifying the original text.
        Drops timezone information.

        :param text: The input string containing date-time stamps.
        :param level: The truncation level ('minute', 'hour', 'date', or 'month').
        :return: The modified string with truncated timestamps.
        """
        # Regex pattern to match ISO 8601 timestamps (YYYY-MM-DDTHH:MM:SSZ or with timezone offsets)
        iso_pattern = re.compile(r"\b(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2}))\b")

        def truncate_match(match):
            try:
                dt = datetime.fromisoformat(match.group(0).replace("Z", "+00:00"))  # Convert ISO 8601 to datetime

                if level == "minute":
                    return dt.strftime("%Y-%m-%dT%H:%M")
                elif level == "hour":
                    return dt.strftime("%Y-%m-%dT%H:00")
                elif level == "date":
                    return dt.strftime("%Y-%m-%d")
                elif level == "month":
                    return dt.strftime("%Y-%m")
                else:
                    raise ValueError("Invalid truncation level. Choose from 'minute', 'hour', 'date', or 'month'.")
            except ValueError:
                return match.group(0)  # Keep original if parsing fails

        return iso_pattern.sub(truncate_match, text)

    def truc_timestamp(self, level="minute"):
        self._json_data = self._truncate_iso_timestamps(self._json_data, level)
        return self

    def strip_quotes(self):
        self._json_data = self._json_data.replace('"', '')
        return self

    def replace(self, old, new):
        self._json_data = self._json_data.replace(old, new)
        return self
    @staticmethod
    def _abbreviate_numbers_in_text(text):
        """""
        Finds numbers in a string and abbreviates them (e.g., 1200000 -> 1.2M, 7500 -> 7.5K),
        excluding timestamps.
        :param text: The input string containing numbers.
        :return: The modified string with abbreviated numbers.
        """
        iso_pattern = re.compile(r"\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})\b")
        number_pattern = re.compile(r"\b\d+\b")

        def abbreviate_match(match):
            num = int(match.group(0))
            if num >= 1_000_000:
                return f"{num / 1_000_000:.1f}M"
            elif num >= 1_000:
                return f"{num / 1_000:.1f}K"
            return str(num)

        # Temporarily replace timestamps with placeholders
        timestamps = {match.group(0): f"{{TIMESTAMP_{i}}}" for i, match in enumerate(iso_pattern.finditer(text))}
        temp_text = text
        for original, placeholder in timestamps.items():
            temp_text = temp_text.replace(original, placeholder)

        # Abbreviate numbers in the modified text
        temp_text = number_pattern.sub(abbreviate_match, temp_text)

        # Restore timestamps
        for original, placeholder in timestamps.items():
            temp_text = temp_text.replace(placeholder, original)

        return temp_text

    def abbreviate_numbers(self):
        self._json_data = self._abbreviate_numbers_in_text(self._json_data)
        return self

    def output(self):
        return self._json_data
