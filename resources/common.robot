# -*- coding: utf-8 -*-
*** Settings ***
Library          Browser
Library          OperatingSystem
Variables        ../config/settings.py
Suite Teardown   Close All Browsers

*** Keywords ***
Open Browser To Test Page
    [Documentation]    Launch browser and navigate to test page
    IF    ${DEFAULT_HEADLESS}
        Open Browser    ${TEST_URL}    browser=${DEFAULT_BROWSER}    headless=${TRUE}
    ELSE
        Open Browser    ${TEST_URL}    browser=${DEFAULT_BROWSER}
    END
    Set Browser Timeout    ${DEFAULT_TIMEOUT}s
    Handle Future Dialogs    action=accept

Login With Test Credentials
    [Documentation]    Perform login using credentials from config
    Wait For Elements State    #login-page    visible    timeout=10s
    Fill Text    #username    ${LOGIN_USERNAME}
    Fill Text    #password    ${LOGIN_PASSWORD}
    Click    .login-btn
    Wait For Elements State    #main-page    visible    timeout=5s

Login With Credentials
    [Arguments]    ${username}    ${password}
    Fill Text    #username    ${username}
    Fill Text    #password    ${password}
    Click    .login-btn
    Wait For Elements State    #main-page    visible    timeout=5s

Get Element Class Attribute
    [Arguments]    ${selector}
    ${class}=    Get Attribute    ${selector}    class
    RETURN    ${class}

Count Pages
    [Documentation]    Return number of open pages in current context
    @{pages}=    Get Pages
    ${count}=    Get Length    ${pages}
    RETURN    ${count}

Wait For And Accept Dialog
    [Documentation]    Wait for dialog, accept it, return message text
    ${dialog}=    Wait For Alert    timeout=5s
    ${text}=    Set Variable    ${dialog}[message]
    Accept Alert
    RETURN    ${text}

Wait For And Dismiss Dialog
    [Documentation]    Wait for dialog, dismiss it, return message text
    ${dialog}=    Wait For Alert    timeout=5s
    ${text}=    Set Variable    ${dialog}[message]
    Dismiss Alert
    RETURN    ${text}

Upload File To Input
    [Arguments]    ${selector}    ${file_path}
    Upload File By Selector    ${selector}    ${file_path}
