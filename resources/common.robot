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
    # 确保有 page 且切到第一个（主页面）
    ${has_page}=    Run Keyword And Return Status    Get Page Ids
    IF    not ${has_page}
        New Page    ${TEST_URL}
    END
    # 多个 page 时切回主页面（URL 含 test_page 的那个）
    ${ids}=    Get Page Ids
    FOR    ${id}    IN    @{ids}
        ${switched}=    Run Keyword And Return Status    Switch Page    ${id}
        IF    ${switched}
            ${url}=    Get Url
            ${is_main}=    Evaluate    'test_page' in '''${url}'''
            IF    ${is_main}
                Exit For Loop
            END
        END
    END
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

Close All Popup Pages
    [Documentation]    Close all popup pages via JS, keep main page
    ${ids}=    Get Page Ids
    ${count}=    Get Length    ${ids}
    Return From Keyword If    ${count} <= 1
    ${main_id}=    Get From List    ${ids}    0
    # 从后往前用 JS 关闭弹窗（不用 Close Page，避免 Browser 库状态异常）
    FOR    ${i}    IN RANGE    1    ${count}
        ${current_ids}=    Get Page Ids
        ${current_len}=    Get Length    ${current_ids}
        Exit For Loop If    ${current_len} <= 1
        ${last_id}=    Get From List    ${current_ids}    -1
        Continue For Loop If    '${last_id}' == '${main_id}'
        ${switched}=    Run Keyword And Return Status    Switch Page    ${last_id}
        IF    ${switched}
            Run Keyword And Ignore Error    Evaluate Javascript    ${NONE}    () => window.close()
        END
    END
    # 等待弹窗关闭
    Sleep    500ms
    # 切回主页面
    ${final_ids}=    Get Page Ids
    ${final_len}=    Get Length    ${final_ids}
    Return From Keyword If    ${final_len} == 0
    ${first}=    Get From List    ${final_ids}    0
    Switch Page    ${first}

Cleanup And Go To Main Page
    [Documentation]    Close all extra pages and reload main page
    Go To    ${TEST_URL}
    Wait For Elements State    \#login-page    visible    10s
    Fill Text    \#username    ${LOGIN_USERNAME}
    Fill Text    \#password    ${LOGIN_PASSWORD}
    Click    .login-btn
    Wait For Elements State    \#main-page    visible    5s
