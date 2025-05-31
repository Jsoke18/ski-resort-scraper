import requests
from crewai.tools import BaseTool

# Configuration - User should replace this with their actual API base URL
YOUR_API_BASE_URL = "http://localhost:3000" # This is correct as per user

class GetResortsTool(BaseTool):
    name: str = "Get Resorts List by Country or ID"
    description: str = (
        "Fetches a list of ski resort names for a specific 'country' (e.g., 'Canada'). "
        "Alternatively, provide 'resort_id' to fetch a specific resort's details. "
        "If no 'resort_id' or 'country' is provided, fetches all basic resort data (this might be a large list)."
    )

    def _run(self, resort_id: str = None, country: str = None) -> dict:
        url = ""
        try:
            if country:
                # GET /resorts/by-country/{countryName}/names
                url = f"{YOUR_API_BASE_URL}/resorts/by-country/Canada/names"
                response = requests.get(url)
            elif resort_id:
                # GET /resorts/:resortId - Assumes this endpoint gives basic resort details
                url = f"{YOUR_API_BASE_URL}/resorts/{resort_id}"
                response = requests.get(url)
            else:
                # GET /resorts (fetches all)
                url = f"{YOUR_API_BASE_URL}/resorts"
                response = requests.get(url)
            
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"API request failed: {e}", "url": url}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {e}", "url_attempted": url }

class GetAllSkiPassesTool(BaseTool):
    name: str = "Get All Ski Passes"
    description: str = "Fetches a list of all ski passes and their details (including IDs) from the API."

    def _run(self) -> dict:
        url = f"{YOUR_API_BASE_URL}/api/ski-passes"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"API request failed: {e}", "url": url}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {e}"}

class AssignSkiPassToResortTool(BaseTool):
    name: str = "Assign Ski Pass to Resort"
    description: str = (
        "Assigns a ski pass to a specific ski resort in the database. "
        "Requires 'resort_id' and 'ski_pass_id'."
    )

    def _run(self, resort_id: str, ski_pass_id: str) -> dict:
        if not resort_id or not ski_pass_id:
            return {"error": "Both 'resort_id' and 'ski_pass_id' are required."}
        
        url = f"{YOUR_API_BASE_URL}/resorts/{resort_id}/ski-passes/{ski_pass_id}"
        try:
            # POST /resorts/:resortId/ski-passes/:skiPassId
            # This endpoint typically doesn't require a request body for assignment,
            # but if it does, you'd add a json={} parameter to requests.post()
            response = requests.post(url)
            response.raise_for_status()
            # Check if the response has content before trying to parse JSON
            if response.status_code == 204: # No Content typically means success for POST/PUT/DELETE
                 return {"success": True, "message": f"Ski pass {ski_pass_id} assigned to resort {resort_id}."}
            if response.content:
                return response.json()
            return {"success": True, "message": f"Ski pass {ski_pass_id} assigned to resort {resort_id} (No content in response)."}

        except requests.exceptions.RequestException as e:
            # Try to get more details from the response if available
            error_detail = str(e)
            if e.response is not None:
                try:
                    error_detail = e.response.json()
                except ValueError: # If response is not JSON
                    error_detail = e.response.text
            return {"error": f"API request failed: {error_detail}", "url": url, "resort_id": resort_id, "ski_pass_id": ski_pass_id}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {e}"}

# You can add more tools here for other endpoints as needed, e.g., for:
# - GET /resorts/:resortId/conditions
# - GET /resorts/weather/:id
# - DELETE /resorts/:resortId/ski-passes/:skiPassId
# - POST /api/ski-passes/upload (Create new ski pass)
# - etc. 