import configparser

_config = configparser.ConfigParser(interpolation=None)
_config.read("config.ini")


class ApplicationSettings:
    def telegram_api_id(self) -> str:
        return _config["telegram"]["api_id"]

    def telegram_api_hash(self) -> str:
        return _config["telegram"]["api_hash"]

    def telegram_phone(self) -> str:
        return _config["telegram"]["phone"]

    def logger_format(self) -> str:
        return _config["logger"]["format"]

    def concat_explain(self) -> bool:
        return _config.getboolean("concat", "explain")

    def concat_timeout_s(self) -> int:
        return int(_config["concat"]["timeout_s"])

    def format_remove_link_preview(self) -> bool:
        return _config.getboolean("format", "remove_link_preview")
