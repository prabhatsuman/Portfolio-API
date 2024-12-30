from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

def fetch_data(url):
    """
    Fetch data from the given URL and handle any HTTP errors.
    Returns a parsed JSON response or an empty dictionary on error.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return {}  # Return empty dictionary on error

@app.route('/codeforces', methods=['GET'])
def codeforces_profile():
    """
    Fetch and format the profile data from Codeforces.
    """
    # Codeforces API endpoints
    user_url = "https://codeforces.com/api/user.info?handles=Prabhat_007"
    contests_url = "https://codeforces.com/api/user.rating?handle=Prabhat_007"
    problems_url = "https://codeforces.com/api/user.status?handle=Prabhat_007"

    # Fetching data
    user_data = fetch_data(user_url)
    contests_data = fetch_data(contests_url)
    problems_data = fetch_data(problems_url)

    # Extract and format data
    contest_count = len(contests_data.get('result', []))
    problems_solved = len([p for p in problems_data.get('result', []) if p.get('verdict') == 'OK'])

    formatted_data = {
        "username": "Prabhat_007",
        "title": user_data.get('result', [{}])[0].get('rank', 'Unranked'),
        "maxTitle": user_data.get('result', [{}])[0].get('maxRank', 'None'),
        "contestRating": user_data.get('result', [{}])[0].get('rating', 0),
        "maxContestRating": user_data.get('result', [{}])[0].get('maxRating', 0),
        "ratedContests": contest_count,
        "problemsSolved": problems_solved,
    }

    return jsonify(formatted_data)

@app.route('/codechef', methods=['GET'])
def codechef_profile():
    """
    Fetch and format the profile data from CodeChef.
    """
    # CodeChef API endpoint
    user_url = "https://codechef-api.vercel.app/handle/prabhats_007"

    # Fetching data
    user_data = fetch_data(user_url)

    # Extract and format data
    formatted_data = {
        "username": "prabhats_007",
        "stars": user_data.get("stars", "Unrated"),
        "currentRating": user_data.get("currentRating", 0),
        "highestRating": user_data.get("highestRating", 0),
        "contestgiven": len(user_data.get("ratingData", [])), 
        "countryrank": user_data.get("countryRank", 0),
    }

    return jsonify(formatted_data)

@app.route('/leetcode', methods=['GET'])
def leetcode_profile():
    """
    Fetch and format the profile data from LeetCode.
    """
    # LeetCode API endpoints
    contest_url = "https://alfa-leetcode-api.onrender.com/Prabhat_007/contest"
    solved_url = "https://alfa-leetcode-api.onrender.com/Prabhat_007/solved"

    # Fetching data
    contest_data = fetch_data(contest_url)
    
    solved_data = fetch_data(solved_url)


    # Extract and format data
    formatted_data = {
        "username": "Prabhat_007",
        "title": contest_data.get("contestBadges", {}).get("name", "None"),
        "contestRating": contest_data.get("contestRating", 0),
        "percentage": contest_data.get("contestTopPercentage", 0),
        "contestGiven": contest_data.get("contestAttend", 0),
        "problemsSolved": solved_data.get("solvedProblem", 0),
    }

    return jsonify(formatted_data)

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8000)

