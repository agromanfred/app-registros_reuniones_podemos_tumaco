SQLALCHEMY_DATABASE_URI = "mysql+pymysql://2yZ2BdEEZzbvjRo.root:Yvy5VzJdfWY9QiNM@gateway01.us-east-1.prod.aws.tidbcloud.com:4000/reuniones_db"
SQLALCHEMY_ENGINE_OPTIONS = {
    "connect_args": {
        "ssl": {
            "ca": "C:/Users/USUARIO/Downloads/isrgrootx1.pem"
        }
    }
}

SQLALCHEMY_TRACK_MODIFICATIONS = False