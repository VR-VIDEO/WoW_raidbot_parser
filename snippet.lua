-- Define a callback function to handle tooltip data updates for items
local function OnTooltipSetItem(tooltip, data)
    if tooltip == GameTooltip then
        local itemId = data.id

        if ItemDB[itemId] then
            tooltip:AddLine(" ") -- Blank line
            tooltip:AddLine("Top Players for Item ID: " .. itemId)

            local players = ItemDB[itemId].players

            -- Sort players based on percentage in descending order
            table.sort(players, function(a, b)
                return a.percentage > b.percentage
            end)

            -- Display top 10 players
            local maxPlayersToShow = math.min(#players, 10)
            for i = 1, maxPlayersToShow do
                local player = players[i]
                tooltip:AddLine(player.name .. " - Percentage: " .. player.percentage .. "%")
            end

            tooltip:Show()
        end
    end
end

-- Register the callback function to handle item tooltip data updates
TooltipDataProcessor.AddTooltipPostCall(Enum.TooltipDataType.Item, OnTooltipSetItem)
