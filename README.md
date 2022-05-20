# Mattermost Online Simulator

If ou can't stay online in Mattermost but have to, then just start this online simulator and that's done:)

You need Docker to use this tool. Install the Docker and just exec the following command:
```bash
docker run --rm --name mattermost-online-simulator -e WORKSPACE_URL=https://YOUR_MATTERMOST_URL -e AUTH_LOGIN=YOUR_MATTERMOST_LOGIN -e AUTH_PASSWORD=YOUR_MATTERMOST_PASSWORD alexsergin/mattermost-online-simulator
```

You can also specify end work hour and minutes with `END_HOUR` and `END_MINUTES` env variables.
You can set an interval for `END_MINUTES` as `FROM:TO` like `30:59`.
In that case client will choose random value from the interval and stop in different time.
If you'll set just a single minute the client stop in specified minute all time. 