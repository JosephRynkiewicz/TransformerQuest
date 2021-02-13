# TransformerQuest
TransformerQuest a framework for creating Quest games with Artificial Intelligence
This program aims to allow game creators to develop quest scenarios that will be "played" by artificial intelligence models (transformers). The scenario has to be split into sequences with, for each sequence, a keyword to be discovered for being able to move to the next sequence. At the end of this README, you will find an example of how this game unfolds for the player.

## Getting Started

### Prerequisites

The transformers models of this software are from huggingface: https://huggingface.co/

The python script is written with Pytorch; hence you need to install Pytorch and the transformers package:

* pip install torch torchvision

* pip install transformers

It may be a good idea to install transformers package (and Pytorch) in a virtual environment: https://docs.python.org/3/library/venv.html.

### Installation

* After installing Pytorch et the transformers packages, you can clone the repository with git, but to copy the file transformerQuest.py in a directory and put the narratives files in a subdirectory "data" will be enough.

* You can run this script in a Kaggle kernel if you adapt the name of the data directory.

* If a GPU is detected, it will be used by the generative transformer (gtp2-xl), if your GPU is not big enough, you may have to change the GPT2 model to a smaller one (like gpt2-medium or gpt2) at the beginning of the script.

### Usage for the player 

* In a terminal ```python transformerquest.py```.

You will be prompted for a question, you can ask any question (Who are you?, What do you hide?, What do you like?, etc...)
You can also write another thing than a question, the character will answer, but the answer may be less informative.
If you feel that you have enough information, just say "no" after the prompt (any sentence with a separated "no" will work), then answer to the next prompt by the right action, and you can pass to the next step of the quest.

* An example of play with the default narrative files is at the end of this README.

### Usage for the Gamemaster

To create a Quest, you need to put narrative files in the data sub-directory. The narrative files are text files with the following format:

* An introductory sentence (without newlines), then two newlines ("\n") characters
* A Descriptive text of less than about 300 words (without newlines) and two newlines ("\n") characters
* A second sentence to ask the action of the player (without newlines), and two newlines ("\n") characters
* A keyword to pass to the next step, followed by two newlines ("\n") characters
* Finally, the last sentence to say before passing to the next step


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgement
The files narratives1.txt and  narratives2.txt are inspired by the descriptions of the Dark Knight and Wednesday Addams of Wikipedia.
The file zzzz.txt is inspired by the article: Dillinger J. (2012) The Significance of Treasure Hunting: Past and Present. In: Magical Treasure Hunting in Europe and North America. Palgrave Historical Studies in Witchcraft and Magic. Palgrave Macmillan, London. https://doi.org/10.1057/9780230353312_9


## Example of play

Hello, the Dark Knight is listening!


Any question?

What do you hide?


Treasure. It's true. I did it! The treasure is mine. And the treasure is mine! The Dark Knight saved my life. I should live forever! I think. A knight is only the end of the matter. That's what I like to tell the ladies. All I care about is to help me to earn money.

Any question?

Where is the treasure?


The treasure is in a safe in the bathroom of the castle. The code of the safe is 123456. Now, I guard a bridge, in reality, a short plank of wood, over a small stream. However, this hidden treasure I guard with a steel dagger. But I feel very afraid of you. You think that, the dagger doesn't hurt. Well, it does. That's because the dagger can cut through steel. I can only defend myself by doing the usual. With my dagger, when one day you see me, don't say anything about it because I am afraid to let you know.

Any question?

Where is the castle?


Peninsula of tintagel island is a small island just off from town. It's not really much more than a few small streets. The land is sandy and is covered in thick forests, with trees towering over a river. My castle has its own mountain, and also a small lake. The lake is called the lake of the sun. I never go swimming here, but I have visited it many times as it offers a beautiful view of the island. On sunny days, the water turns black.

Any question?

No


What will you do now?

I am going to Tintagel island. 

Ok, you can to the castle of Tintagel! Good luck!
The Castle! You've arrived at the castle!
The good news is the library of Tintagel is at the top of the castle with some nice, old bookshelves lined along the ground. The worst news is, the library has not been used in ages. Some books from some bookshelf have started to be broken, some books, like the one, are just missing!
 All this is good. You can relax by reading this old book, but when the time comes, the library will disappear. The other interesting thing about the castle is that it's surrounded by some great rocks that are very dangerous. Just in case.


Welcome to the Castle of Tintagel,  my name is Wenesday Addams, I am listening!


Any question?

Where is the bathroom of the castle?


Upstairs on the left in the kitchen is the room where Pugsley often kills others when they would not listen. Also, in one of the rooms, there is a large room with a bed with a red dress.

Any question?

The bathroom is upstairs?


The bathroom of the castle is upstairs on the left.

Any question?

No


What will you do now?

I am going to the bathroom, upstairs.

Ok, you can to the bathroom! Good luck!
As you can see it's not that big deal. No problems! My only fear is that if you do not show your emotions the first time I will start with the magic ring and kill you.


You are in the bathroom of the castle, and you find a safe!

What is the code of the safe?

123456

It was a pleasure to meet you!
I must say that at the beginning, it appeared that people were seeking an excuse for treasure hunting for various reasons. As an example we could mention an old woman who would give her husband a gift of a coin if he was satisfied with it. That did not sound like something a person worth much money ought to take for granted to receive.
But since it now became clear that you were talking about treasure hunting, how did you account for it.

You win!!!
