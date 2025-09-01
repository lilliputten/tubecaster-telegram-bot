> 2025.09.01

Add a function to update user stats in the module `db/_updateStats.py` named `updateStats`.

Is should update (or create if absent) records in `TotalStats` and `MonthlyStats` tables.

Check data model in `prisma/schema.prisma` for `TotalStats` and `MonthlyStats` tables: there no `id` fields. They use related `userId` as a key. In case of `MonthlyStats` there is a combilned key for userId + year + month (`userId_year_month`).

So, add a `userId` parameter for function:

The signature should be as the following:

`updateStats(userId: int, volume: int)`.

It should increment both `records` fields (or set them to 1 if record was absent). And add the `volume` value to bot `volume` fileds (or set them to this value if absent).

It should use current year and month values (from `d = date.today()`) to create or update the `MonthlyStats` record.

Add corresponding tests and add it to the export in `__init__.py`.

User other methods there as examples. See `addCommand` and its test: `_addCommand.py`
`_addCommand_test.py`, or `addTempMessage` funciton: `_addTempMessage.py`
`_addTempMessage_test.py`

Use the similar variable namings, like in provided examples (eg, camel case form for prisma clients, like `commandClient = Command.prisma()`).

Use a transaction for data update.
