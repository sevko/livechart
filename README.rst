livechart
==========

A command-line utility for rendering quick-and-dirty graphs of STDIN input.

.. figure:: https://cloud.githubusercontent.com/assets/4467604/6364493/ce8e79d0-bc74-11e4-8da2-156426b6d936.png
   :alt: Some sample graphs generated with livechart.

installation
~~~~~~~~~~~~

Tested against Python 2.7.

::

    sudo pip install livechart

usage
~~~~~

Pipe lines containing either JSON-serialized objects or numbers into
``livechart``; the data *must* be consistent for the duration of usage. Input
like ``{"a": 1, "b": 3, "c": 5}`` will result in three graphs, while ``1.00``
will plot just one.

::

    some_script | livechart

Run ``livechart --help`` for all configuration options.
