# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s example.conference -t test_program.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src example.conference.testing.EXAMPLE_CONFERENCE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_program.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Program
  Given a logged-in site administrator
    and an add program form
   When I type 'My Program' into the title field
    and I submit the form
   Then a program with the title 'My Program' has been created

Scenario: As a site administrator I can view a Program
  Given a logged-in site administrator
    and a program 'My Program'
   When I go to the program view
   Then I can see the program title 'My Program'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add program form
  Go To  ${PLONE_URL}/++add++Program

a program 'My Program'
  Create content  type=Program  id=my-program  title=My Program


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I submit the form
  Click Button  Save

I go to the program view
  Go To  ${PLONE_URL}/my-program
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a program with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the program title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
