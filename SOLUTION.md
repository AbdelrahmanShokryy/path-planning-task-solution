# My Solution 

## What I did (Part 1)
1. I ignore cones that are behind the car.
2. I make "middle points" of the track:
   - one blue cone + one yellow cone -> I take the point in the middle of them
   - a cone with no partner -> I move it 1 meter sideways towards the middle (blue goes right, yellow goes left)
   - no cones -> the car just goes straight
3. The car walks from its position to each middle point in steps of 0.5 m.
4. After the last point, it keeps going in the same direction until the path is 9 m long (18 points).

## Part 2 (3 cones on one side)
- I treat each of the 3 cones like a single cone: move each one 1 m towards the middle, then connect the points.
- Why: it is the easiest way and it reuses the same code. 3 cones give a better idea of where the track is going than 1 cone.
- New test cases are 21 to 26 in `src/scenarios.py` (straight, left bend, right bend, 3 blue + 1 yellow, a cone behind the car).

## What I assumed
- The track is 2 m wide.
- Cones behind the car are not useful.
- The first blue cone matches the first yellow cone (closest ones are partners).

## Limitations
- The path has sharp corners, it is not smooth.
- If the track is not 2 m wide, the path will be a bit off when only one side is seen.
- After the last cone it goes straight, so it can not predict a bend that comes later.
- If a cone is missed, the pairing can be wrong.
- Cones placed across the car's direction (scenarios 5, 8, 13) give weird paths.
- No noise, no collision checking, no car turning limits.
