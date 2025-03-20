<!--
 @since 2024.11.20, 02:55
 @changed 2025.03.20, 11:38
-->


# tubecaster-telegram-bot


Simple video to audio caster telegram bot


## Build info (auto-generated)

- Project info: v.0.0.15 / 2025.02.22 05:42:34 +0300


## Resources

Repository: https://github.com/lilliputten/tubecaster-telegram-bot

Vercel panel: https://vercel.com/lilliputtens-projects/tubecaster-telegram-bot

Landing with basic info: https://tubecasterlilliputten.com/


## Updating and deploying

Don't forget to invoke `/start` route from the deployed appliaction to point the telegram webhook api to the actual address (see also `WEBHOOK_HOST` environment parameters).

Keep in mind that deploy on the dedicated VDS server is actually proceeded only for the `main` branch (or other specific if they included into the automatic-webhook-deploy configuration).


## See also

- [Vercel deployment](README.vercel-deployment.md) -- Unused as it's turned out that video and audio related operation require some disk space which is absent on vercel service.
- [Youtube downloader library notes](README.ytdl.md)
