from firebase_admin import credentials, initialize_app, storage, db, delete_app
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
def google_drive():
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    SERVICE_ACCOUNT_FILE = {
    "type": "service_account",
    "project_id": "principal-iris-425023-p0",
    "private_key_id": "c8036096940f266d24ae93382c221e27fac46271",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDGg2NBJP+3ykUu\nYtopSV3NIf4J7Ibf5SOjWJTh7dXy7jjkV8zabv6f8qL1jHnZNObo5OyLnMkzwy3t\n5VChG2C6Zb/75oL3PcIfF88ndQZwsSiF1v2tPFU8GcXw/EEI5jxHMnlgUmFKeyk7\nRg2Rt9p2xwymOAQCjDL6zZQGyleBRaVGPW5su2a5a/vPoSqEkFg4gZM7d1Lcz2yI\nbL5Y0+kzc5A+uJrrLX0lESlzoTwe9Jr1BDXJBMJaZfb2aHLow0+ManYTrjPCVaNV\n2nPoaxRerQq5RU+BxsnEjRWztDVjtqm0tJJPZS0ixzB/hBJadnuAOXWe/Qx1YZSw\n1C12V/K9AgMBAAECggEAB+Tbph7ApO54+1sfo1cb3z6EBi9ydu0JZ9/PV2NPebdA\n+JR6IC0cNQBNn8CJT3OL4Aggqie31W8AvR5KjtvAoRAH4A5kBjCzEnsDkRAAKB3z\nYD49nOK5pPmh1/2HGPp/vEAr6lem9o8nA14RALyJeAIlOkrmZev7Uo2pJZnCCpvI\nUC7B/CJ9YeH28+xafZF94mjGFjkUeOsk5iqMgcF6/fqY1oF9KdRbDDKPNY+rgsS0\ngZQBoRQ/nrczwGTgO5//5b50G8SbF7UvwrEkWk7c0PpGHJbdL50/X5GZxMB4F4Wf\ndaVNBUPco1P/b2r0kIqluoG0fNAvPk92JkhXMVXRBQKBgQDwwVmFIaYluJW1KqzY\nzALGzl2MXCodfdKP/aCKfhC45A2Mz0rPrLpiqdGTR1c6HxS16wOIlMRozZMZgKS2\nyfeqlasCK6KWSQ6WPNL85KGSNch5w90MINedxJS4bQlwp98qAyjZGx+82jrMuM6G\n0Ho4rEdbyJ3/aYJsYc77yQy1ywKBgQDTFUsUqARlD50qYDenZYn3Jct7s5r17571\nwcjffPbfM/H3aIVIHk9ZQEWuPROaT+waVu6w37gy7VjqOdvQ8Iy26+4KHLE8G3Yw\nSYVhnGI5Gk1b0YA7Ugau1t5gYoIrwbscqVySoZpDzIpqZ3alfRMUHteZ3ktxY7U+\ngxmRhDMolwKBgACrKMp723BDYPcN1UkM1/0hWZUoNF28mbcYpzd7PiSlTXxUnwqQ\nmjvn6NMV4aIhr/cJXgslDp6T45KwjsSLLwrkO4NYB62PKmE0bgmRwPkc+R+NcbG0\n7aRchWU1uE79yFrfg1+G+cGWgY9L/BbXwV8i61fP6NBqxJf0dZSxbD2dAoGBAJjr\nFidyySxFsYBfkDIPV3HayZ1mMl71J12288UkjNyKj0LDT7s9ahKog1KFIMxsFgnG\n7MjqalFKrV2SaPLnManbJenhe2ymIGs++AgM+QORUHWyQom3FOxY8WU2OENm6B0N\nfOklddKkPap0JfohsE6lQWBRMKqGp2kQJNfMxBslAoGBAL4PZP9zN56eLbR2kCv0\nU2fXVfTaEnS3L1yPBI2T+Qs+LTgmpvvxxu6wcdjlp+RQ7vX6WFlmBXJY7bDwLjXw\ntStMad2mpTqWWf68qCTD5LWvIVKpusc5fgvX27pwVG4zYcChvQoEDRHUv0+f2uBf\n/Is/0gQjMwpLiZVIhgEZlmNP\n-----END PRIVATE KEY-----\n",
    "client_email": "protocol-driver@principal-iris-425023-p0.iam.gserviceaccount.com",
    "client_id": "106714249503349991659",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/protocol-driver%40principal-iris-425023-p0.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
    }
    creds = service_account.Credentials.from_service_account_info(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    return service

def Firebase_App():

    cred1 = {
    "type": "service_account",
    "project_id": "aicompanydata1",
    "private_key_id": "529bc745b8f2d1692f21493bbbf62bc88f044497",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDtGtXQ2kmZjcJg\nTixPE26DpE0ku59vlhOrGb3iQZqnTziSVqS5RO6WCFnLl8nW4/9JglGFEE2l9Dax\nVldMDzhcnzppN8YTrNKqtvQND+wWpaaPDroitS4zbhVi3RGJOGECerz+cA0FfAIf\n8IL/jRs/gMkTTKBJNFC/s6f9b+NMhNVcKT2E0DHf9KoMspDvgiHqaanWXPNXt3Ol\n90pGUofmCJTX3ioS6hldmVvfbQGH9RP6yHSAYd1S6eGAnPwrdScng5LIZqQ2j+Fw\n20oRt2nKfRuozKHaxgAtlTGMYmSTVPhy7ijeHFm2XSz2cn7i3waUjgPfdBCGN7iS\n39SSVb29AgMBAAECggEAO/mxQyKsQli+5cBwadI2/rqVPujsw/uY3wtkYjKJDbA2\n1aFwCmM63J2hJSQwjJhgj3YU6807bvKO0R3PeDBTZ+5pBotyobByG3eq1REFfZcK\nQh6OC9B7rsu2Qis8T9MAivGEE/JBAPWkzfJ3GHBXh6Eqe6TC2LGQiWVG5Y8jVku4\nxpin0WzqeTl0G8IfKWHXwh2ELP8ubrLfnVHf0cYVnt64DW6sI4U3xSWnvq1g5FKa\nKJM9uj7Uv/84pOFlFSW5WyGR2cJ7ng6J2uRZcCDnVTAOI11cXxQnBbBLcntMwS6D\nLNsQi9vhQoleDwLVRkLhTrvk1yqFJTVHRtwJQStVOwKBgQD79NsuLfacikCxZNaR\nhsHKMsfAxpYzlUqDvOWNjJKyt1aDvRFuPZ2WEa90dVgTPBPNaF75DU3YhEeZyCW/\nYLp12G0e8S0aPdHsdLAvO5ehc75doaiwVVcuH2+uMDSy+IJjXl3h7sc2KNs7mXNE\nyQCCdIwATnwj/onHr6DhB4mKwwKBgQDw6PZS8h8xR6a/TmeJ1jVjRtnM6tEQ2bs/\n4n+l3EnKfy9ane9a3620SFj8AIGjWaua6rD6FEZqdABqisc3IayX7GsSE339gUaI\naLgXQQsm3pKGaZw65dNJ5HZGoquUDjyRNsfdQyIRfHb2LukAKK0hKr6+pxWdg6ph\ntZXApdoNfwKBgGK6+1xoNHf5EQqyegZCqROjvHTFHLyP5sgisE08ZYvUnfk3kGoD\niQnyWi+nf+DhrNzT5ktvtC6A/1G6hVgt/kMJkREL7uGWkfk3bIbFslBY+6LTIzgd\n6PCw7uFyEGSFTwrDQsSy/asybV44blvo6+My6l2AY9Ly/miaYM9tVa9jAoGBANLr\n9HZMvBimVgzatXYN0PJZnul1kZPCPdpCEWaDByw+zJP3ARA8FFZqnVYNj3MYWFGr\nN0XMqJYdeBvP43mWhwkAmgHahQ2FuN5HaR4a+YuPhRQftQQwIhxo5VEUrUpUaJzv\nLG/BjjtnELSb/63+7w3B4f0ERr2BAJTJqhJgYxg7AoGAeEI4skSDN0BILrVoX2mD\ngnnajTRAPpQguTR2RP743KMx6Md09RzKuCtB2F7ET/X6mGr0C3UM31j7q+KTlxAC\nILavy3Ruk6itLe5Ie8X1npe0BIMPKFRCrogfo5SHQDhWd2N/6+m1MgLF5Pqr4cVE\nXrlCtssqR5Upcmq+L5YdLrU=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-47yps@aicompanydata1.iam.gserviceaccount.com",
    "client_id": "102000584574845908426",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-47yps%40aicompanydata1.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
    }

    credt1 = credentials.Certificate(cred1)
    app1 = initialize_app(credt1, {
            'storageBucket': 'aicompanydata1.appspot.com',
            'databaseURL': 'https://aicompanydata1-default-rtdb.europe-west1.firebasedatabase.app'
    }, name='app1')


    bucket = storage.bucket(app=app1)
    return app1, bucket




class OpenAIKeysteste:
    def keys():
        companyname = "teste"
        str_key = "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"
        return str_key
    


            