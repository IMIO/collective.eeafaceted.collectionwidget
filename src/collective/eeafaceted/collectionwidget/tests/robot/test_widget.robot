*** Settings ***
Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/selenium.robot

Library  Remote  ${PLONE_URL}/RobotRemote
Library  plone.app.robotframework.keywords.Debugging

Suite Setup  Suite Setup
Suite Teardown  Close all browsers

*** Test cases ***

Widget shows no collections or categories
    Make faceted folder
    Click link  Faceted criteria
    Page should contain  Base collections
    
Widget shows empty categories
    ${folder}=  Make faceted folder
    ${category}=  Create content  type=Folder  title=News  id=news  container=${folder}
    Click link  Faceted criteria
    Page should contain  Base collections
    Element Text Should Be  css=div#c1_widget li.title  News

Widget shows categories
    [tags]  current
    ${folder}=  Make faceted folder
    ${category}=  Create content  type=Folder  title=News  id=news  container=${folder}
    Create content  type=Collection  title=Info  id=info  container=${category}
    Go to  ${PLONE_URL}/faceted
    Page Should Contain  Info
    Click Element  css=li[title="Info"]
    Wait Until Page Contains Element  css=div.eea-preview-items
    element should contain  css=div.eea-preview-items  Faceted folder


*** Keywords ***
Suite Setup
    Open test browser
    Enable autologin as  Manager

Make faceted folder
    ${folder}=  Create content  type=Folder  title=Faceted folder  id=faceted
    Go to  ${PLONE_URL}/faceted
    Click element  css=#plone-contentmenu-actions a
    Click element  plone-contentmenu-actions-faceted.enable
    [Return]  ${folder}