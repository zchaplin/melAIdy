# melAIdy

Final project for CMPM146 (Game AI) by Miles Berman, Mika Peer Shalem, Zane Chaplin, Lance Dennison

<b> AI melody and chord generator </b> <br>
Our project combines different AI technologies to generate MIDI data on the fly. Through the use of graph structures, weighted connections, and even a basic machine learning model, we successfully produce sonically pleasing and musically logical notes. Our product can also simultaneously generate chords and melodies and can even influence chords based on melodies and vice versa.

# How to run the code?

## Graph Generator

Running graph.py would print out the chosen notes based on our huristics and play the generated song! <br>

## Machine Learning

<i> Training and testing data were taken from: https://github.com/music-x-lab/POP909-Dataset <br>
`@inproceedings{pop909-ismir2020,
    author = {Ziyu Wang* and Ke Chen* and Junyan Jiang and Yiyi Zhang and Maoran Xu and Shuqi Dai and Guxian Bin and Gus Xia},
    title = {POP909: A Pop-song Dataset for Music Arrangement Generation},
    booktitle = {Proceedings of 21st International Conference on Music Information Retrieval, {ISMIR}},
    year = {2020}
}` </i>

In your terminal, move to the `chords` directory, and type `python model.py`
It will print out the converted datasets, compile the model, print the generated chords/notes, and play the completed song!
