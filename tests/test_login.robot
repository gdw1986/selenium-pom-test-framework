# -*- coding: utf-8 -*-
*** Settings ***
Documentation    Login functionality test suite - mirrors selenium-pom test_login.py
Resource         ../resources/common.robot
Suite Setup      Open Browser To Test Page
Suite Teardown   Close All Browsers

*** Test Cases ***

TC_Login_001 Login Page Elements Exist
    [Documentation]    Verify all login page elements are present
    Wait For Elements State    #login-page    visible
    Get Element    #username
    Get Element    #password
    Get Element    .login-btn
    Get Element    #login-error

TC_Login_002 Successful Login With Valid Credentials
    [Documentation]    Login with test/test, verify redirect to main page
    Login With Credentials    ${LOGIN_USER}    ${LOGIN_PASSWORD}
    Wait For Elements State    #main-page    visible    timeout=5s
    Get Element    button[onclick='showAlert()']

TC_Login_003 Login With Wrong Username
    [Documentation]    Wrong username should show error and highlight input
    Login With Credentials    wronguser    ${LOGIN_PASSWORD}
    Wait For Elements State    #login-error    visible    timeout=5s
    ${error_text}=    Get Text    #login-error
    Should Contain    ${error_text}    用户名或密码错误
    ${class}=    Get Element Class Attribute    #username
    Should Contain    ${class}    error

TC_Login_004 Login With Wrong Password
    [Documentation]    Wrong password should show error and highlight input
    Login With Credentials    ${LOGIN_USER}    wrongpassword
    Wait For Elements State    #login-error    visible    timeout=5s
    ${error_text}=    Get Text    #login-error
    Should Contain    ${error_text}    用户名或密码错误
    ${class}=    Get Element Class Attribute    #password
    Should Contain    ${class}    error

TC_Login_005 Login With Both Credentials Wrong
    [Documentation]    Both wrong should highlight both inputs
    Login With Credentials    wronguser    wrongpassword
    Wait For Elements State    #login-error    visible    timeout=5s
    ${class_u}=    Get Element Class Attribute    #username
    ${class_p}=    Get Element Class Attribute    #password
    Should Contain    ${class_u}    error
    Should Contain    ${class_p}    error

TC_Login_006 Login With Empty Credentials
    [Documentation]    Empty submit should show error
    Click    .login-btn
    Wait For Elements State    #login-error    visible    timeout=5s
    ${error_text}=    Get Text    #login-error
    Should Contain    ${error_text}    用户名或密码错误

TC_Login_007 Login By Pressing Enter Key
    [Documentation]    Press Enter in password field to submit
    Fill Text    #username    ${LOGIN_USER}
    Fill Text    #password    ${LOGIN_PASSWORD}
    Press Keys    #password    Enter
    Wait For Elements State    #main-page    visible    timeout=5s

TC_Login_008 Clear Input Fields
    [Documentation]    Clear both inputs and verify they are empty
    Fill Text    #username    ${LOGIN_USER}
    Fill Text    #password    ${LOGIN_PASSWORD}
    Clear Text    #username
    Clear Text    #password
    ${u_val}=    Get Value    #username
    ${p_val}=    Get Value    #password
    Should Be Empty    ${u_val}
    Should Be Empty    ${p_val}
