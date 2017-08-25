# Setting Up Logging

*rwci.py* logs errors and debug information via the [logging](https://docs.python.org/2/library/logging.html) python module. It is strongly recommended that the logging module is configured, as no errors or warnings will be output if it is not set up. Configuration of the `logging` module can be as simple as:

```py
import logging

logging.basicConfig(level=logging.INFO)
```

Placed at the start of the application. This will output the logs from discord as well as other libraries that uses the `logging` module directly to the console.

The optional `level` argument specifies what level of events to log out and can any of `CRITICAL`, `ERROR`, `WARNING`, `INFO`, and `DEBUG` and if not specified defaults to `WARNING`.

More advance setups are possible with the `logging` module. To for example write the logs to a file called `rwci.log` instead of outputting them to to the console the following snippet can be used:

```py
import rwci
import logging

logger = logging.getLogger('rwci')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='rwci.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
```

This is recommended, especially at verbose levels such as `INFO`, and `DEBUG` as there are a lot of events logged and it would clog the stdout of your program.

For more information, check the documentation and tutorial of the [logging](https://docs.python.org/2/library/logging.html) module.
