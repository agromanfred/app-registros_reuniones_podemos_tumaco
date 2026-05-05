SQLALCHEMY_DATABASE_URI = "mysql+pymysql://2yZ2BdEEZzbvjRo.root:Yvy5VzJdfWY9QiNM@gateway01.us-east-1.prod.aws.tidbcloud.com:4000/reuniones_db"
SQLALCHEMY_ENGINE_OPTIONS = {
    "connect_args": {
        "ssl": {
            "ssl_mode": "VERIFY_IDENTITY"
        }
    },
    "pool_recycle": 280
}
 

SQLALCHEMY_TRACK_MODIFICATIONS = False