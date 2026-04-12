# -*- coding: utf-8 -*-
*** Settings ***
Documentation    File upload test suite - mirrors selenium-pom test_file_upload.py
Resource         ../resources/common.robot
Suite Setup      Open Browser To Test Page
Suite Teardown   Close All Browsers

*** Test Cases ***

TC_Upload_001 Upload Section Exists
    [Documentation]    Verify upload drop zone and file input are present
    Login With Test Credentials
    Get Element    #upload-drop-zone
    Get Element    #file-input

TC_Upload_002 Upload Text File
    [Documentation]    Upload a txt file, verify name and meta info displayed
    Login With Test Credentials
    ${tmp}=    Create File    ${TEMPDIR}${/}rf_upload_test.txt    This is a test file for RF Playwright upload testing.
    Upload File To Input    #file-input    ${tmp}
    Wait For Elements State    #upload-file-info.visible    visible    timeout=5s
    ${name}=    Get Text    #upload-file-name
    Should End With    ${name}    rf_upload_test.txt
    # Clean up
    Remove File    ${tmp}

TC_Upload_003 Upload File Fullpath Display
    [Documentation]    After upload, fullpath field should contain fakepath
    Login With Test Credentials
    ${tmp}=    Create File    ${TEMPDIR}${/}rf_fullpath_test.txt    fullpath display test
    Upload File To Input    #file-input    ${tmp}
    ${fp}=    Get Text    #upload-file-fullpath
    Should Contain    ${fp}    fakepath
    Remove File    ${tmp}

TC_Upload_004 Upload Different Extensions
    [Documentation]    Upload files with various extensions
    Login With Test Credentials
    FOR    ${ext}    IN    .txt    .pdf    .doc    .jpg    .png
        ${fname}=    Set Variable    rf_ext_test${ext}
        ${tmp}=    Create File    ${TEMPDIR}${/}${fname}    test content for ${ext}
        Upload File To Input    #file-input    ${tmp}
        Wait For Elements State    #upload-file-info.visible    visible    timeout=5s
        Clear Text    #file-input    # doesn't work for file inputs
        Remove File    ${tmp}
    END

TC_Upload_005 Clear Uploaded File
    [Documentation]    Clear button should hide file info
    Login With Test Credentials
    ${tmp}=    Create File    ${TEMPDIR}${/}rf_clear_test.txt    to be cleared
    Upload File To Input    #file-input    ${tmp}
    Wait For Elements State    #upload-file-info.visible    visible    timeout=5s
    Click    .upload-clear-btn
    Wait For Elements State    #upload-file-info.visible    hidden    timeout=5s
    Remove File    ${tmp}

TC_Upload_006 Upload Empty File
    [Documentation]    Empty file should still upload successfully
    Login With Test Credentials
    ${tmp}=    Create File    ${TEMPDIR}${/}rf_empty_test.txt    ${EMPTY}
    Upload File To Input    #file-input    ${tmp}
    Wait For Elements State    #upload-file-info.visible    visible    timeout=5s
    Remove File    ${tmp}
