<!--
 @since 2025.09.02
 @changed 2026.01.30, 20:12
-->

# CHANGELOG

## [v.0.2.2](https://github.com/lilliputten/tubecaster-telegram-bot/releases/tag/v.0.2.2) - 2026.01.30

- Updated to yt-dlp v.2026.01.29.
- Updated minor version: v.0.2.2.

See also:

- [Compare with the previous version](https://github.com/lilliputten/tubecaster-telegram-bot/compare/v.0.2.1...v.0.2.2)

## [v.0.2.1](https://github.com/lilliputten/tubecaster-telegram-bot/releases/tag/v.0.2.1) - 2025.10.14

- Issue #45: Updated yt-dlp version to 2025.10.12.232804.dev0.
- Updated minor version: v.0.2.1.

See also:

- [Compare with the previous version](https://github.com/lilliputten/tubecaster-telegram-bot/compare/v.0.1.2...v.0.2.1)

## [v.0.1.2](https://github.com/lilliputten/tubecaster-telegram-bot/releases/tag/v.0.1.2) - 2025.10.09

- In case of error 403, the download is repeated several times (5).
- The video retrieving parameter has been removed for pre-requesting the video details.

See also:

- [Compare with the previous version](https://github.com/lilliputten/tubecaster-telegram-bot/compare/v.0.1.1...v.0.1.2)

## [v.0.1.1](https://github.com/lilliputten/tubecaster-telegram-bot/releases/tag/v.0.1.1) - 2025.09.05

Implemented usage control based on different usage plans, added ability to pay for the PAID plan via telegram stars (XTR).

- Added `UserStatus` data model. Added new bot commands: `status`, `plans`, `become_user`, `get_full_access`, `remove_account`, `restore_account`. Updated dialog texts and messages. Users divided by 3 groups: guests, free and paid tiers. Guests and free users have limits (defined by constants in `botCore/constants/limits.py`). Added new db actions: `collectStats`, `updateStats`, `ensureValidUser`, `findUser`. Added new core bot helpers: `addNewValidUser`, `checkValidUser`, `createAcceptNewUserButtonsMarkup`, `createSendRegistrationReguestButtonsMarkup`, `sendNewUserRequestToController`, `showNewUserMessage`. Added api methods: `downloadAndSendAudioToChat`, `sendInfoToChat`, `sendStatsToChat`. Added ability to remove (to mark to removal in a month) and restore (in a month) user's account.
- Already replaced an old checkValidUser/showNewUserMessage valid user checking method with a new checkUserLimitations/showOutOfLimitsMessage.
- Connected telegram XTR invoice payment.
- Updated minor version: 0.1.1.

2025.10.09:

- In case of error 403, the download is repeated several times (5).

See also:

- [Issue #41: Create a plan-based users controlling system with guest, free and paid tiers](https://github.com/lilliputten/tubecaster-telegram-bot/issues/41)
- [Compare with the previous version](https://github.com/lilliputten/tubecaster-telegram-bot/compare/v.0.0.16...v.0.1.1)

## [v.0.0.16](https://github.com/lilliputten/tubecaster-telegram-bot/releases/tag/v.0.0.16) - 2025.09.02

- Added a function to send stats info to the chat, via the `/stats` command.
- Added `updateStats` calls in `downloadAndSendAudioToChat` and `sendInfoToChat` functions.
- Added `updateStats` database action (aimed to update the current user' stats records).
- Updated prisma data models to maintain stats data (`TotalStats` and `MonthlyStats`).

See also:

- [Issue #39: Record and display users usage statistics](https://github.com/lilliputten/tubecaster-telegram-bot/issues/39)
- [Compare with the previous version](https://github.com/lilliputten/tubecaster-telegram-bot/compare/v.0.0.15...v.0.0.16)
