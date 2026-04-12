# -*- coding: utf-8 -*-
*** Settings ***
Documentation    Alert popup test suite - mirrors selenium-pom test_alert.py
Resource         ../resources/common.robot
Suite Setup      Open Browser To Test Page
Suite Teardown   Close All Browsers

*** Test Cases ***

TC_Alert_001 Alert Button Exists
    [Documentation]    Verify Alert button is present on main page
    Login With Test Credentials
    Get Element    button[onclick='showAlert()']

TC_Alert_002 Alert Button Tooltip
    [Documentation]    Hover Alert button and check tooltip text
    Login With Test Credentials
    Hover    button[onclick='showAlert()']
    Sleep    400ms
    ${tooltip}=    Get Text    button[onclick='showAlert()'] .tooltip
    Should Contain    ${tooltip}    悬停

TC_Alert_003 Alert Popup Accept
    [Documentation]    Click Alert button, verify text, accept dialog
    Login With Test Credentials
    Handle Future Dialogs    action=accept
    Click    button[onclick='showAlert()']
    ${dialog}=    Wait For Alert    timeout=5s
    ${msg}=    Set Variable    ${dialog}[message]
    Should Contain    ${msg}    Selenium
    Accept Alert

TC_Alert_004 Alert Popup Dismiss
    [Documentation]    Click Alert button, dismiss dialog
    Login With Test Credentials
    Handle Future Dialogs    action=dismiss
    Click    button[onclick='showAlert()']
    ${dialog}=    Wait For Alert    timeout=5s
    ${msg}=    Set Variable    ${dialog}[message]
    Should Not Be Empty    ${msg}
    Dismiss Alert
