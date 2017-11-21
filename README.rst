PLaYTeX
=======

Render Python objects in LaTeX documents

Basic usage
-----------
Create a playtex-player.yaml file and use the playtex package in your
LaTeX document.

playtex-player.yaml files look something like this:

.. code-block:: yaml
    
    my_player_name:
        play: entry.point:specifier
        requires:
            keyword_arg: relative/path/to/file.dat
            another: {kind: 'module', name: 'local.dep'}

The ``requires`` allow the cache to be automatically invalidated when
requirements are updated in cache mode.

The play function specified by ``play`` can return any Python object.
In your latex document, you'll want to render it.  For example, if your
``play`` function returns a matplotlib figure, use
``\PlaytexMatplotlib{my_player_name}``

See the example for more info.
