# Space Invaders
# python 3.10
# Thanks to Christian Thompson
# Python Game Programming Tutorial: Space Invaders
# http://christianthompson.com/
# Αλλαγές στον κώδικα για την 2η ΑΕ στο ΣΘΕΤ-ΑΨΛ Γαβριηλίδης Γαβριήλ

import turtle
import random
import math
import winsound

win = turtle.Screen()
win.setup(width=0.5, height=0.9)  # Μεγάλωσα το παράθυρο για να φαίνεται καλύτερα το background
win.bgcolor("blue")
win.title("Space Invaders")
win.bgpic("space_invaders_background.gif")

# Register the graphics for the game
win.register_shape("invader.gif")
win.register_shape("player.gif")
win.register_shape("red_enemy.gif")  # Το κόκκινο διαστημόπλοιο


# Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pensize(3)
border_pen.pendown()
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

# Set the score to 0
score = 100  # Άλλαξα το σκορ από 0 σε 100

# Draw the score on stage
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 280)
score_string = "Score: {}".format(score)
score_pen.write(score_string, False, align="left", font=("Arial", 14, "bold"))
score_pen.hideturtle()

# Create the player turtle
player = turtle.Turtle()
player.color("blue")
player.shape("player.gif")
player.speed(0)
player.penup()
player.setposition(0, -250)
player.setheading(90)
player.speed = 15

# Choose number of enemies
number_of_green_enemies = 4  # 'Άλλαξα τον αριθμό των πράσινων διαστημόπλοιων από 5 σε 4

# Create an empty list of enemies
green_enemies = []
red_enemies = []  # Δημιούργησα μια κενή λίστα για τα κόκκινα διαστημόπλοια

# Add enemies to the list
# We need to create more turtle objects

for i in range(number_of_green_enemies):
    # Create the enemy
    green_enemy = turtle.Turtle()
    green_enemy.speed(0)
    green_enemy.shape("invader.gif")
    green_enemy.color("green")
    green_enemy.penup()
    x = random.randint(-200, 200)
    y = random.randint(100, 200)
    green_enemy.setposition(x, y)
    green_enemy.velocity = random.randint(1, 3)  # Τυχαία ταχύτητα των πράσινων διαστημόπλοιων
    green_enemies.append(green_enemy)

# Create the player's bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.speed(0)
bullet.penup()
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.goto(0, -400)  # Στέλνω τη σφαίρα έξω από το παράθυρο γιατί ακόμα και κριμένο,
bullet.hideturtle()  # όταν ήταν στο κέντρο και ερχόταν σε επαφή με διαστημόπλοιο το σκότωνε και μετρούσε στο σκορ
bullet_speed = 20

# Define bullet state
# we have 2 states:
# ready - ready to fire bullet
# fire - bullet is firing

bullet_state = "ready"


# Move the player left and right
def move_left():
    player.direction = 'left'
    player.speed = -15


def move_right():
    player.direction = 'right'
    player.speed = 15


def move_player():
    x = player.xcor()
    x += player.speed
    if x < -280:
        x = -280
    if x > 280:
        x = 280
    player.setx(x)


def fire_bullet():
    # Declare bullet_state as a global if it needs change
    global bullet_state
    if bullet_state == "ready":
        winsound.PlaySound("laser.wav", winsound.SND_ASYNC)

        # Move the bullet to just above the player
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()
        bullet_state = "fire"


def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if distance < 15:
        return True
    else:
        return False


# create keyboard bindings
turtle.listen()
turtle.onkeypress(move_left, "Left")
turtle.onkeypress(move_right, "Right")
turtle.onkey(fire_bullet, "space")

