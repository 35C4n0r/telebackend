from fastapi import FastAPI
import requests
from starlette.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from models.models import postCountryBody

"""Setting Up the Environment Variables"""
load_dotenv()

BASE_URL = "https://covid-193.p.rapidapi.com"

tags_metadata = [{"name": "Create"}]

app = FastAPI(openapi_tags=tags_metadata)

origins = ["*"]

"""Setting up CORS Middleware"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""This is a common header used in all api requests"""
headers = {
    "X-RapidAPI-Key": os.getenv("RAPID_API_KEY"),
    "X-RapidAPI-Host": "covid-193.p.rapidapi.com",
}


@app.get("/")
async def sanity_check():
    """A sanity test run"""
    return {"success": True, "status": "Up & Running fine. UwU"}


@app.get("/countryList")
async def getCountryList():
    """Endpoint to fetch the list of available Countries"""
    try:
        response = requests.request("GET", f"{BASE_URL}/countries", headers=headers)

        return {"success": True, "data": response.json()["response"]}

    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)

    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)

    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)

    except requests.exceptions.RequestException as err:
        print("Something Went Wrong", err)


@app.post("/data")
def postCountryData(body: postCountryBody):
    """Endpoint to get the info for a particular Country"""
    try:
        querystring = {"country": f"{body.country}", "day": f"{body.date}"}
        response = requests.request(
            "GET", f"{BASE_URL}/history", headers=headers, params=querystring
        )
        response = response.json()["response"][0]
        return {
            "success": True,
            "data": {
                "population": response["population"] or 0,
                "recovered": response["cases"]["recovered"] or 0,
                "deaths": response["deaths"]["total"] or 0,
                "active": response["cases"]["active"] or 0,
            },
        }
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)

    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)

    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)

    except requests.exceptions.RequestException as err:
        print("Something Went Wrong", err)

    except IndexError:
        return {
            "success": False,
            "data": {"population": -1, "recovered": -1, "deaths": -1, "active": -1},
        }


@app.get("/all")
def get_all():
    """Endpoint to get data for all countries as of now."""
    try:
        response = requests.request("GET", f"{BASE_URL}/statistics", headers=headers)

        response = response.json()["response"]
        data = []
        for stat in response:
            data.append(
                {
                    "country": stat["country"] or 0,
                    "deaths": stat["deaths"]["total"] or 0,
                    "active": stat["cases"]["active"] or 0,
                }
            )

        return {"success": True, "data": data}

    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)

    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)

    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)

    except requests.exceptions.RequestException as err:
        print("Something Went Wrong", err)

    except IndexError:
        return {
            "success": False,
            "data": {
                "population": None,
                "recovered": None,
                "deaths": None,
                "active": None,
            },
        }
