import os
import sys
import json
import warnings
from glob import glob
from collections import OrderedDict
from pprint import pprint
from typing import Text, List, Dict, Tuple, Optional, Union
warnings.filterwarnings("ignore")

import fire

from sqlalchemy import create_engine
import pandas as pd
from tqdm.auto import trange, tqdm

# Language Detector
from seqtolang import Detector

# Composer
from haystack import BaseComponent, Pipeline

# Schema
from haystack.schema import Document

# Nodes
## Translator
from haystack.nodes import TransformersTranslator, TransformersDocumentClassifier

## Sentiment Analysis
from haystack.nodes import TransformersDocumentClassifier

# Disable Telemery
from haystack.telemetry import disable_telemetry
disable_telemetry()

# Environment Configurations
os.environ['HAYSTACK_TELEMETRY_ENABLED'] = "False"
os.environ['ENDPOINT'] = "database-1.c0tbaqotqgli.us-west-1.rds.amazonaws.com"
os.environ['USER'] = "admin"
os.environ['PASS'] = "adminadmin"
os.environ['DATABASE'] = "database-1"