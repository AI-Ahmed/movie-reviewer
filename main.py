from utils import *
from pipeline import *

# Initialize pipeline
pipe = MovieSentimentReviewsPipeline()

def config_func(filename: Text,
                output_path: Optional[Text]=None) -> None:
  """
  | This function is responsible for reading the `JSON` file from the user
    and sending it to the pipeline for getting the predictions,
    once it gets the predictions it starts to save it in 2 options;
    saving the output in the `JSON` file if the user added `output_path`,
    otherwise it will save the predictions in RDS if it is available to connect with it!
  Args:
    filename [Text]: `JSON` file of the batch data.
    output_path Optional[Text]: if the user insert it, the user wants to save the output predictions, locally | Default: None
  """
  def to_dict(documents: Dict[Text, List[Document]]) -> Dict[Text, Text]:
    """
    | Convert dictionary of list of Documents into batched dictionary
    
    Args:
      documents [Dict[Text, List[Document]]]: output predictions from the pipeline.
    Returns:
      Dict[Text, Text]
    """
    data = OrderedDict()
    for doc in documents['documents']:
      for key, value in doc.to_dict().items():
        data.setdefault(key, []).append(value)
    # Change the key name to translated text
    data['translated_text'] = data.pop('content')
    data.move_to_end('translated_text', last=False)
    return dict(data)
  
  ## =========================================================================== ##
  def to_rds(data: pd.DataFrame) -> None:
    """
    | responsible for saving the data into RDS

    Args:
      data [pd.DataFrame]: output formalized predictions.

    Returns:
      None
    """
    print(" Store Values in RDS Database ".center(100, "="))
    Database_endpoint = os.environ['ENDPOINT']
    Username = os.environ['USER']
    Password = os.environ['PASS']
    database = os.environ['DATABASE']
    try:
      # Create an Engine
      db_data = f'mysql+mysqldb://{Username}:{Password}@{Database_endpoint}:3306/{database}?charset=utf8mb4'
      engine = create_engine(db_data)
      # try:
      #   print("Connecting to "+Database_endpoint)
      #   db = pymysql.connect(host=Database_endpoint,
      #                        port=int(3306),
      #                        user=Username,
      #                        passwd=Password,
      #                        db=database,
      #                        charset="utf8mb4",
      #                        connect_timeout=int(60))
      #   cursor = db.cursor()
      #   print ("Connection successful to "+Database_endpoint)
      # except Exception as e:
      #   print ("Connection unsuccessful due to "+str(e))
      data.to_sql('movie_reviews_predictions', 
                  con=engine,
                  if_exists='append',
                  index=False)
      engine.dispose()
    except Exception as e:
      print(f"Can't connect with RDS, Error: {e}")
      pass
    else:
      print(" Successfully Saved Movie Reviews in RDS ".center(100, "="))

  ## =========================================================================== ##
  batch_data = json.load(open(filename, 'r'))
  df = pd.DataFrame.from_dict(batch_data)
  detector = Detector()

  en_list_of_docs = []
  dutch_list_of_docs = []
  fra_list_of_docs = []

  list_of_docs = []

  for index in trange(len(df), desc='Detecting Language'):

    review_text = df.loc[index, 'review_text']
    languages = detector.detect(review_text, aggregated=True)
    lang_primary_type = languages[0][0]

    df.loc[index,'language'] = lang_primary_type

  for index in trange(len(df), desc='Building the Documents'):
    if df.loc[index, 'language'] == 'eng':
      en_list_of_docs.append(Document(content=df.loc[index, 'review_text'],
                                      meta=df.loc[index, :].to_dict()))
    elif df.loc[index, 'language'] == "deu" or df.loc[index, 'language'] == "nld":
      dutch_list_of_docs.append(Document(content=df.loc[index, 'review_text'],
                                      meta=df.loc[index, :].to_dict()))
    elif df.loc[index, 'language'] == 'fra':
      fra_list_of_docs.append(Document(content=df.loc[index, 'review_text'],
                                      meta=df.loc[index, :].to_dict()))
  
  for document in tqdm([en_list_of_docs, dutch_list_of_docs, fra_list_of_docs], desc='Deploy pred'):
    list_of_docs.append(to_dict(pipe.run(documents=document)))
  
  # Printing the values
  # pprint(list_of_docs, indent=2)
  
  if output_path:
    # Save the file
    with open(os.path.join(output_path, 'prediction_metadata.json'), 'w') as json_file:
      json.dump(list_of_docs, json_file, indent=2)
  else:
    # Write to RDS
    to_rds(pd.DataFrame.from_dict(list_of_docs))

  print(' Successfully saved data '.center(100, '='))
  

if __name__ == "__main__":
  fire.Fire(config_func)