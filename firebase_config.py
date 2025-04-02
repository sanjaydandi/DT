import firebase_admin
from firebase_admin import credentials, auth, firestore

# Replace with your Firebase config
firebase_config = {
  "type": "service_account",
  "project_id": "studoattendance",
  "private_key_id": "6675e4efe5ab1d3a85d42b8ea1800327c75686df",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCsbGKVN1Xepr7b\nqvnVbAv01F2A7CxJgHTLkCFfIMM/vUeCebTvBcX7cAdPgSpKO481NA9+50VqOLp/\n7lz8E0au1h8Do4MUfZobAQBiTWCCu5pkUfHkQZeX5W1RUf5s4wdpjpNlCTJTIfZc\n8gAdjo989+ZdP2KsDCnj1tm0diMF6PizXtPgx+LRLoj8U4ZREHkwnarKSP4GiPFH\n+T4dmf5pju/5FanQ+b379vtketil6eMiitWOdniLi52Ko70QpErswI8bEqBy3T9N\nvzE+JQSttKImVTMTeoK0jEL/CBmNR6Ln9m1YXfkv6yp8numjvyBON16vqemWD3wA\n3S+qhmjFAgMBAAECggEABGn+6RaCUIGgy7NYE35hXPptzV3ecWBEPSzaqdqHHRPd\np4mxl9fkPmBbE445NK7LJv/G8Mb/aC19GsbRoxNkQRgSsa9nLOhdQFk5dwrHkHk4\nhd5yLJeAR790GbuZYZS7TRi9Db5bRzUMn0sDtT3/zuFyyIrVnhVuohpPNvc6RM2r\n9SCvvgue505HgdQQON0bhAFu1rO4cVN40xQtCF/GSrhkk5Ba/wFwwXFlb1wJkXpe\ngu1EPFIdShOF6zpns0g7JM0Y3UrX4ji/e/ZxKpuP19GxAfhY58s0itF6kWfBqA1O\njGPK4AtB6M3L7C7zYLp3QYA0cJiOYS8U4ThuaTt84QKBgQDpb7MEGevahdy18KF/\nuu/dv8xHENR1xeVyzdoI5CJ8mdfU6a5Nj/CIJ2u9UZWlDfDNxMjr4dqoXqxFEpIW\n0c5zIFoftu4tLH/G+JFODPxGwwqn76I2duJdncYwK/mjQYqoR/NoBaS6pRZJsJKc\ntprvxxk3BHP9PUluBLVjkgW5IQKBgQC9FvERKZCf+aiZAjlv/vD7GCx39aQd5LgR\n8WfIibfL5HBMiuTQgdFwSchVV5nfoZhsGp2cYGCEWXS6MyCTVZ6BArjOUOxPaEuW\nDgJrSmCOtaxoM/mJztDuf3twQzIBSspG2XwExqFLp8DRFXX+n2xJ3K+dr49XihpP\nZeNEMYrHJQKBgQDj5ccRo/Tc3H9DqO8icnCnPw7B+q5RZKjDUjEhKQh6OP+7v4AJ\n/RLI+iN3KuU7xMZpPUsi7ta4NeVdcenqGV7Cir0x5TfWJnGA4T+Kwaaxtsz6czsc\njSgmWVgZw3Tua5hg/g2maowOJAoEWzxnfub4XJpDWjea7nB31mT4FqE7wQKBgDt/\nFXkN+AiuGIOUdJgtwotvTsasDuitB9H1gG9UDfXkugULivWkc07+mD9qIeuAwCH7\nue3zUUszjovr/Gr/fLEhNx8LzV8q9OWRIOe7bmhY95eOCw12er0gdamcKwbHDqB+\nXAxwp13TudLQCuGELiGLg+J81AB6Xs7uwzS41e7VAoGBAOQmz8MtxtikDJkzUnyC\nlWlinvmSJcQGUmDUFN7bBmRddx+RQ2FyjXdxQ6zX86CUkaMBGMfspC1h1EeuQA+P\nGNoxi6Peo+QNIpr1XHEgbnm6fCig9l+NCGx/yCI0lEUFGPcXBgCJV5qAS7SP2h+u\nyvNmR2rDrXxeUMiEdzKA2Jh/\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@studoattendance.iam.gserviceaccount.com",
  "client_id": "109319114578818113354",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40studoattendance.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred)

db = firestore.client()  # Firestore database reference
