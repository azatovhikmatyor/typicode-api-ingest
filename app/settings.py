class Settings:
    """Read only properties for project configuration."""

    def __init__(
        self, base_url: str | None = None, endpoints: list | tuple | set | None = None
    ) -> None:
        self.__base_url = (
            base_url if base_url else "https://jsonplaceholder.typicode.com"
        )
        self.__endpoints = (
            endpoints
            if endpoints
            else ("posts", "comments", "albums", "photos", "todos", "users")
        )
        self.__cache_folder = "cache"

    def full_url(self, endpoint: str) -> str:
        if not endpoint in self.endpoints:
            raise ValueError(f"endpoint can only be one of the {self.endpoints}")
        return f"{self.base_url}/{endpoint}"

    @property
    def base_url(self) -> str:
        return self.__base_url

    @property
    def endpoints(self) -> list[str]:
        return self.__endpoints

    @property
    def cache_folder(self) -> str:
        return self.__cache_folder


# default settings
app_settings = Settings()
