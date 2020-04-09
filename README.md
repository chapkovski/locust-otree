# Locust script for testing oTree apps

## Attention:
This code will work with the most recent version of oTree. For older ones, a slightly different approach is needed. DM me.

## Installation:
1. Install locust: 
`pip install locust`

2. Run `locust` in a folder where the `locustfile.py` is located.

3. In browser go to <http://localhost:8089>

4. The front page should look like that:
![alt text][front]

[front]: https://raw.githubusercontent.com/chapkovski/locust-otree/master/img/locust_first_page.png "Front"

5. Open your oTree app and create a session with *browser bots activated*:
![alt text][session10]

[session10]: https://raw.githubusercontent.com/chapkovski/locust-otree/master/img/session_10.gif "Session 10"

6. Copy the *Session-wide link* and paste to Locust. Provide number of users 
(corresponding to number of users in a session you created), and the speed of 
__hatching__ (how quckly they join the game.)

![alt text][paste]

[paste]: https://raw.githubusercontent.com/chapkovski/locust-otree/master/img/paste_to_locust.gif "Session 10"


7. Observe how they start playing and the response times, and if there are any failures there.


 