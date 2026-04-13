# -*- coding: utf-8 -*-
*** Settings ***
Documentation    File upload test suite - mirrors selenium-pom test_file_upload.py
Resource         ../resources/common.robot
Suite Setup      Open Browser To Test Page
Suite Teardown   Close Browser
Test Setup       Login And Go To Main Page

*** Variables ***
${UPLOAD_DIR}    ${TEMPDIR}

*** Test Cases ***

TC_Upload_001 Upload Section Exists
    Get Element    \#upload-drop-zone
    Get Element    \#file-input

TC_Upload_002 Upload Text File
    ${filepath}=    Set Variable    ${UPLOAD_DIR}${/}rf_upload_test.txt
    Create File    ${filepath}    This is a test file for RF Playwright upload testing.
    Upload File To Input    \#file-input    ${filepath}
    Wait For Elements State    \#upload-file-info.visible    visible    5s
    ${name}=    Get Text    \#upload-file-name
    Should End With    ${name}    rf_upload_test.txt
    Remove File    ${filepath}

TC_Upload_003 Upload File Fullpath Display
    ${filepath}=    Set Variable    ${UPLOAD_DIR}${/}rf_fullpath_test.txt
    Create File    ${filepath}    fullpath display test
    Upload File To Input    \#file-input    ${filepath}
    ${fp}=    Get Text    \#upload-file-fullpath
    Should Contain    ${fp}    fakepath
    Remove File    ${filepath}

TC_Upload_004 Upload Different Extensions
    FOR    ${ext}    IN    .txt    .pdf    .doc    .jpg    .png
        ${filepath}=    Set Variable    ${UPLOAD_DIR}${/}rf_ext_test${ext}
        Create File    ${filepath}    test content for ${ext}
        Upload File To Input    \#file-input    ${filepath}
        Wait For Elements State    \#upload-file-info.visible    visible    5s
        Remove File    ${filepath}
    END

TC_Upload_005 Clear Uploaded File
    ${filepath}=    Set Variable    ${UPLOAD_DIR}${/}rf_clear_test.txt
    Create File    ${filepath}    to be cleared
    Upload File To Input    \#file-input    ${filepath}
    Wait For Elements State    \#upload-file-info.visible    visible    5s
    Click    .upload-clear-btn
    Wait For Elements State    \#upload-file-info.visible    hidden    5s
    Remove File    ${filepath}

TC_Upload_006 Upload Empty File
    ${filepath}=    Set Variable    ${UPLOAD_DIR}${/}rf_empty_test.txt
    Create File    ${filepath}    ${EMPTY}
    Upload File To Input    \#file-input    ${filepath}
    Wait For Elements State    \#upload-file-info.visible    visible    5s
    Remove File    ${filepath}