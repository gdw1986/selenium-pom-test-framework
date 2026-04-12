# -*- coding: utf-8 -*-
*** Settings ***
Documentation    Multi-window test suite - mirrors selenium-pom test_windows.py
Resource         ../resources/common.robot
Suite Setup      Open Browser To Test Page
Suite Teardown   Close All Browsers

*** Test Cases ***

TC_Window_001 Open Windows Button Exists
    Login With Test Credentials
    Get Element    button.btn-orange[onclick='openFiveWindows()']

TC_Window_002 Open Windows Button Tooltip
    Login With Test Credentials
    Hover    button.btn-orange[onclick='openFiveWindows()']
    Sleep    400ms
    ${tip}=    Get Text    button.btn-orange .tooltip
    Should Contain    ${tip}    窗口

TC_Window_003 Open Five Windows
    [Documentation]    Clicking opens exactly 5 new windows
    Login With Test Credentials
    ${init_count}=    Count Pages
    Click    button.btn-orange[onclick='openFiveWindows()']
    Sleep    3s
    ${final_count}=    Count Pages
    Should Be Equal As Integers    ${final_count}    ${init_count} + 5

TC_Window_004 Popup Window Content
    [Documentation]    Each popup has h2 title, Alert btn, close btn
    Login With Test Credentials
    Click    button.btn-orange[onclick='openFiveWindows()']
    Sleep    3s
    FOR    ${i}    IN RANGE    1    6
        ${prev}=    Switch Page    ${i}
        Get Element    h2
        Get Element    button[onclick*='alert']
        Get Element    button[onclick='window.close()']
        ${title}=    Get Text    h2
        Should Contain    ${title}    窗口
    END
    # Return to main page
    Switch Page    0
    Wait For Elements State    #main-page    visible    timeout=5s

TC_Window_005 Popup Window Alert
    [Documentation]    Popup's own Alert button shows correct message
    Login With Test Credentials
    Click    button.btn-orange[onclick='openFiveWindows()']
    Sleep    3s
    Switch Page    1
    Handle Future Dialogs    action=accept
    Click    button[onclick*='alert']
    ${dialog}=    Wait For Alert    timeout=5s
    ${msg}=    Set Variable    ${dialog}[message]
    Should Contain    ${msg}    窗口
    Accept Alert
    Switch Page    0

TC_Window_006 Close Popup Window
    [Documentation]    Close button shuts that window
    Login With Test Credentials
    Click    button.btn-orange[onclick='openFiveWindows()']
    Sleep    3s
    ${before}=    Count Pages
    Switch Page    1
    Click    button[onclick='window.close()']
    Sleep    1s
    ${after}=    Count Pages
    Should Be Equal As Integers    ${after}    ${before} - 1
    Switch Page    0

TC_Window_007 Switch Between Windows
    [Documentation]    Can switch to each popup and back to main
    Login With Test Credentials
    Click    button.btn-orange[onclick='openFiveWindows()']
    Sleep    3s
    FOR    ${i}    IN RANGE    1    6
        Switch Page    ${i}
        ${title}=    Get Text    h2
        Should Contain    ${title}    窗口
    END
    Switch Page    0
    Wait For Elements State    #main-page    visible    timeout=5s

TC_Window_008 Popup Window Info
    [Documentation]    Each popup info shows correct window number and hex color
    Login With Test Credentials
    Click    button.btn-orange[onclick='openFiveWindows()']
    Sleep    3s
    FOR    ${i}    IN RANGE    1    6
        Switch Page    ${i}
        ${info}=    Get Text    .info
        # Extract window number from "窗口编号: X"
        ${num_match}=    Evaluate    re.findall(r'\\d+', '''${info}''')    modules=re
        ${num}=    Get From List    ${num_match}    0
        Should Be Equal As Strings    ${num}    ${i}
        # Extract color from "颜色: #XXXXXX"
        ${color_match}=    Evaluate    re.findall(r'#[0-9a-fA-F]{6}', '''${info}''')    modules=re
        Should Not Be Empty    ${color_match}
    END
