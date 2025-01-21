# tw-django-base-library

This library will help you speed your development time here at Techwalnut innovations LLP. You will get all the standard formats and conventions required in this library. You can read about the code in the tw-django-reference shared with you.  

---

## Features

- **Standard model**: Covers the base model and default queryset, object managers and mandatory fields required.
1. Base
- **Pre-configured admin**: All the mandatory and necessary configuration for any admin panel are available here 
1. AdminLogging
2. ApplicationLogging
- **Some common utilities**: Common utility function are available here. 
1. APIPaginatorParams

---

## Installation

Install the library via pip:

```bash
pip install tw-django-base-library
```

## Setup
Add the app in your installed app in settings.py

```bash
INSTALLED_APPS = [
    ...,
    'django_base_library',
    ...
]
```

To import the the base models 
```bash
from django_base_library.models import Base
```

To import the default admin classes
```bash
from django_base_library.admin import AdminLogging, ApplicationLogging
```

To import the utilities
```bash
from django_base_library.utilities import APIPaginatorParams
#You can import any class/function from the available classes/functions
```
