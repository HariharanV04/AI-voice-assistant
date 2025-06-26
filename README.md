# AI-voice-assistant
 AI-Powered Voice Assistant Development

This is a sample of my skillset in using AI powered voice assistant using Openai's Chatgpt using api.

Streamlit is used for the basic UI functions and the streamlit dashboard shows weather report using a weather api along with a voice assistant.
Using the voice assistant the user can set an alarm and during the alarm it plays a given alarm sound(in my case the alarm sound is prowler_theme).
Since streamlit does not support multithreading in the true sense, the alarm hinders the working of the voice assistant. The voice assistant works as usual
after the alarm has been triggered. 

Speech recognition library is used for the voice recognition aspect of the program. This also includes a wake word activation function, which is "hello Victoria".

The talker function-
It is responsible for making the api calls for the openai chatgpt model. It is used with the help of the openai library and the OpenAI() function. By manipulating the parameters of the model like temperature and max_token during api call, we can fine tune its output for our particular use. Alongside this we have the content for the role of the system, where explain the context and other rules that the model must follow.

The play_alarm_sound function-
Is used for the playing the particular alarm sound.(in this case its prowler theme, an mp3 file)

The check_alarm function-
Is used to check the time and if the time matched the alarm, calls the play_alarm_sound function and updates the streamlit session state.

The main body of the program is initiated with Microphone as input and awaits the activation, which is triggered by the wake word.
In worst case scenario of the voice being unrecognized, it displays a particular output and stays in the failed state, until the wake word is spoken.
By taking into account the effect of background noise on the speech recognition component, we use the adjust_for_ambient_noise() function to act as a filter.

The speech recognition component takes into account the three variables that trigger different kinds of action, which are the wake word, sleep word and alarm word. 
Once the speech is processed, it checks for the presence of these words to trigger their respective actions. The sleep word is used to stop the assistant and return to intial state, it is 
triggered by saying stop talking.

Using the threading library, we assign the alarm triggering and the alarm sounds in a different threads(background by setting the daemon as True), alongside updating the session state of streamlit.
(Streamlit does not allow multi-threading, as such the threads work sequentially.) Therefore, there is a stop in the response from the assistant after the alarm is set and the alarm is triggered.
So in order to fully utilize the multi-threading feature make sure to execute the either terminal without the streamlit component or create a dedicated frontend component.

The weather dashboard-
It is set of functions that use api calls to open source website that offers weather data. Currently the city location is set as default chennai.
Since streamlit does not allow multi-threading, any changes to the default value of the weather would cause the program to be rerun in streamlit, since it follows a sequence execution.
Therefore, execute the code without the streamlit component or develope a dedicated frontend component using traditional methods to fully utilize the multi-threading feature effectively.

The values for the apis are stored in an .env (environment variables), which is accessed with the help of the load_dotenv() from the dotenv library.


