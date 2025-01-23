import os, pickle, json
from asyncpg.pool import create_pool
from .utils import create_dummy_data
import numpy as np
from sklearn.ensemble import IsolationForest


DATABASE_URL = "postgresql://anomaly_data_owner:RhsgDvL9wP2U@ep-aged-cherry-a5zocusr.us-east-2.aws.neon.tech/anomaly_data?sslmode=require"
pool = None
MODEL_FILE = "model.pkl"
MODEL_TRAINED_FLAG = "model_trained.flag"
auth = False

async def configure_database():
    global pool
    if not auth:
            return {"error": "Unauthorized: Please authenticate first."}
    if pool is not None:
            return "Database pool is already created."
    try:
        pool = await create_pool(DATABASE_URL)
        return {"database_config_status":"Database pool created successfully","pool":pool}
    except Exception as e:
        return f"Error creating database pool: {str(e)}"

async def get_auth(api_key):
    global auth
    global pool
    
    async def get_db_connection():
        return await pool.acquire()
    
    async def release_db_connection(conn):
        await pool.release(conn)
        
    try:
        if pool is None:
            pool = await create_pool(DATABASE_URL)
            
        conn = await get_db_connection()

        query = '''
            SELECT email, username 
            FROM users 
            WHERE api_key = $1
        '''
        result = await conn.fetchrow(query, api_key)
        if result:
            auth = True
            return {
                "auth_status": "Authentication Success",
                "email": result["email"],
                "name": result["username"]
            }
        else:
            raise Exception("Authentication Failed: API Key not found")
    except Exception as e:
        return {"auth_status": "Authentication Failed", "error": str(e)}

    finally:
        await release_db_connection(conn)
        pool = None
        

        

async def logout():
    """Log out the user and reset authentication."""
    global auth
    auth = False
    if pool is not None:
        await pool.close()
    return {"message": "Logout successful. Authentication status reset."}



    

async def reset_model():
    if not auth:
        return {"error": "Unauthorized: Please authenticate first."}
    try:
        if os.path.exists(MODEL_FILE):
            os.remove(MODEL_FILE)
        if os.path.exists(MODEL_TRAINED_FLAG):
            os.remove(MODEL_TRAINED_FLAG)
        if not os.path.exists(MODEL_FILE):
            model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
            with open(MODEL_FILE, "wb") as f:
                pickle.dump(model, f)
        return {"message": "Model has been reset successfully."}
    except Exception as e:
        return {"error": f"Error resetting the model: {str(e)}"}
    
async def database_reset():
    if not auth:
        return {"error": "Unauthorized: Please authenticate first."}
    async def get_db_connection():
        return await pool.acquire()

    async def release_db_connection(conn):
        await pool.release(conn)
    try:
        conn = await get_db_connection()
        await conn.execute("DELETE FROM public.anomaly_data WHERE id >= 0")
        await conn.execute("ALTER SEQUENCE anomaly_data_id_seq RESTART WITH 1")
        return {"message": "Database has been reset successfully."}
    except Exception as e:
        raise Exception(status_code=500, detail=f"Error resetting the database: {e}")
    finally:
        await release_db_connection(conn)
        
async def get_database():
    if not auth:
        return {"error": "Unauthorized: Please authenticate first."}
    async def get_db_connection():
        return await pool.acquire()

    async def release_db_connection(conn):
        await pool.release(conn)
    try:
        conn = await get_db_connection()
        rows = await conn.fetch("SELECT * FROM anomaly_data")
        data = [dict(row) for row in rows]
        return {"data": data}
    except Exception as e:
        raise Exception(status_code=500, detail=f"Error fetching database: {e}")
    finally:
        await release_db_connection(conn)
        

