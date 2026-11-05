@echo off
chcp 65001 > nul
echo ========================================================
echo   진주퀸공인중개사사무소 로컬 웹서버 실행기
echo ========================================================
echo.
echo 웹서버를 시작하고 브라우저를 엽니다...
echo 주소: http://localhost:8080
echo 관리자: http://localhost:8080/admin.html
echo.
start http://localhost:8080
python server.py
pause

