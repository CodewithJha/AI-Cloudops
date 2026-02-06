import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class AppConfig:
    app_title: str = os.getenv("APP_TITLE", "AI CloudOps")
    default_web_url: str = os.getenv("DEFAULT_WEB_URL", "http://localhost:8000")


@dataclass(frozen=True)
class EmailConfig:
    host: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    port: int = int(os.getenv("SMTP_PORT", "587"))
    username: str = os.getenv("SMTP_USERNAME", "")
    password: str = os.getenv("SMTP_PASSWORD", "")
    from_address: str = os.getenv("SMTP_FROM", "")


@dataclass(frozen=True)
class AWSConfig:
    region: str = os.getenv("AWS_REGION", "us-east-1")
    default_s3_bucket: str = os.getenv("S3_DEFAULT_BUCKET", "")
    profile: str = os.getenv("AWS_PROFILE", "")
    # Access keys are read by boto3 via env if present; prefer using profiles or roles


app_config = AppConfig()
email_config = EmailConfig()
aws_config = AWSConfig()

