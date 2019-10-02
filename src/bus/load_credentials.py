import os
import json


class LoadCredentials:
    """
    Loads the webgenesis credentials and bus credentials from environment variables.

    If environment vars are not found then attempt to load from local files.
    """
    _api_key_env = "SECRET_MH_API_KEY"
    _kafka_brokers_sasl_env = "SECRET_MH_BROKERS"

    @staticmethod
    def load_bus_credentials():
        """
        Load the values from environment variables
        if they cannot be found on environment try to load from local file "bus_credentials.json"

        :return: dictionary with keys ['api_key', 'kafka_admin_url', 'kafka_brokers_sasl']
        """
        cred = dict()

        try:
            cred['api_key'] = os.environ[LoadCredentials._api_key_env]
            cred['kafka_brokers_sasl'] = os.environ[LoadCredentials._kafka_brokers_sasl_env]
            cred['kafka_brokers_sasl'] = cred['kafka_brokers_sasl'].split(',')
        except:
            # If failed reading the env vars, then try to load the values from the local file (as was previously)
            bus_cred_file = "bus_credentials.json"
            print("Loading values form file instead:" + bus_cred_file)
            with open(bus_cred_file) as f:
                return json.load(f)

        return cred



if __name__ == "__main__":
    crebus = LoadCredentials.load_bus_credentials()
    print("credentials loaded")
