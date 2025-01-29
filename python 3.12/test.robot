*** Settings ***

Library           SeleniumLibrary
*** Variables ***
${HOMEPAGE}    http://www.google.com
${BROWSER}     Edge

*** Keywords ***
open the browser
Open Browser    ${HOMEPAGE}    ${BROWSER}

search topic
[Arguments] ${topic}
Input Text name=q ${topic}
Press Key name=q \\13

*** Test Cases ***

Open Browser
open the browser

Search on Google
search topic browserstack