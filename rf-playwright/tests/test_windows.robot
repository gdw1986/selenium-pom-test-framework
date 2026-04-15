# -*- coding: utf-8 -*-
*** Settings ***
Documentation    Multi-window test suite - mirrors selenium-pom test_windows.py
Resource         ../resources/common.robot
Library          Collections
Suite Setup      Open Browser To Test Page
Suite Teardown   Close Browser
Test Setup       Login And Go To Main Page

*** Test Cases ***

TC_Window_001 Open Windows Button Exists
    Get Element    button.btn-orange[onclick='openFiveWindows()']

TC_Window_002 Open Windows Button Tooltip
    Hover    button.btn-orange[onclick='openFiveWindows()']
    Sleep    400ms
    ${tip}=    Get Text    button.btn-orange .tooltip
    Should Contain    ${tip}    窗口

TC_Window_003 Open Five Windows
    ${init_count}=    Count Pages
    Click    button.btn-orange[onclick='openFiveWindows()']
    Sleep    3s
    ${final_count}=    Count Pages
    ${expected}=    Evaluate    ${init_count} + 5
    Should Be Equal As Integers    ${final_count}    ${expected}

TC_Window_004 Popup Window Content
    Click    button.btn-orange[onclick='openFiveWindows()']
    Sleep    3s
    ${page_ids}=    Get Page Ids
    Log    Page IDs: ${page_ids}    level=INFO
    # Get page count to iterate
    ${count}=    Get Length    ${page_ids}
    # Skip first (main page), check each popup
    FOR    ${i}    IN RANGE    1    ${count}
        ${page_id}=    Get From List    ${page_ids}    ${i}
        Switch Page    ${page_id}
        Get Element    h2
        Get Element    button[onclick*='alert']
        Get Element    button[onclick='window.close()']
        ${title}=    Get Text    h2
        Should Contain    ${title}    窗口
    END
    ${first_id}=    Get From List    ${page_ids}    0
    Switch Page    ${first_id}
    Wait For Elements State    \#main-page    visible    5s

TC_Window_005 Popup Window Alert
    Click    button.btn-orange[onclick='openFiveWindows()']
    Sleep    3s
    ${page_ids}=    Get Page Ids
    ${popup_id}=    Get From List    ${page_ids}    1
    Switch Page    ${popup_id}
    Click    button[onclick*='alert']
    Sleep    500ms
    ${main_id}=    Get From List    ${page_ids}    0
    Switch Page    ${main_id}

TC_Window_006 Close Popup Window
    Click    button.btn-orange[onclick='openFiveWindows()']
    Sleep    3s
    ${before}=    Count Pages
    ${page_ids}=    Get Page Ids
    ${popup_id}=    Get From List    ${page_ids}    1
    Switch Page    ${popup_id}
    Click    button[onclick='window.close()']
    Sleep    1s
    ${after}=    Count Pages
    ${expected}=    Evaluate    ${before} - 1
    Should Be Equal As Integers    ${after}    ${expected}

TC_Window_007 Switch Between Windows
    Click    button.btn-orange[onclick='openFiveWindows()']
    Sleep    3s
    ${page_ids}=    Get Page Ids
    ${count}=    Get Length    ${page_ids}
    FOR    ${i}    IN RANGE    1    ${count}
        ${page_id}=    Get From List    ${page_ids}    ${i}
        Switch Page    ${page_id}
        ${title}=    Get Text    h2
        Should Contain    ${title}    窗口
    END
    ${main_id}=    Get From List    ${page_ids}    0
    Switch Page    ${main_id}
    Wait For Elements State    \#main-page    visible    5s

TC_Window_008 Popup Window Info
    Click    button.btn-orange[onclick='openFiveWindows()']
    Sleep    3s
    ${page_ids}=    Get Page Ids
    ${count}=    Get Length    ${page_ids}
    FOR    ${i}    IN RANGE    1    ${count}
        ${page_id}=    Get From List    ${page_ids}    ${i}
        Switch Page    ${page_id}
        ${info}=    Get Text    .info
        ${num_match}=    Evaluate    re.findall(r'\\d+', '''${info}''')    modules=re
        ${num}=    Get From List    ${num_match}    0
        Should Be Equal As Strings    ${num}    ${i}
        ${color_match}=    Evaluate    re.findall(r'\#[0-9a-fA-F]{6}', '''${info}''')    modules=re
        Should Not Be Empty    ${color_match}
    END