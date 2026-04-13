# -*- coding: utf-8 -*-
*** Settings ***
Documentation    Tab feature test suite - iFrame, Task Table, Progress, Notifications, Countdown
Resource         ../resources/common.robot
Library          Collections
Library          BuiltIn
Suite Setup      Open Browser To Test Page
Suite Teardown   Close Browser
Test Setup       Login And Go To Main Page

*** Test Cases ***

# ==================== Tab Navigation ====================

TC_Tab_001 Tab Navigation Exists
    Get Element    \#tab-nav
    ${count}=    Get Element Count    .tab-btn
    Should Be Equal As Integers    ${count}    5

TC_Tab_002 Default Active Tab Is IFrame
    ${active}=    Get Attribute    \#tab-btn-iframe    class
    Should Contain    ${active}    active
    ${content_active}=    Get Attribute    \#tab-iframe    class
    Should Contain    ${content_active}    active

TC_Tab_003 Switch To Task Tab
    Click    \#tab-btn-task
    Wait For Elements State    \#tab-task.active    visible    3s
    ${task_active}=    Get Attribute    \#tab-btn-task    class
    Should Contain    ${task_active}    active

TC_Tab_004 Switch To Progress Tab
    Click    \#tab-btn-progress
    Wait For Elements State    \#tab-progress.active    visible    3s

TC_Tab_005 Switch To Notify Tab
    Click    \#tab-btn-notify
    Wait For Elements State    \#tab-notify.active    visible    3s

TC_Tab_006 Switch To Countdown Tab
    Click    \#tab-btn-countdown
    Wait For Elements State    \#tab-countdown.active    visible    3s

# ==================== iFrame ====================

TC_Tab_007 IFrame Exists And Is Visible
    Wait For Elements State    \#tab-iframe.active    visible    3s
    Get Element    \#iframe-form

# ==================== Task Table ====================

TC_Tab_008 Task Table Has Initial Rows
    Click    \#tab-btn-task
    Wait For Elements State    \#tab-task.active    visible    3s
    ${rows}=    Get Element Count    \#task-tbody tr
    Should Be Equal As Integers    ${rows}    3

TC_Tab_009 Add New Task
    Click    \#tab-btn-task
    Wait For Elements State    \#tab-task.active    visible    3s
    ${init_rows}=    Get Element Count    \#task-tbody tr
    Fill Text    \#new-task-name    新增测试任务
    Click    button:has-text("添加")
    Sleep    300ms
    ${new_rows}=    Get Element Count    \#task-tbody tr
    ${expected}=    Evaluate    ${init_rows} + 1
    Should Be Equal As Integers    ${new_rows}    ${expected}

TC_Tab_010 Delete Task
    Click    \#tab-btn-task
    Wait For Elements State    \#tab-task.active    visible    3s
    ${init_rows}=    Get Element Count    \#task-tbody tr
    Click    \#task-tbody tr:first-child button:has-text("删除")
    Sleep    300ms
    ${new_rows}=    Get Element Count    \#task-tbody tr
    ${expected}=    Evaluate    ${init_rows} - 1
    Should Be Equal As Integers    ${new_rows}    ${expected}

TC_Tab_011 Filter Tasks By Keyword
    Click    \#tab-btn-task
    Wait For Elements State    \#tab-task.active    visible    3s
    Fill Text    \#task-filter    登录
    Sleep    300ms
    ${visible}=    Get Element Count    \#task-tbody tr:not([style*="display: none"])
    ${gt}=    Evaluate    ${visible} > 0
    Should Be True    ${gt}

TC_Tab_012 Task Filter Clear
    Click    \#tab-btn-task
    Wait For Elements State    \#tab-task.active    visible    3s
    Fill Text    \#task-filter    xyznonexistent
    Sleep    300ms
    ${empty_msg}=    Get Element Count    \#task-empty:not([style*="display: none"])
    ${empty_display}=    Get Attribute    \#task-empty    style
    Log    ${empty_display}

