from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # .env 파일에서 읽어올 변수들을 여기에 필드로 선언합니다.
    # 필드 이름은 .env 파일의 변수 이름과 대소문자를 구분하지 않고 일치해야 합니다.
    GOOGLE_API_KEY: str
    PDF_PARSE_API_ENDPOINT: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
