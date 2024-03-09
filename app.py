import openai
import panel as pn
import param

from chatbot import cbfs, unzip_file


def initialize_api_dependent_components(api_key, pdf_doc):
    openai.api_key = api_key
    cb = cbfs(pdf_doc=pdf_doc)
    file_input = pn.widgets.FileInput(accept=".pdf")
    button_load = pn.widgets.Button(name="Load DB", button_type="primary")
    button_clearhistory = pn.widgets.Button(name="Clear History", button_type="warning")
    button_clearhistory.on_click(cb.clr_history)
    inp = pn.widgets.TextInput(placeholder="Enter text here…")
    button_submit = pn.widgets.Button(name="Submit")
    bound_button_load = pn.bind(cb.call_load_db, button_load.param.clicks)
    conversation = pn.bind(cb.convchain, inp)

    jpg_pane = pn.pane.Image("./img/convchain.jpg")

    tab1 = pn.Column(
        pn.Row(inp, button_submit),
        pn.layout.Divider(),
        pn.panel(conversation, loading_indicator=True, height=300),
        pn.layout.Divider(),
    )
    tab2 = pn.Column(
        pn.panel(cb.get_lquest),
        pn.layout.Divider(),
        pn.panel(cb.get_sources),
    )
    tab3 = pn.Column(
        pn.panel(cb.get_chats),
        pn.layout.Divider(),
    )
    tab4 = pn.Column(
        pn.Row(file_input, button_load, bound_button_load),
        pn.Row(
            button_clearhistory,
            pn.pane.Markdown(
                """
                                Clears chat history.
                                Can use to start a new topic"""
            ),
        ),
        pn.layout.Divider(),
        pn.Row(jpg_pane.clone(width=400)),
    )
    dashboard = pn.Column(
        pn.Row(pn.pane.Markdown("# ChatWithYourData_Bot")),
        pn.Tabs(
            ("Conversation", tab1),
            ("Database", tab2),
            ("Chat History", tab3),
            ("Configure", tab4),
        ),
    )

    return dashboard


class Application(param.Parameterized):
    api_key_input = pn.widgets.PasswordInput(
        name="API Key", placeholder="Enter your API key here"
    )
    submit_button = pn.widgets.Button(name="Submit API Key", button_type="primary")
    status_message = pn.pane.Markdown("Enter API Key to unlock full features.")
    main_container = pn.Column()  

    def __init__(self, **params):
        super().__init__(**params)
        self.submit_button.on_click(self.submit_api_key)
        self.main_container.append(self.api_key_input)
        self.main_container.append(self.submit_button)
        self.main_container.append(self.status_message)

    def submit_api_key(self, event):
        api_key = self.api_key_input.value
        print()
        acknowledgment_area = pn.pane.Markdown("")
        # Write API key to .env
        if api_key:
            with open(".env", "w") as env_file:
                env_file.write(f"OPENAI_API_KEY='{api_key}'\n")

            # Display a message to confirm the API key has been stored
            print("API key has been successfully stored in the .env file.")

            # Adds the new folder "resume" to gitignore
            print(
                """
                  add the folders resume and docs/chroma
            to gitignore if it exists or it creates a .gitignore
            if it doesn't exist in this directory.
                  """
            )
            with open(".gitignore", "a") as g:
                g.write("\nresume/")
                g.write("\ndocs/chroma/")
            print("folders added to gitignore and possibly created .gitignore")
            pdf_doc = unzip_file("resume.pdf.zip", "resume")
            dashboard = initialize_api_dependent_components(api_key, pdf_doc)
            self.main_container.clear()  # Clear existing content
            self.main_container.append(dashboard)  # Add the new dashboard

            # Clear the input and update acknowledgment
            self.api_key_input.value = ""
            acknowledgment_area.object = """
            API key successfully added to .env file.
            """
        else:
            self.status_message.object = "Invalid API Key."


# Initialize your application
app_layout = Application()
# Serve or display the main container of the Application class
app_layout.main_container.servable()
