import requests


token ='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'


# url = "https://api.github.com/repos/mozilla/geckodriver/releases/latest"
url = "https://api.github.com/user"

headers = {"Authorization": f"token {token}"}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Autenticação bem-sucedida! 🎉")
    print(response.json())  # Exibe os detalhes do usuário
else:
    print("Erro na autenticação:", response.json())


curl --request GET \
--url "https://api.github.com/octocat" \
--header "Authorization: Bearer YOUR-TOKEN" \
--header "X-GitHub-Api-Version: 2022-11-28"

curl --request POST \
--url "https://api.github.com/applications/YOUR_CLIENT_ID/token" \
--user "YOUR_CLIENT_ID:YOUR_CLIENT_SECRET" \
--header "Accept: application/vnd.github+json" \
--header "X-GitHub-Api-Version: 2022-11-28" \
--data '{"access_token": "ACCESS_TOKEN_TO_CHECK"}'