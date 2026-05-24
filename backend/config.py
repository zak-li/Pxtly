from pathlib import Path

from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class FabricSettings(BaseSettings):
    environment: str = Field(default="development")
    fabric_wallet_path: Path
    fabric_connection_profile: Path
    fabric_channel: str
    fabric_chaincode: str
    fabric_tls_enabled: bool
    fabric_grpc_timeout: int
    redis_url: str

    vault_addr: str = Field(default="https://127.0.0.1:8200")
    vault_token: SecretStr = Field(...)

    groq_api_key: str = Field(default="")
    groq_model: str = Field(default="llama-3.3-70b-versatile")

    fabric_retry_max_attempts: int
    fabric_retry_base_delay: float
    fabric_retry_factor: float
    fabric_retry_jitter: float
    fabric_retry_circuit_breaker_threshold: int
    fabric_retry_circuit_breaker_timeout: float

    fabric_events_rate_limit: float
    fabric_events_redis_channel: str
    fabric_events_targets: str
    fabric_events_required_payload_fields: str
    fabric_events_grpc_reconnect_delay: float
    fabric_events_grpc_simulation_delay: float

    fabric_required_msps: str
    fabric_ledger_not_found_error_string: str
    fabric_endorsement_error_string: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class Settings(FabricSettings):
    database_url: str
    allowed_origins: str
    log_level: str = "INFO"

    # ── Keycloak / OIDC ──────────────────────────────────────────────────────
    keycloak_url: str = Field(
        default="http://10.10.10.150:8080",
        description="Base URL of the Keycloak server (no trailing slash)",
    )
    keycloak_realm: str = Field(default="rwa-platform")
    keycloak_client_id: str = Field(default="rwa-api")
    keycloak_client_secret: str = Field(...)
    # Full URL the browser is redirected to after Keycloak authentication.
    keycloak_callback_url: str = Field(
        default="http://10.10.10.150:8000/api/v1/auth/callback"
    )
    # Set False only for dev with self-signed TLS
    keycloak_verify_tls: bool = Field(default=False)

    # ── gRPC server ──────────────────────────────────────────────────────────
    grpc_port: int = Field(default=50051)
    grpc_server_cert: str = Field(default="")
    grpc_server_key: str = Field(default="")
    grpc_ca_cert: str = Field(default="")

    @field_validator("keycloak_url")
    @classmethod
    def strip_trailing_slash(cls, v: str) -> str:
        return v.rstrip("/")

    @model_validator(mode="after")
    def validate_production_security(self) -> "Settings":
        if self.environment == "production":
            if not self.fabric_tls_enabled:
                raise ValueError("TLS must be enabled in production.")
            if "localhost" in self.database_url:
                raise ValueError("localhost database URL is not allowed in production.")
            if not self.keycloak_verify_tls:
                raise ValueError("KEYCLOAK_VERIFY_TLS must be true in production.")
        return self


settings = Settings()
