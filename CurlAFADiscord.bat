@echo off
    rem ...
    set errorlevel=
    D:\Curl\bin\curl.exe -X POST -H "Content-Type: application/json" -d "{\"username\":\"Adaa\", \"content\": \"https://www.amazon.co.uk/dp/B07GXV4HGW\"}" "https://discord.com/api/webhooks/758719012304715807/71co5w7Njb0Fvw0ntmuzL7YKiaPjPxuavw56HgQ83HpyD5BwonR49xsWBAdaL8etPQJq"
    D:\Downloads\sound1.wav
    IF %errorlevel% ==0 GOTO SUCCESS
    IF %errorlevel% ==1 GOTO ERROR

    :SUCCESS
    echo Success!
    GOTO END

    :ERROR
    echo Error!
    GOTO END

    :END

    