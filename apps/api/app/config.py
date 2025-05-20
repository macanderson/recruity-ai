from functools import lru_cache
from pydantic import BaseSettings

class Settings(BaseSettings):
    api_title: str = "Recruity AI API"
    tenant_header: str = "X-Tenant-ID"

    class Config:
        env_prefix = "RECRUITY_"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
