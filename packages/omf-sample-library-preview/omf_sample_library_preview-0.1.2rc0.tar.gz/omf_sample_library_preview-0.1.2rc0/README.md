# OMF Python Library Sample

**Version:** 0.1.2_preview

This sample library requires Python 3.7+. You can download Python [here](https://www.python.org/downloads/).

## About the library

The python OMF library is an introductory language-specific example of writing OMF Messages against OMF endpoints. It is intended as instructional samples only and are not for production use.

The library can be obtained by running: `pip install omf_sample_library_preview`

Other language libraries and samples are available on the [AVEVA GitHub Organization](https://github.com/AVEVA).

## Testing

The library is tested using PyTest. To test locally, make sure that PyTest is installed, then navigate to the Tests directory and run the test classes by executing 
```
python -m pytest {testclass} 
```

where {testclass} is the name of a test class, for example ./test_omfclient.py. 

Optionally to run end to end tests, rename the appsettings.placeholder.json file to appsettings.json and populate the fields, (This file is included in the gitignore and will not be pushed to a remote repository), then run 
```
python -m pytest {testclass} --e2e True
```

## Logging

Every request made by the library is logged using the standard [Python logging library](https://docs.python.org/3/library/logging.html). If the client application using the library creates a logger, then library will log to it at the following levels:

| Level | Usage                                                                                                                      |
| ----- | -------------------------------------------------------------------------------------------------------------------------- |
| Error | any non 200-level response code, along with the error message                                                              |
| Info  | all request urls and verbs <br/> all response status codes                                                                 |
| Debug | data payload and all request headers (Authorization header value redacted) <br/> response content and all response headers |

The process for creating a logger is described in the [Logging HOWTO documentation](https://docs.python.org/3/howto/logging.html).

An example walkthrough is shown here:

### Logger Creation Example

To initiate logging, the client must create a logger, defining a log file, a desired log level, and default formatting:

```python
    # Step 0 - set up logger
    log_file = 'logfile.txt'
    log_level = logging.INFO
    logging.basicConfig(filename=log_file, encoding='utf-8', level=log_level, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)s %(module)16s,line: %(lineno)4d %(levelname)8s | %(message)s')
```

This creates a logger object that streams any logged messages to the desired output. The libraries called by the client, including this `ADH Sample Library Python`, that have implemented logging will send their messages to this logger automatically.

The [log level](https://docs.python.org/3/library/logging.html#logging-levels) specified will result in any log at that level _or higher_ to be logged. For example, `INFO` captures `INFO`, `WARNING`, `ERROR`, and `CRITICAL`, but ignores `DEBUG`.

### Logger Usage Example

To change the log level after creation, the level can be set using the following command

```python
logging.getLogger().setLevel(logging.DEBUG)
```

This concept is particularly helpful when debugging a specific call within the application. Logging can be changed before and after a call to the library in order to provide debug logs for that specific call only, without flooding the logs with debug entries for every other call to the library.

An example of this can be seen here.

```python
    # Step 4 - Retrieve the data view
    original_level = logging.getLogger().level
    logging.getLogger().setLevel(logging.DEBUG)

    container_service.createContainers(omf_containers)

    logging.getLogger().setLevel(original_level)
```

Note that the original level was recorded, logging was set to debug, the `createContainers` call was performed, then logging was set to its previous level. The logs will contain debug message for only this call, and all other calls before and after will be logged with their original level.

---

Developed using Python 3.10.1

For the main AVEVA samples page [ReadMe](https://github.com/AVEVA)
