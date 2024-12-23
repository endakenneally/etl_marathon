from flask import Blueprint, jsonify, request
from sqlalchemy import create_engine
import pandas as pd

# Create a Flask Blueprint
api_blueprint = Blueprint('api', __name__)

# Database connection string using SQLAlchemy's create_engine
engine = create_engine(
    "postgresql+psycopg2://etl_user:etl_password@etl_db:5432/etl_db")


# Define API routes


@api_blueprint.route('/get_data', methods=['GET'])
def get_data():
    try:
        # Parameters
        limit = request.args.get('limit', default=100, type=int)

        # Query the database
        query = f'SELECT * FROM public.um_data LIMIT {limit}'

        with engine.connect() as conn:
            df = pd.read_sql(query, conn.connection)

        # Convert DataFrame to a list of dictionaries and return as JSON
        return jsonify(df.to_dict(orient="records"))

    except Exception as e:
        # Catch any exceptions and return a meaningful error response
        return jsonify({"error": str(e)}), 500


@api_blueprint.route('/get_batch_data', methods=['GET'])
def get_batch_data():
    try:
        # Parameters
        limit = request.args.get('limit', default=100, type=int)
        offset = request.args.get('offset', default=0, type=int)

        # Query the database
        query = f'SELECT * FROM public.um_data LIMIT {limit} OFFSET {offset}'

        with engine.connect() as conn:
            df = pd.read_sql(query, conn.connection)

        # Convert DataFrame to a list of dictionaries and return as JSON
        return jsonify(df.to_dict(orient="records"))

    except Exception as e:
        # Catch any exceptions and return a meaningful error response
        return jsonify({"error": str(e)}), 500


@api_blueprint.route('/get_count', methods=['GET'])
def get_summary():
    try:
        # Query to get the total number of records
        query = 'SELECT COUNT(*) AS total_records FROM public.um_data'

        # Execute the query using SQLAlchemy
        with engine.connect() as conn:
            result = conn.execute(query).fetchone()

        # Return the result as JSON
        return jsonify({"total_records": result["total_records"]})

    except Exception as e:
        # Catch any exceptions and return a meaningful error response
        return jsonify({"error": str(e)}), 500


@api_blueprint.route('/get_cleaned_data', methods=['GET'])
def get_cleaned_data():
    try:
        # Parameters
        limit = request.args.get('limit', default=100, type=int)

        # Query the database
        query = f'SELECT * FROM public.cleaned_data LIMIT {limit}'

        with engine.connect() as conn:
            df = pd.read_sql(query, conn.connection)

        # Convert DataFrame to a list of dictionaries and return as JSON
        return jsonify(df.to_dict(orient="records"))

    except Exception as e:
        # Catch any exceptions and return a meaningful error response
        return jsonify({"error": str(e)}), 500
