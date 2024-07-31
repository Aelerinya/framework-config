#!/usr/bin/env fish

curl -X POST "https://intend.do/api/v0/u/me/addpomo?auth_token=$INTEND_AUTH_TOKEN"

notify-send --transient --app-name='Create pomodoro script' 'Pomodoro created'

