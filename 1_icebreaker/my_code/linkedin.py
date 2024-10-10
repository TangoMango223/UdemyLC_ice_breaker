# OpenSource Model

# For most tasks, the models perform OK
# Lots of tasks with reasoning are better for First Tier Models

import os
import requests
import json



# # Scrape Linkedin
# def scrape_linkedin_profile(url: str, mock: bool = False):
#     """scrape information from Linkedin profile"""
    

# # ProxyCurl
# headers = {'Authorization': 'Bearer ' + api_key}
# api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
# params = {
#     'linkedin_profile_url': 'https://www.linkedin.com/in/aviraj-garcha-b205381b5/',
#     'extra': 'include',
#     'github_profile_id': 'include',
#     'facebook_profile_id': 'include',
#     'twitter_profile_id': 'include',
#     'personal_contact_number': 'include',
#     'personal_email': 'include',
#     'inferred_salary': 'include',
#     'skills': 'include',
#     'use_cache': 'if-present',
#     'fallback_to_cache': 'on-error',
# }

# # Check response
# response = requests.get(api_endpoint,
#                         params=params,
#                         headers=headers)

# # Parse the JSON content
# json_data = response.json()

# # Pretty-print the JSON data
# pretty_json = json.dumps(json_data, indent=4)

# # Optionally, write the pretty-printed JSON to a new file
# with open('output_pretty.json', 'w') as f:
#     f.write(pretty_json)

# # Print the pretty JSON content (optional)
# print(pretty_json)

# ---- 

def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""

    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/78233eb934aa9850b689471a604465b188e761a0/eden-marco.json"
        response = requests.get(
            linkedin_profile_url,
            timeout=10,
        )
    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        response = requests.get(
            api_endpoint,
            params={"url": linkedin_profile_url},
            headers=header_dic,
            timeout=10,
        )

    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data


if __name__ == "__main__":
    print(
scrape_linkedin_profile("https://www.linkedin.com/in/aviraj-garcha-b205381b5")
    )


# Token Limits:
# GPT-4o, 128,000 windows token limit