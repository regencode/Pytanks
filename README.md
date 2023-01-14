# Pytanks - a top down survival shooter inspired by diep.io


## Brief Description

Pytanks is a endless top-down shooter where you control the player using WASD keys and the mouse. The goal is to survive as long as you can, with increasing difficulty and harder enemies as you stay alive for longer. Level up and collect buffs dropped by enemies in order to upgrade your damage, fire rate, bullet speed and movement speed.


---

## Use-case Diagram

UPLOAD IN GITHUB

---
## Activity Diagram

UPLOAD IN GITHUB

---
## Class Diagram – name of the class, multiplicities and relationships

UPLOAD IN GITHUB

---
## Modules


### Pygame

Pygame is a wrapper for SDL (which is a graphics library), which means that it allows calling SDL functions through the pygame module. However, pygame also has its own functions to help with video game development. 

Pygame allows us to create a window where we can place images - or "surfaces" - inside that window. It has other built-in functionalities that helps in game development, such as the Vector and the Sprite submodules, and the built-in collision dectector function.

### Random

Random is a module that provides randomizers. The most important functions for my game in this module are "randint" and "choice". Randint picks a random integer inside a defined range, and Choice returns a random element of the inputted array/sequence.

### Sys

sys is a module that allows us to call system functions. The most important function in this module that I used in my game is "sys.exit()", which stops the Pytanks program when that function is called.

---
## Essential algorithms

### Game loop

The game loop is a forever loop where various important functions such as sprite updates and screen updates are called. The game surely would not run without it, which makes it an important algorithm for this game.

### World generation

Pytanks use a world generation system in order to create a large map/world from small tiles. How the world generation works is that the world layout is defined as a 2D array in world.py:

---Screenshot of 2D array - 

After that, in camera.py, the code will iterate over every element in the 2D array by using two for loops (one for x pos, the other for y pos). Then the top left of the tiles' rect will be placed on the screen, with a spacing equal to the width/height of the tile to the next tile in the row/column respectively. The tiles are offseted by a negative value in order to position the topleft of the world further to the topleft (so that the player starts in the middle of the world). All of the tiles are stored in a sprite group, which makes it easy to iterate and draw them in the custom_draw() method, which is an important method for the player-follow camera which is explained in the next section.


### Player-follow camera

In camera.py, there are two methods for the player-follow camera, which are center_target_camera() and custom_draw(). The center_target_camera() function will always place the target on the middle of the screen even while it moves, and it also determines the offset vector which is used to move the other sprites with respect to the movement of the centered sprite.

The way custom_draw() works is that we take the position of a sprite, and move it in the opposite direction of the player's movement, which is why we subtract the positions of other sprites' rect with the offset. Therefore, for example, when the player moves to the right, the offset will be positive in the x direction. By subtracting the x pos of the other sprites with the positive x value, the other sprites will be moving in the negative x direction (to the left). This same principle applies to when the player moves in the y direction, in the "negative" direction, diagonally, etc.


### Player rotation

The way the player rotation works is defined inside the rotateSelf() method in player.py. In order to make this work, I made a copy of the player's original image and store it inside an attribute named self.original_image, which would be useful as a reference of the player's original image for the rotation. 

Firstly, we get the distance from the player to the cursor as a Vector2 object. After that I used the to_polar() method of Vector2 objects on the distance vector, which converts a given vector into a magnitude and an angle.
The obtained angle is then used to rotate the original_image by its negative (because it goes the other way), and store the rotated image as self.image in order to keep the original_image unchanged. Finally we update the rect based on the new self.image.


### Simple Enemy AI

The enemy's goal is to reach the player in order to deal damage to the player. In order to create an AI that does that, I made a function that keeps track of the distance from the enemy to the player. 

Then that distance vector is normalized into a circle with a radius equal to the enemy's acceleration threshold (maximum acceleration) so that the resultant acceleration does not change much when the enemy accelerates diagonally. 

The enemy will then accelerate towards the direction where the player is relative to it based on the normalized vector. 

For the rectangle enemy, I made it so that it will fire bullets to the player's direction on a cooldown.

---
## Screenshots of your application

---
## Lessons learned/Reflection

I learned more on how to code in OOP and using the principles of OOP, such as:

- Abstraction - To create a complex method/function, such as creating the enemy acceleration-based movement system as the method "accelerate()", and making it as easy as a function call to run the code inside it, or to incorporate it into other functions. The accelerate() method is used within the moveTowards() method of the enemy class which serves as the enemy's movement AI.

- Inheritance - To get methods and attributes from a parent class, to be used in a child class. I used this principle when making the triangle and rectangle enemies, they have a lot in common so I just took the intersection of methods and attributes and made it a parent class, and the child class will contain the exclusive/different methods and attributes.

- Encapsulation - To bundle the related methods and attributes into a class, and let that class manage its own methods and attributes. For example, I handle the player input in the player class, instead of using an event loop inside the main class. Also, the player's velocity, rotation and shooting methods are only inside of the player class as those methods only concern the Player object. This is increasingly important as more and more classes are added into your program, in order to make it less confusing to build upon it and lower the risk of unintended behavior caused by variable/method conflicts.

- Polymorphism - To define a class that have the same method but with different implementation, for example, the Triangle enemy and the Rectangle enemy's update() method is different from each other. This is because the Rectangle enemy has an additional functionality that has to be added to the update() method, which is the shootBullets() method.

I also learned a lot of things about the Pygame module, as well as the nature of video games in general. Video games are basically just moving images on your screen that respond to an outside input. Pygame is mostly just a graphics library to help with rendering pixels/images on the screen, however there are built-in functions and classes that enables Pygame to be used for video game development, such as allowing user input, handling movement and collision of images, and creating vectors.

This project also made me experience creating something simple at first, and building on it more and more to make it more complex, which taught me that everything that seems complex are built with simple fundamentals. The individual functions and variables won't be able to do anything much on their own, but combine them in a specialized and structured way, and you have made a video game.