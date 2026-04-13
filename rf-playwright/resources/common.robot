# -*- coding: utf-8 -*-
*** Settings ***
Library          Browser
Library          OperatingSystem

*** Variables ***
${BROWSER}           chromium
${HEADLESS}          ${FALSE}
${TEST_URL}          http://localhost:8080/test_page.html
${LOGIN_USERNAME}    test
${LOGIN_PASSWORD}    test
${DEFAULT_TIMEOUT}   10

*** Keywords ***
Open Browser To Test Page
    [Documentation]    Launch browser and navigate to test page
    IF    ${HEADLESS}
        Open Browser    ${TEST_URL}    browser=${BROWSER}    headless=${TRUE}
    ELSE
        Open Browser    ${TEST_URL}    browser=${BROWSER}
    END
    Set Browser Timeout    ${DEFAULT_TIMEOUT}s
    Handle Future Dialogs    action=accept

Go To Login Page
    [Documentation]    Navigate to test page and ensure login page is shown
    Go To    ${TEST_URL}
    Wait For Elements State    \#login-page    visible    10s

Login And Go To Main Page
    [Documentation]    Navigate to test page, login, ensure main page is shown
    Go To    ${TEST_URL}
    Wait For Elements State    \#login-page    visible    10s
    Fill Text    \#username    ${LOGIN_USERNAME}
    Fill Text    \#password    ${LOGIN_PASSWORD}
    Click    .login-btn
    Wait For Elements State    \#main-page    visible    5s

Login With Test Credentials
    [Documentation]    Perform login using credentials
    Wait For Elements State    \#login-page    visible    timeout=10s
    Fill Text    \#username    ${LOGIN_USERNAME}
    Fill Text    \#password       ${LOGIN_PASSWORD}
    Click    .login-btn
    Wait For Elements State    \#main-page    visible    timeout=5s

Login With Credentials
    [Arguments]    ${username}    ${password}
    Fill Text    \#username    ${username}
    Fill Text    \#password    ${password}
    Click    .login-btn

Get Element Class Attribute
    [Arguments]    ${selector}
    ${class}=    Get Attribute    ${selector}    class
    RETURN    ${class}

Count Pages
    [Documentation]    Return number of open pages in current context
    @{page_ids}=    Get Page Ids
    ${count}=    Get Length    ${page_ids}
    RETURN    ${count}

Upload File To Input
    [Arguments]    ${selector}    ${file_path}
    Upload File By Selector    ${selector}    ${file_path}
