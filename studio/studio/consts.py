GITHUB_CLIENT_ID = ""
GITHUB_OAUTH_URL = (
    f"https://github.com/login/oauth/authorize"
    f"?client_id={GITHUB_CLIENT_ID}"
    f"&redirect_uri=http://localhost:3000/auth/callbacks/github"
    f"&scope=read:user"
)

VE_USERPOOL_UID = ""
VE_CLIENT_ID = ""
VE_CLIENT_SECRET = ""
VE_OAUTH_URL = (
    f"https://cis-test.cn-beijing.volces.com/userpool/{VE_USERPOOL_UID}/authorize"
    f"?response_type=code"
    f"&client_id={VE_CLIENT_ID}"
    f"&redirect_uri=http://localhost:3000/auth/callbacks/ve"
    f"&scope=openid+email"
    # f"&state=test"
)
VE_TOKEN_ENDPOINT = (
    f"https://cis-test.cn-beijing.volces.com/userpool/{VE_USERPOOL_UID}/oauth/token"
)
VE_USERINFO_ENDPOINT = (
    f"https://cis-test.cn-beijing.volces.com/userpool/{VE_USERPOOL_UID}/userinfo"
)
