import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from supabase import create_client
from datetime import datetime, date
from models.model_call import call_model
import pytz  # Make sure this import is at the top of your file

# Define the timezone, for example, UTC
tz = pytz.timezone('UTC')

#Load environment varriables
load_dotenv()

# Initialize Flask App
app = Flask(__name__)
# then CORS class is used to wrap the app object to add  CORS headers to all responses from the app 
CORS(app)

app.config['DEBUG'] = os.environ.get('DEBUG')

# Import API keys
API_KEY = os.environ.get('API_KEY')
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

# then below 
supabase = create_client(supabase_url, supabase_key)

@app.route('/')
def hello():
    # here we can past inputs from the frontend to our model
    return render_template('index.html')


@app.route('/call-model', methods=['POST'])
def call_model_route():
    form_data = request.form
    print(date.today().isoformat())
    # So before we past data to call model we going to same data to supabase
    # we need to structure the data
    data_input = { 
        'inserted_at' : datetime.now(tz).isoformat(),
        'updated_at' : datetime.now(tz).isoformat(),
        'username' : 'guest_id',
        'ticker' : form_data['ticker'],
        'investment' : float(form_data['dollars']),
        'months' : form_data['num_months'],
        'iterations' : form_data['num_iter'],
    }

    # Ok then we have to create a schema in supabase 
    try:
        supabase.table('user_upload').insert(data_input).execute()
    except Exception as e:
        print("An exeption occured", e)
        return jsonify({'insert into database  failed error': str(e)})

    # Your logic here, using the form values
    model_result = call_model(API_KEY, form_data)
    
    return jsonify(model_result)


if __name__ == '__main__':
    app.run(debug=True)