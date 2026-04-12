# -*- coding: utf-8 -*-
*** Settings ***
Documentation    Dropdown test suite - mirrors selenium-pom test_dropdown.py
Resource         ../resources/common.robot
Suite Setup      Open Browser To Test Page
Suite Teardown   Close All Browsers

*** Test Cases ***

TC_Dropdown_001 Fruit Select Exists
    Login With Test Credentials
    Get Element    #fruit-select

TC_Dropdown_002 Fruit Select Options
    [Documentation]    Verify fruit dropdown has exactly 6 options
    Login With Test Credentials
    ${options}=    Get Select Options    #fruit-select
    ${count}=    Get Length    ${options}
    Should Be Equal As Integers    ${count}    6
    # Values: "", "apple", "banana", "cherry", "grape", "mango"
    FOR    ${i}    ${expected}    IN ENUMERATE
    ...    ${EMPTY}    apple    banana    cherry    grape    mango    index=1
        ${opt}=    Get From List    ${options}    ${i}
        Should Be Equal    ${opt}[value]    ${expected}
    END

TC_Dropdown_003 Select Fruit By Value Apple
    Login With Test Credentials
    Select Options By    #fruit-select    value    apple
    ${result}=    Get Text    #select-result
    Should Contain    ${result}    苹果
    Should Contain    ${result}    apple

TC_Dropdown_004 Select Fruit By Value Banana
    Login With Test Credentials
    Select Options By    #fruit-select    value    banana
    ${result}=    Get Text    #select-result
    Should Contain    ${result}    香蕉

TC_Dropdown_005 Select Fruit By Value Cherry
    Login With Test Credentials
    Select Options By    #fruit-select    value    cherry
    ${result}=    Get Text    #select-result
    Should Contain    ${result}    樱桃

TC_Dropdown_006 Select Fruit By Value Grape
    Login With Test Credentials
    Select Options By    #fruit-select    value    grape
    ${result}=    Get Text    #select-result
    Should Contain    ${result}    葡萄

TC_Dropdown_007 Select Fruit By Value Mango
    Login With Test Credentials
    Select Options By    #fruit-select    value    mango
    ${result}=    Get Text    #select-result
    Should Contain    ${result}    芒果

TC_Dropdown_008 Select Fruit By Label Text
    [Documentation]    Select by visible text (label)
    Login With Test Credentials
    Select Options By    #fruit-select    label    苹果 Apple
    ${result}=    Get Text    #select-result
    Should Contain    ${result}    苹果
    Should Contain    ${result}    apple

TC_Dropdown_009 Select Fruit By Index
    [Documentation]    Index 1 = first real option (apple)
    Login With Test Credentials
    Select Options By    #fruit-select    index    1
    ${result}=    Get Text    #select-result
    Should Contain    ${result}    苹果

TC_Dropdown_010 City Select Exists
    Login With Test Credentials
    Get Element    #city-select

TC_Dropdown_011 City Select Dynamic Loading
    [Documentation]    City options load asynchronously after ~1.5s delay
    Login With Test Credentials
    Wait For Elements State    #city-select >> option >> nth=1    attached    timeout=5s
    ${options}=    Get Select Options    #city-select
    ${count}=    Get Length    ${options}
    Should Be Equal As Integers    ${count}    7

TC_Dropdown_012 Select City By Value Beijing
    Login With Test Credentials
    Wait For Elements State    #city-select >> option >> nth=1    attached    timeout=5s
    Select Options By    #city-select    value    beijing
    ${result}=    Get Text    #city-result
    Should Contain    ${result}    北京

TC_Dropdown_013 Select City By Value Shanghai
    Login With Test Credentials
    Wait For Elements State    #city-select >> option >> nth=1    attached    timeout=5s
    Select Options By    #city-select    value    shanghai
    ${result}=    Get Text    #city-result
    Should Contain    ${result}    上海

TC_Dropdown_014 Select City By Value Guangzhou
    Login With Test Credentials
    Wait For Elements State    #city-select >> option >> nth=1    attached    timeout=5s
    Select Options By    #city-select    value    guangzhou
    ${result}=    Get Text    #city-result
    Should Contain    ${result}    广州

TC_Dropdown_015 Select City By Value Shenzhen
    Login With Test Credentials
    Wait For Elements State    #city-select >> option >> nth=1    attached    timeout=5s
    Select Options By    #city-select    value    shenzhen
    ${result}=    Get Text    #city-result
    Should Contain    ${result}    深圳

TC_Dropdown_016 Select City By Value Chengdu
    Login With Test Credentials
    Wait For Elements State    #city-select >> option >> nth=1    attached    timeout=5s
    Select Options By    #city-select    value    chengdu
    ${result}=    Get Text    #city-result
    Should Contain    ${result}    成都

TC_Dropdown_017 Select City By Value Hangzhou
    Login With Test Credentials
    Wait For Elements State    #city-select >> option >> nth=1    attached    timeout=5s
    Select Options By    #city-select    value    hangzhou
    ${result}=    Get Text    #city-result
    Should Contain    ${result}    杭州

TC_Dropdown_018 Select City By Label Text
    Login With Test Credentials
    Wait For Elements State    #city-select >> option >> nth=1    attached    timeout=5s
    Select Options By    #city-select    label    上海 Shanghai
    ${result}=    Get Text    #city-result
    Should Contain    ${result}    上海
    Should Contain    ${result}    shanghai

TC_Dropdown_019 City Options Content Verification
    [Documentation]    Verify all 7 city options match expected
    Login With Test Credentials
    Wait For Elements State    #city-select >> option >> nth=1    attached    timeout=5s
    ${options}=    Get Select Options    #city-select
    ${count}=    Get Length    ${options}
    Should Be Equal As Integers    ${count}    7
