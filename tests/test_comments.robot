# -*- coding: utf-8 -*-
*** Settings ***
Documentation    Comment section test suite - mirrors selenium-pom test_comments.py
Resource         ../resources/common.robot
Suite Setup      Open Browser To Test Page
Suite Teardown   Close All Browsers

*** Test Cases ***

TC_Comment_001 Comment Section Exists
    [Documentation]    Verify comment input, submit button, and list exist
    Login With Test Credentials
    Get Element    #comment-input
    Get Element    .comment-submit-btn
    Get Element    #comment-list

TC_Comment_002 Initial Comments Exist
    [Documentation]    Page should have exactly 4 initial comments
    Login With Test Credentials
    ${count}=    Get Element Count    .comment-item
    Should Be Equal As Integers    ${count}    4

TC_Comment_003 Initial Comment Authors
    [Documentation]    Verify the 4 initial comment authors in order
    Login With Test Credentials
    ${authors}=    Create List
    FOR    ${i}    IN RANGE    4
        ${nth}=    Evaluate    str(${i})
        ${el}=    Set Variable    .comment-item >> nth=${nth} >> .comment-author
        ${author}=    Get Text    ${el}
        Append To List    ${authors}    ${author}
    END
    Should Be Equal    ${authors}[0]    林晓雨
    Should Be Equal    ${authors}[1]    张伟明
    Should Be Equal    ${authors}[2]    王思琪
    Should Be Equal    ${authors}[3]    陈浩然

TC_Comment_004 Add Comment Appears At Top
    [Documentation]    New comment appears at top of list with author=me
    Login With Test Credentials
    ${init_count}=    Get Element Count    .comment-item
    ${comment}=    Set Variable    RF+Playwright自动化测试评论
    Fill Text    #comment-input    ${comment}
    Click    .comment-submit-btn
    # Wait for button text to return to normal (submission done)
    Wait For Function    () => document.querySelector('.comment-submit-btn')?.textContent?.includes('发布评论') === true    timeout=5s
    ${new_count}=    Get Element Count    .comment-item
    Should Be Equal As Integers    ${new_count}    ${init_count} + 1
    ${first_author}=    Get Text    .comment-item >> nth=0 >> .comment-author
    Should Be Equal    ${first_author}    我

TC_Comment_005 Add Multiple Comments
    [Documentation]    Adding multiple comments keeps newest at top
    Login With Test Credentials
    FOR    ${c}    IN    第一条RF评论    第二条RF评论    第三条RF评论
        Fill Text    #comment-input    ${c}
        Click    .comment-submit-btn
        Wait For Function    () => document.querySelector('.comment-submit-btn')?.textContent?.includes('发布评论') === true    timeout=5s
    END
    ${first}=    Get Text    .comment-item >> nth=0 >> .comment-content
    Should Be Equal    ${first}    第三条RF评论

TC_Comment_006 Add Empty Comment
    [Documentation]    Empty comment should not increase count
    Login With Test Credentials
    ${init_count}=    Get Element Count    .comment-item
    Fill Text    #comment-input    ${EMPTY}
    Click    .comment-submit-btn
    Sleep    1s
    ${new_count}=    Get Element Count    .comment-item
    Should Be Equal As Integers    ${new_count}    ${init_count}

TC_Comment_007 Comment With Special Characters
    [Documentation]    Special chars and quotes should not break submission
    Login With Test Credentials
    ${comment}=    Set Variable    特殊字符 <tag> & "quotes" 'single'
    Fill Text    #comment-input    ${comment}
    Click    .comment-submit-btn
    Wait For Function    () => document.querySelector('.comment-submit-btn')?.textContent?.includes('发布评论') === true    timeout=5s
    ${first_author}=    Get Text    .comment-item >> nth=0 >> .comment-author
    Should Be Equal    ${first_author}    我

TC_Comment_008 Comment With Long Text
    [Documentation]    Long comment text should be accepted
    Login With Test Credentials
    ${comment}=    Evaluate    "测试评论内容." * 50
    Fill Text    #comment-input    ${comment}
    Click    .comment-submit-btn
    Wait For Function    () => document.querySelector('.comment-submit-btn')?.textContent?.includes('发布评论') === true    timeout=5s
    ${count}=    Get Element Count    .comment-item
    Should Be Equal As Integers    ${count}    5
