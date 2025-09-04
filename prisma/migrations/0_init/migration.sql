-- CreateTable
CREATE TABLE "TempMessages" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "messageId" BIGINT NOT NULL,
    "commandId" INTEGER NOT NULL,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "TempMessages_commandId_fkey" FOREIGN KEY ("commandId") REFERENCES "Commands" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "Commands" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "messageId" BIGINT NOT NULL,
    "updateId" BIGINT NOT NULL,
    "userId" BIGINT NOT NULL,
    "userStr" TEXT NOT NULL DEFAULT '',
    "repeated" INTEGER NOT NULL DEFAULT 1,
    "isActive" BOOLEAN NOT NULL DEFAULT true,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- CreateTable
CREATE TABLE "Users" (
    "id" BIGINT NOT NULL PRIMARY KEY,
    "userStr" TEXT NOT NULL DEFAULT '',
    "isDeleted" BOOLEAN NOT NULL DEFAULT false,
    "deletedAt" DATETIME,
    "languageCode" TEXT,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- CreateTable
CREATE TABLE "UserStatus" (
    "userId" BIGINT NOT NULL,
    "userMode" TEXT NOT NULL DEFAULT 'GUEST',
    "statusChangedAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "paidAt" DATETIME,
    "paymentValidUntil" DATETIME,
    "paymentId" TEXT,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "UserStatus_userId_fkey" FOREIGN KEY ("userId") REFERENCES "Users" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "TotalStats" (
    "userId" BIGINT NOT NULL,
    "requests" BIGINT NOT NULL DEFAULT 0,
    "infoRequests" BIGINT NOT NULL DEFAULT 0,
    "failures" BIGINT NOT NULL DEFAULT 0,
    "volume" BIGINT NOT NULL DEFAULT 0,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "TotalStats_userId_fkey" FOREIGN KEY ("userId") REFERENCES "Users" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "MonthlyStats" (
    "userId" BIGINT NOT NULL,
    "year" INTEGER NOT NULL,
    "month" INTEGER NOT NULL,
    "requests" BIGINT NOT NULL DEFAULT 0,
    "infoRequests" BIGINT NOT NULL DEFAULT 0,
    "failures" BIGINT NOT NULL DEFAULT 0,
    "volume" BIGINT NOT NULL DEFAULT 0,
    CONSTRAINT "MonthlyStats_userId_fkey" FOREIGN KEY ("userId") REFERENCES "Users" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateIndex
CREATE INDEX "Users_isDeleted_idx" ON "Users"("isDeleted");

-- CreateIndex
CREATE UNIQUE INDEX "UserStatus_userId_key" ON "UserStatus"("userId");

-- CreateIndex
CREATE UNIQUE INDEX "TotalStats_userId_key" ON "TotalStats"("userId");

-- CreateIndex
CREATE INDEX "MonthlyStats_year_month_idx" ON "MonthlyStats"("year", "month");

-- CreateIndex
CREATE INDEX "MonthlyStats_userId_year_idx" ON "MonthlyStats"("userId", "year");

-- CreateIndex
CREATE INDEX "MonthlyStats_userId_idx" ON "MonthlyStats"("userId");

-- CreateIndex
CREATE UNIQUE INDEX "MonthlyStats_userId_year_month_key" ON "MonthlyStats"("userId", "year", "month");