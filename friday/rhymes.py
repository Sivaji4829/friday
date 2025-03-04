import random
import speech_recognition as sr
import pyttsx3

def say_rhyme():
    rhymes = [
        "Twinkle, twinkle, little star, How I wonder what you are! Up above the world so high, Like a diamond in the sky.",
        "Jack and Jill went up the hill, To fetch a pail of water. Jack fell down and broke his crown, And Jill came tumbling after.",
        "Baa, baa, black sheep, Have you any wool? Yes sir, yes sir, Three bags full.",
        "Hickory dickory dock, The mouse ran up the clock. The clock struck one, The mouse ran down, Hickory dickory dock.",
        "Humpty Dumpty sat on a wall, Humpty Dumpty had a great fall. All the king's horses and all the king's men, Couldn't put Humpty together again.",
        "Mary had a little lamb, Its fleece was white as snow. And everywhere that Mary went, The lamb was sure to go.",
        "Ring-a-ring o' roses, A pocket full of posies, A-tishoo! A-tishoo! We all fall down.",
        "Old MacDonald had a farm, E-I-E-I-O. And on his farm he had a cow, E-I-E-I-O.",
        "Little Bo-Peep has lost her sheep, And doesn't know where to find them. Leave them alone, and they'll come home, Wagging their tails behind them.",
        "Itsy Bitsy Spider climbed up the water spout. Down came the rain and washed the spider out. Out came the sun and dried up all the rain. And Itsy Bitsy Spider climbed up the spout again."
    ]
    return random.choice(rhymes)