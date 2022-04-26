# JWT-practice

## About

ぼくがJWTの理解をするためのリポジトリ。
簡単なOpenIDConnectをイメージしたデモをpythonで実装した。

## How to run demo

- Run server
```run.sh
cd auth-server
docker build -t auth-server-service .
docker run -p 8000:8000 auth-server
```

- Test JWT authentication
```test.sh
curl - H "Content-Type: application/json" -d '{"user_id": "test_user_id", "password": "pass"}' localhost:8000/oauth/consent
# You'll get <authorization_code>.
curl -H "Content-Type: application/json" -d '{"authorization_code": "<authorization_code>"}' localhost:8000/oauth/token
# You'll get <id_token>.
curl -H "Authorization: Bearer <id_token>" localhost:8000/api/profile/email
# You'll get a secret email address for test_user.
```

## JWTとは？

\<header\>.\<payload\>.\<sign\>からなる。

- header: signのアルゴリズムを表すjsonをbase64encodeしたもの
- payload: 認証情報を表すjsonをbase64encodeしたもの（誰が（iss）誰に（aud）どんな権限（sub, scope)を与え、いつ期限切れ（exp）かなどのClaim）
- sign: \<header\>.\<payload\>に署名してbase64encodeしたもの

signに使われる署名アルゴリズム例
- HS256
    - 共通鍵ベースの署名
    - ハッシュ関数がSHA256のHMAC
        - HMAC = Hash based Massage Authentication Code
            - 適当にカギと連結してハッシュするのはハッシュ関数が甘いときに破られるのでハッシュをハッシュしたり工夫してそこに保険を掛けるのがHMAC
- RS256
    - 公開鍵暗号ベースの署名
    - 調べてないけど公開鍵暗号ならなんなりと署名できそう

## 結局JWTは何に使われる？（ぼくのにんしき）

OAuthのようにアクセストークンとして使われる。この認証方式としてOpenIDConnectがある（OpenIDConnectはOAuthの拡張）。このときのアクセストークンはid tokenと呼ばれる
またOAuthは認可だがJWTは認証もしている。

セッションとの違い。
- Pros. statelessなので検証が軽い（データベースを使わなくてよい）
- Cons. statelessなのでまともなinvalidateする方法がない

SAMLとの違い
- Pros. 軽い（SAMLはXML-based）

Cons.の理由からロングタームな認証トークンとしては使えない。
このため比較的有効期限が長くstatefulなリフレッシュトークンと併用する。リフレッシュトークンはstatefulなトークンでサーバーに送ることで一度だけ新しいリフレッシュトークンとid tokenを再発行できる。これによってstatelessのメリットを利用しつつ、statelessの弱点をカバーできる。

## Authorization codeとは？（SSOで直接id tokenを得られないのはなぜ？）

OpenIDConnectにおける
ID tokenは以下のフローで入手できる。
1. ログイン連携をするサービスのログインページへリダイレクト
2. ログインをする
3. **連携元のサービスへリダイレクト**（連携元がAuthorization codeを入手）
4. Authorization codeをもとにAccess Tokenを入手

連携元のサービスへのリダイレクトが特定の環境下（スマホ）では他のサービスにリダイレクトされてしまうことがある。
この対策として、(1.)のタイミングでログイン連携をするサービスにチャレンジコードというものを送っておく。(4.)においてチャレンジコードとAuthorization codeを送ることでAccess Tokenを入手できるようにする。このようにすれば、Authorization codeそのものだけではAccess Tokenを入手できないことがわかる。（実際には(1.)で生のチャレンジコードではなく、チャレンジコードのハッシュなどを送る）

## TODO

仕様をしっかり読んでいないので読む。
簡単なOpenIDConnectと言いつつ、REQUIREDな仕様もすべて実装していないので実装する。
