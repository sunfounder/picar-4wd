Python Program Control
============================

Python Example Program is in the examples folder. 

.. code-block:: python

    cd /home/pi/picar-4wd/examples

You can run them by using Python3.

keyboard_control.py
---------------------

After running the example, press「W」, 「A」, 「S」, 「D」, and you can get the car going ahead, back, left, right. And the keys「4」and「6」can increase or decrease the power of the motor.

Run it by using the following command.

.. code-block:: python

    python3 keyboard_control.py

obstacle_avoidance.py
------------------------

After running the example, the car goes ahead automatically.

It can also turn right to get around the obstacles if there is anything obstructive ahead.

.. code-block:: python

    python3 obstacle_avoidance.py

track_line.py
---------------

If you paste a black lane (width: around 2.5cm) on the white floor, the car will move along the lane. 

.. code-block:: python

    python3 track_line.py

follow.py
-----------

When the example runs, the car will follow the object ahead.

.. code-block:: python

    python3 follow.py

