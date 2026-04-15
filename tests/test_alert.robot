# -*- coding: utf-8 -*-
*** Settings ***
Documentation    Alert popup test suite - mirrors selenium-pom test_alert.py
Resource         ../resources/common.robot
Suite Setup      Open Browser To Test Page
Suite Teardown   Close Browser
Test Setup       Login And Go To Main Page

*** Test Cases ***

TC_Alert_001 Alert Button Exists
    Get Element    button[onclick='showAlert()']

TC_Alert_002 Alert Button Tooltip
    Hover    button[onclick='showAlert()']
    Sleep    400ms
    ${tooltip}=    Get Text    button[onclick='showAlert()'] .tooltip
    Should Contain    ${tooltip}    悬停

TC_Alert_003 Alert Popup Can Be Triggered
    [Documentation]    Click Alert button, verify the page still works after dialog
    Click    button[onclick='showAlert()']
    Sleep    500ms
    # Verify main page is still visible and interactive after dialog
    Wait For Elements State    \#main-page    visible    5s

TC_Alert_004 Alert Button Can Be Clicked Multiple Times
    [Documentation]    Click Alert button twice, verify stability
    Click    button[onclick='showAlert()']
    Sleep    300ms
    Click    button[onclick='showAlert()']
    Sleep    300ms
    Wait For Elements State    \#main-page    visible    5s