# Main game loop
while True:

    win.update()

    move_player()
    if len(green_enemies) != 0:  # Αν δεν έχει αδειάσει η λίστα
        for green_enemy in green_enemies:

            # This is a forever loop
            # Move the enemy
            x = green_enemy.xcor()
            x = x + green_enemy.velocity
            green_enemy.setx(x)

            # Move enemy back and down
            if green_enemy.xcor() > 280:
                for g in green_enemies:
                    y = g.ycor()
                    y = y - 40
                    g.sety(y)
                green_enemy.velocity *= -1

            if green_enemy.xcor() < -280:
                for g in green_enemies:
                    y = g.ycor()
                    y = y - 40
                    g.sety(y)
                green_enemy.velocity *= -1

            # Check for collision between bullet and enemy
            if isCollision(bullet, green_enemy):
                winsound.PlaySound("explosion.wav", winsound.SND_ASYNC)

                # Reset the bullet
                bullet.hideturtle()
                bullet_state = "ready"
                bullet.setposition(0, -400)
                green_enemies.remove(green_enemy)  # Αφαιρεί από τη λίστα το πράσινο διαστημόπλοιο που χτύπησε η σφαίρα
                green_enemy.hideturtle()  # Κρύβει το πράσινο διαστημόπλοιο που χτύπησε η σφαίρα

                for r in range(2):  # Για κάθε πράσινο διαστημόπλοιο βάζει στη λίστα 2 κόκκινα
                    red_enemy = turtle.Turtle()  # σε τυχαία θέση και με τυχαία ταχύτητα
                    red_enemy.speed(0)
                    red_enemy.shape("red_enemy.gif")
                    red_enemy.color("red")
                    red_enemy.penup()
                    x = random.randint(-200, 200)
                    y = random.randint(100, 200)
                    red_enemy.setposition(x, y)
                    red_enemy.velocity = random.randint(1, 3)
                    red_enemies.append(red_enemy)
                # Update the score
                score += 10
                score_string = "Score: {}".format(score)
                score_pen.clear()
                score_pen.write(score_string, False, align="left", font=("Arial", 14, "bold"))

            # Check for collision between enemy and player
            # Ελέγχει και αν το πράσινο διαστημόπλοιο περάσει στη γραμμή που είναι ο παίκτης
            if isCollision(player, green_enemy) or green_enemy.ycor() < -230:
                winsound.PlaySound("explosion.wav", winsound.SND_ASYNC)
                player.hideturtle()
                green_enemy.goto(1000, 1000)  # Έβαλα να το στέλνει έξω από το παράθυρο γιατί αν άδειαζα
                red_enemies.clear()  # και τις 2 λίστες μου έβγαζε οτι κέρδισα
                # Εμφανίζει Game over!!! και έχει ηχητικό εφέ
                game_over = turtle.Turtle()
                game_over.hideturtle()
                game_over.color("white")
                game_over.shape("circle")
                game_over.speed(0)
                game_over.penup()
                game_over.goto(0, 0)
                game_over.write("Game Over!!!", align="center", font=("Ariel", 40, "bold"))
                winsound.PlaySound("game_over.wav", winsound.SND_ASYNC)
                turtle.Screen().exitonclick()  # Με το break έκλεινε το παράθυρο. Αυτή τη λύση την είδα στο διαδίκτυο

    if len(red_enemies) != 0:  # Αν δεν έχει αδειάσει η λίστα
        for red_enemy in red_enemies:
            # This is a forever loop
            # Move the enemy
            x = red_enemy.xcor()
            x = x + red_enemy.velocity
            red_enemy.setx(x)

            # Move enemy back and down
            if red_enemy.xcor() > 280:
                for r in red_enemies:
                    y = r.ycor()
                    y = y - 40
                    r.sety(y)
                red_enemy.velocity *= -1

            if red_enemy.xcor() < -280:
                for r in red_enemies:
                    y = r.ycor()
                    y = y - 40
                    r.sety(y)
                red_enemy.velocity *= -1

            # Check for collision between enemy and player
            # Ελέγχει και αν το κόκκινο διαστημόπλοιο περάσει στη γραμμή που είναι ο παίκτης
            if isCollision(player, red_enemy) or red_enemy.ycor() < -230:
                winsound.PlaySound("explosion.wav", winsound.SND_ASYNC)
                player.hideturtle()
                red_enemy.goto(1000, 1000)  # Έβαλα να το στέλνει έξω από το παράθυρο γιατί αν άδειαζα
                green_enemies.clear()  # και τις 2 λίστες μου έβγαζε οτι κέρδισα
                # Εμφανίζει Game over!!! και έχει ηχητικό εφέ
                game_over = turtle.Turtle()
                game_over.hideturtle()
                game_over.color("white")
                game_over.shape("circle")
                game_over.speed(0)
                game_over.penup()
                game_over.goto(0, 0)
                game_over.write("Game Over!!!", align="center", font=("Ariel", 40, "bold"))
                winsound.PlaySound("game_over.wav", winsound.SND_ASYNC)
                turtle.Screen().exitonclick()  # Με το break έκλεινε το παράθυρο. Αυτή τη λύση την είδα στο διαδίκτυο

            # Check for collision between bullet and enemy
            if isCollision(bullet, red_enemy):
                winsound.PlaySound("explosion.wav", winsound.SND_ASYNC)
                # Reset the bullet
                bullet.hideturtle()
                bullet_state = "ready"
                bullet.setposition(0, -400)
                red_enemies.remove(red_enemy)  # Αφαιρεί από τη λίστα το κόκκινο διαστημόπλοιο που χτύπησε η σφαίρα
                red_enemy.hideturtle()  # Κρύβει το κόκκινο διαστημόπλοιο που χτύπησε η σφαίρα

                # Αύξηση του σκορ με 20 πόντους για κάθε κόκκινο διαστημόπλοιο
                score += 20
                score_string = "Score: {}".format(score)
                score_pen.clear()
                score_pen.write(score_string, False, align="left", font=("Arial", 14, "bold"))

    if len(green_enemies) == 0 and len(red_enemies) == 0:
        # Αν έχουν μείνει κενές και οι 2 λίστες ο παίκτης είναι νικητής. You Win!!! και ηχητικό εφέ νίκης.
        you_win = turtle.Turtle()
        you_win.hideturtle()
        you_win.color("white")
        you_win.shape("circle")
        you_win.speed(0)
        you_win.penup()
        you_win.goto(0, 0)
        you_win.write("You Win!!!", align="center", font=("Ariel", 40, "bold"))
        winsound.PlaySound("you_win.wav", winsound.SND_ASYNC)
        turtle.Screen().exitonclick()  # Με το break έκλεινε το παράθυρο. Αυτή τη λύση την είδα στο διαδίκτυο

    # Move the bullet only when bullet_state is "fire"
    if bullet_state == "fire":
        y = bullet.ycor()
        y = y + bullet_speed
        bullet.sety(y)

    # Κάθε φορά που πυροβολεί το σκορ μειώνεται κατά 1 πόντο
    if bullet.ycor() == -220:
        score -= 1
        score_string = "Score: {}".format(score)
        score_pen.clear()
        score_pen.write(score_string, False, align="left", font=("Arial", 14, "bold"))

    # Check to see if bullet has reached the top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bullet_state = "ready"
