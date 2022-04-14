mudlet = mudlet or {}; mudlet.mapper_script = true

-- Helper Functions
function tableLen(table)
	-- Get the length of a table
	size = 0
	for _ in pairs(table) do size = size + 1 end
	return size
end

function findAreaID(areaname)
	-- Find an areaId by it's name
  local list = getAreaTable()
  local returnid, fullareaname
  for area, id in pairs(list) do
    if area:find(areaname, 1, true) then
      if returnid then return false, "more than one area matches" end
      returnid = id; fullareaname = area
    end
  end
  return returnid, fullareaname
end

function getCoordsFromStr(coordStr)
	-- Parse coords from gmcp string - ie. "1,1,2" -> {1,1,2}
	local coordTable = {}
	for i in string.gmatch(coordStr, "([^,]+)") do
     table.insert(coordTable, tonumber(i))
  end
	return coordTable
end



-- Init
local locData = gmcp.Core.Location -- Base Location Data
local areaId = locData.area_name .. " (" .. locData.area_id .. ")" -- Generated Area Name

-- If there is an area, use that ID
hasArea, fullAreaName = findAreaID(areaId)
if(hasArea) then areaId = fullAreaName end



-- Script Start

-- 1. Create an area if none exists
areas = getAreaTable()
local area = areas[areaId]
if(not hasArea) then
	area = addAreaName(areaId)
end



-- 2.  - Add current room to area
-- 2.1 - Setup
roomCoords = getCoordsFromStr(locData.room_coord)
rooms = getRoomsByPosition(area, roomCoords[1], roomCoords[2], roomCoords[3])

if(tableLen(rooms) > 0) then
	centerview(locData.room_id)
end

-- 2.2 - Delete overlapping/existing rooms at this coord
-- Add validation for creating a room here. ie. If you don't want to delete a room at this spot
roomValid = true

if(roomValid) then
  for r in pairs(rooms) do
  	deleteRoom(r)
  end
	
	addRoom(locData.room_id)
  setRoomCoordinates(locData.room_id, roomCoords[1], roomCoords[2], roomCoords[3])
  setRoomArea(locData.room_id, areaId)
  centerview(locData.room_id)
	
	-- 2.3 - Create exits
	roomExits = locData.room_exits
	for key, val in pairs(roomExits) do
		addCustomLine(locData.room_id, val, key, "dot line", {255, 255, 255}, false)
	end
end
