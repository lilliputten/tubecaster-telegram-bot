<!--
 @since 2025.09.02
 @changed 2025.09.02, 02:52
-->

# CHANGELOG

## [v.0.0.16](https://github.com/lilliputten/tubecaster-telegram-bot/releases/tag/v.0.0.16) - 2025.09.02

- Added a function to send stats info to the chat, via the `/stats` command.
- Added `updateStats` calls in `downloadAndSendAudioToChat` and `sendInfoToChat` functions.
- Added `updateStats` database action (aimed to update the current user' stats records).
- Updated prisma data models to maintain stats data (`TotalStats` and `MonthlyStats`).

See also:

- [Issue #39: Record and display users usage statistics](https://github.com/lilliputten/tubecaster-telegram-bot/issues/39)
- [Compare](https://github.com/lilliputten/tubecaster-telegram-bot/compare/v.0.0.15...v.0.0.16)
