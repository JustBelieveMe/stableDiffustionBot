Stable Diffusion Bot

New feature:
1. i2i function
2. easy negative
3. add the current bot version at status

Bug fix:
1. the most length of embed output is now under 1024 characters. However, this will make the repaint function that only remember the embed content.

----------------------

2023/05/21 release 0.2.0

New feature:
1. repaint button (green) 
2. delete button (red)

Known Bug:
1. the most length of embed output should be restrict.


----------------------

2023/05/17 hot fix 0.1.1

Bug fix:
1. easypaint mode is now ok

----------------------
2023/05/17 release 0.1.0

New feature:
1. bot return format change as embed, including all parameter and current model.
2. new command: /changesd. A command that change the stable diffusion model running now.
3. new model: AOM3, CF3 and 7th.
4. the auth mode is change to guilds auth, currently, there is no necessary to add individual user.
5. the bot statement will show  the running model.

Bug fix:
1. The searching method is now all change to hash table(dict), this should improve the efficiency.

Known bugs:
1. Currently, the command is facing a problem that multiple command sent will cause interaction 404.

Discussion:
1. A suggestion: the variable naming style is not unifing, next time should be fixed.


----------------------
2023/05/11 release 0.0.2

New feature:
1. detail paint for five parameter.
2. separate auth function to another py file.
3. add help message via /help functio

Bug fix:
None

Discussion:
1. According to community, discord.py is still not support select menu in modal that it only support textInput. Also, it is heard of that the modal can only stack five components. By this I decide to decrease the function that the detail can do: {prompt, ng_prompt, size, sampler, CFG}

2. I expect to have memorize function in detailpaint function but current is not complete