

class localization():
    """Performing Bayesian Updating to Produce a Distribution of Likely Positions in the Environment"""

    def __init__(self, colours, measurements, motions, sensor_right, p_move):
        self.world = colours
        self.measurements = measurements
        self.motions = motions
        self.sensor_right = sensor_right
        self.p_move = p_move

        # Initialate Uniform Prior
        pinit = 1.0 / float(len(colours)) / float(len(colours[0]))
        self.p = [[pinit for row in range(len(colours[0]))] for col in range(len(colours))]

    def sense(self, p, world, measurement):
        """Compute probabilities after sensing the world (with some confidence)"""
        q = [[0.0 for row in range(len(world[0]))] for col in range(len(world))]

        s = 0.0
        for i in range(len(p)):
            for j in range(len(p[i])):
                hit = (measurement == world[i][j])
                q[i][j] = p[i][j] * (hit * self.sensor_right + (1-hit)*(1-self.sensor_right))
                s += q[i][j]

        # normalize
        for i in range(len(q)):
            for j in range(len(p[0])):
                q[i][j] /= s

        return q


    def move(self, p, motion):
        """Compute probabilities after moving through world (with some confidence)"""
        q = [[0.0 for row in range(len(self.world[0]))] for col in range(len(self.world))]

        for i in range(len(p)):
            for j in range(len(p[0])):
                q[i][j] = (self.p_move * p[(i-motion[0]) % len(p)][(j-motion[1]) % len(p[i])]) + ((1-self.p_move) * p[i][j])
        return q


    def compute_posterior(self):
        """Call Computation"""
        p = self.p
        for i in range(len(self.measurements)):
            p = self.move(p, self.motions[i])
            p = self.sense(p, self.world, self.measurements[i])

        return p


    def show(self, p):
        rows = ['[' + ','.join(map(lambda x: '{0:.5f}'.format(x),r)) + ']' for r in p]
        print('[' + ',\n '.join(rows) + ']')



# -------------- Call Class ----x

colours = [['R','G','G','R','R'],
          ['R','R','G','R','R'],
          ['R','R','G','G','R'],
          ['R','R','R','R','R']]
measurements = ['G','G','G','G','G']
motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]

localization = localization(colours=colours, measurements=measurements, motions=motions, sensor_right=0.7, p_move=0.8)
posterior = localization.compute_posterior()
localization.show(posterior)







# -------------- Instructions ----x

# The function localize takes the following arguments:
#
# colours:
#        2D list, each entry either 'R' (for red cell) or 'G' (for green cell)
#
# measurements:
#        list of measurements taken by the robot, each entry either 'R' or 'G'
#
# motions:
#        list of actions taken by the robot, each entry of the form [dy,dx],
#        where dx refers to the change in the x-direction (positive meaning
#        movement to the right) and dy refers to the change in the y-direction
#        (positive meaning movement downward)
#        NOTE: the *first* coordinate is change in y; the *second* coordinate is
#              change in x
#
# sensor_right:
#        float between 0 and 1, giving the probability that any given
#        measurement is correct; the probability that the measurement is
#        incorrect is 1-sensor_right
#
# p_move:
#        float between 0 and 1, giving the probability that any given movement
#        command takes place; the probability that the movement command fails
#        (and the robot remains still) is 1-p_move; the robot will NOT overshoot
#        its destination in this exercise
#
# The function should RETURN (not just show or print) a 2D list (of the same
# dimensions as colours) that gives the probabilities that the robot occupies
# each cell in the world.
#
# Compute the probabilities by assuming the robot initially has a uniform
# probability of being in any cell.
#
# Also assume that at each step, the robot:
# 1) first makes a movement,
# 2) then takes a measurement.
#
# Motion:
#  [0,0] - stay
#  [0,1] - right
#  [0,-1] - left
#  [1,0] - down
#  [-1,0] - up
