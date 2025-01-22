### PATTAN-MONGO-SURVEY

Support a surveyJS frontend with a mongodb backend.

## Configuration
    
# crete an instance of a the pattan-mongo-survey class with a dictionary containing the following keys.
1. MONGDB_USER
2. MONGDB_PASSWD
3. MONGDB_HOST
4. MONGDB_DB
5. MONGDB_SURVEY_COLLECTION - collection used to store survey questions
6. MONGDB_DB_RESPONSE_COLLECTION - collection used to store survey responses

## Documentation
[Docs](https://github.com/pattan-net/pattan-mongo-survey/tree/main/docs)

## Logging
pattan-mongo-survey creates its own logger (of the same name) which the calling application can configure.

```python
from pattan_mongo_survey import MongoSurveyService
import logging

mongo_logger = logging.getLogger('pattan_mongo_survey')
mongo_logger.addHandler(logging.FileHandler('example.log'))
mongo_logger.setLevel(logging.DEBUG)
```
