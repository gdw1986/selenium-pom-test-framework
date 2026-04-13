*** Settings ***
Library    Browser
Test Timeout    30s

*** Test Cases ***

Simple Test
    Open Browser    http://localhost:8080/test_page.html    browser=chromium    headless=${TRUE}
    Wait For Elements State    \#login-page    visible    10s
    Fill Text    \#username    test
    Fill Text    \#password    test
    Click    .login-btn
    Wait For Elements State    \#main-page    visible    5s
    Close Browser