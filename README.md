## Project: 3D Motion Planning
![Quad Image](./misc/enroute.png)



## [Rubric](https://review.udacity.com/#!/rubrics/1534/view) Points

---


### Explain the Starter Code

#### 1. Explain the functionality of what's provided in `motion_planning.py` and `planning_utils.py`
In the first project (Backyard Flyer) we assumed / did not consider the obstacles there by had a static set of way points. However in a real world scenario , Planning consitutes an important role and it has been incorporated in this project (Motion Planning)

![backyard flyer vs motion planning state transition](./misc/images/comparison_backyard_Vs_motionplanning.png)

The additional funcationalities in `motion_planning.py` & `planning_utils.py` includes

[Motion planning](motion_planning.py)
1. Introduction of `Planning` State & `plan_path()` & `send_waypoints` method.

[Planning Util](planning_utils.py)
 
1. `Create_grid` method to define a grid & set a safety margin.
2. `a_star` method that finds the 'Ideal' path between start and the goal.



### Implementing Your Path Planning Algorithm
![motion planning screenshot one](./misc/images/two.png)
#### 1. Set your global home position
```
def retrieve_lat_lon(filename):
    with open(filename) as f:
        match = re.match(r'^lat0 (.*), lon0 (.*)$', f.readline())
        if match:
            return np.fromstring(f'{match.group(1)},{match.group(2)}', dtype='Float64', sep=',')

 lat0, lon0 = retrieve_lat_lon('colliders.csv')

 self.set_home_position(lon0, lat0, 0)
```

#### 2. Set your current local position
Here as long as you successfully determine your local position relative to global home you'll be all set. Explain briefly how you accomplished this in your code.

```
local_north, local_east, local_down = global_to_local(global_position, self.global_home)
    
```

#### 3. Set grid start position from local position
This is another step in adding flexibility to the start location. As long as it works you're good to go!
```
grid_start = (int(np.ceil(local_north - north_offset)), int(np.ceil(local_east - east_offset)))
```
![motion planning screenshot two](./misc/images/four.png)
#### 4. Set grid goal position from geodetic coords
This step is to add flexibility to the desired goal location. Should be able to choose any (lat, lon) within the map and have it rendered to a goal location on the grid.
```
goal_north, goal_east, goal_down = global_to_local(self.global_goal_position, self.global_home)
        grid_goal = (int(np.ceil(goal_north - north_offset)), int(np.ceil(goal_east - east_offset)))
```

#### 5. Modify A* to include diagonal motion (or replace A* altogether)
Minimal requirement here is to modify the code in planning_utils() to update the A* implementation to include diagonal motions on the grid that have a cost of sqrt(2), but more creative solutions are welcome. Explain the code you used to accomplish this step.
![motion planning screenshot three](./misc/images/five.png)
```
    WEST = (0, -1, 1)
    EAST = (0, 1, 1)
    NORTH = (-1, 0, 1)
    SOUTH = (1, 0, 1)
    SOUTH_EAST = (1, 1, np.sqrt(2))
    NORTH_EAST = (-1, 1, np.sqrt(2))
    SOUTH_WEST = (1, -1, np.sqrt(2))
    NORTH_WEST = (-1, -1, np.sqrt(2))
```

```
if x - 1 < 0 or y - 1 < 0 or grid[x-1,y-1] == 1:
        valid_actions.remove(Action.NORTH_WEST)
    if x - 1 < 0 or y + 1 > m or grid[x-1,y+1] == 1:
        valid_actions.remove(Action.NORTH_EAST)
    if x + 1 > n or y - 1 < 0 or grid[x+1,y-1] == 1:
        valid_actions.remove(Action.SOUTH_WEST)
    if x + 1 > n or y + 1 > m or grid[x+1,y+1] == 1:
        valid_actions.remove(Action.SOUTH_EAST)
```

#### 6. Cull waypoints 
For this step you can use a collinearity test or ray tracing method like Bresenham. The idea is simply to prune your path of unnecessary waypoints. Explain the code you used to accomplish this step.
![Prune](./misc/images/one.png)



```
def prune(path, epsilon=1e-6):
    
    def point(p):
        return np.array([p[0], p[1], 1.]).reshape(1, -1)

    def collinearity_check(p1, p2, p3):   
        m = np.concatenate((p1, p2, p3), 0)
        det = np.linalg.det(m)
        return abs(det) < epsilon

    pruned_path = [p for p in path]
    i = 0
    while i < len(pruned_path) - 2:
        p1 = point(pruned_path[i])
        p2 = point(pruned_path[i+1])
        p3 = point(pruned_path[i+2])
        collinear = collinearity_check(p1, p2, p3)
        if collinear:
            pruned_path.remove(pruned_path[i+1])
        else:
            i += 1
    return pruned_path

```

### Execute the flight
#### 1. Does it work?
It works!

![Landing](./misc/images/three.png)
