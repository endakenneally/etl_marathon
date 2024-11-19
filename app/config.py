class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://etl_user:etl_password@etl_db:5432/etl_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
