from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./super_inspections.db"
    # Comma-separated list of allowed frontend origins (e.g. your Netlify URL).
    cors_origins: str = "http://localhost:5173"

    class Config:
        env_file = ".env"

    @property
    def sqlalchemy_url(self) -> str:
        """Neon gives postgresql://...; SQLAlchemy needs the psycopg (v3) driver name."""
        url = self.database_url
        for prefix in ("postgres://", "postgresql://"):
            if url.startswith(prefix):
                return "postgresql+psycopg://" + url[len(prefix):]
        return url

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip().rstrip("/") for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
