# Push metrics to Google Sheets

This project was created to pull metrics from Freshdesk on specific intervals and push them to Google Sheets after processing the data in correct format.

## Installation

```bash
pip install requirements.txt
```
Generate an access token and place the token JSON in the root folder of this project to allow access to your Google Sheets spreadsheets.For more information on this process, kindly visit the official [Google Documentation](https://developers.google.com/identity/protocols/oauth2#2.-obtain-an-access-token-from-the-google-authorization-server.).

Also add your Freshdesk credentials as a environmental variable labelled `FRESHDESK_AGENT_API_KEY`.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.