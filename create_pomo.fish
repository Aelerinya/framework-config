#!/usr/bin/env fish

curl -X POST "https://intend.do/api/v0/u/me/addpomo?auth_token=$INTEND_AUTH_TOKEN"
set ret (notify-send --transient --app-name='Create pomodoro script' 'Pomodoro created' --action=go='See on Intend')
if test "$ret" = go
    xdg-open https://intend.do/aelerinya/today &> /dev/null
end

