# cse312project
#PROJECT TITLE
#PROJECT DESCRIPTION
#FEATURES
#INSTALLATION
#DEPENDENCIES
#AUTHORS


## Objective 1/3 test cases

1. Open 3 browser (2 normal tab and 1 incognito) for simplicity tab1, tab2, tab3 = p1, p2, p3
2. Sign up and log in, Navigate to battle page by click on battle button on top right (all 3 tabs)
3. p1 and p2 click on battle button
    - Ensure all tabs can see p1 and p2 battle request
    - p1 can not see p1's battle request button (or vice vera for p2)
4. p1 click on p2 battle request (or vice versa)
    - use p3 to see that p1 battle request is gone (if p1 click on p2 or vice versa)
    - p3 see p1 and p2 battle on going request
    - make sure p1 and p2 are redirected to war_zone page
    - Ensure all values are there (p1info and p2info) on war_zone page
5. p1 click on attack p2 do nothing for 60 secs (or vice versa)
    - Ensure message say p1 win b/c p2 fail to make  move
    - You are redirected to battle page after match is done
    - wait 10 seconds on the battle page to ensure you don't get redirected again
    - repeat for p2 
    - repeat for both p1 and p2 not pressing any button
6. when battle is done ensure that its gone from the battle list
7. Restart another battle
    - in p1 tab control-f (id="p1_attack_button" onclick="attack('p1')") change onclick="attack('p1')" to onclick="attack('p2')" and click attack
    - Ensure that message said p1modifiy value p2 win
    - repeat for defend button id="p1_defend_button" onclick="defend('p1')" to onclick="defend('p2')
    - Repeat 7a-7c for p2
8. Restart another battle
    - ensure that p1 win and ensure that result is corrent
    - repeat for p2 
9. Go back to home page
    - ensure that leaderboard is correct 
10. Restart another battle
    - use p1 press forfeit button, Ensure result is correct
    - repeat for p2
