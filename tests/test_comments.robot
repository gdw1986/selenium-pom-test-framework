# -*- coding: utf-8 -*-
*** Settings ***
Documentation    Comment section test suite - mirrors selenium-pom test_comments.py
Resource         ../resources/common.robot
Library          Collections
Suite Setup      Open Browser To Test Page
Suite Teardown   Close Browser
Test Setup       Login And Go To Main Page

*** Test Cases ***

TC_Comment_001 Comment Section Exists
    Get Element    \#comment-input
    Get Element    .comment-submit-btn
    Get Element    \#comment-list

TC_Comment_002 Initial Comments Exist
    ${count}=    Get Element Count    .comment-item
    Should Be Equal As Integers    ${count}    4

TC_Comment_003 Initial Comment Authors
    ${authors}=    Create List
    FOR    ${i}    IN RANGE    4
        ${nth}=    Evaluate    str(${i})
        ${author}=    Get Text    .comment-item >> nth=${nth} >> .comment-author
        Append To List    ${authors}    ${author}
    END
    Should Be Equal    ${authors}[0]    林晓雨
    Should Be Equal    ${authors}[1]    张伟明
    Should Be Equal    ${authors}[2]    王思琪
    Should Be Equal    ${authors}[3]    陈浩然

TC_Comment_004 Add Comment Appears At Top
    ${init_count}=    Get Element Count    .comment-item
    ${comment}=    Set Variable    RF+Playwright自动化测试评论
    Fill Text    \#comment-input    ${comment}
    Click    .comment-submit-btn
    Wait For Function    () => document.querySelector('.comment-submit-btn')?.textContent?.includes('发布评论') === true    timeout=5000
    ${new_count}=    Get Element Count    .comment-item
    ${expected}=    Evaluate    ${init_count} + 1
    Should Be Equal As Integers    ${new_count}    ${expected}
    ${first_author}=    Get Text    .comment-item >> nth=0 >> .comment-author
    Should Be Equal    ${first_author}    我

TC_Comment_005 Add Multiple Comments
    FOR    ${c}    IN    第一条RF评论    第二条RF评论    第三条RF评论
        Fill Text    \#comment-input    ${c}
        Click    .comment-submit-btn
        Wait For Function    () => document.querySelector('.comment-submit-btn')?.textContent?.includes('发布评论') === true    timeout=5000
    END
    ${first}=    Get Text    .comment-item >> nth=0 >> .comment-content
    Should Be Equal    ${first}    第三条RF评论

TC_Comment_006 Add Empty Comment
    ${init_count}=    Get Element Count    .comment-item
    Fill Text    \#comment-input    ${EMPTY}
    Click    .comment-submit-btn
    Sleep    1s
    ${new_count}=    Get Element Count    .comment-item
    Should Be Equal As Integers    ${new_count}    ${init_count}

TC_Comment_007 Comment With Special Characters
    ${comment}=    Set Variable    特殊字符 <tag> & "quotes" 'single'
    Fill Text    \#comment-input    ${comment}
    Click    .comment-submit-btn
    Wait For Function    () => document.querySelector('.comment-submit-btn')?.textContent?.includes('发布评论') === true    timeout=5000
    ${first_author}=    Get Text    .comment-item >> nth=0 >> .comment-author
    Should Be Equal    ${first_author}    我

TC_Comment_008 Comment With Long Text
    ${comment}=    Evaluate    "测试评论内容." * 50
    Fill Text    \#comment-input    ${comment}
    Click    .comment-submit-btn
    Wait For Function    () => document.querySelector('.comment-submit-btn')?.textContent?.includes('发布评论') === true    timeout=5000
    ${count}=    Get Element Count    .comment-item
    Should Be Equal As Integers    ${count}    5