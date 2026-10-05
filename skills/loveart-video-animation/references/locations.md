# Location Database

Use these exact names when locking and referencing locations. Expand the list as the project grows.

## Core Locations

- bedroom
- bedroom_angle_front
- bedroom_angle_side
- bedroom_angle_window
- kitchen
- kitchen_angle_counter
- kitchen_angle_table
- living_room
- living_room_angle_sofa
- living_room_angle_window
- bathroom
- store
- store_interior
- store_exterior
- street_next_to_house
- street_next_to_shop
- park
- park_bench
- cafe_interior
- cafe_exterior
- hallway
- balcony
- garden
- school_classroom
- office
- car_interior
- bus_stop

## Rules

- Always prefer the most specific name available (e.g. bedroom_angle_window instead of just bedroom).
- When a new location appears in the script, propose a clear snake_case name and lock a reference image for it.
- Multiple angles of the same room are treated as separate locked references.
- In every generation prompt explicitly state the location name so the correct visual reference can be attached.
