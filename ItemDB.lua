-- ItemDB.lua

-- Sample database storing item information and player data
local ItemDB = {
    [202470] = { -- Example item ID
        players = {
            {name = "Player1", percentage = 80},
            {name = "Player2", percentage = 75},
            -- Add more player data here for this item ID
        }
    },
    -- Add more item IDs and corresponding player data as needed
}

return ItemDB
