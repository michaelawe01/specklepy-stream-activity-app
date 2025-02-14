import streamlit as st
import pandas as pd
import plotly.express as px

# SpecklePy libraries
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.api import operations
from specklepy.transports.server import ServerTransport
from specklepy.objects import Base
from specklepy.api.resources.current.version_resource import CreateVersionInput
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_account_from_token



# --------------------------
# PAGE CONFIG
st.set_page_config(
    page_title="Speckle Stream Activity",
    layout="wide"
)

# --------------------------
# CONTAINERS
header = st.container()
input_section = st.container()
viewer = st.container()
report = st.container()
graphs = st.container()

# --------------------------
# HEADER
with header:
    st.title("Speckle Stream Activity App ")
    with st.expander("About this app", expanded=True):
        st.markdown(
            """This is a beginner web app developed using Streamlit to interact with Speckle API via SpecklePy. 
            The app retrieves and modifies elements in a Revit model stored in Speckle.
            """
        )

# INPUT SECTION
#with input:
    st.subheader("Inputs")

    #Columns for inputs
    serverCol, tokenCol = st.columns([1,2])
    #User Input boxes
    speckleServer = serverCol.text_input("Server URL", "https://app.speckle.systems/", help="Speckle server to connect.")
    #speckleToken = tokenCol.text_input("Speckle token", "YOUR OWN TOKEN", help="If you don't know how to get your token, take a look at this [link](https://speckle.guide/dev/tokens.html)👈")
    speckleToken = tokenCol.text_input("Speckle token", "YOUR OWN TOKEN", help="If you don't know how to get your token, take a look at this [link](https://speckle.guide/dev/tokens.html)👈")
    

    #CLIENT
    client = SpeckleClient(host=speckleServer)
    #Get account from Token
    account = get_account_from_token(speckleToken, speckleServer)
    #Authenticate
    client.authenticate_with_account(account)

    
    #Projects List

    projects = client.active_user.get_projects()
    projectNames = [p.name for p in projects.items]
    # Dropdown for project selection
    pName = st.selectbox(label="Select your project", options=projectNames)

    # Find the selected project by name
    selected_project = next((p for p in projects.items if p.name == pName), None)

    # Get models related to the selected project
    models = client.model.get_models(project_id=selected_project.id)
    modelNames = [m.name for m in models.items]
    # Dropdown for model selection
    mName = st.selectbox(label="Select your model", options=modelNames)

    # Find the selected model by name
    selected_model = next((m for m in models.items if m.name == mName), None)

    # Get versions related to the selected model
    versions = client.version.get_versions(project_id=selected_project.id, model_id=selected_model.id, limit=100)


    # Display the results (optional)
    st.write("Selected Project:", selected_project)
    st.write("Selected Model:", selected_model)
    st.write("Versions:", versions)

#create a definition to convert your list to markdown
def listToMarkdown(list, column):
    list = ["- " + i + " \n" for i in list]
    list = "".join(list)
    return column.markdown(list)


def model2viewer(projects, models):
    embed_src = f"https://app.speckle.systems/projects/{projects.id}/models/{models.id}#embed=%7B%22isEnabled%22%3Atrue%7D"
    return embed_src  # Return the correct URL

with viewer:
    st.subheader("Latest version👇")
    #<iframe title="Speckle" src="https://app.speckle.systems/projects/96d2667014/models/a0db08e966#embed=%7B%22isEnabled%22%3Atrue%7D" width="600" height="400" frameborder="0"></iframe>
    #st.components.v1.iframe(src= "https://app.speckle.systems/projects/96d2667014/models/a0db08e966#embed=%7B%22isEnabled%22%3Atrue%7D", width=600, height=400)
    
    embed_link = model2viewer(selected_project, selected_model)
    st.components.v1.iframe(src=embed_link, width=600, height=400)

with report:
    st.subheader("Statistics")

    projectCol, versionCol, connectorCol, contributorCol = st.columns(4)


    connectorList = [v.sourceApplication for v in versions.items]

    projectCol.metric(label="Number of Projects", value = len(projects.items))
    #st.write([p.name for p in projects.items])
    listToMarkdown([p.name for p in projects.items], projectCol)


    versionCol.metric(label="Number of versions", value = versions.totalCount)

    connectorCol.metric(label="Number of connectors", value = len(dict.fromkeys(connectorList)))
    listToMarkdown([v.sourceApplication for v in versions.items], connectorCol)

    #contributorCol.metric(label="Number of collaborators", value = len(selected_model.author))
    #st.write([selected_model.author])


# I am not motivated to continue as the rest of the graphs are not part of the scope of what I am learning to build. These updates will be useful for anyone looking to follow through with your work.
