1. 필수 라이브러리 설치
requirements.txt 파일을 이용하여 프로젝트에 필요한 모든 라이브러리를 한 번에 설치합니다.
```
pip install -r requirements.txt
```
2. Google API 인증 정보 발급
Google 로그인을 사용하려면 Google Cloud Console에서 클라이언트 ID와 클라이언트 보안 비밀을 발급받아야 합니다.

**Google Cloud Console**에 접속하여 새 프로젝트를 생성합니다.

**'API 및 서비스' > 'OAuth 동의 화면'**으로 이동하여 앱 이름, 이메일 등 기본 정보를 입력하고 저장합니다.

'테스트 사용자'에는 로그인에 사용할 본인의 Google 이메일 계정을 추가합니다.

'API 및 서비스' > '사용자 인증 정보' 메뉴로 이동합니다.

**'+ 사용자 인증 정보 만들기' > 'OAuth 클라이언트 ID'**를 선택합니다.

애플리케이션 유형을 **'웹 애플리케이션'**으로 선택합니다.

'승인된 리디렉션 URI' 섹션에 다음 두 개의 주소를 정확하게 추가합니다.

http://127.0.0.1:8000/accounts/google/login/callback/
http://localhost:8000/accounts/google/login/callback/

'만들기' 버튼을 누른 후, 표시되는 클라이언트 ID와 클라이언트 보안 비밀을 복사해 둡니다.

3. Django 설정 파일 수정
복사해 둔 인증 정보를 프로젝트에 적용합니다.

google_login_project/settings.py 파일을 엽니다.

파일 맨 아래의 SOCIALACCOUNT_PROVIDERS 부분을 찾아, 복사해 둔 값으로 교체합니다.

# settings.py
```
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': 'YOUR_GOOGLE_CLIENT_ID',       # 👈 여기에 발급받은 클라이언트 ID 붙여넣기
            'secret': 'YOUR_GOOGLE_SECRET_KEY',         # 👈 여기에 발급받은 클라이언트 보안 비밀 붙여넣기
            'key': ''
        },
        # ...
    }
}
```
4. 데이터베이스 설정
터미널에 아래 명령어를 입력하여 데이터베이스 테이블을 생성합니다.
```
python manage.py migrate
```
5. (선택) 관리자 계정 생성
데이터를 직접 확인하고 싶을 경우, 관리자 페이지에 접속할 수 있는 계정을 생성합니다.
```
python manage.py createsuperuser
```
▶️ 서버 실행
모든 설정이 완료되었습니다. 아래 명령어로 개발 서버를 실행합니다.
```
python manage.py runserver
```
웹 브라우저를 열고 http://127.0.0.1:8000/ 주소로 접속하여 "Google 계정으로 로그인" 버튼을 통해 기능을 테스트할 수 있습니다.