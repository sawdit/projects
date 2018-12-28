import adal
import flask
import uuid
import requests
# Imports the config.py where we set our Azure connection requirements
import config
import json

app = flask.Flask(__name__)
app.debug = True
app.secret_key = 'development'

PORT = 5000  # A flask app by default runs on PORT 5000
AUTHORITY_URL = config.AUTHORITY_HOST_URL + '/' + config.TENANT
REDIRECT_URI = 'https://localhost:{}/getAToken'.format(PORT)
TEMPLATE_AUTHZ_URL = ('https://login.microsoftonline.com/{}/oauth2/authorize?' +
                      'response_type=code&client_id={}&redirect_uri={}&' +
                      'state={}&resource={}')


@app.route("/")
def main():
    login_url = 'https://localhost:{}/login'.format(PORT)
    resp = flask.Response(status=307)
    resp.headers['location'] = login_url
    return resp


@app.route("/login")
def login():
    auth_state = str(uuid.uuid4())
    flask.session['state'] = auth_state
    authorization_url = TEMPLATE_AUTHZ_URL.format(
        config.TENANT,
        config.CLIENT_ID,
        REDIRECT_URI,
        auth_state,
        config.RESOURCE)
    resp = flask.Response(status=307)
    resp.headers['location'] = authorization_url
    return resp


@app.route("/getAToken")
def main_logic():
    code = flask.request.args['code']
    state = flask.request.args['state']
    if state != flask.session['state']:
        raise ValueError("State does not match")
    auth_context = adal.AuthenticationContext(AUTHORITY_URL)
    token_response = auth_context.acquire_token_with_authorization_code(code, REDIRECT_URI, config.RESOURCE,
                                                                        config.CLIENT_ID, config.CLIENT_SECRET)
    # It is recommended to save this to a database when using a production app.
    flask.session['access_token'] = token_response['accessToken']

    return flask.redirect('/listsubscriptions')

# List the Azure Subscriptions you have access to
@app.route('/listsubscriptions')
def listsubscriptions():
    if 'access_token' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    endpoint = "https://management.azure.com/subscriptions/?api-version=2016-06-01"
    #config.RESOURCE + '/subscriptions/' + config.SUBSCRIPTION_ID + '/providers/Microsoft.Compute/virtualMachines?api-version=2018-06-01'
    http_headers = {'Authorization': 'Bearer ' + flask.session.get('access_token'),
                    'User-Agent': 'adal-python-sample',
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'client-request-id': str(uuid.uuid4())}
    graph_data = requests.get(endpoint, headers=http_headers, stream=False).json()

    #
    # Need to put something here to handle the login timeout KeyError: 'value'
    if 'value' not in graph_data:
        return flask.redirect(flask.url_for('login'))

    #
    # Need to put something here to handle the NextLink
    if graph_data.get('nextLink'):
        NLA = graph_data.get('nextLink')
        print(NLA)
    else:
        print('No nextLink present in Subscriptions List')
    
    
    #print(graph_data)

    def subList(graph_data):
        for props in graph_data['value']:
            json_data = props
            json_data_loop.append(json_data)
                
    json_data_loop = []

    subList(graph_data)

    return flask.render_template('display_azure_subscriptions.html', graph_data = json_data_loop )

# List the VMs in a given Subscription
@app.route('/listvms/<path:sub_id>')
def listvms(sub_id):
    if 'access_token' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    endpoint = "https://management.azure.com/subscriptions/" + sub_id + "/providers/Microsoft.Compute/virtualMachines?api-version=2018-06-01"
    #config.RESOURCE + '/subscriptions/' + config.SUBSCRIPTION_ID + '/providers/Microsoft.Compute/virtualMachines?api-version=2018-06-01'
    http_headers = {'Authorization': 'Bearer ' + flask.session.get('access_token'),
                    'User-Agent': 'adal-python-sample',
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'client-request-id': str(uuid.uuid4())}
    graph_data = requests.get(endpoint, headers=http_headers, stream=False).json()
    print('Main Loop in VMs List')
    #
    # Need to put something here to handle the login timeout KeyError: 'value'
    if 'value' not in graph_data:
        return flask.redirect(flask.url_for('login'))
    #
    #
     
    #
    # Need to put something here to handle the NextLink
            
    ## Create a function to loop through nextLink calls until no more exist
    json_data_loop = []
    

    def listvmsloop(NLA, NLD):
        
        ## Check if the nextLink is in the first call to def listvms()
            for props in NLD:
                json_data = props
                json_data_loop.append(json_data)
                # count += 1
                # print(count)

            # print(NLA)

            endpoint_nextLink = NLA
            http_headers = {'Authorization': 'Bearer ' + flask.session.get('access_token'),
                        'User-Agent': 'adal-python-sample',
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                        'client-request-id': str(uuid.uuid4())}
            graph_data_nextLink = requests.get(endpoint_nextLink, headers=http_headers, stream=False).json()
            # print(graph_data_nextLink.get('nextLink'))

            if graph_data_nextLink.get('nextLink'):
                NLA = graph_data_nextLink.get('nextLink')
                NLD = graph_data_nextLink['value']
                print('Next Loop ')
                listvmsloop(NLA, NLD)
            else:
                print('No nextLink present on Next Loop in VMs List')
                NLD = graph_data_nextLink['value']
                # count = 0
                for props in NLD:
                    json_data = props
                    json_data_loop.append(json_data)
                    # count += 1
                    # print(count)
                return flask.render_template('display_azure_vms.html', graph_data = json_data_loop)
   
    if graph_data.get('nextLink'):
            NLA = graph_data.get('nextLink')
            NLD = graph_data['value']
            print('First Loop ')
            listvmsloop(NLA, NLD)
    else:
            print('No nextLink present on First Loop in VMs List')
            json_data_loop = []
            # count = 0
            for props in graph_data['value']:
                json_data = props
                json_data_loop.append(json_data)
        
          
    return flask.render_template('display_azure_vms.html', graph_data = json_data_loop)

@app.route('/listvmdetails/<path:vm_id>')
def listvmdetails(vm_id):
    if 'access_token' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    endpoint = "https://management.azure.com/subscriptions/<subscription_ID>/providers/Microsoft.Compute/virtualMachines?api-version=2018-06-01"
    #config.RESOURCE + '/subscriptions/' + config.SUBSCRIPTION_ID + '/providers/Microsoft.Compute/virtualMachines?api-version=2018-06-01'
    http_headers = {'Authorization': 'Bearer ' + flask.session.get('access_token'),
                    'User-Agent': 'adal-python-sample',
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'client-request-id': str(uuid.uuid4())}
    graph_data = requests.get(endpoint, headers=http_headers, stream=False).json()
    json_data_loop = []
        
    for props in graph_data['value']:
        json_data = props['properties']
        json_data_loop.append(json_data)

        vtypej = type(props)
        print(vtypej)

        print(json_data_loop)
          
    return flask.render_template('display_azure_vm_details.html', graph_data = json_data_loop)

    
if __name__ == "__main__":
    app.run(ssl_context='adhoc')