async def feed_model(data,pool, batch_size=10):
    if not auth:
        return {"error": "Unauthorized: Please authenticate first."}
    async def get_db_connection():
        return await pool.acquire()

    async def release_db_connection(conn):
        await pool.release(conn)

    async def fetch_training_data():
        try:
            conn = await get_db_connection()
            rows = await conn.fetch('''SELECT typing_frequency_email,typing_frequency_password, keypress_duration_email,keypress_duration_password, 
                                field_interaction_time_mail, field_interaction_time_password, 
                                login_submission_time, mouse_movement_pattern, mouse_or_tab FROM anomaly_data''')
        
            data = np.array([[
                row['typing_frequency_email'],
                row['typing_frequency_password'],
                row['keypress_duration_email'],
                row['keypress_duration_password'],
                row['field_interaction_time_mail'],
                row['field_interaction_time_password'],
                row['login_submission_time'],
                row['mouse_movement_pattern'],
                row['mouse_or_tab']
            ] for row in rows])
            return data
        except Exception as e:
            raise Exception(f"Error fetching data: {e}")
        finally:
            await release_db_connection(conn)

    try:
        if pool is None:
            raise Exception("Error: Database pool is not created.")
        try:
            parsed_data = json.loads(data)
        except json.JSONDecodeError as e:
            raise Exception(f"Provided data is not a valid JSON: {e}")

        if not parsed_data or not isinstance(parsed_data, dict):
            raise Exception("The data is empty or not a valid JSON object.")

        required_fields = [
            'typing_frequency_email', 'typing_frequency_password', 'keypress_duration_email', 'keypress_duration_password',
            'field_interaction_time_mail', 'field_interaction_time_password', 'login_submission_time', 
            'mouse_movement_pattern', 'mouse_or_tab'
        ]
        
        missing_fields = [field for field in required_fields if field not in parsed_data]
        if missing_fields:
            raise Exception(f"Missing required fields in data: {', '.join(missing_fields)}")

        conn = await get_db_connection()
        response_message = ""

        if os.path.exists(MODEL_TRAINED_FLAG):
            with open(MODEL_FILE, "rb") as f:
                model = pickle.load(f)

            input_data = np.array([[
                parsed_data['typing_frequency_email'],
                parsed_data['typing_frequency_password'],
                parsed_data['keypress_duration_email'],
                parsed_data['keypress_duration_password'],
                parsed_data['field_interaction_time_mail'],
                parsed_data['field_interaction_time_password'],
                parsed_data['login_submission_time'],
                parsed_data['mouse_movement_pattern'],
                parsed_data['mouse_or_tab']
            ]])

            prediction = model.predict(input_data)
            is_anomaly = str(prediction[0])

            if is_anomaly == "-1":
                response_message = "Anomaly detected. Data not stored."
                return {"message": response_message, "is_anomaly": is_anomaly}

        query = '''
            INSERT INTO anomaly_data (
                typing_frequency_email, typing_frequency_password, keypress_duration_email, keypress_duration_password,
                mouse_or_tab, field_interaction_time_mail,
                field_interaction_time_password, login_submission_time,
                mouse_movement_pattern
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9) RETURNING id;
        '''
        data_id = await conn.fetchval(query,
                                      parsed_data['typing_frequency_email'],
                                      parsed_data['typing_frequency_password'],
                                      parsed_data['keypress_duration_email'],
                                      parsed_data['keypress_duration_password'],
                                      parsed_data['mouse_or_tab'],
                                      parsed_data['field_interaction_time_mail'],
                                      parsed_data['field_interaction_time_password'],
                                      parsed_data['login_submission_time'],
                                      parsed_data['mouse_movement_pattern'])

        if data_id >= batch_size and data_id % batch_size == 0:
            training_data = await fetch_training_data()
            dummy_data = create_dummy_data(training_data)

            combined_data = np.vstack([training_data, dummy_data])
            model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)

            model.fit(combined_data)
            with open(MODEL_FILE, "wb") as f:
                pickle.dump(model, f)
            with open(MODEL_TRAINED_FLAG, 'w') as f:
                f.write("Model has been trained.")
            response_message = "Model Trained Successfully!"

        if not response_message:
            response_message = "No Anomaly detected"

        if os.path.exists(MODEL_TRAINED_FLAG):
            return {"message": response_message, "is_anomaly": "1", "data_id": data_id}

        response_message = "Collecting training data!"
        return {"message": "Training Phase, Data Stored", "is_anomaly": "0", "data_id": data_id}

    except Exception as e:
        raise Exception(f"Error saving data: {e}")
    finally:
        await release_db_connection(conn)
