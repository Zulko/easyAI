easyAI
======
    

EasyAI is an artificial intelligence framework for two-players abstract games such as Tic Tac Toe, Connect 4, Reversi, etc.

It is written in Python and makes it easy to define the mechanisms of a game and play against the computer or solve the game (see :ref:`a-quick-example`).

Under the hood, the AI is a Negamax algorithm with alpha-beta pruning and transposition tables as described on Wikipedia_. It has been written with clarity/simplicity in mind, rather than speed, so it can be slow, but there are fixes (see :ref:`speedup`).

.. raw:: html
    
    
    <a href="https://twitter.com/share" class="twitter-share-button"
    data-text="easyAI, a Python AI framework" data-size="large" data-hashtags="easyAI">Tweet
    </a>
    <script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';
    if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+'://platform.twitter.com/widgets.js';
    fjs.parentNode.insertBefore(js,fjs);}}(document, 'script', 'twitter-wjs');
    </script>
    
    <iframe src="http://ghbtns.com/github-btn.html?user=Zulko&repo=easyAI&type=watch&count=true&size=large"
    allowtransparency="true" frameborder="0" scrolling="0" width="152px" height="30px"></iframe>
    

User's Guide
--------------

.. toctree::
   :maxdepth: 1
   
   installation
   get_started
   examples/examples
   speedup
   ai_descriptions
   ref

Contribute !
-------------

EasyAI is an open source software originally written by Zulko_ and released under the MIT licence.
It is hosted on Github_, where you can submit improvements, get support, etc.

Some ideas of improvements are: AI algos for incomplete information games, better game solving strategies, (efficient) use of databases to store moves,  AI algorithms using parallelisation. Want to make one of these happen ?

.. raw:: html

        <a href="https://github.com/Zulko/easyAI">
        <img style="position: absolute; top: 0; right: 0; border: 0;"
        src="https://s3.amazonaws.com/github/ribbons/forkme_right_red_aa0000.png"
        alt="Fork me on GitHub"></a>

.. _Wikipedia: http://en.wikipedia.org/wiki/Negamax
.. _`game design`:
.. _`AI design/optimization`:
.. _Zulko : https://github.com/Zulko
.. _JohnAD : https://github.com/JohnAD
.. _Github :  https://github.com/Zulko/easyAI

Maintainers
-----------

- Zulko_ (owner)
- JohnAD_
