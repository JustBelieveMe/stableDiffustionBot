Stable Diffusion Bot
----------------------
2023/05/11 release 0.0.2

New feature:
1. detail paint for five parameter.
2. separate auth function to another py file.
3. add help message via /help function


Bug fix:
None

Discussion:
1. According to community, discord.py is still not support select menu in modal that it only support textInput. Also, it is heard of that the modal can only stack five components. By this I decide to decrease the function that the detail can do: {prompt, ng_prompt, size, sampler, CFG}

2. I expect to have memorize function in detailpaint function but current is not complete