# ==================== Progress Bar ====================

TC_Tab_013 Progress Bar Initial State
    Click    \#tab-btn-progress
    Wait For Elements State    \#tab-progress.active    visible    3s
    ${label}=    Get Text    \#progress-label
    Should Be Equal    ${label}    0%

TC_Tab_014 Progress Bar Increase
    Click    \#tab-btn-progress
    Wait For Elements State    \#tab-progress.active    visible    3s
    Click    \#btn-progress-plus
    Sleep    500ms
    ${label}=    Get Text    \#progress-label
    Should Be Equal    ${label}    10%

TC_Tab_015 Progress Bar Decrease
    Click    \#tab-btn-progress
    Wait For Elements State    \#tab-progress.active    visible    3s
    Click    \#btn-progress-plus25
    Sleep    500ms
    Click    \#btn-progress-minus25
    Sleep    500ms
    ${label}=    Get Text    \#progress-label
    Should Be Equal    ${label}    0%

TC_Tab_016 Progress Bar Reset
    Click    \#tab-btn-progress
    Wait For Elements State    \#tab-progress.active    visible    3s
    Click    \#btn-progress-plus25
    Click    \#btn-progress-plus25
    Click    \#tab-progress button:text-is("重置")
    Sleep    500ms
    ${label}=    Get Text    \#progress-label
    Should Be Equal    ${label}    0%

TC_Tab_017 Progress Bar Max 100
    Click    \#tab-btn-progress
    Wait For Elements State    \#tab-progress.active    visible    3s
    FOR    ${i}    IN RANGE    12
        Click    \#btn-progress-plus
    END
    Sleep    500ms
    ${label}=    Get Text    \#progress-label
    Should Be Equal    ${label}    100%

# ==================== Notifications ====================

TC_Tab_018 Notify Tab Shows Triggers
    Click    \#tab-btn-notify
    Wait For Elements State    \#tab-notify.active    visible    3s
    Get Element    button:has-text("成功通知")
    Get Element    button:has-text("警告通知")
    Get Element    button:has-text("错误通知")
    Get Element    button:has-text("普通通知")

TC_Tab_019 Success Notification Appears
    Click    \#tab-btn-notify
    Wait For Elements State    \#tab-notify.active    visible    3s
    Click    button:has-text("成功通知")
    Sleep    500ms
    ${notif}=    Get Element Count    .notif.success
    Should Be Equal As Integers    ${notif}    1

TC_Tab_020 Error Notification Appears
    Click    \#tab-btn-notify
    Wait For Elements State    \#tab-notify.active    visible    3s
    Click    button:has-text("错误通知")
    Sleep    500ms
    ${notif}=    Get Element Count    .notif.error
    Should Be Equal As Integers    ${notif}    1

# ==================== Countdown ====================

TC_Tab_021 Countdown Default State
    Click    \#tab-btn-countdown
    Wait For Elements State    \#tab-countdown.active    visible    3s
    ${display}=    Get Text    \#countdown-display
    Should Be Equal    ${display}    00:00

TC_Tab_022 Countdown Start 30s
    Click    \#tab-btn-countdown
    Wait For Elements State    \#tab-countdown.active    visible    3s
    Click    button:has-text("30秒")
    Sleep    1500ms
    ${display}=    Get Text    \#countdown-display
    ${match}=    Evaluate    re.match(r'^[0-2][0-9]:[0-5][0-9]$', '''${display}''') is not None    modules=re
    Should Be True    ${match}

TC_Tab_023 Countdown Reset
    Click    \#tab-btn-countdown
    Wait For Elements State    \#tab-countdown.active    visible    3s
    Click    button:has-text("30秒")
    Sleep    1000ms
    Click    \#tab-countdown button:text-is("重置")
    ${display}=    Get Text    \#countdown-display
    Should Be Equal    ${display}    00:00
