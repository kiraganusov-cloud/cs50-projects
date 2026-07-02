-- Keep a log of any SQL queries you execute as you solve the mystery.

-- read the description from the crime scene reports
SELECT description
FROM crime_scene_reports
WHERE month = 7 and day = 28 and street = 'Humphery Street';

-- read the transcripts from the interviews
SELECT transcript
FROM interviews
WHERE month = 7 and day = 28 and year = 2025;


-- theifs name
SELECT name
FROM people
WHERE id IN(
    SELECT person_id
    FROM bank_accounts
    WHERE account_number IN(
        SELECT account_number
        FROM atm_transactions
        WHERE month = 7 and day = 28 and year = 2025 and atm_location = 'Leggett Street' and transaction_type = 'withdraw' and account_number IN(
            -- find bank account numbers of possible suspects
            SELECT account_number
            FROM bank_accounts
            WHERE person_id IN(
                -- possible theifs ids
                SELECT id
                FROM people
                WHERE phone_number IN (
                    -- phone calls that happened that day less than a minute long
                    SELECT caller
                    FROM phone_calls
                    WHERE year = 2025 and month = 7 and day = 28 and duration < 60
                ) AND passport_number IN(
                    -- passports on passenger on the flights that departed the next dau
                    SELECT passport_number
                    FROM passengers
                    WHERE flight_id IN(
                        SELECT id
                        FROM flights
                        WHERE year = 2025 and month = 7 and day = 29
                        ORDER BY hour, minute
                        LIMIT 1
                    )
                ) AND license_plate IN(
                    -- license plates that were at bakery
                    SELECT license_plate
                    FROM bakery_security_logs
                    WHERE year = 2025 and month = 7 and day = 28 and hour = 10 and minute BETWEEN 15 and 25
                )
            )
        )
    )
);

-- accomplice
SELECT name
FROM people
WHERE phone_number = (
    SELECT receiver
    FROM phone_calls
    WHERE caller = (
        SELECT phone_number
        FROM people
        WHERE name = 'Bruce'
    ) and year = 2025 and month = 7 and day = 28 and duration < 60
);


-- destination
SELECT city
FROM airports
WHERE id = (
    SELECT destination_airport_id
    FROM flights
    WHERE id IN (
        SELECT flight_id
        FROM passengers
        WHERE passport_number IN(
            SELECT passport_number
            FROM people
            WHERE name = 'Bruce'
        )
    )
);
