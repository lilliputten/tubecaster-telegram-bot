41-usage-plans
https://github.com/lilliputten/tubecaster-telegram-bot/issues/41
Issue #41:
Create a plan-based users controlling system with guest, free and paid tiers.

- Added `UserStatus` data model. Added new bot commands: `status`, `plans`, `become_user`, `get_full_access`, `remove_account`, `restore_account`. Updated dialog texts and messages. Users divided by 3 groups: guests, free and paid tiers. Guests and free users have limits (defined by constants in `botCore/constants/limits.py`). Added new db actions: `collectStats`, `updateStats`, `ensureValidUser`, `findUser`. Added new core bot helpers: `addNewValidUser`, `checkValidUser`, `createAcceptNewUserButtonsMarkup`, `createSendRegistrationReguestButtonsMarkup`, `sendNewUserRequestToController`, `showNewUserMessage`. Added api methods: `downloadAndSendAudioToChat`, `sendInfoToChat`, `sendStatsToChat`. Added ability to remove (to mark to removal in a month) and restore (in a month) user's account.
- Already replaced an old checkValidUser/showNewUserMessage valid user checking method with a new checkUserLimitations/showOutOfLimitsMessage.
- Connected telegram XTR invoice payment.
- Updated version: 0.1.1.
