# -*- coding: utf-8 -*-
*** Settings ***
Documentation    Multi-window test suite
Resource         ../resources/common.robot
Library          Collections
Suite Setup      Open Browser To Test Page
Suite Teardown   Close Browser
Test Setup       Login And Go To Main Page
Test Teardown    Cleanup And Go To Main Page

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
    ${main_id}=    Get From List    ${page_ids}    0
    ${count}=    Get Length    ${page_ids}
    FOR    ${i}    IN RANGE    1    ${count}
        ${page_id}=    Get From List    ${page_ids}    ${i}
        ${alive}=    Run Keyword And Return Status    Switch Page    ${page_id}
        Continue For Loop If    not ${alive}
        # 用 URL 区分：弹窗是 about:blank，主页面含 test_page
        ${url}=    Get Url
        Continue For Loop If    'test_page' in '''${url}'''
        # 校验弹窗内容
        ${h2_count}=    Get Element Count    h2
        Should Be Equal As Integers    ${h2_count}    1
        ${title}=    Get Text    h2
        Should Contain    ${title}    窗口
        Get Element    button[onclick*='alert']
        Get Element    button[onclick='window.close()']
    END
    # 切回主页面（重新加载确保状态正确）
    Go To    ${TEST_URL}
    Wait For Elements State    \#login-page    visible    10s
    Fill Text    \#username    test
    Fill Text    \#password    test
    Click    .login-btn
    Wait For Elements State    \#main-page    visible    5s

TC_Window_005 Popup Window Alert
    Click    button.btn-orange[onclick='openFiveWindows()']
    Sleep    3s
    ${page_ids}=    Get Page Ids
    ${popup_id}=    Get From List    ${page_ids}    1
    Switch Page    ${popup_id}
    Click    button[onclick*='alert']
    Sleep    500ms
    Go To    ${TEST_URL}

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
    ${main_id}=    Get From List    ${page_ids}    0
    ${count}=    Get Length    ${page_ids}
    FOR    ${i}    IN RANGE    1    ${count}
        ${page_id}=    Get From List    ${page_ids}    ${i}
        ${alive}=    Run Keyword And Return Status    Switch Page    ${page_id}
        Continue For Loop If    not ${alive}
        ${url}=    Get Url
        Continue For Loop If    'test_page' in '''${url}'''
        ${title}=    Get Text    h2
        Should Contain    ${title}    窗口
    END
    Go To    ${TEST_URL}
    Wait For Elements State    \#login-page    visible    10s
    Fill Text    \#username    test
    Fill Text    \#password    test
    Click    .login-btn
    Wait For Elements State    \#main-page    visible    5s

TC_Window_008 Popup Window Info
    Click    button.btn-orange[onclick='openFiveWindows()']
    Sleep    3s
    ${page_ids}=    Get Page Ids
    ${count}=    Get Length    ${page_ids}
    # 找到所有弹窗（URL 为 about:blank 的）
    ${found}=    Set Variable    ${0}
    FOR    ${i}    IN RANGE    1    ${count}
        ${p_id}=    Get From List    ${page_ids}    ${i}
        ${sw}=    Run Keyword And Return Status    Switch Page    ${p_id}
        Continue For Loop If    not ${sw}
        ${u}=    Get Url
        Continue For Loop If    'test_page' in '''${u}'''
        ${found}=    Evaluate    ${found} + 1
        ${inf}=    Get Text    .info
        ${nm}=    Evaluate    re.findall(r'\\d+', '''${inf}''')    modules=re
        ${n}=    Get From List    ${nm}    0
        # 验证编号在 1-5 范围内
        ${valid}=    Evaluate    1 <= int(${n}) <= 5
        Should Be True    ${valid}
        ${cl}=    Evaluate    re.findall(r'\#[0-9a-fA-F]{6}', '''${inf}''')    modules=re
        Should Not Be Empty    ${cl}
    END
    # 只要有弹窗被验证即可
    Should Be True    ${found} >= 4
    Go To    ${TEST_URL}
    Wait For Elements State    \#login-page    visible    10s
    Fill Text    \#username    test
    Fill Text    \#password    test
    Click    .login-btn
    Wait For Elements State    \#main-page    visible    5s
