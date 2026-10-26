from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://car_agency:car_agency@localhost:5433/car_agency"

    # JWT signing key, required. Generate one with: python -c "import secrets; print(secrets.token_urlsafe(32))"
    secret_key: str
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # Initial API user created by app.seed, only if both are set
    first_user_email: str | None = None
    first_user_password: str | None = None


settings = Settings()
